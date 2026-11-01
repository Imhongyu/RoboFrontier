import json
from pathlib import Path
import tempfile
import unittest

from robofrontier.cli import _frozen_configuration, plan, prepare, preflight
from robofrontier.configuration import load_configuration, rendering_environment
from robofrontier.run_setup import verify_inputs


class UnifiedConfigurationTests(unittest.TestCase):
    def test_default_plan_is_offline_and_selects_all_released_tasks(self):
        result = plan(load_configuration())
        self.assertEqual((result['task_count'], result['parallel']), (36, 36))
        self.assertEqual((result['model'], result['effort'], result['topology']),
                         ('gpt-6-luna', 'high', 'adaptive'))
        self.assertEqual((result['startup_interval_s'], result['task_wall_limit_s']), (.3, 86400))
        self.assertEqual(result['model_calls'], 0)
        self.assertFalse(result['simulator_started'])

    def test_partial_toml_and_explicit_options_override_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'custom.toml'
            path.write_text('[batch]\nparallel=8\n[selection]\nlevel=1\nmin_arms=true\n')
            config = load_configuration(path, {'batch': {'parallel': 4}})
            self.assertEqual(config['batch']['parallel'], 4)
            self.assertEqual(plan(config)['task_count'], 4)
            self.assertEqual(config['render']['device'], 'nvidia')

    def test_invalid_options_fail_before_installation_or_launch(self):
        cases = [{'batch': {'paralell': 3}}, {'batch': {'parallel': True}},
                 {'batch': {'startup_interval_s': float('nan')}},
                 {'batch': {'startup_interval_s': -.1}}, {'batch': {'task_wall_limit_s': 0}},
                 {'policy': {'topology': 'adpative'}}, {'policy': {'profile': '../secret'}},
                 {'selection': {'families': ['dial', 'dial']}},
                 {'evidence': {'delete_sources': True}},
                 {'evidence': {'auto_collect': False, 'auto_archive': True}}]
        for overrides in cases:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                load_configuration(overrides=overrides)

    def test_preflight_without_spend_confirmation_never_calls_a_provider(self):
        from unittest.mock import patch
        with patch('subprocess.run') as launch:
            report=preflight(load_configuration())
            self.assertEqual(report['status'],'not_run')
            self.assertEqual(report['model_calls'],0)
            launch.assert_not_called()

    def test_renderer_selection_never_silently_falls_back(self):
        cpu = rendering_environment('cpu', 'Linux', {'CUDA_VISIBLE_DEVICES': '2', 'SECRET': 'retained'})
        self.assertEqual(cpu['MUJOCO_GL'], 'osmesa')
        self.assertEqual(cpu['CUDA_VISIBLE_DEVICES'], '')
        gpu = rendering_environment('nvidia', 'Linux', cpu)
        self.assertEqual(gpu['MUJOCO_GL'], 'egl')
        self.assertNotIn('GALLIUM_DRIVER', gpu)
        native = rendering_environment('native', 'Darwin', cpu)
        self.assertNotIn('MUJOCO_GL', native)
        with self.assertRaisesRegex(ValueError, 'requires Linux'):
            rendering_environment('nvidia', 'Darwin', {})
        with self.assertRaisesRegex(ValueError, 'requires macOS'):
            rendering_environment('native', 'Linux', {})

    def test_prepare_freezes_effective_settings_and_rejects_later_edits(self):
        config = load_configuration(overrides={'render': {'device': 'native'},
            'selection': {'cases': ['transport-a04-d1']}, 'batch': {'parallel': 1}})
        with tempfile.TemporaryDirectory() as temporary:
            batch = Path(temporary)/'batch'
            prepare(batch, config)
            self.assertEqual(_frozen_configuration(batch), config)
            document = json.loads((batch/'batch.json').read_text())
            run = Path(document['jobs'][0]['run_directory'])
            self.assertEqual(verify_inputs(run), [])
            harness = json.loads((run/'private/inputs/harness.json').read_text())
            self.assertEqual(harness['startup_timeout_s'], 600)
            self.assertEqual(harness['startup_protocol'], 'direct_controller_v2')
            document['execution']['startup_interval_s'] = 0
            (batch/'batch.json').write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, 'frozen configuration'):
                _frozen_configuration(batch)

    def test_new_standing_team_batches_freeze_direct_start_without_a_ready_barrier(self):
        for topology in ('controller-worker', 'worker-worker'):
            with self.subTest(topology=topology), tempfile.TemporaryDirectory() as temporary:
                config = load_configuration(overrides={'policy': {'topology': topology},
                    'selection': {'cases': ['transport-a04-d1']}, 'batch': {'parallel': 1}})
                batch = Path(temporary)/'batch'
                prepare(batch, config)
                job = json.loads((batch/'batch.json').read_text())['jobs'][0]
                run = Path(job['run_directory'])
                harness = json.loads((run/'private/inputs/harness.json').read_text())
                self.assertEqual(harness['startup_protocol'], 'direct_team_v3')
                roles = json.loads((run/'public/inputs/roles.json').read_text())['roles']
                self.assertEqual(set(roles), {'Meta', 'Controller', 'A', 'B', 'C', 'D'} if topology == 'controller-worker' else {'Meta', 'A', 'B', 'C', 'D'})
                self.assertEqual(verify_inputs(run), [])


if __name__ == '__main__':
    unittest.main()
