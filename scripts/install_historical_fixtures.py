"""Install an explicitly supplied, checksum-pinned optional historical test bundle."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'robofrontier.local-legacy-test-fixture.v1'
PRESERVATION_RECEIPT = 'docs/generated/frontier-v2/relay-r15/source-preserved-hashes.json'


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def relative_path(value):
    if not isinstance(value, str):
        raise ValueError('Fixture path must be a string')
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or '..' in path.parts or '\\' in value
            or str(path) != value):
        raise ValueError('Invalid fixture path: ' + value)
    if not (value.startswith('configs/environments/') or value.startswith('runs/oracle/')
            or value == PRESERVATION_RECEIPT):
        raise ValueError('Outside historical fixture roots: ' + value)
    return path


def destination(root, name):
    path = root.joinpath(*relative_path(name).parts)
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError('Fixture destination contains a symbolic link: ' + name)
    if path.exists() and not path.is_file():
        raise ValueError('Fixture destination is not a regular file: ' + name)
    return path


def matches(path, entry):
    return path.stat().st_size == entry['bytes'] and digest(path) == entry['sha256']


def install(archive, manifest, manifest_sha256, root=ROOT):
    archive, manifest, root = Path(archive), Path(manifest), Path(root).resolve()
    if not re.fullmatch('[a-f0-9]{64}', manifest_sha256):
        raise ValueError('Require the SHA-256 from the independent bundle delivery receipt')
    raw = manifest.read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest_sha256:
        raise ValueError('Fixture manifest checksum mismatch')
    payload = json.loads(raw)
    if payload.get('schema') != SCHEMA:
        raise ValueError('Unsupported historical fixture schema')
    if archive.stat().st_size != payload['archive_bytes'] or digest(archive) != payload['archive_sha256']:
        raise ValueError('Fixture archive checksum mismatch')
    tracked = set(subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=root).decode().split('\0'))
    entries = {}
    existing = set()
    for entry in payload['files']:
        name = str(relative_path(entry['path']))
        if name in entries or name in tracked:
            raise ValueError('Duplicate or tracked fixture destination: ' + name)
        if (type(entry['bytes']) is not int or entry['bytes'] < 0
                or not re.fullmatch('[a-f0-9]{64}', entry['sha256'])):
            raise ValueError('Invalid fixture checksum or size: ' + name)
        path = destination(root, name)
        if path.exists():
            if not matches(path, entry):
                raise ValueError('Existing fixture differs; preserve and inspect it: ' + name)
            existing.add(name)
        entries[name] = entry
    if not entries:
        raise ValueError('Historical fixture bundle is empty')
    # Validate all content before installing anything. Hardlinks are shared only
    # among staged copies; no installed file links back to an existing fixture.
    with tempfile.TemporaryDirectory(prefix='.historical-fixtures-', dir=root) as temporary:
        stage = Path(temporary)
        seen = set()
        with tarfile.open(archive, 'r|gz') as stream:
            for member in stream:
                name = member.name
                if name not in entries or name in seen:
                    raise ValueError('Unexpected or duplicate archive member: ' + name)
                entry = entries[name]
                target = stage.joinpath(*relative_path(name).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                if member.islnk():
                    if member.linkname not in seen:
                        raise ValueError('Hardlink must name an earlier verified fixture: ' + name)
                    linked = entries[member.linkname]
                    if (linked['sha256'], linked['bytes']) != (entry['sha256'], entry['bytes']):
                        raise ValueError('Hardlink content does not match manifest: ' + name)
                    os.link(stage/member.linkname, target)
                elif member.isfile() and member.size == entry['bytes']:
                    with stream.extractfile(member) as source, target.open('xb') as output:
                        shutil.copyfileobj(source, output)
                    if not matches(target, entry):
                        raise ValueError('Fixture member checksum mismatch: ' + name)
                else:
                    raise ValueError('Only manifest-sized files and verified hardlinks are allowed: ' + name)
                seen.add(name)
        if seen != entries.keys():
            raise ValueError('Fixture archive is incomplete')
        for name, entry in entries.items():
            target = destination(root, name)
            if name in existing:
                if not target.exists() or not matches(target, entry):
                    raise ValueError('Existing fixture changed during verification: ' + name)
            elif target.exists():
                raise ValueError('Fixture appeared during verification: ' + name)
        for name in sorted(entries.keys() - existing):
            target = destination(root, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation: never replace an existing file. If interrupted,
            # rerunning verifies and reuses the already installed exact files.
            os.link(stage/name, target)
    return {'schema': SCHEMA, 'manifest_sha256': manifest_sha256,
            'archive_sha256': payload['archive_sha256'], 'verified': len(entries),
            'installed': len(entries) - len(existing), 'reused': len(existing),
            'scope': 'Historical development fixtures only; no current-task or provider qualification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = install(args.archive, args.manifest, args.manifest_sha256, args.root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
