"""Publish discrete BEST-feedback distributions, with sampling provenance."""
from pathlib import Path
import csv
import html
import json
import shutil

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'runs/oracle/dial-feedback-alphabet-20261025'
OUT=ROOT/'docs/generated/frontier-v2/dial-alphabet-comparison';OUT.mkdir(parents=True,exist_ok=True)
summary=json.loads((B/'summary.json').read_text());rows=[]
prior=json.loads((ROOT/'runs/oracle/dial-feedback-comparison-20261025/best-smart-percentiles.json').read_text())
for p in prior['results']:
    rows.append(dict(dials=p['dials'],alphabet=3,passwords=p['cases'],tested=p['cases'],exhaustive=True,
        mean=p['mean'],percentiles={f'P{q}':p[f'P{q}'] for q in (5,20,50,80,95)},baseline=True))
rows+=summary['results'];rows.sort(key=lambda r:(r['dials'],r['alphabet']))
md=['# BEST feedback: trial distributions for 3–7 valid settings','',
    'Valid settings exclude invalid initial 0. The reference policy retains candidate elimination, entropy and neighborhood experiments around record-setting combinations. These are neither globally optimal counts nor GPT/MuJoCo measurements.',
    '','The 3-setting baseline reuses earlier exhaustive enumeration. All settings for 4 dials and 4 settings for 6 dials are exhaustive; other groups uniformly sample 4096 codes without replacement. Candidate posteriors remain exact. Only above 8192 candidates, query entropy uses 8192 candidates sampled independently of test codes.',
    '','For 3 settings, the extension reproduced every earlier query/change count across 81, 729 and 4096 test paths. Four regression tests passed.']
tables=[]
for n in (4,6,8):
    md+=['',f'## {n} dials','', '| Valid settings | Mean trials | P5 | P20 | P50 | P80 | P95 |','|---|---:|---:|---:|---:|---:|---:|']
    html_rows=[]
    for r in [r for r in rows if r['dials']==n]:
        values=[str(r['alphabet']),f"{r['mean']:.2f}"]+[str(r['percentiles'][f'P{p}']) for p in (5,20,50,80,95)]
        md.append('| '+' | '.join(values)+' |')
        html_rows.append('<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in values)+'</tr>')
    tables.append(f'<h2>{n} dials</h2><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['Valid settings','Mean trials','P5','P20','P50','P80','P95'])+'</tr></thead><tbody>'+''.join(html_rows)+'</tbody></table>')
md+=['','## Interpretation','',
    '- P95=36 means at least 95% of sampled codes finished within 36 trials, not the probability of exactly 36. Counts include initial and successful trials. Sample percentiles fluctuate; JSON retains mean intervals and percentile Bootstrap intervals.',
    '- For eight dials/seven settings: mean about 27.20 trials, approximate 95% mean interval 27.04–27.37; P95 Bootstrap interval 36–37. These describe code-sampling uncertainty only, excluding policy, model and physics changes/errors.',
    '- Within this range/policy, adding one valid setting for six/eight dials adds about 3 / 4 mean trials. This is a numerical observation, not a complexity theorem.',
    '- A simple coordinate-wise record policy guarantees at most 1+N×(K−1) trials: 25 / 37 / 49 for 4 / 6 / 8 dials with seven settings. It is not optimal and is slower on average than the tabulated policy, but shows that K^N codes need not all be tried.',
    '- Setting angles, extra intermediate-motion settlements, grasp errors, arm collisions and GPT reasoning errors are unmodeled. Trial-count ratios are not real-duration ratios.',
    '- The earlier Oracle engineering cap of 24 rounds should not carry unchanged to every new difficulty. Specify logical and mechanical-time budgets before conflating budget exhaustion with reasoning failure.',
    '', 'This analysis changed no actual scenes, codes, evaluation interfaces or old recordings.']
(B/'report.md').write_text('\n'.join(md)+'\n')
(B/'combined-summary.json').write_text(json.dumps(dict(assumptions=summary['assumptions'],results=rows),indent=2)+'\n')
with (B/'percentiles.csv').open('w',newline='') as file:
    fields=['dials','alphabet','passwords','tested','exhaustive','mean','P5','P20','P50','P80','P95'];w=csv.DictWriter(file,fieldnames=fields);w.writeheader()
    for r in rows:w.writerow({**{k:r[k] for k in fields[:6]},**r['percentiles']})
for name in ['report.md','combined-summary.json','percentiles.csv','baseline-validation.json']:
    shutil.copyfile(B/name,OUT/name)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BEST: settings and trial distributions</title><style>body{font:17px system-ui;background:#f3f5f6;color:#1a3041;line-height:1.8}main{max-width:1100px;padding:24px;margin:24px auto}h1{font-size:34px}table{border-collapse:collapse;background:white;width:100%}th,td{padding:12px;text-align:right;border-bottom:1px solid #d9e3e9}th{background:#e6eef2}th:first-child,td:first-child{text-align:left}h2{margin-top:36px}a{color:#0c638c}.note{padding:18px;background:#fff3d8;border-left:4px solid #c99a3b}</style><main><h1>BEST feedback: trial distributions with 3–7 settings</h1><p>Valid settings exclude 0. The candidate-elimination/record-neighborhood policy is retained; this is neither a theoretical optimum nor a GPT measurement.</p><p class="note">The 3-setting baseline, every setting for 4 dials and 4 settings for 6 dials are exhaustive. Other groups uniformly sample 4096 codes, with estimated percentiles. Code filtering is always exact; large posteriors sample 8192 candidates only for query entropy.</p>'''+''.join(tables)+'''<h2>Interpretation and limits</h2><p>A percentile gives the trial count within which that fraction of codes finishes, including the first and final successful attempts. Robots, angular layouts and automatic intermediate-motion updates are unmodeled. Eight-dial/seven-setting P95 is estimated at 36, Bootstrap interval 36–37.</p><p>With seven settings, the simple coordinate policy guarantees upper bounds of 25 / 37 / 49 trials, without exhaustive code search. These reference-policy results predict neither GPT success rates nor physical duration.</p><p><a href="report.md">Full report</a> · <a href="percentiles.csv">Download statistics CSV</a> · <a href="combined-summary.json">Statistics and uncertainty JSON</a> · <a href="baseline-validation.json">3-setting path reproduction check</a></p></main></html>'''
(OUT/'index.html').write_text(page)
print(OUT/'index.html')
