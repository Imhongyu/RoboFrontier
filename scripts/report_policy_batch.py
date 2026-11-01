"""Produce a portable human index from collected GPT results, not Oracle data."""
import argparse
from html import escape
import json
from pathlib import Path

LABELS={'transport':'Transport','mosaic':'Mosaic','relay':'Relay','dial':'Dial'}


def progress(row):
    if row.get('total_goals') is not None:return f"{row['matched_goals']}/{row['total_goals']}"
    if row.get('total_payloads') is not None:return f"{row['completed_payloads']}/{row['total_payloads']}"
    if row.get('valid_trials') is not None:return 'Passed' if row.get('task_success') else f"{row['valid_trials']} valid trials"
    return 'Not collected'


def report(output):
    output=Path(output);result=json.loads((output/'results.json').read_text());rows=result['cases']
    lines=['# Historical GPT trial: 12 minimum-scale cases','',
        'Adaptive; gpt-6.1-sol / high; each task had at most 20 wall-clock minutes from START, including thinking, communication, tools and forks. Initialization was excluded. At the deadline, new actions stopped; braking and sealing were logged separately.',
        '', 'Three levels at minimum scale in each family. Dial always had 4 dials: L1 used 4 arms, L2/L3 used 8. Other families: Transport 4 arms, Mosaic 4 arms, Relay 8 arms.',
        '', 'These were user-authorized time-limited policy trials, without establishing 36-case Oracle engineering acceptance. Every case started with a fresh Controller context, without Oracle/previous-level experience. The Controller chose temporary delegates within its task.',
        '', '| Family | Level | Arms | Physical acceptance | Goal count/feedback | Task wall time | Delegates | Original-speed video |',
        '| --- | --- | ---: | --- | --- | --- | ---: | --- |']
    cards=[]
    for r in rows:
        state='Passed' if r.get('task_success') else 'Incomplete at deadline' if r.get('budget_exhausted') else 'Incomplete' if 'evaluation_ref' in r else 'Awaiting collection'
        if r.get('process_compliant') is False:state+='; process violations recorded'
        seconds=r.get('task_wall_s');duration='—' if seconds is None else f'{int(seconds)//60:02d}:{int(seconds)%60:02d}'
        filename=Path(r['video']).name if r.get('video') else None;link=f'[Play]({filename})' if filename else '—'
        lines.append(f"| {LABELS[r['family']]} | L{r['level']} | {r['arms']} | {state} | {progress(r)} | {duration} | {r['delegates']} | {link} |")
        media=f'<video controls preload="none" src="{escape(filename)}"></video>' if filename else '<p>Video not collected</p>'
        cards.append(f'<article><h2>{LABELS[r["family"]]} L{r["level"]} · {r["arms"]} arms</h2><p>{escape(state)} · {escape(progress(r))} · {duration}</p>{media}</article>')
    lines+=['','Goal counts alone were not whole-task success: these historical trials required both physical goals and process rules. Deadline outcomes use pre-braking budget-cutoff.json; objects settling only after stop do not count as on-time completion.','',
        'Recordings retain original-speed waiting and thinking. results.json contains full video decoding, source motion frame counts, actual model/effort/permissions and fork-parent checks. Complete 60Hz source states remain in each run private/outputs/motion for offline Factory import. float32 quantization and subsequent lossless compression semantics remain unchanged; these are not physics restart checkpoints.','',
        'Permissions were not an OS file sandbox. Tool-input text audits are retained separately, without claiming complete protection against malicious access violations.']
    (output/'README.md').write_text('\n'.join(lines)+'\n')
    (output/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Historical GPT videos: 12 cases</title><style>body{font:16px system-ui;background:#f5f7f9;color:#21313d;margin:28px}main{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:20px}article{background:white;border:1px solid #dce3e8;padding:18px;border-radius:12px}h2{font-size:19px}video{width:100%;background:#e8edf1}</style><h1>Historical GPT: 12 minimum-scale cases · Original-speed video</h1><p>Adaptive · gpt-6.1-sol / high · Each case: at most 20 minutes after START. See README.md and results.json for criteria and audits.</p><main>'+''.join(cards)+'</main>')
    print(json.dumps(dict(index=str(output/'index.html'),readme=str(output/'README.md'))))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);a=p.parse_args();report(a.output)
