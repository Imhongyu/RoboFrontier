"""Build or verify an offline English atlas of current public policy tasks.

No Oracle, puzzle input, runtime database, model or physics stepping is used.
Rendering only resets the declared initial keyframe and runs forward kinematics.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = ('scripts/build_task_atlas.py', 'web/task-atlas/index.html',
                'web/task-atlas/style.css', 'web/task-atlas/atlas.js')
FAMILIES = ('transport', 'mosaic', 'relay', 'dial')
TITLES = dict(transport='Transport', mosaic='Mosaic', relay='Relay', dial='Dial')
DESCRIPTIONS = {
    'transport': 'Deliver visibly identified materials to their requested stations and physical placements.',
    'mosaic': 'Assemble every cell of a shared color pattern using released, stable cubes.',
    'relay': 'Move complete beam assemblies into the final goal, coordinating shared manipulation.',
    'dial': 'Manipulate physical dial modules and solve a hidden code using visible aggregate feedback.',
}
# These are fields of the policy's actual public contract, not raw environment or
# reference-executor state. Do not replace this allowlist with task/environment dumps.
PUBLIC_FIELDS = ('id', 'family', 'level', 'arms', 'coordinate_frame', 'objective',
    'rules', 'completion', 'mechanism', 'target', 'initial_supplies', 'orders',
    'dials', 'stations', 'closed_loop', 'workspace_world_m', 'table_geometry',
    'observation_contract', 'gripper_profile', 'process_requirements')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode()


def english(value):
    if re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', value):
        raise ValueError('Atlas source contains untranslated text')


def public_case(case_id):
    """Use the same terminal-scoring overlay as a new policy run."""
    from robofrontier.task_config import public_task
    from robofrontier.task_families import freeze_public, policy_task, resolve_case
    task = policy_task(case_id)
    public = public_task(task)
    with tempfile.TemporaryDirectory(prefix='rf-atlas-public-') as temporary:
        root = Path(temporary)
        (root/'public/inputs').mkdir(parents=True)
        (root/'private/inputs').mkdir(parents=True)
        freeze_public(task, root, public)
        # Relay keeps a terminal description; the other families publish their Skill.
        family = root/'public/inputs/family'
        guidance = (family/'family-guidance.md' if (family/'family-guidance.md').is_file() else family/'skill.md').read_text()
    family, _, case = resolve_case(case_id)
    record = {key: public[key] for key in PUBLIC_FIELDS if key in public}
    record['arm_count'] = len(task['arms'])
    record['family_guidance'] = guidance
    record['source'] = {'scene_sha256': case['source_files']['scene.xml'],
                        'task_sha256': case['source_files']['task.json'],
                        'qualification': case['qualification']}
    record['views'] = {camera: f'images/{case_id}-{camera}.jpg' for camera in ('top', 'global')}
    english(encoded(record).decode())
    return record


def current_data():
    from robofrontier.task_families import RELEASE
    release = json.loads((ROOT/RELEASE).read_text())
    cases = [public_case(c['id']) for name in FAMILIES for c in release['families'][name]['gpt']]
    return {'schema': 'robofrontier.public-task-atlas.v1',
            'release_sha256': digest(ROOT/RELEASE), 'cases': cases,
            'scope': 'Public current policy contracts and static initial renders; no task-success or physical-qualification claim'}


def render_case(record, output):
    import mujoco
    import numpy as np
    from PIL import Image
    from robofrontier.task_families import resolve_case
    _, _, case = resolve_case(record['id'])
    model = mujoco.MjModel.from_xml_path(str(ROOT/case['directory']/'scene.xml'))
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key('initial').id)
    mujoco.mj_forward(model, data)
    initial = data.qpos.copy()
    model.vis.global_.offwidth = max(896, model.vis.global_.offwidth)
    model.vis.global_.offheight = max(560, model.vis.global_.offheight)
    with mujoco.Renderer(model, width=896, height=560, max_geom=max(5000, model.ngeom+1000)) as renderer:
        from robofrontier.render_backend import current_backend
        backend = current_backend(os.environ['ROBOFRONTIER_ATLAS_DEVICE'])
        for camera, name in record['views'].items():
            renderer.update_scene(data, camera=camera)
            image = Image.fromarray(renderer.render())
            image.save(output/name, format='JPEG', quality=85)
    if data.time != 0 or not np.array_equal(initial, data.qpos):
        raise ValueError('Static atlas renderer changed the initial state')
    return backend


def card(record):
    esc = lambda value: html.escape(str(value), quote=True)
    case_id = record['id']
    rules = ''.join('<li>'+esc(rule)+'</li>' for rule in record['rules'])
    completion = esc(json.dumps(record['completion'], indent=2))
    source = record['source']
    return f'''<article class="case" id="{esc(case_id)}" data-family="{esc(record['family'])}" data-level="{record['level']}" data-arms="{record['arm_count']}">
<div class="case-meta"><span>{TITLES[record['family']]} / Level {record['level']}</span><span>{record['arm_count']} arms</span></div>
<h3>{esc(case_id)}</h3>
<a class="image-link" href="{record['views']['top']}" target="_blank" rel="noopener"><img loading="lazy" width="896" height="560" src="{record['views']['top']}" alt="Initial top view of {esc(case_id)}"></a>
<div class="view-buttons" aria-label="Camera view"><button type="button" data-view="top" aria-pressed="true">Top</button><button type="button" data-view="global" aria-pressed="false">Front</button></div>
<p>{esc(record['objective'])}</p>
<details><summary>Task rules and completion</summary><ol>{rules}</ol><p>Completion is evaluated independently. Process events are reported separately. Dial remains complete after its first valid unlock.</p><pre>{completion}</pre></details>
<details><summary>Published source identity</summary><p>Scene SHA-256</p><code>{source['scene_sha256']}</code><p>Source qualification label</p><code>{esc(source['qualification'])}</code><p>This label is provenance, not a new validation result.</p></details>
<a class="download" href="tasks/{esc(case_id)}.json" download>Download public task JSON <span aria-hidden="true">↗</span></a>
</article>'''


def page(data, *, template=None):
    family_links = ''.join(f'<a class="family-card" href="#cases" data-family-filter="{name}"><img src="{next(c for c in data["cases"] if c["family"] == name)["views"]["global"]}" width="896" height="560" alt="{TITLES[name]} initial scene"><span><strong>{TITLES[name]}</strong><small>{DESCRIPTIONS[name]}</small></span></a>' for name in FAMILIES)
    if template is None:
        template = (ROOT/'web/task-atlas/index.html').read_text()
    for key, value in {'FAMILY_CARDS': family_links,
                       'CASE_CARDS': '\n'.join(card(c) for c in data['cases']),
                       'RELEASE_SHA': data['release_sha256']}.items():
        template = template.replace('{{'+key+'}}', value)
    return template


def build(output):
    output = Path(output)
    if output.exists():
        raise ValueError('Choose a new atlas output; existing atlases are never overwritten')
    data = current_data()  # Validate all public inputs before creating output.
    output.mkdir(parents=True)
    (output/'images').mkdir()
    (output/'tasks').mkdir()
    backends = []
    for record in data['cases']:
        backends.append(render_case(record, output))
        (output/'tasks'/(record['id']+'.json')).write_bytes(encoded(record))
        print(record['id'], file=sys.stderr, flush=True)
    for name in ('style.css', 'atlas.js'):
        (output/name).write_bytes((ROOT/'web/task-atlas'/name).read_bytes())
    (output/'tasks.json').write_bytes(encoded(data))
    (output/'index.html').write_text(page(data))
    (output/'.nojekyll').write_text('')
    # The rendered artifact is traceable to the exact generator/templates, not a
    # mutable branch name. Subsequent modifications make verification fail.
    files = {p.relative_to(output).as_posix(): digest(p) for p in sorted(output.rglob('*')) if p.is_file()}
    manifest = {'schema': 'robofrontier.task-atlas-manifest.v1',
                'release_sha256': data['release_sha256'], 'cases': len(data['cases']),
                'sources': {name: digest(ROOT/name) for name in SOURCE_FILES},
                'files': files, 'renderer': backends[0],
                'model_calls': 0, 'physics_steps': 0, 'image_profile': 'jpeg_896x560_q85'}
    if any(backend != backends[0] for backend in backends):
        raise ValueError('Atlas renderer changed between cases')
    (output/'atlas-manifest.json').write_bytes(encoded(manifest))
    return verify(output)


def verify(output):
    """Verify delivered files and current public inputs without opening OpenGL."""
    return _verify(output, {name:(ROOT/name).read_bytes() for name in SOURCE_FILES})


def _verify_capture(manifest):
    """Bind refreshed presentation to unchanged original capture evidence."""
    capture=manifest['capture']
    original=capture['manifest']
    if (not re.fullmatch(r'[0-9a-f]{40}',capture['source_commit']) or
        original['schema']!='robofrontier.task-atlas-manifest.v1' or
        hashlib.sha256(encoded(original)).hexdigest()!=capture['manifest_sha256']):
        raise ValueError('Atlas capture provenance differs')
    for field in ('release_sha256','cases','renderer','model_calls','physics_steps','image_profile'):
        if manifest[field]!=original[field]:
            raise ValueError('Atlas capture metadata changed: '+field)
    if set(original['sources'])!=set(SOURCE_FILES) or set(original['files'])!=set(manifest['files']):
        raise ValueError('Atlas capture inventory differs')
    for name,checksum in original['files'].items():
        # Public contract text may be refreshed; captured images may not.
        if (name not in ('index.html','style.css','atlas.js','tasks.json') and not name.startswith('tasks/')
                and manifest['files'][name]!=checksum):
            raise ValueError('Atlas captured payload changed: '+name)


def _verify(output, sources, expected=None):
    from PIL import Image
    output = Path(output)
    manifest = json.loads((output/'atlas-manifest.json').read_text())
    if manifest['schema'] not in ('robofrontier.task-atlas-manifest.v1','robofrontier.task-atlas-manifest.v2'):
        raise ValueError('Unknown task atlas schema')
    data = json.loads((output/'tasks.json').read_text())
    expected = current_data() if expected is None else expected
    if data != expected:
        # A reviewed task-only revision changes the release identity, not the
        # captured images (configs/policy-assets.json archive_release_sha256).
        from scripts.benchmark_handoff import pinned_asset_release
        try:
            original_release = pinned_asset_release(ROOT,
                json.loads((ROOT/'configs/policy-assets.json').read_text()))
        except (ValueError, KeyError, OSError):
            original_release = None
        if original_release is not None:
            expected = dict(expected, release_sha256=original_release)
    if data != expected:
        raise ValueError('Atlas public contracts are stale or changed')
    if manifest['cases'] != len(data['cases']) or manifest['release_sha256'] != data['release_sha256']:
        raise ValueError('Atlas release identity differs')
    if set(manifest['sources']) != set(SOURCE_FILES):
        raise ValueError('Atlas source inventory differs')
    for name, checksum in manifest['sources'].items():
        if hashlib.sha256(sources[name]).hexdigest() != checksum:
            raise ValueError('Atlas generator changed: '+name)
    payload_names = {'index.html', 'style.css', 'atlas.js', 'tasks.json', '.nojekyll'}
    for record in data['cases']:
        payload_names.add('tasks/'+record['id']+'.json')
        payload_names.update(record['views'].values())
    if set(manifest['files']) != payload_names:
        raise ValueError('Atlas payload inventory differs from the public allowlist')
    expected = payload_names | {'atlas-manifest.json'}
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    if actual != expected or any(p.is_symlink() for p in output.rglob('*')):
        raise ValueError('Unexpected atlas file or symlink')
    for name, checksum in manifest['files'].items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or digest(output/name) != checksum:
            raise ValueError('Atlas payload changed: '+name)
        if relative.suffix in ('.html', '.css', '.js', '.json'):
            text = (output/name).read_text()
            english(text)
            if re.search(r'/Users/|/home/|file://|code_symbols|private/inputs|oracle_solution', text):
                raise ValueError('Atlas contains local/private data: '+name)
    if manifest['schema']=='robofrontier.task-atlas-manifest.v2':
        _verify_capture(manifest)
    if (output/'index.html').read_text() != page(data,template=sources['web/task-atlas/index.html'].decode()):
        raise ValueError('Atlas page differs from current public contracts/templates')
    for name in ('style.css', 'atlas.js'):
        if (output/name).read_bytes() != sources['web/task-atlas/'+name]:
            raise ValueError('Atlas browser source differs: '+name)
    for record in data['cases']:
        if json.loads((output/'tasks'/(record['id']+'.json')).read_text()) != record:
            raise ValueError('Per-case atlas contract differs')
        for name in record['views'].values():
            with Image.open(output/name) as image:
                if image.format != 'JPEG' or image.size != (896, 560):
                    raise ValueError('Unexpected atlas image profile')
                image.load()
    # All local links must be portable, including file:// offline use.
    from html.parser import HTMLParser
    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key in ('src', 'href') and value and not value.startswith(('#', 'https://')):
                    relative = Path(value)
                    if relative.is_absolute() or '..' in relative.parts or not (output/relative).is_file():
                        raise ValueError('Broken atlas link: '+value)
    Links().feed((output/'index.html').read_text())
    return {'cases': len(data['cases']), 'images': len(data['cases'])*2,
            'release_sha256': data['release_sha256'], 'verified': True,
            'bytes': sum(p.stat().st_size for p in output.rglob('*') if p.is_file())}


def refresh(source, output, source_revision):
    """Regenerate presentation from a committed publication; never render.

    All inputs/contracts and captured image bytes must still match the original
    publication. The supplied commit checks the incoming manifest and
    generator/template identities against local Git history before any write.
    """
    source,output=Path(source),Path(output)
    if output.exists():
        raise ValueError('Choose a new atlas output; existing atlases are never overwritten')
    if output.resolve().is_relative_to(source.resolve()):
        raise ValueError('Place refreshed output outside the source atlas')
    if not isinstance(source_revision,str) or not re.fullmatch(r'[0-9a-f]{40}',source_revision):
        raise ValueError('Supply the full immutable source commit ID')
    def committed(name):
        try:
            return subprocess.check_output(['git','show',source_revision+':'+name],cwd=ROOT,stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as exc:
            raise ValueError('Source commit/publication unavailable; fetch its history first') from exc
    original_bytes=(source/'atlas-manifest.json').read_bytes()
    if original_bytes!=committed('docs/task-atlas/atlas-manifest.json'):
        raise ValueError('Atlas does not match the committed publication')
    sources={name:committed(name) for name in SOURCE_FILES}
    # The source must match its own publication; its contracts may predate current ones.
    _verify(source,sources,json.loads(committed('docs/task-atlas/tasks.json')))
    original=json.loads(original_bytes)
    if original['schema']=='robofrontier.task-atlas-manifest.v1':
        if encoded(original)!=original_bytes:
            raise ValueError('Original capture manifest must use canonical encoding')
        capture={'source_commit':source_revision,'manifest_sha256':digest(source/'atlas-manifest.json'),
                 'manifest':original}
    else:
        capture=original['capture']
    output.mkdir(parents=True)
    for name in original['files']:
        target=output/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source/name,target)
    old=json.loads((source/'tasks.json').read_text())
    data=current_data()
    if data['release_sha256']!=old['release_sha256']:
        # A reviewed task-only revision keeps the captured release identity (see
        # _verify); any other release change needs a new capture.
        from scripts.benchmark_handoff import pinned_asset_release
        if old['release_sha256']==pinned_asset_release(ROOT,json.loads((ROOT/'configs/policy-assets.json').read_text())):
            data=dict(data,release_sha256=old['release_sha256'])
    # Text-only refresh: the same cases, scenes and captured views; only the contract
    # (its text and its task hash) may change.
    captured=lambda cases:[(c['id'],c['views'],{k:v for k,v in c['source'].items() if k!='task_sha256'}) for c in cases]
    if data['release_sha256']!=old['release_sha256'] or captured(data['cases'])!=captured(old['cases']):
        raise ValueError('Release, cases or scenes changed; build and capture a new atlas instead')
    (output/'tasks.json').write_bytes(encoded(data))
    for record in data['cases']:(output/'tasks'/(record['id']+'.json')).write_bytes(encoded(record))
    (output/'index.html').write_text(page(data))
    for name in ('style.css','atlas.js'):
        (output/name).write_bytes((ROOT/'web/task-atlas'/name).read_bytes())
    manifest={**original,'schema':'robofrontier.task-atlas-manifest.v2','capture':capture,
        'sources':{name:digest(ROOT/name) for name in SOURCE_FILES},
        'files':{name:digest(output/name) for name in original['files']}}
    (output/'atlas-manifest.json').write_bytes(encoded(manifest))
    return verify(output)


def archive(output, target):
    target = Path(target)
    if target.resolve().is_relative_to(Path(output).resolve()):
        raise ValueError('Place the ZIP outside the atlas directory')
    verify(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as zipped:
        for path in sorted(Path(output).rglob('*')):
            if path.is_file():
                entry = zipfile.ZipInfo(path.relative_to(output).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                zipped.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(target) as zipped:
        if zipped.testzip() is not None:
            raise ValueError('Atlas ZIP verification failed')
    return {'zip': str(target), 'sha256': digest(target), 'bytes': target.stat().st_size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('build', 'refresh', 'verify', 'zip'))
    parser.add_argument('--output', type=Path, default=ROOT/'docs/task-atlas')
    parser.add_argument('--render', choices=('native', 'nvidia', 'cpu'), default='nvidia')
    parser.add_argument('--zip', type=Path)
    parser.add_argument('--source',type=Path,default=ROOT/'docs/task-atlas',help='Committed publication to reuse for refresh')
    parser.add_argument('--source-revision',help='Full commit ID of the source publication; required for refresh')
    args = parser.parse_args()
    if args.command == 'build':
        from robofrontier.configuration import rendering_environment
        os.environ.update(rendering_environment(args.render, platform.system(), os.environ))
        # rendering_environment deliberately removes stale backend settings.
        for key in ('MUJOCO_GL', 'PYOPENGL_PLATFORM', 'LIBGL_ALWAYS_SOFTWARE', 'GALLIUM_DRIVER'):
            if key not in rendering_environment(args.render, platform.system(), {}):
                os.environ.pop(key, None)
        os.environ['ROBOFRONTIER_ATLAS_DEVICE'] = args.render
        result = build(args.output)
    elif args.command == 'refresh':
        if not args.source_revision:
            parser.error('refresh requires --source-revision with the full source commit ID')
        result=refresh(args.source,args.output,args.source_revision)
    elif args.command == 'verify':
        result = verify(args.output)
    else:
        if not args.zip:
            parser.error('zip requires --zip /path/to/new-task-atlas.zip')
        result = archive(args.output, args.zip)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
