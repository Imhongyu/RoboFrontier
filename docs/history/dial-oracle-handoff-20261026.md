> Historical record, not current operating instructions. Current rules/defaults:
> [Dial family](../tasks/dial-best5.md). The pause/resume instructions below applied
> to this archived session, not subsequently authorized integration work.

# Dial Oracle handoff: 2026-10-26 pause before compaction

## Instructions and state at that time

**The user-requested pause was in effect. Experiments were not to restart until
the user said to continue after compaction.**

The latest request was to retain failed worlds instead of immediately ending
Oracle, allowing GPT to analyze failures and perform actual recovery, with
backtracking exploration if needed but no stitching different trajectories into
continuous success. Continue the three L3 cases; first-round 6/9 was not the
end of the overall task.

No task physics, solver/evaluator subprocess or recovery experiment remained
running. All first-round cases had ended, all 18 front/rear videos had exported
and fully decoded, and all 9 blind-decoder audits had completed.

## Historical assigned worktree

- `/Users/fanchangxuan/.codex/worktrees/dial-best5-oracle/roomscript2`
- Branch: `task/dial-best5-oracle`.
- HEAD: `1b6e5c7`, the first formal round's frozen source.
- Original project: `/Users/fanchangxuan/Repos/roomscript2`, initially without Git, then given a shared main.
- Shared baseline `8e7872f`; ignored external-data-link correction `d3e5916`.
- **This task was unmerged. Do not modify/schedule the user's other three families' forks/worktrees.**
- Large model assets stayed outside Git. Required model files used independent APFS COW copies with distinct inodes. `.venv`, vendor, runs, outputs, docs/generated and private evaluator inputs were external links.
- Shared `scripts/setup_worktree_data.py` was on main; other families were managed in separate user sessions.
- Recovery code had uncommitted changes, **not a verified version; in particular its default shoulder-grasp strategy must not launch directly.**

## Formal first round: actual outcomes, six passes not to rerun

Directory: `/Users/fanchangxuan/Repos/roomscript2/runs/oracle/dial-best5-r11-worktree-20261025`.

- `batch-status.json`: active=false; 9 cases ended, 6 passed.
- `audit.json`: all 9 replayed consistently using only solver input logs, without private codes.
- `manifest.json`: frozen commit/workspace/configuration/budgets.
- Each `dial-best5-nXX-dY/attempt-001/` contained report, actions, trace, motion, frozen source and evaluator logs.

| Task | Outcome | Key evidence |
| --- | --- | --- |
| 4 dials L1 | Passed | 136.3 s; 8 explicit query choices / 20 actual valid inputs; zero failed actions/violations/unknowns; peak 4 arms moving |
| 4 dials L2 | Passed | 160.0 s; 6 explicit choices / 9 valid inputs; zero failed actions |
| 4 dials L3 | Unpassed | BEST2/4; G kept turning after D04 blue support loss; `driven_red_without_support` at sim276.442 s |
| 6 dials L1 | Passed | 149.1 s; 22 valid inputs; zero failed actions |
| 6 dials L2 | Passed | 441.7 s; 20 valid inputs; zero failed actions |
| 6 dials L3 | Unpassed | `Blue grasp did not requalify before red operation: D04`, about 159 s; guard stopped further rotation |
| 8 dials L1 | Passed | 250.9 s; 21 valid inputs; zero failed actions |
| 8 dials L2 | Passed | 568.8 s; 14 valid inputs; zero failed actions |
| 8 dials L3 | Unpassed | BEST6/8, about 885.6 s; `No reachable small open-crank exit I`; no reachable small release exit; 6 failed actions, no unresolved actions at end |

Videos: `/Users/fanchangxuan/Repos/roomscript2/outputs/oracle/dial-best5-r11-worktree-20261025`.
Each had global/global_rear, reconstructed offline from actual 60Hz states at
12x, **without reintegrating physics to manufacture a video**.

Historical completed-nine-case result page:
`http://127.0.0.1:56719/best5-blind-oracle-worktree-20261025/index.html`.
Initial-state gallery: `http://127.0.0.1:56719/best5-dials-r11/all-tasks-top.png`.

Management session 85896, first export 74255, final export 50844 and final audit 33771
had ended. Do not wait on them again or treat them as live processes.

## Blind-test and physics boundaries

- Nine R11 cases: 4/6/8 dials × L1/L2/L3. L1 used 4/6/8 arms; L2/L3 used 8/12/16.
- Marks 0..5, with 1..5 valid at 60° spacing. 3 may be ±180°; 4/5 may use -120°/-60°.
- Feedback was historical BEST, initially 0. READY: gray invalid / amber qualifying / green ready. Not-ready digits dimmed but retained the record; green brightened digits.
- Original validity: nonzero mark ±4°, 250ms, actual red bilateral contact and active force holding; L2/L3 additionally independent blue support and entire mechanism at least 20mm clear of external support.
- **Automatic settlements included actual intermediate combinations**, not just requested targets. An unchanged BEST was not the current score.
- Only the evaluator process read private codes. The solver received N/K, time, actually visible combinations and historical BEST, retaining multiple explanations for ambiguous attribution.
- Actual geometry/joints/mechanism angles were **Oracle privileges**, not new ground-truth tools for GPT roles.
- Do not read `private-evaluator-input.json` or `configs/evaluations/private/...` contents into research context or alter paired codes.
- Do not change physics, friction/NoSlip/force limits or acceptance to repair success. Settings were 2ms, NoSlip20 and pd1000-v1 hand control. Ordinary grasp commands could change only through real execution/logging.
- Recorded violations must remain. Recovery unlock could establish goal_reached separately from clean success. A fresh initial-state run with the repaired strategy could establish compliance; stitched rollback segments could not.
- This authorization was Oracle only, **without automatic GPT start or main merge**.

## Uncommitted recovery work at that stage

Inspect `git status --short` and diffs first. Main files:

1. `robofrontier/suite/dial_live_repair.py`, new:
   - A private Dial LiveRepair bridge reusing generic `OracleRecovery`, not another executor.
   - Controlled stop on recoverable errors; record images, robot feedback, mechanism poses and original errors while retaining world and blind decoder.
   - Publish `trial/recovery/awaiting.json`; research submits ordinary commands through `pause-NNN/plan.json`, then continues the same goal.
   - Plan: `{"source":"research_gpt","batches":[{"A":["gripper",{"mode":"move","width_m":0.08,"speed_m_s":0.05}]}],"resume":true}`.
   - Write atomically and retain every request/result/failed plan. No qpos reset, violation deletion or code disclosure.
   - Respect user STOP/ReferenceStopped; waiting counts toward wall budget.
   - Actual failure end-to-end validation remained; only loop/executor tests existed.
2. `robofrontier/suite/oracle_recovery.py`, pre-existing:
   - **It already existed and must not be overwritten.** A temporary naming collision was corrected by restoring the complete original module.
   - Added only `reattach(owner)`, `acknowledge(owner,id,review,assisted=False)` and `resume(owner)` for repeated terminal handback/retake with the same physical owner.
   - Retained uncertainty fencing, independent robot sequences, source hashes and assisted classification.
3. `dial_best_oracle.py`:
   - solve entered LiveRepair after lift/set_symbols failure instead of closing immediately.
   - Retried the same guess with blind history/BEST retained, without rollback stitching.
   - New release candidate: once red force mode ended with valid blue support, ordinary blue motion translates the module 12mm to create relative withdrawal instead of extending an already-limited red arm. Bounded attempts had not yet succeeded physically.
   - **Unsafe pending default: `blue_capture_mode='shoulder'` was default despite failed initial-pose shoulder checks. Restore `stem` before formal L3. Shoulder belongs only in explicit experiments.**
   - Shoulder used a 32mm outer-shoulder span, closure along the blue-handle long axis and a grasp between shoulders; it remained unpassed.
4. `dial_oracle.py` / `dial_oracle_v2.py`:
   - blue_capture_options/blue_approach_aperture extended old references without changing their defaults.
   - Best L3 could pre-open empty fingers to target span +12mm. A 44mm test did not resolve shoulder collision.
   - `rule_failure()` allowed continuation only in an engineering attempt explicitly recovering a recorded violation; Monitor violations/task_success remained unchanged.
5. `oracle.py`:
   - execute exceptions retained submitted nonterminal calls as uncertain with original commands and advanced IDs, preventing reuse; actual stop feedback was separate.
   - llm_used reflected online intervention; generic recovery-adapter close still needed to supply full assisted metadata.
6. Formal runner/batch:
   - `run_blind_dial_oracle.py` used `dial-best5-continuous-grasp-repair-v2`, adding goal_reached, intervention count and continued_after_violation.
   - **Important incomplete wiring:** runner finally still polled/trial.close directly. Attached generic recovery needed adapter.pause/advance draining and adapter.close(report), without unauthorized polling or lost assisted/recovery metadata.
   - `run_best5_dial_batch.py` no longer blocked other cases after first failure, matching the user's continue-on-failure request.
   - A new batch required a separate directory, preferably only the three failed L3 cases with live recovery channels, without overwriting round one.

## Verified/rejected physical leads

First-round read-only D04 blue-support diagnostics:
`support-geometry-diagnostic.json`, `diagnose_support_geometry.py`.

- On lift, blue hand H aperture was about 19.9mm with normal module/hand relation.
- Before 4-dial L3 failure, the module rolled about 36° relative to H and aperture reached about 35mm. Shoulder/H-palm contact preceded support loss.
- Before failure, red hand G showed only ordinary finger contact with the red handle. No evidence there established red-palm/disk collision; do not assert that cause without evidence.

Shoulder probes:
`/Users/fanchangxuan/Repos/roomscript2/runs/engineering/best5-recovery-20261026/shoulder-d04/attempt-001`, `attempt-002`.

- Neither reached D04 turning. Both first failed initial D01 blue approach: `No side-access blue grasp D01`.
- First aperture was 80mm; narrowing to 44mm in the second also failed.
- Independent zero-step FK/collision checks showed the 32mm axial shoulder grasp put the palm into the white disk, about 12.7mm penetration. It was not simply unreachable IK; position error was small.
- Further FK-only tests grasped a 4mm wing near the outer shoulder (z=-.078), offset y±22mm, still producing about 10–14mm palm/link7 interference. Some 20/35/50/65-degree tilted candidates also lacked collision-free initial-table endpoints. These wing/tilt searches were **diagnostic only, unimplemented and not dynamic grasp successes**.
- Unimplemented/unproven directions included first lifting by the verified stem grasp, temporary support by another hand, airborne blue regrasp, or changing disk presentation to reduce eccentric gravity/provide red-hand clearance. Use ordinary interfaces and small units without changing physics/secrets.

## Test versions must remain distinct

- Frozen commit `1b6e5c7` passed 57 software tests before formal launch.
- The latest recovery group passed 30: `tests.test_oracle_live_repair tests.test_oracle_recovery tests.test_best5_oracle tests.test_dial_hold_oracle`.
- Later small blue-approach-aperture changes had no complete recovery end-to-end pass; do not claim every recovery was verified.
- Initial FakeWorld tests lacked model and left a thread waiting. Fixtures/daemon were fixed and old PID 3730 explicitly stopped.
- Generic recovery tests received R10 four-arm Transport COW assets as fixtures, without changes to other families.
- New `tests/test_oracle_live_repair.py` covered continuation after failed plans, real executor commands, interrupted-ID nonreuse and shoulder rotation/span math. The latter was not physical grasp qualification.

## Historical post-compaction sequence

1. Confirm the user's continue instruction, read this file/diffs and use the assigned worktree rather than editing original main.
2. Restore failed shoulder default to stem; retain/isolate the experiment instead of repeating initial failure.
3. Complete existing OracleRecovery runner drain/close integration; retain violations, unknown IDs and accurate assisted labels.
4. Validate one controlled recoverable failure end-to-end: retain world → publish awaiting → research ordinary repair actions → continue the same decoder, beyond helper-only tests.
5. For 8-dial L3 unreachable exit, minimally test blue-assisted relative withdrawal. For D04 support, test a more stable control/regrasp plan first.
6. After checks, commit the branch and use new directories for the three L3 attempts with the same private paired codes. Retain failed worlds for analysis instead of immediate shutdown.
7. Continued execution after recorded violations may demonstrate goal_reached, never fabricated clean success. If needed, rerun the repaired strategy from standard initialization for continuous compliant evidence.

## Compaction-protection backup

External directory: `/Users/fanchangxuan/Repos/roomscript2/runs/oracle/dial-recovery-20261026/`.

- `working-source.tar.gz`: full copies of 11 modified/new source files, made before this handoff.
- `working-tree.patch`: tracked changes relative to `1b6e5c7`.
- `working-source-manifest.json`: branch, base commit, paths and per-file SHA256.
- This record would be copied there as `HANDOFF.md`.

The then-uncommitted worktree file was `docs/dial-oracle-handoff.md`; compaction
does not delete files. **Do not use reset/clean to tidy uncommitted recovery work.**
