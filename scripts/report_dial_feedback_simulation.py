"""Research report and public tables; no environment or evaluator mutation."""
from pathlib import Path
import json
import html
import shutil

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'runs/oracle/dial-feedback-comparison-20261025'
OUT=ROOT/'docs/generated/frontier-v2/dial-feedback-comparison';OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((B/'summary.json').read_text());lookup={(r['dials'],r['policy']):r for r in data['results']}
rows=[];actions=[];details=[]
for n in (4,6,8):
    c=lookup[n,'current_entropy'];b=lookup[n,'record_entropy'];a=lookup[n,'record_local_entropy'];simple=lookup[n,'record_coordinate']
    pct=lambda x,y:100*(x/y-1)
    rows.append(f"| {n} | {3**n:,} | {c['queries']['mean']:.2f} | {b['queries']['mean']:.2f} | +{pct(b['queries']['mean'],c['queries']['mean']):.1f}% | {a['queries']['mean']:.2f} |")
    actions.append(f"| {n} | {c['changed_dials']['mean']:.2f} | {b['changed_dials']['mean']:.2f} | {a['changed_dials']['mean']:.2f} | +{pct(a['changed_dials']['mean'],c['changed_dials']['mean']):.1f}% | {simple['changed_dials']['mean']:.2f} |")
    for name,title in [('current_entropy','Current count / entropy-first'),('record_entropy','Record high / matched entropy-first'),('record_local_entropy','Record high / record-neighborhood experiments'),('record_coordinate','Record high / coordinate comparison')]:
        r=lookup[n,name];details.append(f"| {n} | {title} | {r['queries']['mean']:.2f} | {r['queries']['p95']:.0f} | {r['queries']['maximum']} | {r['changed_dials']['mean']:.2f} |")
report='''# Record-high feedback: exhaustive discrete-complexity simulation

This historical discrete-logic simulation started no MuJoCo, arms or GPT. It exhaustively tested 81 / 729 / 6,561 equally weighted codes for 4 / 6 / 8 dials, totaling 29,484 complete solution paths across four policies. It used neither the nine actual task answers nor hidden answers as inputs for choosing the next query.

## Mean logical trials

| Dials | All codes | Current correct count | Record high: matched policy | Increase | Record high: adapted neighborhood |
|---|---:|---:|---:|---:|---:|
'''+ '\n'.join(rows)+'''

The first two solvers shared a candidate-sampling cap of 96, entropy priority and a 0.015 change penalty; they updated candidates according to their respective feedback semantics. The adapted policy additionally permitted single-dial experiments around a known record-setting combination. It received neither the current correct count nor per-digit correctness.

## Mean individual dial changes

| Dials | Current count / entropy-first | Record high / matched policy | Record high / adapted neighborhood | Increase over current count | Record high / coordinate comparison |
|---|---:|---:|---:|---:|---:|
'''+ '\n'.join(actions)+'''

Changes count individual dials altered between consecutive submitted combinations, including initial changes from 0 to nonzero. After an unsuccessful coordinate experiment, restoring the old setting also counts toward the next submission. These are not low-level robot action counts; angles, trajectories, withdrawal, collision and grasp recovery are excluded.

## Tails and policy differences

| Dials | Policy | Mean trials | P95 | Maximum trials | Mean changes |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(details)+'''

The matched entropy policy worst case of 57 trials for eight dials is a policy limitation, not a requirement of 57 trials. An independent coordinate-record policy needs at most 9 / 13 / 17 trials across all codes, establishing an achievable upper bound. Neighborhood search uses fewer trials on average but is not globally optimal. Poor adaptation of an old algorithm is not intrinsic task difficulty.

## Findings

- The candidate space remains 3^N. Feedback loses whether a query is worse than or equal to the record, adding mainly experiment design, historical-input attribution and candidate-constraint bookkeeping.
- Matched-policy mean logical trials increase about 28% / 64% / 86%. Adapting to the new feedback reduces increases to about 26% / 51% / 70%, while individual dial changes increase only about 3% / 10% / 15%. This can add reasoning work without proportional mechanical motion.
- A coordinate policy can trade more logical trials for fewer changes. Report trials, changes, holding time and total time separately; motion parallelism alone cannot assess this task.
- Mean candidate/query matching work for matched policies increases only about 4% / 12% / 14%. These are computation-work proxies, not GPT-time or physical-simulation predictions. Shared decision-tree prefixes make total simulation time different from running every instance independently.

## Scope and limits

Each complete input is one unambiguous settlement. The simulation excludes automatic intermediate-motion counts, regrasping, missed observations, LLM reasoning errors and robot dynamics. Table ratios predict neither GPT success-rate changes nor MuJoCo wall-time ratios. With continuous automatic updates, intermediate pauses can update BEST; record events must correspond to observable inputs. Otherwise the added burden is attribution ambiguity rather than the intended reasoning challenge.

This analysis overwrote none of the nine old environments or old recordings CORRECT labels. Labels, rules, evaluator and decoder must change together, rather than changing text alone. The historical rule draft is in feedback-contract.md.
'''
(B/'report.md').write_text(report)
contract='''# BEST feedback rule draft, not deployed by this historical analysis

Panel title: BEST / NN, where NN is the dial count. The value is the episode maximum correct count from a complete valid input, rather than the current input correct count.

1. Before any valid trial, show BEST --. After the first valid settlement, show 00–NN.
2. A complete input is valid only when all dials are actually held within the original ±4° tolerance of nonzero marks for 0.25 seconds. L2/L3 retain original support conditions.
3. At each valid settlement, the evaluator privately counts correct digits in the complete combination and exposes only the updated historical maximum. Do not disclose a lower current count, per-digit matches or the code.
4. An unchanged BEST means the current count is at most the record. When BEST increases and the settlement input is unambiguous, the new value equals that input correct count.
5. A record must come from one complete simultaneous combination, never a collage of per-dial results at different times. Unlock only when all are actually correct simultaneously.
6. Invalid, released or zero inputs retain the record but extinguish READY. Settlement resumes only after valid input is restored. READY communicates validity alone, without additional correctness information.
7. Records persist only within this episode world and reset for a new episode. Existing sealed records are unchanged.

Settlement attribution: before deployment, choose explicit discrete submissions or observable trial/record-setting events for continuous settlement. Intermediate motion can satisfy stability; its record cannot be assigned without evidence to the final intended combination. This affects valid-trial counts and must be versioned.

Solver update: if the record rises from B to B2, the unambiguously settled input scores exactly B2. If it remains B, the input scores ≤B. Retain the record-setting input/evidence, without treating its record as proof that the currently held input is still correct.

Engineering scope: add feedback_mode=current or best_so_far, an integer record and settlement sequence, reusing existing state/recording. These rules do not alter physics, setting counts or the generic robot interface. Task text/panel titles must match scoring semantics. Existing appearance events continue recording BEST/READY changes for offline replay.
'''
(B/'feedback-contract.md').write_text(contract)
for name in ['summary.json','report.md','feedback-contract.md','per-password.csv']:
    shutil.copyfile(B/name,OUT/name)
table_html=''
for title,rs,heads in [('Mean logical trials',rows,['Dials','Codes','Current count','Record high: matched policy','Increase','Record high: adapted policy']),
                       ('Mean individual dial changes',actions,['Dials','Current count','Record high: matched policy','Record high: adapted policy','Increase','Record high: coordinate'])]:
    body=''.join('<tr>'+''.join('<td>'+html.escape(v.strip())+'</td>' for v in row.strip('|').split('|'))+'</tr>' for row in rs)
    table_html+=f'<h2>{title}</h2><table><thead><tr>'+''.join('<th>'+h+'</th>' for h in heads)+'</tr></thead><tbody>'+body+'</tbody></table>'
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BEST feedback complexity simulation</title><style>body{font:17px system-ui;background:#f3f5f6;color:#172e3f;line-height:1.8}main{max-width:1150px;margin:40px auto;padding:0 24px}h1{font-size:34px}h2{margin-top:36px}table{width:100%;border-collapse:collapse;background:white}th,td{padding:12px;text-align:right;border-bottom:1px solid #dce4e9}th:first-child,td:first-child{text-align:left}th{background:#e7eff3}a{color:#08618d}.note{background:#fff5dd;border-left:4px solid #d59c35;padding:18px}code{background:#e7eff3;padding:3px 6px}</style><main><h1>From CORRECT to BEST: how much harder?</h1><p>Three valid settings are unchanged. Exhaustive codes for 4 / 6 / 8 dials yield 29,484 paths across four policies. The nine actual codes were not read; no arms or GPT ran.</p>'''+table_html+'''<p>Matched policies share entropy priority/change penalties. The adapted policy adds local experiments around a known record-setting combination, without receiving current correct counts.</p><p class="note">These are discrete logical trials/change counts, not MuJoCo actions or time ratios. Automatic intermediate updates, grasp recovery and model errors are unmodeled. More trials need not mean proportional mechanical motion.</p><h2>Change descriptions and interface together</h2><p>Label the panel <code>BEST / NN</code> and explain that it shows the episode maximum correct count for a complete valid input, not current correctness. A separate READY indicator can distinguish valid input without improvement from no valid input.</p><p>This historical work supplied simulation and a rule draft only, leaving old environments, CORRECT labels and videos unchanged. Deployment must address record attribution for intermediate motion.</p><p><a href="report.md">Full analysis and tail statistics</a> · <a href="feedback-contract.md">Rule draft</a> · <a href="summary.json">All statistics JSON</a> · <a href="per-password.csv">Per-code CSV</a></p></main></html>'''
(OUT/'index.html').write_text(page)
print(OUT/'index.html')
