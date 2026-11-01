"""Historical v1 three-arm/six-slot exporter; not a current generic evaluator.

Writes into the explicitly selected old run. Do not use on v3 runs.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import subprocess

p=argparse.ArgumentParser();p.add_argument('run_dir',type=Path);args=p.parse_args();d=args.run_dir.resolve()
if (d/'private/inputs/manifest.json').exists():raise SystemExit('Historical v1 exporter only; current runs use their own runtime outputs')
s=json.loads((d/'private/runtime.json').read_text())
if not s['ended']:raise SystemExit('Trial still running; no completion claim exported')
events=[json.loads(line) for line in (d/'private/events.jsonl').read_text().splitlines() if line]
start=next(e for e in events if e['kind']=='START');end=next(e for e in events if e['kind']=='TEAM_FINISH_PROPOSED')
threads=json.loads((d/'private/threads.json').read_text())['threads'];models={}
sessionroot=Path.home()/'.codex/sessions'
for a,t in threads.items():
    files=list(sessionroot.rglob('*'+t+'.jsonl'));turns=[];calls=[]
    for file in files:
        for line in file.open():
            r=json.loads(line);v=r.get('payload',{})
            if r.get('type')=='turn_context':turns.append({k:v.get(k) for k in ('turn_id','model','effort')})
            if r.get('type')=='response_item' and v.get('type')=='function_call':calls.append(v.get('name'))
    models[a]={'thread_id':t,'turns':turns,'tool_names':dict(Counter(calls)),
               'all_luna_xhigh':bool(turns) and all(v['model']=='gpt-6-luna' and v['effort']=='xhigh' for v in turns)}
(d/'private/model-verification.json').write_text(json.dumps(models,ensure_ascii=False,indent=2)+'\n')
manifest=json.loads((d/'private/manifest.json').read_text());unchanged=all(Path(f).exists() and hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in manifest['source_sha256'].items())
evaluation=json.loads((d/'private/evaluation.json').read_text());jobs=list(s['jobs'].values())
allowed=all((m['from']=='Meta' and all(t in 'ABC' for t in m['to'])) or (m['from'] in 'ABC' and m['to']==['Meta']) for m in s['messages'])
research_motion=[e for e in events if e['kind']=='ACTION_STARTED' and e['actor']=='research']
started={e['action']['action_id']:e for e in events if e['kind']=='ACTION_STARTED'}
finished={e['call_id']:e for e in events if e['kind']=='TOOL_RETURN' and 'execution' in e.get('result',{}) and e['result']['execution'].get('status') in ('completed','failed')}
intervals=[]
for key,e in started.items():
    if key in finished:intervals.append((max(0,e['wall_s']-start['wall_s']),max(0,finished[key]['wall_s']-start['wall_s'])))
merged=[]
for lo,hi in sorted(intervals):
    if merged and lo<=merged[-1][1]+.3:merged[-1]=(merged[-1][0],max(merged[-1][1],hi))
    else:merged.append((max(0,lo-.15),hi+.15))
observations=[e['result']['observation'] for e in events if e['kind']=='TOOL_RETURN' and 'observation' in e.get('result',{})]
last_observation=observations[-1]
released_and_still=all(r['gripper_width_m']>.07 and r['tcp_m'][2]>.55 and max(abs(v) for v in r['joint_velocity_rad_s'])<.005 for r in last_observation['robot'].values())
checks={'final_grippers_open_arms_raised_and_still':released_and_still,'six_slots_correct':evaluation['all_goals_met'],'all_sessions_luna_xhigh':all(x['all_luna_xhigh'] for x in models.values()),
        'engineering_files_unchanged':unchanged,'tree_messages_only':allowed,'research_did_not_control_arms':not research_motion,
        'no_running_actions':all(j['status']!='running' for j in jobs),
        'video_encoder_ok':bool(s['video']) and s['video']['error'] is None,'video_no_dropped_frames':bool(s['video']) and s['video']['dropped_frames']==0}
# Actual overlap of action execution across arms, using wall clock events.
changes=[]
for key,e in started.items():
    if key in finished:changes.extend([(e['wall_s'],1),(finished[key]['wall_s'],-1)])
active=peak=0
for _,delta in sorted(changes,key=lambda x:(x[0],x[1])):active+=delta;peak=max(peak,active)
checks['three_arms_executed_concurrently']=peak>=3
report={'checks':checks,'evaluation':evaluation,'wall_seconds':round(end['wall_s']-start['wall_s'],3),
        'simulation_seconds':round(end['sim_s']-start['sim_s'],3),'messages':len(s['messages']),
        'actions_by_arm':dict(Counter(j['arm'] for j in jobs)),'action_status':dict(Counter(j['status'] for j in jobs)),
        'turns_by_role':{a:len(v['turns']) for a,v in models.items()},'peak_simultaneous_actions':peak,
        'action_clip_wall_seconds':round(sum(hi-lo for lo,hi in merged),3),
        'video':s['video'],'final_observation':last_observation,'scope':'One controlled desktop-session pilot. Public initial positions allowed; no policy dynamic object-state endpoint. Research session drives native lifecycle. Not an unattended daemon or OS sandbox.'}
(d/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
video=d/'global-realtime.mp4'
if video.exists() and merged:
    select='+'.join(f'between(t,{lo:.3f},{hi:.3f})' for lo,hi in merged)
    filt=d/'private/action-only.filter';filt.write_text("select='"+select+"',setpts=N/15/TB")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-filter_script:v',str(filt),'-an','-c:v','libx264','-preset','veryfast','-crf','22',str(d/'actions-only.mp4')],check=True)
rows=['# Meta + three Workers: historical real MuJoCo pilot','',f"Six-slot result: {evaluation['all_goals_met']}; experiment wall time {report['wall_seconds']:.1f} s; simulation advance {report['simulation_seconds']:.1f} s.",'',
      'All used gpt-6-luna / xhigh; actual per-turn verification is in private/model-verification.json. Initial coordinates were public; subsequent observations were RGB + robot state.', '',
      f"Actions {len(jobs)}; messages {len(s['messages'])}; peak concurrently executing {peak} arms.",'',
      '## Verification','']
rows += [f"- {'PASS' if ok else 'FAIL'}: {key}" for key,ok in checks.items()]
rows += ['','## Key coordination sequence','',
         'B initially reported withdrawal, but its TCP remained directly above the board blocks. A identified the conflict from permitted robot state and waited. Meta asked B to lift and return to its region; A checked before receiving. See messages m18–m31. The research session supplied no correction plan.', '',
         '## Recording quality','',f"Encoder error: {s['video']['error']}; dropped frames {s['video']['dropped_frames']} frames. The original is not a lossless frame-by-frame wall-clock record. Action segments use event-time cuts; dropped frames can shift boundaries by roughly seconds.",'','## Files','', '- global-realtime.mp4: complete original-speed recording.','- actions-only.mp4: intervals with any executing arm-tool action, removing mostly action-free waits and retaining original playback speed.','- report.json: machine-readable verification and statistics.','- private/events.jsonl: original tools, messages and timeline.','- private/driver.jsonl: actual session state and wakeups.','',
         '## Scope','',report['scope'],'',
         'Slot evaluation checks only attributes, center position and height. Final release/withdrawal needs image and tool-log review. One trial cannot establish overall success rate or architecture superiority.']
(d/'report.md').write_text('\n'.join(rows)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
