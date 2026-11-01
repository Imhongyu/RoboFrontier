import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from scripts.communication_report import report_run


class CommunicationReportTest(unittest.TestCase):
    def test_role_attribution_and_overlaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            state = run / 'private/state'
            state.mkdir(parents=True)
            out = run / 'private/outputs'
            out.mkdir(parents=True)
            conn = sqlite3.connect(state / 'runtime.sqlite')
            conn.executescript('create table agents(id text,value text); create table events(seq integer,created real,kind text,actor text,value text);')
            for name in ('A', 'B'):
                conn.execute('insert into agents values (?,?)', (name, json.dumps({'kind':'worker','thread_id':'thread-'+name})))
            events = [
                (1, 1, 'MESSAGE_PERSISTED', 'A', {}),
                (2, 3, 'DELIVERY_PREPARED', 'B', {'messages':[{'created_at':1}]}),
                (3, 4, 'WAKE_SENT', 'Meta', {'actor':'B'}),
                (4, 7, 'ACTION_FINISHED', 'A', {'started_at':2,'finished_at':7,'arm':'A'}),
                (5, 8, 'ACTION_FINISHED', 'B', {'started_at':5,'finished_at':8,'arm':'B'}),
            ]
            conn.executemany('insert into events values (?,?,?,?,?)', [(s,t,k,a,json.dumps(v)) for s,t,k,a,v in events])
            conn.commit()
            conn.close()
            (out/'codex-host.jsonl').write_text(json.dumps({'event':'thread/tokenUsage/updated','thread_id':'thread-A','at':4,
                'token_usage':{'total':{'inputTokens':100},'last':{'inputTokens':20}}})+'\n')
            result = report_run(run)
            self.assertEqual(result['roles']['A']['messages_sent'], 1)
            self.assertEqual(result['roles']['B']['wake_sent'], 1)
            self.assertEqual(result['roles']['B']['delivery_delay']['mean_s'], 2)
            self.assertEqual(result['roles']['A']['latest_recorded_token_total']['inputTokens'], 100)
            self.assertEqual(result['pairwise_action_overlap_s'], 2)


if __name__ == '__main__':
    unittest.main()
