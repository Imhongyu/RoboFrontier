"""Place each source workstation's inspection cameras in the factory."""
import argparse
import itertools
import json
import math
from pathlib import Path

import mujoco
import numpy as np

from robofrontier.task_families import ROOT
from robofrontier.workstation import Workstation


def make_cameras(scene):
    scene = Path(scene)
    manifest = json.loads((scene.parent / 'manifest.json').read_text())
    model = mujoco.MjModel.from_xml_path(str(scene))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    labels = {row['id']: row for row in manifest['factory_labels']['labels']}
    cameras = []
    for place in manifest['placements']:
        case = place['case_id']
        path = manifest.get('source_overrides', {}).get(case, ROOT / place['source_directory'])
        source = Workstation(path)
        source.frame()
        yaw = place['yaw_rad']
        c, s = math.cos(yaw), math.sin(yaw)
        rotation = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.]])
        shift = np.asarray(place['translation_m'])
        for view, source_name in (('front', 'global'), ('top', 'top'), ('side', 'global_side')):
            cid = source.model.camera(source_name).id
            if source.model.cam_projection[cid] != 0:
                raise ValueError(f'{case}/{source_name}: expected perspective source camera')
            position = rotation @ source.data.cam_xpos[cid] + shift
            orientation = rotation @ source.data.cam_xmat[cid].reshape(3, 3)
            fov = float(source.model.cam_fovy[cid])
            if view == 'top':
                label = labels['ws_caption_' + case]['bounds_xy_m']
                table = place['table_bounds_xy_m']
                low = np.minimum(table[:2], label[:2]); high = np.maximum(table[2:], label[2:])
                position[:2] = (low + high) / 2
                # Preserve the source direction and lens, moving back only as
                # needed to fit the desk and its floor caption at 16:10.
                gids = [model.geom(name).id for name in manifest['workstation_names'][case]['geom_names'].values()]
                gids.append(model.geom('ws_caption_' + case).id)
                points = []
                for gid in gids:
                    box = model.geom_aabb[gid]; r = data.geom_xmat[gid].reshape(3, 3)
                    center = data.geom_xpos[gid] + r @ box[:3]
                    half = np.abs(r) @ box[3:]
                    points.extend(center + half * signs for signs in itertools.product((-1, 1), repeat=3))
                local = (np.asarray(points) - position) @ orientation
                tangent = math.tan(math.radians(fov) / 2)
                needed = np.maximum(np.abs(local[:, 0]) / (tangent * 1.6), np.abs(local[:, 1]) / tangent) * 1.1 + local[:, 2]
                position += orientation[:, 2] * max(0., float(np.max(needed)))
                # Reduce parallax so raised robot parts do not cover a floor
                # caption that is clear from the overhead inspection direction.
                position[2] *= 4
                fov = math.degrees(2 * math.atan(tangent / 4))
            cameras.append(dict(id=f'{case}--{view}', station=case, source_camera=source_name,
                position_m=position.tolist(), target_m=(position - orientation[:, 2]).tolist(),
                rotation_matrix=orientation.tolist(), projection='perspective',
                vertical_fov_deg=fov,
                show_caption=view == 'top',
                hidden_layers=['roof', 'north', 'south', 'east', 'west']))
    return cameras


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cameras = make_cameras(args.scene)
    args.output.write_text(json.dumps(cameras, indent=2) + '\n')
    print(f'{len(cameras)} cameras for {len(cameras)//3} workstations')
