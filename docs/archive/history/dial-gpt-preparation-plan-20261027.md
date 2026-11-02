> Historical record: this preserves the planning at the time, not current operating instructions. See the [Dial family guide](../../tasks/dial-best5.md) for current rules, defaults and entries.

# Dial tasks: consistency and multi-workstation replay before GPT execution

Date: 2026-10-27. This is the initial review plan. The user subsequently authorized
family-local implementation; see the [Dial family guide](../../tasks/dial-best5.md)
for delivery boundaries and usage. Shared merge work, formal GPT execution and
the full-factory multi-table renderer had not been implemented at this checkpoint.

The user's “worksheet” was interpreted as each task branch's worktree. This
owner covered only the nine Dial tasks, reading other families' interfaces to
identify conflicts without changing their rules or implementations. This round
only added this plan: no environment, prompt, Skill, harness or code changes,
run preparation/launch, Oracle rerun or branch merge.

Review baseline: Dial `db15b32`, main `d3e5916`; committed interfaces were also
read from Mosaic `56f4658`, Relay `16e8e16` and Transport `90dd0c5`. Later branch
changes require another comparison. Current integration status is tracked in
[unified main](../unified-main.md).

## 1. Goals and boundaries

Before formal GPT execution, the frozen environment, public task, family guide,
common role/tool instructions, evaluator and control configuration should refer
to one coherent version. Oracle proofs and engineering experience remain private
evidence. Answers, privileged state and execution scripts are not extra GPT inputs.

Each family owns its rules, configuration, documentation and adapters. Changes to
shared runtime, harness, role prompts, Skills or recording/replay cores should
be proposed with acceptance criteria and implemented once by the integration
owner. Register existing shared changes without reverting or expanding them here.

The Factory display uses completed Oracle recordings for offline kinematic
replay. All stations may appear together, but each independently skips its own
unproductive waits before one renderer produces the frame. This neither reruns
multiple physical Oracles concurrently nor proves that the original trials ran
in one shared physical world.

## 2. Facts confirmed in this review

| Area | Confirmed fact | Follow-up |
| --- | --- | --- |
| Nine Oracles | Each has passing evidence; eight programmatic Oracles, assisted Oracle for eight-dial L3 | Bind each case to its original evidence/version; do not call all nine autonomous or one uniform-version batch |
| Task entry | `configs/suites/dial-best5-r11.json` selects the correct nine BEST5 tasks | Select it explicitly in the new Dial entry |
| R11 task prose | Already includes 1..5, 60-degree increments, BEST, READY, automatic settlement, real red-handle grasping and L2/L3 airborne support | Preserve these facts; review structured fields and frozen runtime copies |
| Environment | Table height 0.8m, white-dial diameter 0.3m; layout, support and scoreboard placement/scale vary by case | Extract from each frozen environment; do not reuse one case's coordinates for all nine |
| Readiness metadata | Catalog/task/validation still say preview/generated and `oracle_verified=false` | Register version-bound evidence instead of changing every historical file to true |
| Existing GPT batch | `prepare_policy_minimum_batch.py` still selects R10, minimum scale per family/level, historical 1200s probe protocol | It cannot directly launch these nine formal R11 tasks |
| Formal gate | `suite/v2.py::validate_task` accepts preview or explicit bounded probe; `World.start_trial` rejects preview | Design formal readiness during integration; do not disguise formal runs as probes or bypass gates |
| Role prompts / Skills | Common responsibilities, RGB/robot-feedback boundaries and holding/release semantics exist; no BEST5 section | Retain common content and add family guidance rather than shared Dial exceptions |
| Public projection | `v2.public_task` exposes rules/mechanism/dials, but lacks structured completion and independent table geometry/height | Add necessary static specifications/rules without exposing all private fields |
| Control configuration | Frozen harnesses of the nine selected trials match current `harness-frontier-v2-servo2.json` as JSON | A table-height change alone does not justify a common harness change |
| Workspace | `World.tcp_command_bounds` prefers task `workspace_world_m`; READY reports actual bounds | Verify runtime resolution; old harness fallback is not these cases' actual workspace |
| Single-task idle removal | Independent edits already bind original 60Hz recordings, rather than cutting rendered videos | Reuse this layer; it does not cover every new requirement below |
| Factory output | Nine per-case simple/factory pairs match, default 10x/30fps | One case plays while other stations are static; this is not independent nine-station time skipping |
| Persistent visible jitter | Existing thresholds retain sufficient displacement/rotation without detecting prolonged no-progress oscillation | **Not yet sufficient** for the latest requirement; add semantic/phase evidence |
| Force evidence | Shared motion mainly stores qpos/appearance; actions include commands/force settings, not complete measured contact forces | qpos cannot establish “measured mechanical force is zero” |

Sources: `scripts/build_best5_dials.py`, R11 task/environment/public-task files,
`robofrontier/suite/{dial_feedback,evaluate,v2}.py`, `pipeline.py`, `run_setup.py`,
`prompts/common.md`, `prompts/roles/adaptive-controller.md`,
`.agents/skills/robot-collaboration/`, `motion_edit.py`, `factory_workstations.py`,
`scripts/replay_motion_in_factory.py`. Selected evidence starts at
`runs/oracle/dial-best5-recovery-20261026/batch-status.json`.

### 2.1 Old rules prone to misuse

The generic Dial builder in `suite/v2.py` still contains old 1/2/3,
quarter-turn and current CORRECT-count rules. The R11 builder overrides the nine
generated task texts; those texts are not all wrong. The risk is reintroducing
old rules during generation, run preparation or incorrect catalog selection.

Public R11 prose already states the 4-degree and 0.25s rules. Missing structured
completion does not mean GPT never received them. Establish checkable agreement
between public prose, structured parameters and evaluator instead of copying
another rule set that can drift.

Original `run_setup` freezes the task, roles, Skills and source, but does not
automatically turn recent engineering experience into a policy family guide.
File copying alone does not establish that every recent change is synchronized.

## 3. Family package: align facts before writing guidance

Proposed family-owned specification and per-case evidence index:

- `configs/task_families/dial/best5-r11.json`: nine IDs, catalog, source hashes,
  specification/evaluator versions, evidence references, programmatic/assisted
  flags and display speed. Secret combinations retain evaluator references only.
- `docs/tasks/dial-best5.md`: human-facing task/version documentation.
- `prompts/tasks/dial-best5.md`: policy family guide frozen into runs; not created here.
- Dial-owned check/preparation scripts/tests: consume this configuration instead
  of hardcoding nine cases in a shared launcher.

Check every case, rather than one representative:

| Area | Required agreement |
| --- | --- |
| Identity | case_id, 4/6/8 dials, L1/L2/L3, actual arm count, scene revision, asset/environment-logic hashes |
| Static geometry | Table height, actual outline/openings, dimensions, robot bases/orientations, workspace, camera calibration, scoreboard location |
| Mechanism | Fixed/free modules, L3 eccentric crank, dial/handle dimensions, local frames, allowed rotation |
| Input | Repeated 1..5 allowed; 0 invalid; 60 degrees per increment; negative angles reach 4/5; ±180 denotes the same symbol 3 |
| Feedback | BEST is the historical maximum over complete valid inputs, not current hits; READY has gray/yellow/green and brightness semantics |
| Settlement | Every dial remains within a nonzero tolerance band for 0.25s, all red handles genuinely grasped; intermediate motion configurations can settle automatically |
| Support | For L2/L3 another arm first establishes bilateral blue-handle support; entire module at least 20mm clear of external support; preserve qualification/loss timing |
| Success | One simultaneous complete correct input; distinguish success latching from continuing physics; unlocking does not erase process violations |
| Interface | READY capabilities, units, speed/force ranges, failed/unknown execution semantics; grasp inference is not measured object support |
| Observation | RGB, robot proprioception and permitted static specifications; no secret combination, per-dial correctness or live object truth |

`environment.tables` may be only a bounding description. One box does not
represent a ring table's hole. Derive specifications/diagrams from actual frozen
static table geometry. Public table/base specifications differ from precise
initial/live object coordinates; review the latter under the observation
protocol instead of exporting every private pose under “complete geometry.”

`nominal_robots` is a layout reference, not permanent ownership or the only legal
division of work. Actual red/blue separation, support and contact prerequisites
come from evaluator rules.

### 3.1 Permitted family guidance

Explain how to associate BEST/READY with visible inputs, preserve established
settings while testing alternatives, schedule concurrency around dependencies
and collisions, couple blue support with red operation, combine translation and
rotation for eccentric handles, and reassess grasp/open/retreat/regrasp after
failure using RGB and robot feedback.

Do not give policies private Oracle IK candidates, case-hardcoded coordinates,
optimal attempt sequences, answers, live object truth, BEST decoders or online
engineering repair channels. Register general tool/public-rule guidance
separately from authorized learning across runs. Do not inherit engineering
chats by default to increase success; this original chat contained combinations
and was particularly unsuitable as initial policy history.

## 4. Readiness registration and future GPT preparation

1. Pin nine evidence entries to selected reports, assets, evaluator, control and
   Oracle execution versions. Retain assisted eight-dial L3; identical physical
   control fingerprints do not imply identical Oracle source versions.
2. Compare each final package. Separate rule text, public static specifications,
   control/evaluator behavior and assets. Do not promote old commissioning flags
   such as `return_dynamics_verified=false` wholesale; a complete success does
   not verify every diagnostic capability.
3. Produce a family readiness sidecar identifying evidence for specific frozen
   inputs. Preserve original task/validation bytes and hash chains.
4. Put common readiness registration/validation/public-projection changes in
   section 5's merge list. Formal status follows integration; do not disguise
   new formal experiments as historical bounded probes.
5. Design a Dial preparation entry explicitly reading nine R11 cases and final
   shared configuration. Preview reviewable inputs before creating runs. Show
   the complete task/roles/Skills/camera images GPT will receive, not merely
   whether a source field exists.
6. Preparation starts neither physics nor inference; even preparation was out
   of scope in this original round. Later start a Controller with fresh context;
   legal runtime delegates inherit only permitted policy context.
7. Model, topology and cost/runtime budgets belong to the new protocol. Old
   1200s settings must not silently become defaults, nor should the Oracle's
   unlimited budget transfer automatically. Decide and freeze before launch.
   Display speed 10x changes neither real control speed nor the physical clock.

Reuse input/source hashing and common Skills in `run_setup`. If integration
changes shared control/evaluator behavior, analyze impact and run appropriate
focused checks. Display/documentation-only changes do not automatically require
all nine physical Oracles again; actual changes determine evidence needs.

## 5. Worktree ownership and shared merge list

Later family work should touch Dial modules, configuration, documentation and
tests. Shared proposals retain reason, interface, call sites, evidence,
acceptance and compatibility requirements; shared locations were out of scope.

| Shared area | Work proposed for integration |
| --- | --- |
| `suite/v2.py` / public task | Formal readiness; static specifications/structured rules; versioned old/new Dial rules |
| `run_setup.py` | Optional family guide/configuration loading/freezing and input preview; no family experience hardcoded into common prompts |
| `pipeline.py` / dispatcher | Formal readiness, observation boundaries and recovery compatibility only; no duplicated ownership/scheduling/tool semantics across branches |
| Common roles / Skills | Common responsibilities, tools, safety and evidence semantics; one family-guide entry, with content owned by families |
| Harness | Same physical capability; change only for verified discrepancies; task/READY geometry rather than copied fallback constants |
| Recording/editing core | One edit protocol, force/action/progress evidence sources, family profiles and old-file compatibility |
| Factory / renderer | Independent station cursors, batch pose updates before one render, materials/transforms and completion policy |
| Oracle base / recovery | Integrate Dial finalization/assistance needs with Transport and others by behavior, without whole-file overwrite |

### 5.1 Concrete existing conflicts

Committed differences from main included:

- Dial/Mosaic both changed `motion_edit.py`, `test_motion_edit.py`,
  `render_frontier_oracle.py`, `replay_motion_in_factory.py`.
- Dial/Relay both changed `motion_edit.py`, `test_motion_edit.py`, `factory_workstations.py`.
- Dial/Transport both changed `suite/oracle.py`, `render_frontier_oracle.py`.

The three edit APIs differed: Dial exposed `IdleSettings/build_edit/EditedMotion`,
Mosaic `build_timeline/MotionEdit`, Relay
`keep_intervals/select_source_rows/retained_timeline/video_rows`. This requires
protocol integration, beyond Git text-conflict resolution.

Suggested order: family specifications/evidence/shared requirements → one shared
recording/edit protocol → compatibility adapters for three existing products →
family profiles in family namespaces → unified replay/launch → minimum
cross-family checks → formal preparation. Preserve old recordings/edits;
interface unification alone does not require original Oracles to be rerun.

## 6. Independent time skipping across workstations

Each station i owns its original recording, edit, appearance cursor, transform
and display speed: `source_i = map_i(presentation_time)`. For output frame k:

```text
global_time = k / 30
for each workstation i:
    resolve source_frame_i / source_time_i from its own edit
    read original qpos and consume appearance events due in its source time
    apply fixed translation/yaw to the complete station
    update its visible objects
after all station updates, set the global display clock and render once
```

If A waits during original 10..30s and B during 15..20s, A skips its own 20s and
B its own 5s. Their subsequent source times differ. Do not cut a global video
interval or require every station to share one source simulation time.

`FactoryPlayback.apply` sets `data.time` to each case's source time. Separate
station source clocks from global display time so the last update does not
control the factory clock. Batch mocap/appearance updates before one FK/render,
rather than rendering the entire factory separately per station.

The frame index records global frame/time and each station's case, source run,
loop number, source frame/time, edit hash, completion state and skip reason.
Simple and Factory backgrounds consume the same edit; camera/material changes
do not reclassify it. Dial keeps default 10x/30fps; other families retain their
confirmed settings. No action, IK, contact or physics rerun, and no invented
interpolation across skipped segments.

### 6.1 Completion requires a display decision

Short tasks finish earlier and remain at their final pose. That differs from
unproductive mid-task waiting. Choose before implementation:

- Audit replay: play each station once, mark completion and hold the final state;
  continuous movement at every station cannot be promised.
- Continuous exhibition: independently loop short stations' effective segments,
  explicitly mark replay restarts and show completion at least once. Global
  duration may be the longest station's first completion. Loops do not represent
  physically continuous execution.

Continuous exhibition was recommended for “every table always working,” but
loops/duration had not been implemented or decided unilaterally. Preserve valid
support and completion events in either mode.

## 7. Persistent visible oscillation

Amplitude thresholds alone are insufficient. Increasing them can remove slow
real movement, spring return, falls or necessary corrections. A family classifier
should emit `active / idle / hold / settling / oscillating_without_progress /
unknown` display phases, changing only replay edits.

Combine at least these evidence groups:

1. **Effective command changes:** action starts/ends, actual TCP/joint/gripper
   target changes and execution progress. Repeated identical hold commands do
   not establish progress; an empty job does not establish absent holding force.
   An action interval can contain unproductive waits and is not all protected.
2. **Object motion:** windowed center/net displacement, genuine directional
   trends and oscillation amplitude/period around the same state. Remove the
   middle of prolonged no-progress oscillation while preserving cause, context
   and actual outcome. Slow drift is not automatically jitter.
3. **Task events:** new valid inputs, BEST, READY, red/blue support changes,
   detachment, failures, regrasp, violations, recovery and unlock. An unchanged
   BEST can accompany a meaningful new attempt; protect more than color changes.
   Keep event context or explicitly record omitted wait/source spans.

Analyze old `motion/events.jsonl`, `trace.jsonl`, `actions.json`, `process.jsonl`
and recovery records offline without physics. Private engineering evidence may
inform display classification without becoming GPT observation input. Mark
insufficient evidence unknown and apply an explicit conservative/manual policy;
an algorithmic usefulness judgment is not a physical measurement.

“No mechanical force” was interpreted as no useful drive or task progress.
Stationary airborne blue support may continuously exert force, so `force == 0`
is not a valid required condition. Recordings lack complete contact-force
telemetry, and commanded `force_n` is not measured load. A future measured-force/
mechanical-work criterion needs a separate read-only telemetry proposal with
sampling, units and sources; old data cannot supply invented force evidence.

## 8. Implementation order and acceptance

| Stage | Family deliverable | Integration dependency / acceptance |
| --- | --- | --- |
| A Facts | Nine case→specification→evidence entries and differences | No GPT launch; original hashes and assisted labels retained |
| B Guidance | Dial rules/static geometry, policy guide, read-only checks | Common roles/Skills unchanged; no combinations/privileged scripts |
| C Integration | Shared requirements and adapter proposals only | Unified readiness/projection/loading/edit protocol/station scheduling |
| D Without physics | Classify existing Dial recordings | Staggered two-station idle intervals, three edit types, feedback preserved, independent clocks, no `mj_step` |
| E Input preview | Inspect frozen public task/family guide/roles/Skills/READY per case | Fresh context, correct nine R11 cases, reviewed behavior agreement with evidence |
| F New experiment | Prepare/launch only after package/protocol confirmation | Small connectivity/observation check, then expansion under a separate protocol; not executed here |

Classifier acceptance includes small fast jitter, large prolonged no-progress
oscillation, very slow displacement, small effective finger closure, real falls,
spring return, necessary receiving/support waits, new inputs without BEST change,
READY changes, failure/recovery, unknown execution, unequal completion times and
loop restarts. A shorter video alone is insufficient.

Record task/rule consistency, policy information boundaries, original physics
evidence, edit classification and Factory pose/frame provenance separately.
Edited time and multi-table display cannot replace real duration or concurrency
measurements. Loop policy, GPT budgets and formal settings remained undecided.

## 9. Original stopping point

The original round ended with facts, gaps, branch ownership, shared merge work,
independent-time scheduling and prolonged-oscillation requirements documented.
It stopped at planning without automatically starting implementation or GPT
simulation. This historical scope does not pause current authorized integration.
