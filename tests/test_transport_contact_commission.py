"""Compile isolated candidates without qualifying their physical operation."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import mujoco
import numpy as np

from robofrontier.task_families import ROOT, resolve_case
from robofrontier.workstation import Workstation
from scripts.commission_transport_contacts import candidate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TransportContactCommissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, _, case = resolve_case('transport-a08-d2')
        cls.source = ROOT/case['directory']

    def test_released_control_preserves_source_bytes_and_compiled_parameters(self):
        with TemporaryDirectory() as temporary:
            target = Path(temporary)/'scene'
            result = candidate(self.source, target, 'released')
            self.assertEqual(result['scene_sha256'], result['parent_scene_sha256'])
            for name in ('scene.xml', 'task.json', 'environment.json', 'workstation.json'):
                self.assertEqual(digest(target/name), digest(self.source/name))
            self.assertEqual(result['changed_cylinder_geoms'], [])
            self.assertEqual(result['contact_cone'], int(mujoco.mjtCone.mjCONE_PYRAMIDAL))
            Workstation(target)  # Checks actual source hashes and registries.

    def test_only_cone_and_selected_rolling_change_without_touching_originals(self):
        original = mujoco.MjModel.from_xml_path(str(self.source/'scene.xml'))
        before = {str(p.relative_to(self.source)): digest(p)
                  for p in self.source.rglob('*') if p.is_file()}
        with TemporaryDirectory() as temporary:
            target = Path(temporary)/'scene'
            result = candidate(self.source, target, 'elliptic-1mm')
            compiled = Workstation(target).model
            self.assertEqual(compiled.opt.cone, mujoco.mjtCone.mjCONE_ELLIPTIC)
            self.assertNotEqual(result['scene_sha256'], result['parent_scene_sha256'])
            self.assertGreater(len(result['changed_cylinder_geoms']), 0)
            ids = [compiled.geom(n).id for n in result['changed_cylinder_geoms']]
            np.testing.assert_array_equal(compiled.geom_condim, original.geom_condim)
            np.testing.assert_array_equal(compiled.geom_friction[:, :2], original.geom_friction[:, :2])
            np.testing.assert_array_equal(compiled.geom_friction[ids, 2], np.full(len(ids), .001))
            task = json.loads((target/'task.json').read_text())
            self.assertEqual(task['scene_sha256'], result['scene_sha256'])
            self.assertFalse(task['oracle_verified'])
            self.assertEqual(task['engineering_physics_candidate']['variant'], 'elliptic-1mm')
        self.assertEqual(before, {name:digest(self.source/name) for name in before})

    def test_contact_cone_is_in_the_new_candidate_fingerprint(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline = candidate(self.source, root/'original', 'released')
            ellipse = candidate(self.source, root/'ellipse', 'elliptic-30mm')
            self.assertEqual(baseline['rolling_friction_m'], ellipse['rolling_friction_m'])
            self.assertNotEqual(baseline['physics_sha256'], ellipse['physics_sha256'])
            summary = json.loads((root/'ellipse/compiled-physics.json').read_text())
            self.assertEqual(summary['solver']['cone'], int(mujoco.mjtCone.mjCONE_ELLIPTIC))
            self.assertEqual(summary['solver']['noslip_tolerance'], ellipse['noslip_tolerance'])

    def test_invalid_candidate_and_source_subdirectory_fail_before_copy(self):
        with TemporaryDirectory() as temporary:
            target = Path(temporary)/'scene'
            with self.assertRaisesRegex(ValueError, 'Unknown contact candidate'):
                candidate(self.source, target, 'unpublished')
            self.assertFalse(target.exists())
        with self.assertRaisesRegex(ValueError, 'separate from the source'):
            candidate(self.source, self.source/'not-a-candidate', 'elliptic-1mm')
        self.assertFalse((self.source/'not-a-candidate').exists())


if __name__ == '__main__':
    unittest.main()
