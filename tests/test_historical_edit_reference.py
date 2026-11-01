"""Authenticate relocated historical timelines without renaming original evidence."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.prepare_factory_edits import historical_edit, MOSAIC_VIDEO_INDEX
from robofrontier.task_families import sha


class HistoricalEditReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.case = 'mosaic-a04-6x12-d1'
        self.relative = Path(MOSAIC_VIDEO_INDEX).parent/'legacy-timelines'/(self.case+'.json')
        self.edit = self.root/self.relative
        self.edit.parent.mkdir(parents=True)
        self.edit.write_text('{"original": true}\n')
        self.entry = dict(case_id=self.case,
            motion_edit_timeline=str(Path('/Users/fanchangxuan/Repos/roomscript2')/self.relative),
            motion_edit_timeline_sha256=sha(self.edit))
        self.index = self.root/MOSAIC_VIDEO_INDEX
        self.row = dict(id=self.case, edit='current-edit.json', edit_sha256='unused',
            historical_edit=dict(kind='mosaic_video_index', path=MOSAIC_VIDEO_INDEX, sha256=''),
            historical_edit_sha256=sha(self.edit))
        self.publish([self.entry])

    def publish(self, entries):
        self.index.write_text(json.dumps(dict(videos=entries)))
        self.row['historical_edit']['sha256'] = sha(self.index)

    def test_legacy_root_relocates_and_duplicate_views_share_one_original(self):
        self.publish([self.entry, deepcopy(self.entry)])
        before = self.edit.read_bytes(), self.index.read_bytes()
        path, checksum = historical_edit(self.row, self.root)
        self.assertEqual(path, self.edit)
        self.assertEqual(checksum, sha(self.edit))
        self.assertEqual(before, (self.edit.read_bytes(), self.index.read_bytes()))

    def test_relative_and_current_absolute_references_relocate(self):
        for path in (str(self.relative), str(self.edit.absolute()), str(self.edit.resolve())):
            with self.subTest(path=path):
                self.publish([dict(self.entry, motion_edit_timeline=path)])
                self.assertEqual(historical_edit(self.row, self.root)[0], self.edit)

    def test_index_and_edit_tampering_are_independently_rejected(self):
        self.index.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'index differs'):
            historical_edit(self.row, self.root)
        self.publish([self.entry])
        self.edit.write_text('different original')
        with self.assertRaisesRegex(ValueError, 'edit bytes'):
            historical_edit(self.row, self.root)

    def test_wrong_case_checksum_and_ambiguous_views_are_rejected(self):
        for entries in ([dict(self.entry, case_id='other')],
                        [dict(self.entry, motion_edit_timeline_sha256='wrong')],
                        [self.entry, dict(self.entry, motion_edit_timeline=str(
                            self.relative.parent.parent/'other'/(self.case+'.json')))]):
            with self.subTest(entries=entries):
                self.publish(entries)
                with self.assertRaises(ValueError):
                    historical_edit(self.row, self.root)

    def test_external_roots_traversal_wrong_names_and_symlinks_are_rejected(self):
        for path in ('/another/home/'+str(self.relative), '../'+str(self.relative),
                     str(self.relative.parent/'wrong-case.json'), 'bad\\path.json'):
            with self.subTest(path=path):
                self.publish([dict(self.entry, motion_edit_timeline=path)])
                with self.assertRaises(ValueError):
                    historical_edit(self.row, self.root)
        outside = self.root/'outside.json'
        outside.write_bytes(self.edit.read_bytes())
        self.edit.unlink()
        self.edit.symlink_to(outside)
        self.publish([self.entry])
        with self.assertRaisesRegex(ValueError, 'escapes'):
            historical_edit(self.row, self.root)

    def test_direct_paths_remain_supported_and_checked(self):
        row = dict(self.row, historical_edit=str(self.relative))
        self.assertEqual(historical_edit(row, self.root), (self.edit, sha(self.edit)))
        self.edit.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'edit bytes'):
            historical_edit(row, self.root)

    def test_unknown_index_reference_is_rejected(self):
        for field, value in [('kind', 'other'), ('path', 'other-index.json'), ('extra', True)]:
            with self.subTest(field=field):
                row = deepcopy(self.row)
                row['historical_edit'][field] = value
                with self.assertRaisesRegex(ValueError, 'Unknown historical'):
                    historical_edit(row, self.root)
