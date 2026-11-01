from pathlib import Path
import unittest

from scripts.diagnose_mosaic_live_replan import cache_status


class ReplanCacheTests(unittest.TestCase):
    def test_stale_keys_follow_the_frozen_executor(self):
        source = (Path(__file__).resolve().parents[1] / 'robofrontier/suite/mosaic_oracle_v2.py').read_text()
        angles = {frozenset(('A', 'C')): {}, frozenset(('D', 'F')): {}}
        missing, prunes, effective = cache_status(source, angles, {})
        self.assertEqual(len(missing), 2)
        self.assertTrue(prunes)
        self.assertEqual(effective, [])

        legacy = 'def solve(trial):\n    pass\n'
        missing, prunes, effective = cache_status(legacy, angles, {})
        self.assertFalse(prunes)
        self.assertEqual(effective, missing)
        self.assertEqual(cache_status(legacy, angles, angles)[2], [])

    def test_comment_or_unrelated_function_does_not_authorize_resume(self):
        source = '''
def unrelated(trial, edges):
    trial.mosaic_angled_edges = {key: value for key, value in getattr(trial, 'mosaic_angled_edges', {}).items() if key in edges}
def solve(trial):
    pass
'''
        missing, prunes, effective = cache_status(source, {frozenset(('A', 'C')): {}}, {})
        self.assertFalse(prunes)
        self.assertEqual(effective, missing)
