"""Editable, source-bound Factory cameras and English video post-production.

Projects are editable until copied into a render plan. Captions never advance
physics; their compositor verifies media, not the scene depicted by an input.
"""
from copy import deepcopy
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from . import factory_bundle as bundle

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'robofrontier.factory-editorial.v1'
DEFAULT_DURATION = 210.5
FONT = ROOT/'assets/robo_factory/fonts/BarlowCondensed-SemiBold.ttf'
LICENSE = FONT.with_name('OFL.txt')
FIELDS = {'schema', 'language', 'duration_s', 'fps', 'source', 'camera_plan',
          'titles', 'subtitles', 'font', 'font_license', 'style'}
STYLE = {'title_size': 64, 'subtitle_size': 40, 'title_margin': 60,
         'subtitle_margin': 64, 'horizontal_margin': 90, 'color': '#FFFFFF'}
STAMP = re.compile(r'(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})\Z')


def _number(value, name, minimum=0, maximum=86400):
    if type(value) not in (int, float) or not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError('Invalid editorial '+name)
    return value


def _source(data_root):
    root = Path(data_root).resolve()
    manifest = bundle.read(root/'bundle.json')
    return {'bundle_sha256': bundle.digest(root/'bundle.json'),
            'scene_sha256': bundle.digest(bundle.inside(root, manifest['scene'])),
            'cameras_sha256': bundle.digest(bundle.inside(root, manifest['cameras'])),
            'release_sha256': bundle.digest(bundle.inside(root, manifest['release']))}


def _timestamp(value, ass=False):
    ticks = round(value*(100 if ass else 1000))
    unit = 100 if ass else 1000
    hours, ticks = divmod(ticks, 3600*unit)
    minutes, ticks = divmod(ticks, 60*unit)
    seconds, fraction = divmod(ticks, unit)
    return (f'{hours}:{minutes:02}:{seconds:02}.{fraction:02}' if ass else
            f'{hours:02}:{minutes:02}:{seconds:02},{fraction:03}')


def _srt(cues):
    return ''.join(f'{i}\n{_timestamp(a)} --> {_timestamp(b)}\n{text}\n\n'
                   for i, (a, b, text) in enumerate(cues, 1))


def captions(path, duration):
    """Read plain SRT with ordered nonoverlapping cues within one track."""
    text = Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').strip()
    if not text:
        return []
    cues = []
    for block in re.split(r'\n\s*\n', text):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].isdigit():
            raise ValueError('Expected numbered editorial SRT cues')
        bounds = lines[1].split(' --> ')
        if len(bounds) != 2:
            raise ValueError('Invalid editorial SRT interval')
        times = []
        for stamp in bounds:
            match = STAMP.fullmatch(stamp)
            if not match:
                raise ValueError('Invalid editorial SRT timestamp')
            h, m, s, ms = map(int, match.groups())
            times.append(h*3600+m*60+s+ms/1000)
        start, end = times
        body = '\n'.join(lines[2:])
        if (start < 0 or start >= end or end > duration+.000001
                or (cues and start < cues[-1][1]-.000001)
                or any(ord(c) < 32 and c != '\n' for c in body)
                or re.search('[\u3400-\u9fff]', body)):
            raise ValueError('Editorial cues must be ordered English text within the project duration')
        cues.append((start, end, body))
    return cues


def camera_plan(path, duration=None):
    """Validate editable position/target/FOV waypoints and derive native masks."""
    from scripts.promo_preview import make_camera
    rows = bundle.read(path)
    if not isinstance(rows, list) or len(rows) < 4 or len(rows) > 10000:
        raise ValueError('Editorial camera plan needs at least four waypoints')
    out = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'t', 'camera', 'label'}:
            raise ValueError('Unknown editorial camera waypoint fields')
        t = _number(row['t'], 'camera time')
        c = row['camera']
        if not isinstance(c, dict) or set(c) != {'position_m', 'target_m', 'vertical_fov_deg'}:
            raise ValueError('Edit camera position, target and FOV only; masks are derived')
        for field in ('position_m', 'target_m'):
            if not isinstance(c[field], list) or len(c[field]) != 3:
                raise ValueError('Expected three camera coordinates')
            for x in c[field]:
                _number(x, 'camera coordinate', -10000, 10000)
        if sum((a-b)**2 for a, b in zip(c['position_m'], c['target_m'])) < 1e-12:
            raise ValueError('Camera position and target must differ')
        _number(c['vertical_fov_deg'], 'camera FOV', 1, 179)
        if not isinstance(row['label'], str) or len(row['label']) > 256:
            raise ValueError('Invalid camera label')
        if out and t <= out[-1]['t']:
            raise ValueError('Editorial camera times must increase strictly')
        out.append({'t': t, 'camera': make_camera(**{
            'position': c['position_m'], 'target': c['target_m'], 'fov': c['vertical_fov_deg']}),
            'label': row['label']})
    if out[0]['t'] != 0 or (duration is not None and abs(out[-1]['t']-duration) > 1e-8):
        raise ValueError('Camera plan must span zero through the full project duration')
    return out


def load(path, data_root=None):
    path = Path(path).absolute()
    if path.is_symlink() or path.stat().st_size > 1024*1024:
        raise ValueError('Invalid editorial project file')
    path = path.resolve()
    project = bundle.read(path)
    if not isinstance(project, dict) or set(project) != FIELDS or project.get('schema') != SCHEMA or project.get('language') != 'en':
        raise ValueError('Unknown editorial project fields, schema or language')
    duration = _number(project['duration_s'], 'duration', .001)
    if type(project['fps']) is not int or project['fps'] != 30:
        raise ValueError('Factory editorial projects use 30 fps')
    if not math.isclose(duration*30, round(duration*30), abs_tol=1e-8, rel_tol=0):
        raise ValueError('Editorial duration must contain a whole number of 30-fps frames')
    if (not isinstance(project['source'], dict) or set(project['source']) !=
            {'bundle_sha256', 'scene_sha256', 'cameras_sha256', 'release_sha256'}
            or any(not isinstance(v, str) or not re.fullmatch('[a-f0-9]{64}', v)
                   for v in project['source'].values())):
        raise ValueError('Expected a frozen Factory source fingerprint')
    if data_root is not None and project['source'] != _source(data_root):
        raise ValueError('Editorial project belongs to a different Factory source')
    style = project['style']
    if not isinstance(style, dict) or set(style) != set(STYLE):
        raise ValueError('Unknown editorial style fields')
    for name in set(STYLE)-{'color'}:
        if type(style[name]) is not int:
            raise ValueError('Editorial style dimensions must be integers')
        _number(style[name], name, 1, 1000)
    if not isinstance(style['color'], str) or not re.fullmatch('#[a-fA-F0-9]{6}', style['color']):
        raise ValueError('Expected an editorial RGB color')
    files = {path.name: bundle.digest(path)}
    for field in ('camera_plan', 'titles', 'subtitles', 'font', 'font_license'):
        name = project[field]
        if not isinstance(name, str) or name == path.name or name in files:
            raise ValueError('Expected distinct project-relative editorial files')
        file = bundle.inside(path.parent, name)
        if not file.is_file() or file.stat().st_size > (16 if field == 'font' else 1)*1024*1024:
            raise ValueError('Missing or oversized editorial input: '+name)
        files[name] = bundle.digest(file)
    keys = camera_plan(path.parent/project['camera_plan'], duration)
    titles = captions(path.parent/project['titles'], duration)
    subtitles = captions(path.parent/project['subtitles'], duration)
    from PIL import ImageFont
    font_family = ImageFont.truetype(str(path.parent/project['font']), 24).getname()[0]
    return {'path': path, 'project': project, 'files': files, 'camera_plan': keys,
            'titles': titles, 'subtitles': subtitles, 'font_family': font_family}


def _create_verified(data_root, output):
    """Internal: caller has just verified the full Factory bundle."""
    from scripts.promo_preview import plan
    data_root, output = Path(data_root).resolve(), Path(output).resolve()
    if output.exists():
        raise FileExistsError('Choose a new editable project directory')
    manifest = bundle.read(data_root/'bundle.json')
    scene = bundle.inside(data_root, manifest['scene'])
    placements = bundle.read(scene.parent/'manifest.json')
    cameras = {c['id']: c for c in bundle.read(bundle.inside(data_root, manifest['cameras']))}
    families = {p['family'] for p in placements.get('placements', [])}
    if families != {'relay', 'transport', 'mosaic', 'dial'} or len(placements['placements']) != 36:
        raise ValueError('Full Factory editorial tour requires all 36 source workstations')
    if any(sum(p['family'] == family and p['case_id'].endswith('-d'+str(level))
               for p in placements['placements']) != 3
           for family in families for level in (1, 2, 3)):
        raise ValueError('Full Factory tour needs three scales at every family/level')
    keys, _ = plan(placements, cameras)
    editable = [{'t': r['t'], 'label': r['label'], 'camera': {
        k: deepcopy(r['camera'][k]) for k in ('position_m', 'target_m', 'vertical_fov_deg')}} for r in keys]
    tasks = {s['id']:bundle.read(Path(s['directory'])/'task.json')
             for family in bundle.resolved_release(data_root)['families'].values() for s in family['oracle']}
    titles = [(0., 10., 'RoboFrontier\nBenchmarking How LLM Agents Organize, Communicate,\nand Collaborate in a Multi-Robot World')]
    subtitles = [(0., 11.5, 'Four task families. Thirty-six workstations.\nRecorded physical state replayed in a complex Factory background.')]
    descriptions = {
        'relay': 'Relay | Carry beam assemblies through coordinated support and handovers.',
        'transport': 'Transport | Match stock to orders, place objects, and seat physical connectors.',
        'mosaic': 'Mosaic | Collaborate to assemble the declared color pattern.',
        'dial': 'BEST5 Dial | Coordinate support and rotation using aggregate feedback.'}
    for i, family in enumerate(('relay', 'transport', 'mosaic', 'dial')):
        start = 13.5+(41+9/1.4)*i
        end = start+41+4/1.4
        titles.append((start, start+5, family.title() if family != 'dial' else 'BEST5 Dial'))
        subtitles.append((start, start+7, descriptions[family]))
        rows = [k for k in keys if start <= k['t'] <= end and 'hold' not in k['label'] and 'overview' not in k['label']]
        for row, next_row in zip(rows[1:], rows[2:]+[{'t':end}]):
            # Match the actual camera to a source task, not a guessed scale.
            matches = [c for c in cameras.values() if all(c.get(field) == row['camera'][field]
                       for field in ('position_m', 'target_m', 'vertical_fov_deg'))]
            if len(matches) != 1:
                raise ValueError('Tour waypoint has no unique source inspection camera')
            ident = matches[0]['id'].rsplit('--', 1)[0]
            task = tasks[ident]
            label = f"{ident} | Level {task['level']} | {len(task['arms'])} arms"
            a = max(row['t'], start+7)
            if next_row['t'] > a:
                subtitles.append((a, next_row['t'], family.title()+' | '+label))
    subtitles.append((204.5, DEFAULT_DURATION, 'One recorded world per task. Independent station clocks.\nPresentation does not establish a new policy score.'))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.factory-project-', dir=output.parent) as temporary:
        temp = Path(temporary)
        (temp/'fonts').mkdir()
        shutil.copy2(FONT, temp/'fonts'/FONT.name)
        shutil.copy2(LICENSE, temp/'fonts/OFL.txt')
        bundle.write(temp/'camera-plan.json', editable)
        (temp/'titles.srt').write_text(_srt(titles))
        (temp/'subtitles.srt').write_text(_srt(subtitles))
        project = {'schema':SCHEMA, 'language':'en', 'duration_s':DEFAULT_DURATION, 'fps':30,
                   'source':_source(data_root), 'camera_plan':'camera-plan.json',
                   'titles':'titles.srt', 'subtitles':'subtitles.srt', 'font':'fonts/'+FONT.name,
                   'font_license':'fonts/OFL.txt', 'style':dict(STYLE)}
        bundle.write(temp/'project.json', project)
        load(temp/'project.json', data_root)
        temp.rename(output)
    return {'project':str(output/'project.json'), 'duration_s':DEFAULT_DURATION,
            'camera_waypoints':len(keys), 'model_calls':0, 'physics_steps':0}


def create(data_root, output):
    bundle.verify(data_root)
    return _create_verified(data_root, output)


def freeze(path, output, data_root=None):
    loaded = load(path, data_root)
    output = Path(output)
    if output.exists():
        raise FileExistsError('Choose a new frozen editorial directory')
    output.mkdir(parents=True)
    for name, sha in loaded['files'].items():
        source, target = loaded['path'].parent/name, output/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if bundle.digest(source) != sha or bundle.digest(target) != sha:
            raise ValueError('Editorial input changed during preparation')
    return {'project':loaded['path'].name, 'files':loaded['files']}


def _probe(video):
    report = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames',
        '-select_streams','v:0','-show_entries','stream=width,height,avg_frame_rate,nb_read_frames',
        '-of','json',str(video)], text=True, timeout=120))
    if len(report.get('streams', [])) != 1:
        raise ValueError('Expected one video stream')
    stream = report['streams'][0]
    a, b = map(int, stream['avg_frame_rate'].split('/'))
    return {'width':int(stream['width']), 'height':int(stream['height']),
            'fps':a/b, 'frames':int(stream['nb_read_frames'])}


def _ass(loaded, width, height):
    style = loaded['project']['style']
    family = loaded['font_family'].replace(',', ' ')
    color = style['color'].lstrip('#')
    color = '&H00'+color[4:6]+color[2:4]+color[0:2]
    header = f'[Script Info]\nScriptType: v4.00+\nPlayResX: {width}\nPlayResY: {height}\nWrapStyle: 0\n\n'
    header += '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
    scale = height/1080
    for name, size, alignment, margin in [('Title','title_size',8,'title_margin'), ('Subtitle','subtitle_size',2,'subtitle_margin')]:
        header += f'Style: {name},{family},{style[size]*scale},{color},{color},&H00101010,&H80000000,0,0,0,0,100,100,0,0,1,2,1,{alignment},{round(style["horizontal_margin"]*width/1920)},{round(style["horizontal_margin"]*width/1920)},{round(style[margin]*scale)},1\n'
    header += '\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    for name, cues in [('Title', loaded['titles']), ('Subtitle', loaded['subtitles'])]:
        for start, end, text in cues:
            text = text.replace('\\','\\\\').replace('{','\\{').replace('}','\\}').replace('\n',r'\N')
            header += f'Dialogue: 0,{_timestamp(start, True)},{_timestamp(end, True)},{name},,0,0,0,,{text}\n'
    return header


def render(project, video, output, *, run_command=None):
    """Composite text onto media; only the caller can establish scene identity."""
    loaded = load(project)
    video, output = Path(video).resolve(), Path(output).resolve()
    if output.exists() or not video.is_file():
        raise ValueError('Choose a new editorial output and an existing source movie')
    source_sha = bundle.digest(video)
    source = _probe(video)
    if source['fps'] != 30 or source['frames'] > math.ceil(loaded['project']['duration_s']*30):
        raise ValueError('Source movie must use 30 fps and fit the full editorial timeline')
    if source['frames'] < 1:
        raise ValueError('Source movie is empty')
    output.mkdir(parents=True)
    frozen = freeze(loaded['path'], output/'project')
    if frozen['files'] != loaded['files']:
        raise ValueError('Editorial input changed before rendering')
    (output/'fonts').mkdir()
    # Render-local copies share bytes with the retained editable project.
    (output/'fonts/font.ttf').hardlink_to(output/'project'/loaded['project']['font'])
    (output/'editorial.ass').write_text(_ass(loaded, source['width'], source['height']))
    if run_command is None:
        def run_command(command, *, cwd):
            subprocess.run(command, cwd=cwd, check=True)
    run_command(['ffmpeg','-v','warning','-nostdin','-i',str(video),'-map','0:v:0',
        '-map','0:a?','-vf','ass=editorial.ass:fontsdir=fonts','-c:v','libx264',
        '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
        str(output/'factory.mp4')], cwd=output)
    actual = _probe(output/'factory.mp4')
    if actual != source:
        raise ValueError('Editorial output changed video dimensions, frame count or rate')
    run_command(['ffmpeg','-v','error','-nostdin','-i',str(output/'factory.mp4'),
                 '-f','null','-'], cwd=output)
    if bundle.digest(video) != source_sha:
        raise ValueError('Source movie changed during editorial rendering')
    for name, sha in loaded['files'].items():
        if bundle.digest(loaded['path'].parent/name) != sha:
            raise ValueError('Editorial input changed during rendering')
    report = {'schema':'robofrontier.factory-editorial-render.v1', 'source_video_sha256':source_sha,
              'video_sha256':bundle.digest(output/'factory.mp4'), 'media':actual,
              'full_decode_passed':True, 'project_sha256':loaded['files'][loaded['path'].name],
              'project_files':loaded['files'], 'source_factory':loaded['project']['source'],
              'ass_sha256':bundle.digest(output/'editorial.ass'),
              'title_cues':len(loaded['titles']), 'subtitle_cues':len(loaded['subtitles']),
              'scope':'Text post-production only. Scene identity must be verified by the source render plan; no physics or task score is established.'}
    bundle.write(output/'report.json', report)
    return {'video':str(output/'factory.mp4'), 'report':str(output/'report.json'),
            'project':str(output/'project'/loaded['path'].name),
            'frames':actual['frames'], 'model_calls':0, 'physics_steps':0}
