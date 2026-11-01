"""Render each selected factory workstation's full edited timeline, one view at a time."""
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from robofrontier.motion_timeline import sample_timeline


def run(command, log):
    with log.open('a') as f:
        f.write('\nCOMMAND '+json.dumps([str(x) for x in command])+'\n'); f.flush()
        subprocess.run([str(x) for x in command], cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, check=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--families', nargs='+', choices=['transport','relay','dial','mosaic'], required=True)
    parser.add_argument('--levels', nargs='+', type=int, choices=[1,2,3], required=True)
    parser.add_argument('--blender', required=True)
    parser.add_argument('--device', choices=['METAL','OPTIX','CUDA'], required=True)
    parser.add_argument('--require-single-gpu', action='store_true')
    parser.add_argument('--release',type=Path,default=ROOT/'configs/task_families/current.json')
    parser.add_argument('--scene',type=Path,default=ROOT/'outputs/robo-factory/layout-label-below/scene.xml')
    parser.add_argument('--cameras',type=Path,default=ROOT/'outputs/robo-factory/layout-label-below/desk-cameras-larger-front.json')
    parser.add_argument('--asset',type=Path,default=ROOT/'outputs/robo-factory/layout-label-below-asset')
    parser.add_argument('--collect-videos',type=Path,help='Hard-link validated videos into one shared directory')
    args=parser.parse_args()
    os.chdir(ROOT)
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    log=output/'batch.log'
    release=json.loads(args.release.read_text())
    camera_file=args.cameras
    cameras={c['id']:c for c in json.loads(camera_file.read_text())}
    asset=args.asset
    jobs=[]
    for name in args.families:
        family=release['families'][name]
        for spec in family['oracle']:
            level=spec.get('level')
            if level is None:level=json.loads((ROOT/spec['directory']/'task.json').read_text())['level']
            if level not in args.levels: continue
            edit_path=ROOT/spec['edit']; edit=json.loads(edit_path.read_text())
            if edit['schema']!='robofrontier.station-edit.v2': raise ValueError('Unsupported edit schema')
            with np.load(edit_path.parent/edit['selection_file'],allow_pickle=False) as z:
                frames=len(sample_timeline(z['keep'],edit['source_hz'],family['speedup'],release['presentation']['fps']))
            for view in ('front','side'):
                if spec['id']+'--'+view not in cameras: raise ValueError('Missing camera')
            jobs.append(dict(family=name,id=spec['id'],frames=frames,fps=release['presentation']['fps']))
    if not jobs: raise ValueError('No selected desks')
    (output/'plan.json').write_text(json.dumps(jobs,indent=2)+'\n')
    for job in jobs:
        case=output/job['id'];case.mkdir()
        poses=case/'poses'
        # The exporter rounds upward. Half a frame below the boundary gives exactly frames.
        duration=(job['frames']-.5)/job['fps']
        run([sys.executable,'-m','scripts.factory','poses','--scene',args.scene,'--release',args.release,'--output',poses,'--duration',str(duration),'--camera','desk-front','--station',job['id'],'--desk-cameras',camera_file,'--families',job['family'],'--levels',*[str(x) for x in args.levels]],log)
        animation=poses/'animation.json';data=json.loads(animation.read_text())
        if len(data['frames'])!=job['frames']:raise ValueError('Pose count differs from selected timeline')
        side=json.loads(animation.read_text())
        for frame in side['frames']:frame['camera']=cameras[job['id']+'--side']
        sidefile=poses/'animation-side.json';sidefile.write_text(json.dumps(side,indent=2)+'\n')
        for view, anim in [('front',animation),('side',sidefile)]:
            cmd=[args.blender,'--background','--python-exit-code','1','--python',ROOT/'scripts/render_factory_blender.py','--','--asset',asset,'--animation',anim,'--output',case/view,'--engine','cycles','--profile','fast','--device',args.device,'--width','1920','--height','1080','--samples','64','--noise-threshold','0.1','--min-samples','4']
            if args.require_single_gpu:cmd.append('--require-single-gpu')
            run(cmd,log)
            if args.collect_videos:
                report=json.loads((case/view/'report.json').read_text())
                if report.get('animation',{}).get('full_decode_passed') is not True:
                    raise ValueError('Only a fully decoded video may be collected')
                args.collect_videos.mkdir(parents=True,exist_ok=True)
                os.link(case/view/'factory.mp4',args.collect_videos/(job['id']+'--'+view+'.mp4'))
        (case/'complete.json').write_text(json.dumps(dict(job=job,completed_unix=time.time()),indent=2)+'\n')
    (output/'complete.json').write_text(json.dumps(dict(jobs=len(jobs),completed_unix=time.time()),indent=2)+'\n')

if __name__=='__main__':main()
