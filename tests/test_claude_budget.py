from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import sqlite3
import threading
import unittest
from unittest.mock import patch

from robofrontier.claude.budget import BudgetLedger


class SharedBudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'budget.sqlite'
        self.ledger=BudgetLedger.create(self.path, 1)
    def tearDown(self): self.ledger.close(); self.tmp.cleanup()

    def test_busy_budget_reservation_waits_and_is_recorded_once(self):
        from robofrontier import sqlite_busy
        self.assertEqual(self.ledger.db.execute('PRAGMA busy_timeout').fetchone()[0],30000)
        self.ledger.db.execute('PRAGMA busy_timeout=20')
        other=sqlite3.connect(self.path,isolation_level=None,check_same_thread=False)
        other.execute('BEGIN IMMEDIATE')
        timer=threading.Timer(.11,other.rollback);timer.start()
        try:
            with patch.object(sqlite_busy,'MAX_BEGIN_ATTEMPTS',12), \
                 patch.object(sqlite_busy,'RETRY_DELAY_SECONDS',.01), \
                 self.assertLogs('robofrontier.sqlite_busy',level='WARNING'):
                self.assertEqual(self.ledger.reserve('turn','Controller',.3),.3)
            rows=self.ledger.snapshot()['reservations']
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['id'],'turn')
        finally:
            timer.join();other.close()

    def test_concurrent_process_connections_cannot_overreserve(self):
        gate=threading.Barrier(10)
        def reserve(i):
            ledger=BudgetLedger(self.path)
            try:
                gate.wait()
                try: return ledger.reserve('turn-'+str(i),'actor',.3)
                except ValueError: return 0
            finally: ledger.close()
        with ThreadPoolExecutor(max_workers=10) as pool: amounts=list(pool.map(reserve,range(10)))
        self.assertAlmostEqual(sum(amounts),1.0)
        self.assertEqual(self.ledger.snapshot()['reserved_usd'],'1.0')
        self.assertEqual(self.ledger.snapshot()['status'],'exhausted')

    def test_settled_cost_releases_unused_allowance(self):
        self.assertEqual(self.ledger.reserve('parent','Controller',.6),.6)
        self.assertEqual(self.ledger.reserve('child','Delegate',.6),.4)
        result=self.ledger.settle('parent',.2,outcome_known=True)
        self.assertEqual(result['reported_spend_usd'],'0.2')
        self.assertEqual(result['available_usd'],'0.4')
        self.assertEqual(self.ledger.reserve('next','Controller',.6),.4)
        with self.assertRaises(ValueError): self.ledger.settle('parent',.2,outcome_known=True)

    def test_uncapped_ledger_records_missing_cost_without_blocking_known_turns(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = BudgetLedger.create(Path(tmp)/'uncapped.sqlite')
            try:
                self.assertIsNone(ledger.reserve('first', 'Controller'))
                self.assertEqual(ledger.snapshot()['uncapped_pending_count'], 1)
                state = ledger.settle('first', None, outcome_known=True)
                self.assertEqual(state['status'], 'tracking')
                self.assertIsNone(state['limit_usd'])
                self.assertIsNone(state['available_usd'])
                self.assertEqual(state['unreported_cost_count'], 1)
                self.assertIsNone(ledger.reserve('second', 'Delegate'))
                self.assertEqual(ledger.settle('second', 0, outcome_known=True)['status'], 'tracking')
                self.assertIsNone(ledger.reserve('third', 'Controller'))
                self.assertEqual(ledger.settle('third', 1234, outcome_known=True)['reported_spend_usd'], '1234')
                ledger.reserve('uncertain', 'Controller')
                self.assertEqual(ledger.settle('uncertain', None, outcome_known=False)['status'], 'uncertain')
                with self.assertRaises(ValueError): ledger.reserve('later', 'Controller')
            finally: ledger.close()

    def test_task_cap_without_turn_cap_reserves_remaining_allowance(self):
        self.assertEqual(self.ledger.reserve('turn', 'Controller'), 1)
        self.ledger.settle('turn', .25, outcome_known=True)
        self.assertEqual(self.ledger.reserve('next', 'Controller'), .75)

    def test_turn_cap_without_task_cap_is_still_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = BudgetLedger.create(Path(tmp)/'uncapped.sqlite')
            try:
                self.assertEqual(ledger.reserve('turn', 'Controller', .2), .2)
                self.assertEqual(ledger.settle('turn', .3, outcome_known=True)['status'], 'uncertain')
            finally: ledger.close()

    def test_unknown_missing_or_above_reservation_blocks_future(self):
        for cost,known in ((None,True),(0,True),(.7,True),(.1,False)):
            with self.subTest(cost=cost,known=known), tempfile.TemporaryDirectory() as tmp:
                ledger=BudgetLedger.create(Path(tmp)/'budget.sqlite',1)
                try:
                    ledger.reserve('parent','Controller',.6)
                    self.assertEqual(ledger.settle('parent',cost,outcome_known=known)['status'],'uncertain')
                    with self.assertRaisesRegex(ValueError,'uncertain'): ledger.reserve('child','Delegate',.1)
                finally: ledger.close()

    def test_no_duplicate_or_implicit_release_after_reopen(self):
        self.ledger.reserve('turn','Controller',.2)
        other=BudgetLedger(self.path)
        try:
            self.assertEqual(other.snapshot()['reserved_usd'],'0.2')
            with self.assertRaises(ValueError): other.reserve('turn','Controller',.1)
            other.abandon_before_launch('turn')
            self.assertEqual(other.snapshot()['available_usd'],'1')
            with self.assertRaises(ValueError): other.reserve('turn','Controller',.1)
        finally: other.close()


if __name__=='__main__': unittest.main()
