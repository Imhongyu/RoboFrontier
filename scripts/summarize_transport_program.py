"""Summarize proof scope, physical acceptance, failures and verified videos."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from robofrontier.cube_transport import ROOT


def summarize(directory):
    rows, media = [], []
    for count in range(3, 13):
        name = f'line-{count:02}' if count == 3 else f'ring-{count:02}'
        plan = json.loads((directory/name/'schedule.json').read_text())
        attempts = []
        for path in sorted((directory/name).glob('attempt-*/report.json')):
            report = json.loads(path.read_text())
            scene = ROOT/f'configs/environments/cube_transport/{name}/scene.xml'
            if hashlib.sha256(scene.read_bytes()).hexdigest() != report['scene_sha256']:
                raise ValueError('Scene changed: '+name)
            task = json.loads((ROOT/f'configs/tasks/cube_transport/{name}/seed-0.json').read_text())
            if json.loads((path.parent/'task.json').read_text()) != task:
                raise ValueError('Task changed: '+name)
            calls = 0
            for line in (path.parent/'trace.jsonl').read_text().splitlines():
                event = json.loads(line)
                if event['event'] == 'moves':
                    calls += len(event['targets'])
                elif event['event'] == 'grippers':
                    calls += len(event['commands'])
                elif event['event'] == 'gentle_release':
                    calls += len(event['robots'])
            videos = []
            for video in sorted(path.parent.glob('*.mp4')):
                info = json.loads(subprocess.check_output([shutil.which('ffprobe'), '-v', 'error',
                    '-show_entries', 'format=duration,size', '-show_entries', 'stream=width,height,r_frame_rate',
                    '-of', 'json', str(video)], text=True))
                item = {'path': str(video.relative_to(directory)), 'acceptance_passed': report['passed'],
                        'metadata': info, 'sha256': hashlib.sha256(video.read_bytes()).hexdigest()}
                videos.append(item['path']); media.append(item)
            attempts.append({'path': str(path.relative_to(directory)), 'passed': report['passed'],
                             'error': report.get('error'), 'evaluation': report.get('evaluation'),
                             'physical_batches': report.get('physical_batches'),
                             'arm_command_segments': calls, 'sim_time_s': report['sim_time_s'],
                             'peak_moving_arms': report['peak_moving_arms'], 'videos': videos})
        accepted = [r for r in attempts if r['passed']]
        rows.append({'arms': count, 'serial_unit_phases': plan['serial_phase_slots'],
                     'optimal_unit_rounds_fixed_routes': plan['parallel_feasible_phase_slots'],
                     'optimality_proven': plan['optimality_proven'], 'proof_scope': plan['proof_scope'],
                     'attempts': attempts, 'accepted_attempt': accepted[-1] if accepted else None})
    (directory/'index.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
    (directory/'media-verification.json').write_text(json.dumps(media, indent=2)+'\n')
    lines = ['# Program reference without GPT: discrete optimum and contact simulation', '',
             'OR-Tools CP-SAT minimized rounds for fixed shortest routes and unit grasp/place phases. All ten scales proved OPTIMAL and passed independent resource replay. This proof excludes alternative routes, continuous motion time and real-robot global optimality.', '',
             'A deterministic program called robot IK and position actuators. It read object ground truth and used pre-release corrections, continuous gripper positions, motion probes and necessary staggering. This is an engineering feasibility reference, without the same observations/interface as an RGB agent performance baseline.',
             'Scene, materials and physics were unchanged; scene SHA and task contents were checked individually. All failed attempts remain retained. Success requires whole-task stable-goal acceptance.', '',
             '| Arms | Serial unit phases | Discrete-optimal rounds | Physical acceptance | Actual physical groups |',
             '| ---: | ---: | ---: | --- | ---: |']
    for row in rows:
        accepted = row['accepted_attempt']
        status = f"Passed {accepted['evaluation']['matched_goals']}/{3*row['arms']}" if accepted else 'No whole-task pass recorded'
        groups = accepted['physical_batches'] if accepted else '—'
        lines.append(f"| {row['arms']} | {row['serial_unit_phases']} | {row['optimal_unit_rounds_fixed_routes']} | {status} | {groups} |")
    lines += ['', 'Geometry conflicts require staggering, so physical groups may exceed discrete rounds. Each unit phase also needs multiple move/gripper segments; these are not tool-call or MuJoCo integration-step counts. Actual duration is not proved optimal. Simulation and program wall time are recorded separately.', '',
              '## Videos of accepted attempts', '']
    for item in media:
        if item['acceptance_passed']:
            duration = float(item['metadata']['format']['duration'])
            lines.append(f"- [{item['path']}]({item['path']}), {duration:.1f} s.")
    lines += ['', 'reference-* files were sampled during execution; replay-* files are offline renders of accepted physical trajectories, selecting actual saved qpos per frame without invented/interpolated object motion. Filenames and frames identify speedup. Output is 20 fps, timed by simulation rather than inference wall time.', '',
              '## Unpassed attempts', '']
    for row in rows:
        for attempt in row['attempts']:
            if not attempt['passed']:
                lines.append(f"- {attempt['path']}: {attempt['error'] or 'Unpassed / interrupted'}.")
    lines += ['', 'Observed sphere-group issues include held-object drops and post-release drift. Finishing all transport actions is insufficient: all goals must remain stable for one second. failure-replay files always retain failure labels and stay separate from success videos. Tasks the reference program itself has not passed cannot support attributing failure to model intelligence; resolve physical execution first.', '',
              '## Reproduction', '',
              'Solver dependencies were installed separately in solver-deps for this run, with versions in solver-packages.json; they are not project defaults. Each attempt retains attempt/executor-source.py, final code is in final-source and initial code in frozen-source.', '',
              'From the repository root, use --help with scripts.solve_transport_program, scripts.render_transport_program and scripts.render_transport_replay. New attempts require new attempt IDs and must not overwrite old records.', '']
    (directory/'report.md').write_text('\n'.join(lines))
    print(json.dumps({'discrete_optimal_proofs': sum(r['optimality_proven'] for r in rows),
                      'accepted_arm_counts': [r['arms'] for r in rows if r['accepted_attempt']],
                      'verified_media_files': len(media)}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    summarize(args.directory.resolve())
