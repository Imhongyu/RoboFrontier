# Historical Mosaic GPT readiness and multi-workstation replay plan

This page preserves planning and implementation history. See the [task guide](../../tasks/mosaic.md)
for current tasks/purpose selection and [merge handoff](../plans/suite-v2/mosaic-merge-handoff.md)
for current commands, integration order and shared work.

Date: 2026-10-27 (Asia/Hong_Kong). This records the original plan.

Subsequent progress: after the user authorized “start,” the Mosaic R13 package,
independent Skill/prompt, specification/evidence checks and private trajectory
reviewer were implemented. Shared harness, launch gates, public-material loading
and multi-table playback were unchanged. Entries are in `docs/tasks/mosaic-r13.md`;
shared requests are in `docs/tasks/mosaic-shared-integration.md`. “Planning only”
below describes the earlier checkpoint and does not revoke later authorization.
“Worksheet” meant a task family's Git worktree. That original round added only
this document: no task/prompt/Skill/harness/evaluator/replay changes, GPT run
preparation/launch, Oracle rerun, branch merge or edits to other family worktrees.

The user explicitly selected: **completed stations retain their final products;
stationary completed stations are allowed, without looping.** Remove useless
mid-task waiting/jitter, not the display of completed products.

## 1. Final goals and assessment at the time

Goal A: formal GPT execution must see the final workstation, task rules, tools,
public inputs and evaluator. Families own specifications/guidance/adapters;
common infrastructure is integrated once.

Goal B: display several completed Oracle trajectories simultaneously by skipping
confirmed useless intervals independently at each table, taking original states
and composing them in one image. No physics rerun or global post-render cutting;
each table has its own source and edited time.

**Existing delivery covered only part of goal B.** Mosaic had original-60Hz-bound
30x/30fps frame mappings, full-rate retained windows, single-station Factory
replay and a matching station. This worktree lacked complete independent-clock
orchestration and evidence that idle detection recognized large, prolonged,
no-progress oscillation. Existing mappings also included decisions made from
simple-scene images, rather than a complete camera-independent physical-action
classifier.

All nine complete original tasks and independent recording audits were complete,
covering 1566 targets. This is privileged-state/assisted-recovery Oracle evidence,
not GPT policy validation. Other families select and describe their own evidence.

## 2. Facts checked

Baseline: main `d3e59165`, this branch `f43c0e37`. Dial/Relay/Transport worktrees
also had uncommitted changes; cross-branch comparisons were read-only snapshots,
not frozen merge inputs.

| Area | Checked fact | Planning consequence |
| --- | --- | --- |
| Nine actual stations | Final motion/source scene hashes and frozen tasks match current Mosaic R13 | Existing records reflect changes; do not broadly claim geometry was never updated |
| Default entry | `suite/v2.py::cases()` still selects Mosaic R10; `prepare_policy_minimum_batch.py` fixes R10, minimum scale, historical 1200s probe | Formal entry must explicitly select nine R13 cases rather than launch the old batch |
| Readiness | Tasks still say `environment_preview_only`, `oracle_verified=false`; catalog describes geometry-check stage | Register version-bound new policy readiness; preserve historical source bytes |
| Formal gate | `validate_task` accepts preview/explicit bounded probe; `World.start_trial` rejects preview | Shared integration requirement; no disguised probes or gate bypass |
| Public prose | Already includes 60mm blocks, 81mm pitch, 80mm L1 pockets, L2 red lines, L3 without grids, four colors, whole-pattern rotation and nonexclusive supplies | Preserve correct facts, fill gaps and prevent regeneration from old builders |
| Public completion | No structured public completion; private completion retains generic commissioning prose, actual tolerances mostly in evaluator | Map rules/public specifications/evaluator; do not change scoring to fit prose |
| Static tables | Public target.center_world_m z already implies 0.8m, but complete independent table outline is missing | GPT was not wholly uninformed about height; add checkable static geometry |
| Prompt/Skill loading | run_setup freezes common prompts/roles/Skills; no explicit Mosaic-material loading chain | Adding family files alone does not put them in GPT context; propose shared loading hook |
| Controls | Nine executor-source/inputs/harness.json files match current servo2 JSON, all pd1000-v1; physical fingerprints match, execution source versions vary | Do not change shared control because of table height; private Oracle 0.2/0.35rad/s settings are not automatically GPT rules |
| Workspace | World prefers task workspace_world_m; READY reports actual bounds | Old harness fallback numbers are not these cases' actual command bounds |
| Old protocol docs | R13 worktree still describes historical 1800s pilot and initial two instances | Mark completed stages and freeze a new protocol; no implicit new GPT deadline |
| Replay | replay_motion_in_factory consumes one recording/edit at a time; other tables do not advance independently | Reuse single-station replay, add shared orchestration |
| Original evidence | All nine have 60Hz qpos, actions.json, trace.jsonl, process.jsonl; no complete framewise measured contact forces | Analyze effects/progress; poses or force settings do not establish measured zero force |

Check each of nine cases; the three scales have different complete table sizes:

| Arms / target grid | Table width × depth (m) | Height (m) | Targets in each L1/L2/L3 |
| --- | ---: | ---: | ---: |
| 4 / 6×12 | 2.465×2.66175 | 0.8 | 72 |
| 6 / 9×18 | 3.0725×3.41125 | 0.8 | 162 |
| 8 / 12×24 | 3.68×3.3435 | 0.8 | 288 |

Evidence: `final_verified_cases` in
`runs/oracle/mosaic-continuation-20261026/evidence-summary.json`; display entry:
`videos/video-index.json` in the same namespace. Action frequency/physics timestep,
60Hz recording, online observation-video fps, offline 30fps and display 30x are
separate. Default Mosaic 30x changes neither controls/integration nor other
families' display defaults.

## 3. Proposed Mosaic-owned package

The original plan proposed, but did not yet create:

- `configs/task_families/mosaic/r13.json`: nine versions/evidence entries,
  specification version, hashes, control fingerprint, evaluator version,
  assistance/failure flags and default 30x display.
- `docs/tasks/mosaic-r13.md`: final human-facing task/level guide.
- `prompts/tasks/mosaic-r13.md`: only permitted policy facts, rules and guidance.
- `robofrontier/suite/mosaic_policy_package.py`, dedicated build/check scripts
  and tests: reviewable package without hardcoding nine cases in a common launcher.
- Mosaic-owned Skill supplements if needed; common loading/references await
  integration, without more family exceptions in shared SKILL.md.

### 3.1 Fields to check per case

1. case_id, R13 source version, actual scene/asset hashes, arm count/bases/yaws,
   table outline/height, axes/units, camera calibration and actual READY bounds.
2. Blocks 60mm, permitted public mass/friction assumptions, pitch 81mm, correct
   pattern/world direction, four colors/images and inventory conservation;
   list 6×12, 9×18 and 12×24 separately.
3. L1 pocket opening/depth/floor; L2 3mm red lines; L3 no visible grid but a
   defined target coordinate system.
4. Public conditions mapped to scoring: release, 1s stability, color/one block
   per cell, orientation; L2/L3 center xy5mm/z3mm and 8-degree axis alignment;
   L1 full footprint containment, 0.3mm inclusion margin, floor 0.8mm and actual
   contact. Check values against current evaluator/specification rather than
   inventing a second drifting standard; include stable-speed and bilateral
   boundary-inclusion semantics.
5. Supply ownership is nonexclusive; safe handoffs, center/table buffering and
   concurrent arms are allowed. No mandated pairings/routes/color order or
   return-home barriers.
6. Failed/unknown actions, protecting finished cells, separate release/retreat
   milestones; retain tool/observation contracts without Oracle recovery tools.

Static table/robot geometry and precise initial/live object poses have different
public boundaries. Review added fields individually instead of exporting all
private JSON. Guidance may use RGB/robot feedback to infer grasps and offsets,
consider aperture/neighbors, plan handoff/release/retreat, protect completed
cells and revise concurrent plans. Do not inherit private IK, coordinate traces,
repair recipes, hidden truth or engineering chats. Experience reuse across runs
requires an explicit experiment declaration.

### 3.2 New policy readiness and preparation

Pin evidence and permitted facts → compare final environment/evaluator/tools →
produce family package/differences → integrate shared readiness/loading → preview
new frozen run inputs → launch GPT.

Never rewrite frozen tasks, motion/source or Oracle reports to say ready. Use
sidecars binding assets/logic/controls to evidence. Freeze new model, topology,
observation/cost/runtime protocols separately; old 1200s probes, Oracle pilots
or display speeds do not silently become new experiment limits. Separate
preparation from physical/inference launch.

## 4. Worktree boundaries and shared integration

Family work belongs in Mosaic modules/configuration/docs/tests. Register existing
shared changes without reverting/expanding them in this round; the integration
owner absorbs behavior once. Do not edit, commit, reset or merge other worktrees'
uncommitted files.

| Shared location | Observed overlap | Integration requirement |
| --- | --- | --- |
| robofrontier/motion_edit.py | Mosaic/Dial both call different structures motion-edit.v1 | One versioned contract and explicit adapters; no same-name overwrite |
| robofrontier/motion_timeline.py | Transport has same-schema JSON+NPZ retained windows | Define inclusive/half-open intervals, sampling phase, event checksums/migration |
| render_frontier_oracle.py / replay_motion_in_factory.py | Different Mosaic/Dial/Transport versions | Common entries with family data/plugins |
| factory_workstations.py | Dial/Relay/Transport changes | Source bindings/layout/batch poses; Relay apply_arrays vectorization alone is not multi-station clocks |
| export_factory_recorded_pose.py / build_factory_workstations.py | Different exports/builders | Common transform/source/timeline contract with old adapters |
| suite/oracle.py, recovery, some evaluators | Independent branch changes | Review behavior/fingerprints; no newest-whole-file selection |
| Shared prompt/Skill, run_setup, readiness | Family loading/formal gates need agreement | Integrate once, with no integrity bypass |

Order: family specifications/evidence/requirements → frozen branch snapshots
(including explicitly selected uncommitted work) → one format/adapter contract →
shared integration → per-family input/evaluator/tool consistency → frozen new
policy run → GPT simulation.

Display/docs alone do not mandate all Oracle reruns. Asset/control/scoring changes
need impact analysis and affected checks. Matching control fingerprints do not
mean all Oracle execution source versions match.

## 5. Multi-workstation playback

Station i owns immutable recording R_i, reviewed retained windows K_i, source-time
mapping, speed s_i, rigid transform T_i and completion state. Only output frame k
and fps are shared.

```text
factory display time τ = k / fps
for each playing station i:
    resolve original state index and source time t_i from its edit
    advance events through t_i, including cuts; restore recorded pose/appearance
    apply its own T_i
for completed stations: retain exact final pose/appearance and mark complete
set display clock τ after all station updates, then render the factory once
```

In one output frame, source times may be 20s, 500s and 9000s. Do not share one
source clock/global deletion table. FactoryPlayback.apply writes data.time=t_i;
the orchestrator must restore display time after all updates.

**Chosen end_policy=hold_final:** all start at their first frame, each stops at its
finished product, and the video ends when the longest trajectory finishes. Allow
completed stations to be still; no loops or equal-duration stretching. Replay
loops/cuts do not represent new Oracle experiments.

- Exact existing delivery: consume each render_frames; Mosaic default 30x/30fps.
- New speed/fps: resample full retained states with a continuous edited-clock
  sampling phase, avoiding phase resets at cuts. Preserve old frame mappings
  for exact historical reproduction rather than silently changing their semantics.
- Bind hashes of source/events/edit/station/transform. Use a new explicit format
  such as v2, with conversions/acceptance for existing v1 variants.
- Translate/yaw the entire table/base/arms/objects, retaining dimensions/relative
  layout. Old trajectories do not guarantee arbitrary rearrangement/scaling.
  Old v6 Mosaic stations differ from actual R13; known matching output is
  outputs/robo-factory/v6-mosaic-recorded-20261027. Freeze each family's binding.
- Decode/cache required chunks efficiently, do FK as needed, aggregate all poses
  and render once; no full-factory render per table, physics, IK or contact rerun.

## 6. Prolonged visible no-effect oscillation

**This layer was incomplete.** Image-change thresholds retain substantial motion,
while deleting every stationary arm would lose useful holding/support/contact.
Neither qpos, commanded force_n nor absence of actions proves measured zero force.

Derive family semantic labels from original trajectories/actions/events/progress,
then freeze an independent source timeline. Classification should not depend on
Factory pixels or global post-render cutting.

1. **Protect useful processes:** transport, effective arm/finger motion,
   grasp/release, handoffs, net object motion/mechanism changes, failure/recovery,
   progress/support/qualification/success events. Static support, force holding,
   settling and scoring dwell may matter despite zero displacement.
2. **Identify candidates:** several seconds without useful operation, local object
   oscillation, large path length but little net displacement/trend, and no change
   in grasp, target approach, progress or qualification. Use physical units,
   windows, trend/amplitude/period and hysteresis, beyond one speed threshold.
   Calibrate against original footage; thresholds were not yet verified.
3. **Allow removal despite amplitude:** use family purpose/protected windows;
   meaningful Dial attempts, solution search, controlled regrasp, recovery or
   active contact are not useless solely because no score improved.
4. **Review levels:** confirmed useless→remove; confirmed useful→retain;
   unknown purpose/force→review, without fabricated zero force. Keep representative
   boundaries/results of clearly redundant oscillation and record reasons,
   source windows and reviews.
5. **Events/causality:** restore correct post-cut appearance/state, retain needed
   transitions, do not interpolate across cuts or alter original time/failure
   counts. Measure actual costs/concurrency from full records, not edited duration.

Existing evidence supports some offline analysis, not a complete measured-force
claim. Future torque/contact/support telemetry needs shared fields, sampling,
units and sources after integration. Do not invent old telemetry or rerun all
Oracles solely to edit a video.

## 7. Implementation and acceptance stages

| Stage | Family product | Completion / shared dependency |
| --- | --- | --- |
| A Facts | Nine R13 specifications/evidence entries and differences | Each actual station maps to public rules/evaluator/controls |
| B Package | Mosaic configuration, prompt/Skill, checks/tests | No privileged Oracle experience; reviewable package without simulation |
| C Shared | Requirements/adapters | Unified readiness/projection/loading/edit format/multi-table scheduling |
| D Review | Family phase/effect labels and candidate/regression windows | Remove long idle/useless large oscillations; preserve useful slow movement/holding/recovery |
| E Display | Two staggered tables → nine Mosaic tables → all families | Independent source clocks, accurate appearance, 30fps, hold_final, no global post-cut |
| F Formal preparation | Frozen task/roles/Skills/tools/observation/protocol inventory | Review actual loaded content after shared gates; launch GPT separately |

Required examples:

- Staggered waits: A skipping must preserve B's useful motion and vice versa.
- Small fast jitter, large long-period useless oscillation, very slow useful drift.
- Stationary effective support/holding, small genuine finger actions, handoff,
  release and recovery.
- Score/appearance/qualification/progress events across cuts; exact endpoints.
- Early completion holds the finished product and marks complete; no loop or
  further deletion that skips global frames.
- Rigid relocation/material changes preserve source selections; reject wrong
  versions or scaling.
- Preserve original hashes; do not use edited duration as actual performance or
  replay as permitted policy training. Unknown/force gaps cannot silently become
  confirmed uselessness.

## 8. Original stopping point

The initial round checked facts, ownership, interface conflicts and implementation
order and added only this document. It did not prepare/launch GPT, rerun Oracle or
implement classifiers/orchestration. Next was the Mosaic package; shared harness
work remained merge requirements. This is historical, not a current pause.

## 9. Implementation record (2026-10-27, after “start” authorization)

A/B implemented: registry, public completion/static specifications, dedicated
prompt/Skill, nine-case build/check scripts and tests. Review package:
outputs/policy-packages/mosaic-r13-20261027; policy_launch_ready stayed false.
Original R13 tasks, Oracle recordings and shared launchers were unchanged.

D's family review component produced 135 idle proposals and retained 5 slow-drift
windows. Tests cover repeated object/finger oscillation, quaternion sign, useful
slow motion and holding/failed-opening protection. Actual candidates contained no
review_repeated_* findings. These are private proposals, not approved cuts, and
were not applied to existing videos/timelines. Unknown forces/effects remain
unknown rather than guaranteed zero force/uselessness.

Shared C/E/F remained pending: formal readiness, public supplements and material
freezing/loading, unified edit format and independent multi-table clocks. No new
GPT run was prepared or launched. Early finishers hold their products, without loops.
