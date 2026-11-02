import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from robofrontier.run_metrics import export_metrics, native_codex_sessions, native_subagent_calls, run_skills, usage


class RunMetricTests(unittest.TestCase):
    def test_claude_cache_writes_setup_and_duplicate_terminal_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp); output = run/'private/outputs'; output.mkdir(parents=True)
            first = {'event':'cli_turn_completed', 'actor':'Controller', 'session_id':'s', 'at':10,
                     'events_name':'turn1', 'phase':'policy', 'duration_s':4, 'reported_cost_usd':.1,
                     'usage':{'input_tokens':10,'cache_read_input_tokens':20,'cache_creation_input_tokens':30,'output_tokens':4}}
            setup = {**first, 'actor':'Delegate_a', 'events_name':'fork1', 'phase':'fork_setup', 'at':11,
                     'reported_cost_usd':.2}
            (output/'claude-host.jsonl').write_text('\n'.join(map(json.dumps,[first, first, setup]))+'\n')
            result = export_metrics(run, 'claude')
            self.assertEqual(result['usage']['input_tokens'],120)
            self.assertEqual(result['usage']['cached_input_tokens'],40)
            self.assertAlmostEqual(result['reported_cost_usd'],.3)
            self.assertTrue(result['usage_complete']); self.assertTrue(result['cost_complete'])
            self.assertEqual(result['phase_counts'], {'fork_setup':1,'policy':1})
            self.assertEqual(result['model_process_wall_seconds_union'],5)
            self.assertEqual(result['model_process_seconds_sum'],8)
            self.assertEqual(result['by_actor']['Delegate_a']['input_tokens'],60)

    def test_codex_uses_first_last_then_cumulative_deltas_not_inherited_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'private/outputs'; output.mkdir(parents=True)
            def event(total, cached, out):
                return {'event':'thread/tokenUsage/updated','thread_id':'child','actor':'Delegate_a',
                        'token_usage':{'total':{'inputTokens':total,'cachedInputTokens':cached,'outputTokens':out},
                                       'last':{'inputTokens':100,'cachedInputTokens':40,'outputTokens':5}}}
            first=event(1000,500,40); later=event(1250,650,50)
            (output/'codex-host.jsonl').write_text('\n'.join(map(json.dumps,[first,first,later]))+'\n')
            result=export_metrics(tmp,'codex')
            self.assertEqual(result['usage']['input_tokens'],350)
            self.assertEqual(result['usage']['cached_input_tokens'],190)
            self.assertEqual(result['usage']['output_tokens'],15)
            self.assertAlmostEqual(result['cache_hit_rate'],190/350)
            self.assertIsNone(result['reported_cost_usd'])

    def test_missing_cache_fields_are_unknown_and_legacy_reports_are_partial(self):
        self.assertIsNone(usage('claude', {'input_tokens':10})['input_tokens'])
        with tempfile.TemporaryDirectory() as tmp:
            evidence=Path(tmp)/'private/evidence'; evidence.mkdir(parents=True)
            (evidence/'old-summary.json').write_text(json.dumps({'actor':'Controller','record':{
                'summary':{'usage':{'input_tokens':10,'output_tokens':4},'total_cost_usd':.1}}}))
            result=export_metrics(tmp,'claude')
            self.assertFalse(result['cost_complete']); self.assertFalse(result['usage_complete'])
            self.assertEqual(result['evidence_scope'],'legacy_policy_only')
            self.assertEqual(result['reported_cost_usd'],.1)

    def test_claude_model_usage_is_aggregate_and_unfinished_turn_is_not_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'private/outputs';output.mkdir(parents=True)
            values={'inputTokens':10,'cacheReadInputTokens':20,'cacheCreationInputTokens':30,'outputTokens':4}
            done={'event':'cli_turn_completed','events_name':'turn1','usage':{'input_tokens':1},
                  'model_usage':{'model1':values,'model2':values},'reported_cost_usd':.1}
            started={'event':'cli_turn_started','events_name':'turn2'}
            (output/'claude-host.jsonl').write_text('\n'.join(map(json.dumps,[done,started]))+'\n')
            result=export_metrics(tmp,'claude')
            self.assertEqual(result['usage']['input_tokens'],120)
            self.assertEqual(result['usage']['output_tokens'],8)
            self.assertEqual(result['known_usage_subtotals']['input_tokens'],120)
            self.assertEqual(result['rows'][0]['usage_source'],'model_usage')
            self.assertEqual(result['unfinished_cli_turns'],1)
            self.assertFalse(result['usage_complete']);self.assertFalse(result['cost_complete'])

    def test_collected_session_mapping_wins_over_stale_batch_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); run=root/'batch/profile/case'; run.mkdir(parents=True)
            (root/'batch/codex-home.json').write_text('{"codex_home":"/missing/original-server"}')
            session=root/'sessions/Controller.jsonl';session.parent.mkdir();session.write_text('{}\n')
            (root/'collection.json').write_text(json.dumps({'jobs':[{'run':'batch/profile/case','roles':[
                {'thread_id':'native','session':'sessions/Controller.jsonl'}]}]}))
            self.assertEqual(native_codex_sessions(run,'native'),[session.resolve()])

    def test_batch_home_does_not_fall_back_to_another_default_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); run=root/'batch/case';run.mkdir(parents=True)
            home=root/'other';(home/'sessions').mkdir(parents=True)
            (home/'sessions/native.jsonl').write_text('{}')
            (root/'batch/codex-home.json').write_text('{"codex_home":"/missing/original-server"}')
            with patch.dict('os.environ', {'CODEX_HOME':str(home)}):
                self.assertEqual(native_codex_sessions(run,'native'),[])
                self.assertEqual(native_codex_sessions(run,'native',home),[(home/'sessions/native.jsonl').resolve()])


class RunEvidenceTests(unittest.TestCase):
    def test_run_skills_lists_each_heading_of_the_shared_lessons_file(self):
        from robofrontier.policy_bootstrap import SKILLS_HEADER
        from robofrontier.run_layout import manifest_record
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp); (run/'private/inputs').mkdir(parents=True)
            self.assertEqual(run_skills(run), [])  # A legacy run has no lessons file.
            (run/'private/inputs/manifest.json').write_text(json.dumps(manifest_record('codex')))
            self.assertEqual(run_skills(run), [])
            lessons = run/'workspace/skills.md'; lessons.parent.mkdir()
            lessons.write_text(SKILLS_HEADER)
            self.assertEqual(run_skills(run)[0]['entries'], [])
            lessons.write_text(SKILLS_HEADER + '\n## [fix] Reopen before regrasp — Controller — tags: grasp, recovery\n'
                               'Content: x\n### rev 2 — Delegate_ab — open to 4 cm; faster\nContent: y\n'
                               '## loose heading\n### a loose revision\n')
            [record] = run_skills(run)
            self.assertEqual(record['path'], 'workspace/skills.md')
            self.assertEqual(record['entries'], [
                {'type': 'fix', 'title': 'Reopen before regrasp', 'role': 'Controller', 'tags': ['grasp', 'recovery'],
                 'revisions': [{'rev': 2, 'role': 'Delegate_ab', 'change': 'open to 4 cm; faster'}]},
                {'type': None, 'title': 'loose heading', 'role': None, 'tags': [],
                 'revisions': [{'rev': None, 'role': None, 'change': 'a loose revision'}]}])

    def test_native_subagent_calls_are_counted_but_robot_and_text_are_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            codex, claude = Path(tmp)/'rollout.jsonl', Path(tmp)/'session.jsonl'
            codex.write_text('\n'.join(json.dumps(r) for r in [
                {'type':'response_item','payload':{'type':'function_call','name':'spawn_agent','namespace':'collaboration'}},
                {'type':'response_item','payload':{'type':'function_call','name':'collaboration.wait_agent'}},
                {'type':'response_item','payload':{'type':'function_call','name':'robot','arguments':'{"op":"return_task"}'}},
                {'type':'response_item','payload':{'type':'message','content':[{'text':'I will not spawn_agent'}]}}])+'\n')
            claude.write_text('\n'.join(json.dumps(r) for r in [
                {'type':'assistant','message':{'content':[{'type':'tool_use','name':'Agent','input':{}}]}},
                {'type':'assistant','message':{'content':[{'type':'tool_use','name':'mcp__robot__robot','input':{'op':'send_message'}}]}},
                {'type':'user','message':{'content':'Task: place the blocks'}}])+'\n')
            self.assertEqual(native_subagent_calls([codex]), {'spawn_agent': 1, 'wait_agent': 1})
            self.assertEqual(native_subagent_calls([claude]), {'Agent': 1})
            self.assertEqual(native_subagent_calls([]), {})

    def test_cache_miss_has_one_definition_for_both_engines(self):
        # The same request: 100 input tokens, 90 read from cache, 9 of the rest written to cache.
        claude = usage('claude', {'input_tokens':1,'cache_read_input_tokens':90,'cache_creation_input_tokens':9,'output_tokens':4})
        codex = usage('codex', {'inputTokens':100,'cachedInputTokens':90,'outputTokens':4})
        self.assertEqual((claude['input_tokens'], claude['cache_miss_input_tokens'], claude['uncached_input_tokens']), (100, 10, 1))
        self.assertEqual((codex['input_tokens'], codex['cache_miss_input_tokens'], codex['uncached_input_tokens']), (100, 10, 10))
        self.assertIsNone(usage('codex', {'inputTokens':100})['cache_miss_input_tokens'])


if __name__ == '__main__': unittest.main()
