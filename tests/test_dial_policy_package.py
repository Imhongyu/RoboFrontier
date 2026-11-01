from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from robofrontier.suite.dial_policy_package import (
    REGISTRY, assert_public, build_review, public_review, read, registry, verify_review, static_geometry,
    selected_report, same_harness,
)
from robofrontier.workstation import Workstation


ROOT = Path(__file__).resolve().parents[1]


class DialPolicyPackageTests(unittest.TestCase):
    def test_relocated_selection_uses_only_the_pinned_local_report(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);relative='runs/oracle/batch/case/attempt/report.json'
            report=root/relative;report.parent.mkdir(parents=True);report.write_text('{"synthetic":true}')
            pinned={'report':relative,'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest()}
            original={'report':'/retired/author/checkout/'+relative}
            self.assertEqual(selected_report(root,original,pinned),report)
            with self.assertRaisesRegex(ValueError,'logical path'):
                selected_report(root,{'report':'/other/report.json'},pinned)
            with self.assertRaisesRegex(ValueError,'checksum'):
                selected_report(root,original,dict(pinned,report_sha256='0'*64))
            with self.assertRaisesRegex(ValueError,'Invalid pinned'):
                selected_report(root,original,dict(pinned,report='../outside/report.json'))

    def test_role_label_rename_does_not_admit_other_harness_changes(self):
        old={'coordinator':'Coordinator','gripper_position_servo':'pd1000-v1'}
        current=dict(old,coordinator='Controller')
        self.assertTrue(same_harness(old,current))
        self.assertEqual(old['coordinator'],'Coordinator')
        self.assertFalse(same_harness(old,dict(current,gripper_position_servo='legacy')))
        self.assertFalse(same_harness(old,dict(current,coordinator='other')))

    def test_historical_witness_cannot_silently_qualify_the_current_candidate(self):
        from robofrontier.suite import dial_policy_package as package
        original=package.read
        for scope in (None,'Qualified current physics'):
            registered=original(ROOT/REGISTRY)
            registered['cases'][0].pop('oracle_evidence_scope',None)
            if scope is not None:registered['cases'][0]['oracle_evidence_scope']=scope
            def altered(path):
                return registered if Path(path)==ROOT/REGISTRY else original(path)
            with self.subTest(scope=scope),patch.object(package,'read',side_effect=altered):
                with self.assertRaisesRegex(ValueError,'Catalog source differs'):
                    registry(ROOT)

    def test_historical_evaluator_bytes_are_verified_without_equating_current_scoring(self):
        from robofrontier.suite import dial_policy_package as package
        original=package.digest
        def altered(path):
            return '0'*64 if str(path).endswith('executor-source/robofrontier/suite/evaluate.py') else original(path)
        with patch.object(package,'digest',side_effect=altered):
            with self.assertRaisesRegex(ValueError,'Frozen evaluator source differs'):
                registry(ROOT)

    def test_all_nine_sources_and_evidence_are_bound_without_promoting_runtime(self):
        with patch('mujoco.mj_step',side_effect=AssertionError('No review physics')):
            value = registry(ROOT)
        self.assertEqual(value,read(ROOT/REGISTRY))
        self.assertEqual(len(value['cases']),9)
        self.assertEqual(sum(c['oracle_evidence']['assisted'] for c in value['cases']),1)
        self.assertFalse(value['formal_policy_ready'])
        self.assertTrue(all(c['runtime_readiness']=='pending_shared_integration' for c in value['cases']))

    def test_public_contract_preserves_best5_and_real_table_holes_without_object_truth(self):
        row = read(ROOT/REGISTRY)['cases'][-1]
        source = Workstation(ROOT/row['oracle_evidence']['recording']/'source')
        with patch('mujoco.mj_step',side_effect=AssertionError('No projection physics')):
            task = public_review(source)
        self.assertEqual(task['mechanism']['feedback']['symbol_count'],5)
        self.assertEqual(task['completion']['stable_duration_sim_s'],.25)
        self.assertEqual(task['task_revision']['scene_revision'],11)
        self.assertTrue(task['process_requirements']['blue_support_required'])
        self.assertEqual(task['static_workstation']['tabletop_z_m'],.8)
        self.assertEqual(task['static_workstation']['geometry_reference'],'table-geometry.json')
        geometries = static_geometry(source)['table_collision_geometries']
        self.assertGreater(len(geometries),10)
        self.assertTrue(any(g['shape']=='mesh' for g in geometries))
        for geom in geometries:
            if 'mesh' in geom:
                mesh = geom['mesh']
                self.assertLess(max(max(f) for f in mesh['triangular_faces']),len(mesh['vertices_local_m']))
        self.assertNotIn('objects',task)
        self.assertNotIn('initial_center_m',task['dials'][0])
        self.assertFalse(task['process_requirements']['nominal_robot_groups_are_exclusive_assignments'])
        self.assertEqual(task['execution_readiness'],'environment_preview_only')

    def test_private_field_and_engineering_path_checks_are_recursive(self):
        for bad in ({'nested':[{'code_symbols':[1,2,3]}]}, {'reference':'runs/oracle/secret'},
                    {'dials':[{'initial_center_m':[0,0,1]}]}):
            with self.assertRaises(ValueError):assert_public(bad)
        assert_public({'arms':{'A':{'base_position_m':[1,0,.8]}}})

    def test_review_build_has_no_runtime_and_rejects_stale_registry(self):
        registered = read(ROOT/REGISTRY)
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)/'review'
            with (patch('mujoco.mj_step',side_effect=AssertionError('No physics')),
                  patch('robofrontier.run_setup.prepare_run',side_effect=AssertionError('No actual run'))):
                build_review(ROOT,folder,registered)
            report = read(folder/'review.json')
            self.assertFalse(report['inference_started'])
            self.assertFalse(report['formal_policy_ready'])
            self.assertEqual(len(list(folder.glob('dial-*/public/task.json'))),9)
            self.assertFalse(list(folder.glob('**/runtime.sqlite')))
            self.assertFalse(list(folder.glob('**/connections')))
            self.assertFalse(list(folder.glob('**/suite-code.json')))
            self.assertEqual(verify_review(ROOT,folder)['cases_verified'],9)
            task_path = folder/registered['cases'][0]['case_id']/'public/task.json'
            task = read(task_path)
            task['completion']['stable_duration_sim_s'] = .5
            task_path.write_text(json.dumps(task))
            with self.assertRaisesRegex(ValueError,'Public task'):
                verify_review(ROOT,folder)
            bad = deepcopy(registered)
            bad['cases'][0]['source_sha256']['scene.xml'] = 'stale'
            with self.assertRaisesRegex(ValueError,'no longer matches'):
                build_review(ROOT,Path(td)/'stale',bad)


if __name__ == '__main__':unittest.main()
