# Post-Oracle Relay alignment and multi-table Factory replay plan

Date: 2026-10-27. Original status: **review/planning only; not implemented and no
GPT simulation started.** This historical scope does not pause later authorized
integration; see [unified main](../development/unified-main.md) for current status.

The original round added only this plan: no runtime/task/Prompt/Skill/harness
changes, other-worktree operations, branch merges, Oracle reruns or new videos.
Requirements and acceptance below describe future work at that checkpoint.

## 1. User intent and ownership

“Worksheet” meant task-specific Git worktrees. `codex/relay-continuation` owned
nine Relay tasks; Transport/Mosaic/Dial retained their worktrees. Other interfaces
and docs were read only, without taking over tasks.

Future GPT tasks, physics, tools and scoring must agree. Engineering-assisted
Oracle completion does not establish a ready formal GPT entry. Each family owns
its environment/rules/docs/references/evaluation; common harness, lifecycle,
tools, loaders, Prompt/Skill and joint Factory playback are integration requests.

“All Oracles running together” means **simultaneous replay of existing Oracle
recordings**, not 36 reruns or a new concurrent physical experiment.

The user selected **hold each table's final state after playback**, without loops
or resets. Completion labels/other UI were not requested and are not mandatory.

## 2. Verified status

### 2.1 Nine Relay cases

- User-rule evidence covers 9/9 cases and 27/27 timbers. Old native reports/scores
  remain unchanged, not rewritten as new-rule passes.
- L1 catalogs: 8-arm R13, 12-arm R15, 16-arm R13. Preserve L1 apparatus/layout.
- Six L2/L3 entries select R17 prose with R16 physics; all nine exported scene
  SHA256 values match current sources.
- 8/12-arm L2/L3 initial endpoint span 1.15m; 16-arm 1.20m, 16-arm opposing
  radial separation 1.40m.
- L2 arc turn 63°; L3 manufactured bend 31.5°, internal angle 148.5°; each reduces
  its early shape angle by 30%.
- L2/L3 underside rings attach directly 100mm from the main timber end, with no
  connecting post. Same 170mm wooden pendulum and 600g weight; all L3 use
  out_of_plane passive elastic joints limited to ±25°.
- Table height 0.80m; derive outlines/bases/regions from each frozen source
  instead of copying old documentation.

### 2.2 GPT inputs remained inconsistent

| Area | Finding | Follow-up |
| --- | --- | --- |
| Nine Relay entries in `configs/suites/frontier-v2.json` | All `environment_preview_only`, `oracle_verified=false` | Explicit readiness/evidence binding, not mass flag changes |
| `task.json` / public task | Still says stable, fully inside, stable for 1 second | New semantics matching final user rules |
| R17 near-table release | `max_timber_release_gap_m=.020`, prose measures lowest timber | Align user rules and engineering release definitions |
| Engineering Goal policy | 50mm boundary tolerance, entire apparatus's lowest component near-table value 30mm | Basis for review, not automatically an extra GPT constraint |
| Native evaluation | About 2mm inside tolerance, speed threshold/continuous 1 second, stricter support | New family evaluator; preserve old reports |
| User endpoint review | 50mm, real release/landing or permitted stacking, real handoffs; no speed/dwell gate | Versioned new-contract basis and separate evidence |
| Static geometry | arms/mechanism/route_regions, no complete common table_geometry block | Derive missing permitted dimensions from frozen source |
| Preparation | Copies common/role Prompt and robot-collaboration Skill; no family loading point | Self-contained required family rules first; common loading proposed for integration |

Sources: `robofrontier/suite/relay_goal_release.py`, `relay_user_goal_policy.py`,
Relay in `evaluate_v2.py`, `scripts/check_relay_user_goal.py`,
`robofrontier/suite/v2.py:task_for/public_task/validate_task`, `run_setup.py`, `pipeline.py`.

READY already prefers task `workspace_world_m` and reports installed aperture,
bases and tools. Old harness workspace_z fallback alone does not establish actual
limits. Check loaded model, task bounds and READY without changing global defaults.

### 2.3 Other families, read only

| Family | Existing family input | Owner handoff needed |
| --- | --- | --- |
| Transport | `frontier-transport-r13.json`; airborne handoff/safe table buffering, no fixed transfer box | Nine final sources, boards/tabs/identity rules, evidence and GPT-visible guide |
| Mosaic | `frontier-mosaic-r13.json`; separate edit format/Factory relocation | Final patterns/grid/colors/inventory/acceptance version and exact source/frame maps |
| Dial | `dial-best5-r11.json`; 1..5, 60°, historical BEST | BEST/qualification rules, observations, final sources and blind decoding; private combinations |

Do not infer latest inputs from every `frontier-v2.json`: Mosaic/Dial still held
R10 there, while family catalogs selected new versions. Dial IDs also changed to
`dial-best5-*`. This review did not requalify other families or treat old planning
incompleteness as current status.

## 3. Next stage: Relay-owned alignment

### R1: authoritative nine-case manifest

Bind case ID, source, scene/asset/task hashes, control fingerprint, rules,
recording prefix/completion time, evidence and privileged-assisted class.
Preserve mixed geometry provenance without rebuilding L1 just for uniform labels.
Separate environment, rules, executor and media-edit versions.

### R2: one final user-rule contract

1. All apparatus reaches GOAL; arbitrary legal arrangements/contact/stacking,
   without Oracle template centers or mandatory timber separation.
2. Boundary tolerance 50mm; define full apparatus envelope in GOAL coordinates.
3. Actual release, no arm support, resting on table or permitted cargo support
   chains. No extra stationary duration/speed gate; opening above GOAL alone is
   not immediate completion.
4. Low release may begin before table contact; timber and weight need not both
   touch first. Define lowest component versus timber, legal support surface
   and distance to resolve 20/30mm mismatch. Current engineering 30mm is a
   candidate value, not a precise quotation from the user.
5. Real qualified airborne handoffs, receiving support before sender release;
   explicit bilateral support/process-violation rules.
6. Permitted recovery, retained violations and no rollback/respawn; a particular
   Oracle recovery route is not mandatory.

Generate task.json, public task, Chinese/English documentation, evaluator
parameters and positive/negative examples from that contract. Parameter changes
create new task semantics without rewriting frozen inputs. Shared Relay wiring
belongs to integration, not repeated shared-file edits in each worktree.

### R3: task, family reference and Skill responsibilities

- Task: apparatus dimensions, static tables/bases/regions, goals, allowed contact,
  handoff and endpoint criteria.
- Family reference: public mechanisms/tool semantics, such as L3 joint frames,
  possible finger support after opening and completion versus retreat. No
  private contacts, Oracle grasps or recorded answers.
- Common Prompt/Skill: planning/concurrency/evidence/roles/recovery; retain
  existing principles instead of rewriting everything for one Relay example.
- Family docs/references may be prepared locally; common loading integrates once.
  Until then required rules must be self-contained in the actual public task path.

### R4: verify policy capabilities rather than copy Oracle privileges

Inventory TCP/rotation/joint motion, aperture/force grasp, concurrent batch, RGB
and proprioception. Check that short empty-hand exits, reorientation, two-arm
transport and handoffs are expressible. Oracle poses/contact graphs/private
search/hot loading are not GPT tools, and assistance does not prove equivalent
policy capabilities. Propose missing generic tools with observation boundaries.

### R5: preparation checks without GPT execution

Check nine source identities, contract/public agreement, boundary/support/release
examples, static READY across arm counts, and no Oracle trajectories/private
truth in public packages. Read-only reevaluation distinguishes user acceptance,
old native outcomes and engineering assistance. Shared recognition of readiness
belongs to C2, beyond changing `oracle_verified`. GPT experiments follow completed
alignment/wiring/regression and separate explicit launch authorization.

## 4. Worktree boundaries and integration

| Family-local preparation | Shared integration only |
| --- | --- |
| Relay environments/tasks/contract/docs/helpers/tests/catalog | Global catalog, public projection/loading/readiness |
| Equivalent handoffs from other owners | `pipeline`, `robot_control`, run_setup, lifecycle/tools, Prompt/Skill |
| Authentic sources/evidence/family edit decisions | Common trajectory format, multi-table playback, metrics/display clock |

Observed overlaps:

- Relay/Mosaic add different `robofrontier/motion_edit.py` and `tests/test_motion_edit.py`.
- Both say `robofrontier.motion-edit.v1`; Relay is a complete derived recording,
  Mosaic a JSON selection referencing originals. Schema text alone is insufficient.
- Transport/Dial change `suite/oracle.py`.
- Transport/Mosaic/Dial change `scripts/render_frontier_oracle.py`.
- Smaller overlaps include `.gitignore`.

Preserve existing changes/evidence without rollback/migration/cherry-picks here.
Collect four handoffs/frozen baselines, separate local patches/shared proposals,
and assign one integrator per common entry. Merge actual semantics/interfaces,
not whole-file ours/theirs. Check formats/rules/source bindings/clocks even when
Git reports no conflict.

### Shared requests

| ID | Request | Acceptance |
| --- | --- | --- |
| C1 | Family public projection/loading | Actual GPT context has latest family guide without other-family overwrite |
| C2 | Formal readiness/rule/physics/control/evidence binding | New semantics load legally; old preview/reports are not silently relabeled passes |
| C3 | Common edit format and two legacy adapters | Distinguish same-name formats, preserve source frames/times/hashes/cuts, reject misreads |
| C4 | Independent tables and one composition | Different source seconds per output frame, hold final, no global post-cut |
| C5 | Runtime/observation/concurrency/recording regression | Same frozen baseline, consistent actions/unknowns/failure histories |

No new common harness/global budget here. Action timeout, coordination lease and
experiment duration differ; old 20-minute probes do not define formal GPT budgets.
Media speed/wait removal changes display, not actual execution costs/statistics.

## 5. Previous edit delivery and gaps

**Delivered:** nine separate idle-removed 60Hz recordings, source/edited times and
original frames, exact frozen models, appearance events and hashes. Nine simple
and nine Factory videos share selections, 30fps/20x. Originals unchanged; material
or common rigid placement does not require repeated motion detection.

**Missing:**

1. `render_all` calls `render_case` serially, advancing one table per video. A
   nine-table Factory or nine videos is not simultaneous nine-table playback.
2. Only nine Relay cases delivered, not unified edits for 27 other-family cases.
3. Small numerical jitter/isolated weight sway is removed, but larger timber/L3
   passive motion can keep triggering retention. Prolonged visible no-progress
   oscillation is not reliably excluded; displacement alone is not usefulness.

Read-only screening of existing 20Hz masks found 153 intervals of about ≥3 seconds
without useful arm movement but retained timber/large-weight motion, including
47 in 16-arm L3. These are review candidates, not 153 approved cuts; falls,
release, slip or recovery may be meaningful.

## 6. Correct multi-table clocks

Table i owns source s_i, effective e_i, state Q_i and appearance events. At video
time T, use its approved speed v_i and `e_i = min(v_i × T, L_i)`, then
`source_time_i(e_i)`. Relay v_i=20; other families keep approved settings rather
than inheriting Relay defaults. L_i is effective duration; then hold the original
completed final pose. End when the longest finishes; completion hold is not waiting.

One frame may contain A at source second 10, B at 300 and completed C. Removing
A's 100-second wait does not remove B's 100 seconds of useful work. Retiming is
between tables; all arms/objects within a table share source time to preserve
support/handoffs.

Each output frame:

1. Resolve original state from each edited clock, without cut interpolation/physics.
2. Apply events through source time, including skipped intervals.
3. FK with exact source model, then rigidly translate/yaw table/bases/links/objects.
4. Update every table, then render once.
5. Record `global_frame → edited_time/source_time/source_frame/segment/ended` per table.

For four families/36 tables, owners supply selections/sources; do not guess latest
paths or mix old R10 stations with new recordings. No need for 36 full renders first.

## 7. Additional no-progress oscillation classification

Use layered interval evidence beyond amplitude:

- **Useful active motion:** genuine arm/finger action/progress protects the table;
  commands alone or an action ID do not protect prolonged no-progress servo jitter.
- **Meaningful passive process:** release/fall/landing/slip/support/mechanism
  transitions retain context/process even with stationary arms.
- **No-progress passive oscillation:** no useful arm activity/new task/contact/phase
  facts, bounded return near one state over several seconds; candidate waiting
  even when weight/timber/spring amplitudes are visible.
- **Uncertain:** inspect original logs/images; never hide failure to satisfy editing.

Combine short/long-window net progress, path length, cycles, envelope/duration,
actual action outcomes and events. Version thresholds; review the 153 candidates
and representative normal windows. No useful arm motion does not mean zero
contact force; static holding exerts force, force alone does not imply motion,
and stationary arms do not justify cutting a real fall. Engineering labels do
not add hidden contact sensors to GPT.

Classify once at original-recording level with background-independent reasons/
intervals. Images may inform one review, not mandatory redetection for every
material/camera. Preserve original qualification/handoff overlap/failure/recovery
times; edited duration cannot rescore tasks or imply actual speedup.

## 8. Performance and acceptance order

1. Authoritative sources/contracts from all owners; Relay first in this worktree.
2. Local consistency/endpoint examples without GPT or rerunning completed Oracles.
3. Shared C1—C3 and legacy adapters, avoiding repeated full decode/copy.
4. C4 clocks, update all states then one render; load required states only,
   cache joint/body maps/chunks, vectorize FK/transforms, no per-frame full JSON/IK.
5. Two staggered unequal-duration tables with large useless sway → nine Relay →
   36 integrated tables; no stretching, loops or cut smoothing to invent continuity.
6. Correct source states/events, remove useless sway, preserve falls/handoffs,
   exact final hold, per-table speed/common 30fps/maps, reusable full decoding.
7. Shared regression, public-boundary/readiness checks, then separate GPT launch.

The original result was this plan. R1—R5, C1—C5 and joint rendering remained work.
Nine independent reusable edits did not establish joint playback or generalized
no-progress removal. Later implementation status belongs to the current ledger.
