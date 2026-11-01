"""Self-contained XML/preview fixtures for legacy *protocol* tests.

These contain no Panda robots and make no physical qualification claim. Real
metadata and validation rules are retained, but FakeWorld supplies execution and
measurements. No MuJoCo model, renderer, IK solver or ignored asset is required.
"""
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from PIL import Image


def _scene(source, destination):
    source, destination = Path(source), Path(destination)
    destination.mkdir(parents=True)
    for name in ('environment.json', 'parameters.json', 'task-draft.json'):
        if (source/name).is_file():
            shutil.copy2(source/name, destination/name)
    (destination/'assets').mkdir()
    (destination/'model-assets').mkdir()
    root = ET.Element('mujoco', model='Synthetic protocol fixture; no robots')
    ET.SubElement(root, 'compiler', meshdir='model-assets', angle='radian')
    world = ET.SubElement(root, 'worldbody')
    for camera in ET.parse(source/'scene.xml').findall('worldbody/camera'):
        ET.SubElement(world, 'camera', camera.attrib)
    return root, world


def beam_scene(source, destination):
    root, world = _scene(source, destination)
    env = json.loads((Path(source)/'environment.json').read_text())
    beam = env['beam']
    body = ET.SubElement(world, 'body', name=beam['id'])
    ET.SubElement(body, 'geom', type='box',
        size=' '.join(str(beam[key]/2) for key in ('width_m', 'length_m', 'height_m')),
        mass=str(beam['mass_kg']))
    ET.ElementTree(root).write(Path(destination)/'scene.xml', encoding='unicode')
    Image.new('RGB', (32, 24), 'white').save(Path(destination)/'preview-top.png')


def spring_scene(source, destination):
    root, world = _scene(source, destination)
    params = json.loads((Path(source)/'parameters.json').read_text())
    dial = params['dial']
    for arm in 'ABCD':
        body = ET.SubElement(world, 'body', name='dial_'+arm)
        ET.SubElement(body, 'joint', name='dial_'+arm+'_hinge', axis='0 0 -1',
            springref='0', stiffness=str(dial['spring_nm_per_rad']),
            damping=str(dial['damping_nm_s_per_rad']),
            range=' '.join(map(str, dial['range_rad'])))
        ET.SubElement(body, 'geom', type='sphere', size='.01', mass='.01')
    ET.SubElement(ET.SubElement(root, 'keyframe'), 'key', name='initial', qpos='0 0 0 0')
    ET.ElementTree(root).write(Path(destination)/'scene.xml', encoding='unicode')
    Image.new('RGB', (32, 24), 'white').save(Path(destination)/'preview-board.png')
