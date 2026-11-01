import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

from scripts.install_historical_fixtures import SCHEMA, install


class HistoricalFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base/'checkout'
        self.root.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.archive = self.base/'fixtures.tar.gz'
        self.manifest = self.base/'fixtures.json'

    def bundle(self, files, members=None):
        with tarfile.open(self.archive, 'w:gz') as stream:
            for name, value in (members or files).items():
                member = tarfile.TarInfo(name)
                if isinstance(value, tuple):
                    member.type, member.linkname = value
                    stream.addfile(member)
                else:
                    member.size = len(value)
                    stream.addfile(member, io.BytesIO(value))
        payload = {'schema': SCHEMA, 'archive_bytes': self.archive.stat().st_size,
                   'archive_sha256': hashlib.sha256(self.archive.read_bytes()).hexdigest(),
                   'files': [{'path': n, 'bytes': len(v), 'sha256': hashlib.sha256(v).hexdigest()}
                             for n, v in files.items()]}
        self.manifest.write_text(json.dumps(payload))
        return hashlib.sha256(self.manifest.read_bytes()).hexdigest()

    def run_install(self, pin):
        return install(self.archive, self.manifest, pin, self.root)

    def test_relocated_install_reuses_exact_files_and_shares_only_new_copies(self):
        first, second = 'configs/environments/old/assets/a.png', 'runs/oracle/closed/motion/events.jsonl'
        pin = self.bundle({first: b'original', second: b'original'},
                          {first: b'original', second: (tarfile.LNKTYPE, first)})
        report = self.run_install(pin)
        self.assertEqual((report['installed'], report['reused']), (2, 0))
        self.assertEqual((self.root/first).read_bytes(), b'original')
        self.assertEqual((self.root/first).stat().st_ino, (self.root/second).stat().st_ino)
        self.assertEqual(self.run_install(pin)['reused'], 2)
        self.assertFalse(list(self.root.glob('.historical-fixtures-*')))

    def test_wrong_manifest_or_archive_pin_never_installs(self):
        pin = self.bundle({'configs/environments/old/a.png': b'original'})
        with self.assertRaisesRegex(ValueError, 'manifest checksum'):
            self.run_install('0'*64)
        with self.archive.open('ab') as output:
            output.write(b'changed')
        with self.assertRaisesRegex(ValueError, 'archive checksum'):
            self.run_install(pin)
        self.assertFalse((self.root/'configs').exists())

    def test_existing_different_evidence_is_preserved(self):
        name = 'runs/oracle/closed/report.json'
        pin = self.bundle({name: b'original'})
        target = self.root/name
        target.parent.mkdir(parents=True)
        target.write_bytes(b'local-different')
        with self.assertRaisesRegex(ValueError, 'Existing fixture differs'):
            self.run_install(pin)
        self.assertEqual(target.read_bytes(), b'local-different')

    def test_tracked_source_cannot_be_installed_even_when_identical(self):
        name = 'configs/environments/old/scene.xml'
        pin = self.bundle({name: b'<original/>'})
        target = self.root/name
        target.parent.mkdir(parents=True)
        target.write_bytes(b'<original/>')
        subprocess.run(['git', 'add', name], cwd=self.root, check=True)
        with self.assertRaisesRegex(ValueError, 'tracked fixture'):
            self.run_install(pin)

    def test_path_traversal_and_unrelated_roots_are_rejected(self):
        for name in ('/runs/oracle/a', 'runs/oracle/../../outside', 'runs/oracle//a',
                     'runs/oracle/./a', 'robofrontier/pipeline.py', '.codex/auth.json',
                     'outputs/oracle/relay-edited-tracks-20261027/relay-a08-d1/session.json',
                     'outputs/oracle/relay-edited-tracks-20261027/relay-a08-d1/source/unreviewed.py'):
            with self.subTest(name=name):
                pin = self.bundle({name: b'original'})
                with self.assertRaises(ValueError):
                    self.run_install(pin)
        self.assertFalse((self.root/'runs').exists())

    def test_dated_relay_source_alias_and_assets_are_portable(self):
        prefix = 'outputs/oracle/relay-edited-tracks-20261027/relay-a08-d1/source/'
        files = {prefix+'scene.xml': b'original scene', prefix+'assets/label.png': b'original asset'}
        pin = self.bundle(files)
        self.assertEqual(self.run_install(pin)['installed'], 2)
        for name, content in files.items():
            self.assertEqual((self.root/name).read_bytes(), content)

    def test_destination_symlink_is_rejected(self):
        outside = self.base/'outside'
        outside.mkdir()
        (self.root/'runs').symlink_to(outside, target_is_directory=True)
        pin = self.bundle({'runs/oracle/closed/report.json': b'original'})
        with self.assertRaisesRegex(ValueError, 'symbolic link'):
            self.run_install(pin)
        self.assertEqual(list(outside.iterdir()), [])

    def test_late_corruption_installs_nothing(self):
        first, second = 'runs/oracle/old/a.json', 'runs/oracle/old/b.json'
        pin = self.bundle({first: b'original', second: b'original'},
                          {first: b'original', second: b'tampered'})
        with self.assertRaisesRegex(ValueError, 'member checksum'):
            self.run_install(pin)
        self.assertFalse((self.root/'runs').exists())

    def test_hardlink_to_outside_or_unverified_content_is_rejected(self):
        first, second = 'runs/oracle/old/a', 'runs/oracle/old/b'
        for link in ('/etc/passwd', '../outside', second):
            with self.subTest(link=link):
                pin = self.bundle({first: b'original'}, {first: (tarfile.LNKTYPE, link)})
                with self.assertRaisesRegex(ValueError, 'earlier verified'):
                    self.run_install(pin)
        pin = self.bundle({first: b'original', second: b'different'},
                          {first: b'original', second: (tarfile.LNKTYPE, first)})
        with self.assertRaisesRegex(ValueError, 'Hardlink content'):
            self.run_install(pin)

    def test_incomplete_or_extra_archive_members_are_rejected(self):
        first, second = 'runs/oracle/old/a', 'runs/oracle/old/b'
        for files, members in (({first: b'a', second: b'b'}, {first: b'a'}),
                               ({first: b'a'}, {first: b'a', second: b'b'})):
            pin = self.bundle(files, members)
            with self.assertRaises(ValueError):
                self.run_install(pin)
        self.assertFalse((self.root/'runs').exists())

    def test_archive_symlink_cannot_write_outside_checkout(self):
        name = 'runs/oracle/old/report.json'
        pin = self.bundle({name: b'original'}, {name: (tarfile.SYMTYPE, '/tmp/outside')})
        with self.assertRaisesRegex(ValueError, 'Only manifest-sized files'):
            self.run_install(pin)
        self.assertFalse((self.root/'runs').exists())


if __name__ == '__main__':
    unittest.main()
