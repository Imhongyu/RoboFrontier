"""Public-contract and portable-artifact checks, with no model/physics calls."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from scripts import build_task_atlas as atlas


class TaskAtlasTests(unittest.TestCase):
    def test_contracts_cover_current_release_and_terminal_overlays_without_secrets(self):
        with patch('mujoco.mj_step', side_effect=AssertionError('No physics')):
            data = atlas.current_data()
        rows = data['cases']
        self.assertEqual(len(rows), 36)
        self.assertEqual(len({row['id'] for row in rows}), 36)
        for family in atlas.FAMILIES:
            self.assertEqual(sum(row['family'] == family for row in rows), 9)
        by_id = {row['id']: row for row in rows}
        self.assertFalse(by_id['transport-a04-d1']['completion']['acceptance']['process_compliance_required'])
        self.assertFalse(by_id['mosaic-a04-6x12-d1']['completion']['process_violations_clear_required'])
        self.assertFalse(by_id['relay-a08-d1']['completion']['required_airborne_handover'])
        self.assertIn('latched', by_id['dial-best5-n04-d1']['completion']['success_semantics'])
        text = atlas.encoded(data).decode()
        for forbidden in ('code_symbols', 'private/inputs', '/Users/', '/home/', 'oracle_solution'):
            self.assertNotIn(forbidden, text)
        atlas.english(text)

    def test_raw_private_fields_never_enter_the_public_atlas(self):
        from robofrontier.task_families import policy_task
        task = policy_task('dial-best5-n04-d1')
        task['oracle_solution'] = 'SECRET_NOT_FOR_ATLAS'
        task['code_symbols'] = [1, 2, 3, 4]
        with patch('robofrontier.task_families.policy_task', return_value=task):
            text = atlas.encoded(atlas.public_case(task['id'])).decode()
        self.assertNotIn('SECRET_NOT_FOR_ATLAS', text)
        self.assertNotIn('code_symbols', text)

    def test_delivered_site_is_current_and_zip_restores_every_file(self):
        source = atlas.ROOT/'docs/task-atlas'
        self.assertEqual(atlas.verify(source)['images'], 72)
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary)/'atlas.zip'
            result = atlas.archive(source, archive)
            with zipfile.ZipFile(archive) as zipped:
                self.assertIsNone(zipped.testzip())
                self.assertEqual(len(zipped.namelist()), len(set(zipped.namelist())))
                restored = Path(temporary)/'restored'
                zipped.extractall(restored)
            self.assertTrue(atlas.verify(restored)['verified'])
            for name in json.loads((source/'atlas-manifest.json').read_text())['files']:
                self.assertEqual((source/name).read_bytes(), (restored/name).read_bytes())
            self.assertEqual(result['sha256'], atlas.digest(archive))
            # Delivery generation is deterministic and refuses replacement.
            other = Path(temporary)/'other.zip'
            atlas.archive(source, other)
            self.assertEqual(archive.read_bytes(), other.read_bytes())
            with self.assertRaises(FileExistsError):
                atlas.archive(source, archive)

    def test_tampered_image_and_unlisted_files_fail_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'atlas'
            shutil.copytree(atlas.ROOT/'docs/task-atlas', output)
            image = next((output/'images').glob('*.jpg'))
            original = image.read_bytes()
            image.write_bytes(b'not the delivered image')
            with self.assertRaisesRegex(ValueError, 'payload changed'):
                atlas.verify(output)
            image.write_bytes(original)
            (output/'secret.txt').write_text('unexpected')
            with self.assertRaisesRegex(ValueError, 'Unexpected atlas file'):
                atlas.verify(output)

    def test_stale_public_contract_rejected_even_if_payload_hash_is_rewritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'atlas'
            shutil.copytree(atlas.ROOT/'docs/task-atlas', output)
            data = json.loads((output/'tasks.json').read_text())
            data['cases'][0]['completion']['acceptance']['process_compliance_required'] = True
            (output/'tasks.json').write_bytes(atlas.encoded(data))
            manifest = json.loads((output/'atlas-manifest.json').read_text())
            manifest['files']['tasks.json'] = atlas.digest(output/'tasks.json')
            (output/'atlas-manifest.json').write_bytes(atlas.encoded(manifest))
            with self.assertRaisesRegex(ValueError, 'contracts are stale'):
                atlas.verify(output)

    def test_even_manifest_listed_extra_payload_is_not_publishable(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'atlas'
            shutil.copytree(atlas.ROOT/'docs/task-atlas', output)
            (output/'.env').write_text('SHOULD_NOT_BE_PUBLIC=fixture')
            manifest = json.loads((output/'atlas-manifest.json').read_text())
            manifest['files']['.env'] = atlas.digest(output/'.env')
            (output/'atlas-manifest.json').write_bytes(atlas.encoded(manifest))
            with self.assertRaisesRegex(ValueError, 'public allowlist'):
                atlas.verify(output)

    def test_zip_cannot_include_itself_or_contaminate_published_site(self):
        output = atlas.ROOT/'docs/task-atlas'
        target = output/'should-not-exist.zip'
        with self.assertRaisesRegex(ValueError, 'outside the atlas'):
            atlas.archive(output, target)
        self.assertFalse(target.exists())

    def test_existing_atlas_is_not_rebuilt_or_overwritten(self):
        with patch('scripts.build_task_atlas.render_case') as renderer:
            with self.assertRaisesRegex(ValueError, 'never overwritten'):
                atlas.build(atlas.ROOT/'docs/task-atlas')
        renderer.assert_not_called()


if __name__ == '__main__':
    unittest.main()
