> Historical archive. See the [Transport task guide](../tasks/transport.md) for current specifications/status and [handoff](../plans/suite-v2/transport-merge-handoff.md) for integration. This preserves the original process and evidence.

# Implementation update: family R14 package and source edits completed

The user subsequently authorized implementation and half-size holes for GPT
physics. Family P0 source/physics selection, P1 package and P2 source-native edits
were implemented and checked. Shared C1—C5, multi-table drawing and formal GPT
execution remained integration work. Continuous post-completion display was
undecided; the interface held final state. See the [Transport task guide](../tasks/transport.md)
and [merge handoff](../plans/suite-v2/transport-merge-handoff.md). The original
planning snapshot below does not mean every listed item remained unimplemented.

# Transport: pre-GPT alignment, worktree ownership and multi-table Factory replay

Date: 2026-10-27. Original status: **read-only review and planning; proposed work
had not yet been implemented.**

“Worksheet” meant each task's Git worktree. This branch owned nine Transport
cases: four/eight/twelve arms × L1/L2/L3. Other families retained their owners;
this review read their interfaces/plans without editing files or taking over
experiments. No GPT run, inference/simulation, Oracle rerun, new video render or
branch merge was started. Existing implementations/evidence were preserved.

Baseline `90dd0c5`, main `d3e5916`, including previously uncommitted media changes.
Other worktrees changed during review; cross-branch findings are interface
snapshots, not final integration acceptance.

## 1. Conclusions and completion boundary

Original Transport physics goals were complete: nine independent full passes,
216/216, three frozen programs and six engineering-assisted recoveries. Videos,
idle-removed source indexes and single-table Factory mapping were delivered.

This does not establish:

1. GPT received final-Oracle-consistent instructions/environment/control/scoring;
   metadata and formal launch still had gaps.
2. Independent wait skipping and simultaneous replay of every workstation in one
   Factory frame; existing validation was single-station.

Build coherent versioned family public packages, with shared integration once.
Factory reads existing trajectories without recomputing actions, IK or contacts.
Each table compresses its own waits; its arms/objects remain synchronized. Update
all tables before drawing one frame.

## 2. Read-only findings

| Area | Verified fact | Next stage |
| --- | --- | --- |
| Evidence | Nine independent full passes, three programmatic/six assisted; actual failures/timing retained | Per-case evidence index; no claim of nine autonomous cases or one executor version |
| Scene entry | Family catalog selects nine R13 cases; generated scenes match selected successful sources | Select family catalog explicitly, not guessed global/latest versions |
| Rules/environment | R13 boards, target spacing, order graphics and arbitrary handoff/table buffering already in rules/mechanism | Preserve correct content; complete checks/guide |
| Readiness | Tasks still `environment_preview_only`, `oracle_verified=false`; catalog says no Oracle | Version-bound sidecars, preserving frozen files rather than mass true edits |
| Documentation | `docs/frontier-v2-environments.md`, initial R13/worktree docs still say incomplete | Mark history and link current evidence/specification |
| Public projection | `v2.public_task` has rules/mechanism/orders/arms, lacks independent table geometry/height, structured completion/workspace | Add necessary static specs/success conditions; READY is actual command range; no private live truth |
| Workspace | `World.tcp_command_bounds` prefers task `workspace_world_m`, otherwise old harness fallback | Verify actual resolution rather than changing common harness based on fallback height |
| Control/scoring | All control fingerprints `ac85b406…3479`, environment logic `cd615e0b…135b`; effective harnesses match servo2 JSON, finger servo `pd1000-v1` | Preserve baseline; record new integration fingerprints/compatibility |
| Formal gate | `validate_task` accepts preview/explicit bounded probes; `World.start_trial` rejects preview | Integrate formal readiness without disguised probes/bypass |
| Old GPT batch | `prepare_policy_minimum_batch.py` fixes R10, minimum family/level scale and 1200s probe | New family package; common launch wiring during integration |
| Prompt/Skill | Common roles, tools, observation and concurrency/handoffs exist; no Transport guide loading point | Family materials plus one shared loading hook |
| Center hole | Half-hole only in render model; original physical R13/collision/GPT entry unchanged | Decide GPT physics separately; render default is not physical default |
| Idle data | Nine 60Hz source keep/index maps, hashes/default references; rerenders skip source states directly | Preserve/adapt without repeated detection per background or full render first |
| Multi-table | `replay_motion_in_factory.py` reads one recording; `FactoryPlayback.apply` writes shared `data.time` from that source | Add independent source/global display clocks |
| General jitter | Reviewed isolated rattle removed; added large-rattle check covers free bodies, arms still about ≥8s, bounded envelope with amplitude/trend limits | Does not cover arbitrary amplitude/passive-joint oscillation; add semantics/review |

Use persistent `COMPLETION.md`, complete per-case `report.json` and motion/source,
not stale catalog status, to establish the nine trials' exact outcomes.

## 3. Family package consistency

Check every case rather than substituting four-arm L1 for the other eight.
Generate public documentation from one family specification with differences,
not several handwritten rule/dimension copies. Original proposed paths:

- `configs/task_families/transport/r13-qualified.json`: nine sources/versions,
  evidence, controls and physics/display variants.
- `docs/tasks/transport.md`: human task/status guide.
- `prompts/tasks/transport.md`: allowed GPT guidance, later frozen as reference.
- Dedicated package/check scripts and tests: no GPT launch or common launcher edits.

| Area | Facts to align |
| --- | --- |
| Identity/count | 4/8/12 arms, 12/24/36 objects, three levels, case ID, scene/rule/evaluator/control versions |
| Table/layout | Height 0.8m, outer side 1.938/2.720/3.536m; solid four-arm table, center holes for eight/twelve; bases/yaws/boards/workspace; ring bounding box is not support surface |
| Board/targets | R13 board 143×396mm, target spacing 120mm, color/shape marks 84mm, gaps 36mm; board/support 50mm outward from R10; use frozen positions |
| Objects/orders | 60mm cubes or cylinders of diameter/height 60mm; source identity/color/shape per order; source IDs are not exclusive robot ownership |
| Insertion | Two tabs 2.5×12×24mm, spacing 24mm; real blind slots 4.5×15mm, depth 26mm, board thickness 32mm; distinguish slots from center table hole |
| Levels | L1 stable released placement; L2 real bilateral insertion/seating/release on fixed board; L3 same sockets on passive z/roll/pitch spring board with moving local target frame |
| Cooperation | Direct airborne handoff, stable table buffering or waiting; no fixed buffer box/route/pair; establish receiving support before release; parallel independent work |
| Scoring | Source identity/pose/full occupancy/two tabs, board/object stability, no gripper contact, continuous 1s and process compliance map to evaluator; 84mm mark is not an 84mm acceptance area |
| Actions/observation | READY tools/bounds; Cartesian/joint targets, aperture/force, known failure versus unknown execution; RGB/proprioception, not grasp inference as support truth |
| Recovery/efficiency | Recover from observed state; weigh avoidable table regrasp/handoffs against parallel duration; no universal rewind/solver-snapshot resume |

Details: `suite/evaluate.py::sample_goals` and
`evaluate_v2.py::placement_candidates`. L1 checks full occupancy; L2/L3 check real
tab envelopes, depth/seating in current board coordinates. “On the board” or a
larger mark does not mean pass. Project/test tolerances from this contract
without inventing broader standards.

### 3.1 Permitted GPT guidance

Allow rules, public dimensions/calibration, frames, support-before-release,
continuous feasibility through grasp/reorientation/receiving/insertion, and
observation-based reassignment/concurrency. Exclude private candidate graphs,
grasps, object poses, QP results, shortest routes, recovery inboxes, support/
contact truth and traces. Oracle measured 20mm lift/contact checks are not extra
policy feedback or a fixed answer recipe. GPT can plan its own lift and judge
through permitted RGB/proprioception.

`check_motion` is bounded-horizon inter-robot geometry screening, default 2cm,
with an unmodifiable request threshold and no held-object/table truth. Its
conservative rejection does not prove physical impossibility; the Oracle's
private loaded-scene screen must not be disguised as a policy tool. Propose any
new common capability separately.

## 4. Separate half-hole physics from display

Existing display default: eight-arm hole 0.952→0.476m, twelve-arm 1.666→0.833m,
half in both dimensions; outer dimensions, height, legs, robots/objects unchanged.
Original physics and passing evidence were unchanged. Geometric checks covered
1,998,263 saved states over six holed scenes without new contact. This is pose
compatibility, not full execution in the new physics scene.

Before GPT, register separately:

- Same-physics comparison: original frozen R13 physics; half-hole is display-only.
- Approved half-hole GPT physics: new family scene/variant, actual collision
  geometry, environment/task/public specs/previews/hashes, existing control and
  scoring contract. Check initial/source compatibility, then affected physical
  grasp/handoff/insertion behavior. Complete new-environment claims need complete
  corresponding physics evidence; do not relabel old PASS.

This original round did not select physics for the user, alter successful sources
or restart old worlds. Later authorization is recorded above.

## 5. Ownership

| Family-local preparation | Shared integration requirements only |
| --- | --- |
| Environments/catalog/rules/docs/reference/prompt/checks/tests/evidence | Global catalog, public projection/validation/loading, formal readiness |
| Geometry variants/evidence, jitter labels/selections/adapters | Harness, `pipeline`, control, `run_setup`, tools/lifecycle |
| Public/private Oracle boundary checks | Common roles, `prompts/common.md`, Skill root |
| Per-case retained windows/source mappings | Recording/edit protocol, unified FactoryPlayback, multi-table/display clock |

Register/preserve existing shared changes rather than reverting history to claim
family-only work. Future work follows ownership; four owners should not each
change a shared launcher/Skill root.

### 5.1 Merge risks

- Transport/Dial both touch `suite/oracle.py`; Transport/Dial/Mosaic touch
  `scripts/render_frontier_oracle.py`, plus intersecting replay/recording changes.
- Dial/Mosaic differ in `robofrontier/motion_edit.py`; Transport uses
  `motion_timeline.py`. All may claim `robofrontier.motion-edit.v1` despite
  different fields/semantics.
- Relay was migrating shared code to `relay_motion_edit.py`, including deletes,
  renames and uncommitted work. Recollect actual files/handoffs rather than only
  HEAD or old plans.
- Global builder/projection/scoring/control fingerprints can conflict semantically
  even after a clean Git merge.

Owners should provide catalogs, per-case evidence, local patches, shared diffs,
old-format notes, uncommitted/untracked files and test results. One integrator
merges by behavior with provenance/version retention, without whole-file
ours/theirs or bulk cherry-picks of other families here.

## 6. Shared work proposed for integration

C1—C5 align with other family proposals; all were plans at this checkpoint.

| ID | Work | Acceptance |
| --- | --- | --- |
| C1 | Public projection/freezing/loading | Actual run receives correct family reference; common roles/Skill supply general pointers; no other-family overwrite/private Oracle data |
| C2 | Formal readiness/evidence binding | Separate scene/rule/evaluator/control/package evidence; legal formal loading, rejection of preview/wrong sources; no historical-probe authorization reuse |
| C3 | Source-index edit protocol/adapters | Producer/version, units/clocks, interval endpoints, source frames/times/hashes, keep/drop reasons and precision; same v1 label is insufficient |
| C4 | Independent tables, rigid mapping, one render | Different source seconds in one frame, table-local sync/wait removal, correct cut events, explicit completion and frame provenance |
| C5 | Runtime/observation/concurrency/recording regression and formal batch settings | Common baseline/READY/error semantics, explicit model/effort/topology/budget; no inherited 1200s probe/Oracle limit; display speed does not change efficiency |

Shared wiring can change file fingerprints. Record old/new hashes and reviewed
compatibility/tests, without fabricating old hashes or silently inheriting
qualification across changed rules/controls. Validate actual incompatible changes.

## 7. Previous idle-removal delivery

- Full 60Hz sources preserved; nine JSON+NPZ edits/default trial references.
- 2,131,885 source states; 1,143,461 retained, 988,424 removed; about 7.6MB new NPZ.
- Direct retained-source rerendering, without first rendering the entire Factory;
  color events restored by source time.
- Reviewed idle/isolated rattle removed; any useful arm/finger/object motion
  protects the complete synchronized table.
- Single-table rigid mapping/half-hole checks; 288 sampled states across nine
  cases match source FK after additional translation/yaw.
- 18 front/rear simple videos, 20x/30fps; full Factory/multi-table video
  batch remained ungenerated.

The timeline conservatively expands source-state cells represented by reviewed
video samples back to 60Hz. Cuts still depend on original review sampling/margins,
not independent decisions on every source frame. Current classification uses old
manifests/videos; future recordings need direct source selection without an
existing-video prerequisite. Preserve checked selections across background changes.

## 8. Multi-table clocks and frames

For global video time T, table i has effective e_i, source s_i, keep indexes and
speed v_i. Compute `e_i = v_i * T`, then `source_i(e_i)` independently. Transport
uses 20x/30fps; other families use approved defaults unless integration explicitly
changes them.

If A waits at 10..30s and B at 15..20s, A skips 20s and B 5s. One Factory frame
may represent A at 40s, B at 25s. Removing A's wait does not remove B's actions.

**Motion OR applies within one table.** No factory-wide mask or independently
cut arms, which would destroy support, handoffs and coupled mechanisms.

For every output frame:

1. Resolve each table's source frame without interpolation across cuts or physics.
2. Restore appearance/score events through s_i, including events inside skips.
3. FK with exact frozen model; rigidly translate/yaw table, bases, arms, objects,
   mechanisms and targets together. Background/material/camera changes do not
   trigger reclassification.
4. Write all mocap/appearance, update global FK/camera and render once. Shared
   data.time is display time; retain each s_i separately.
5. Record global frame/time → case/source run/frame/time/effective time/edit hash/
   interval/completion, plus loop number if applicable.

Compose the Factory from exact source versions, not old v6 stations with changed
joints/geometry. Absolute relocation/material changes preserve relative geometry;
independent robot relocation, arbitrary objects or scaling are not qualified.

### 8.1 Completion is different from waiting

A single audit replay can hold exact final states, mark completion and end when
the longest finishes; it cannot promise continuous motion at every table.

Continuous exhibition would need explicit independently labeled loops, one shown
completion and loop IDs. Restart is a display transition, not continuous physics.
The original round did not choose loops or conceal restarts, discard final states
or slow shorter tasks to create an illusion of constant work.

## 9. General no-progress jitter

Interpret “no mechanical force” as no useful execution/progress, not measured zero
contact force. Existing qpos/action/appearance lacks full measured force series;
static grasping exerts force. Do not add hidden GPT sensors for offline editing.

Label whole-table source intervals once:

| Interval | Display treatment |
| --- | --- |
| Useful arm/finger operation, directed object movement, useful rotation | Preserve complete table synchronization |
| Real release/fall/landing/slip/lost support/recovery/mechanism/completion change | Preserve process/boundaries; do not hide failure for smoothness |
| No useful operation/phase/goal/contact progress, prolonged bounded back-and-forth near one state | Remove as waiting even with visible amplitude; displacement/action ID/force setting alone does not protect it |
| Uncertain/brief transition | Review logs/representative images, without one broad amplitude threshold |

Combine short/long windows, net displacement/path length, reversals/period,
envelope/duration, actual results and phase. Cover free bodies, passive hinges/
spring boards and servo oscillation, not cylinders only. Include duration
boundaries, visible amplitude, another active arm, genuine falls without arm
motion and slow transport.

Transport already had 16/64s trend and ≥8s rattle checks, but 6cm/π envelope caps;
free-body checks do not cover every passive joint. Find uncovered examples, keep
new labels family-local and shared consumption in C3. Relabel original 60Hz if
needed, **without physics reruns**. Representative images are one-time review,
not a full-video prerequisite or repeated detection after material changes.

Qualification/stability durations use original time. Display may compress waits
while preserving events/source times/completion; do not rescore edited time or
claim actual execution became faster.

## 10. Implementation order and completion

| Stage | Work | Acceptance |
| --- | --- | --- |
| P0 | Final owner sources/evidence/local changes; Transport hole/completion choices | No guessed latest; physical/display versions separate; unresolved choices recorded |
| P1 | Family specs/docs/public draft/reference/checks | Nine cases align in boards/slots/orders/poses/stability; no private recipes |
| P2 | Source-native jitter labels/selections/adapters | Remove idle/long visible no-progress oscillation; preserve cooperation/falls/recovery; no full-render prerequisite |
| P3 | Shared C1—C3 and needed runtime wiring | Adapt/reject old formats correctly, correct frozen inputs, formal gates bound to source/rules/controls |
| P4 | C4: staggered two tables, then nine Transport, then all families | Different source times, synchronized tables, correct events/end/loop policy, traceable 20x30fps |
| P5 | C5/final preparation | Shared/observation/variant checks and explicit model/budget/topology; reviewable prepared package, GPT only after user launch authorization |

Read required states, cache chunks/joint/body maps, batch FK/transforms; avoid
per-frame full JSON rebuilds, repeated NPZ decompression or per-table full-factory
renders. Version thresholds/labels. Start with two short examples, not 36 long
videos. Planning completion meant recorded differences, ownership, work,
acceptance and gaps, not implemented readiness/playback.

## 11. Evidence and handoff entries

- Historical local artifact (not distributed): `runs/oracle/transport-continuation-20261026/COMPLETION.md`
- Historical local artifact (not distributed): `runs/oracle/transport-continuation-20261026/20X_VIDEO_HANDOFF.md`
- Historical local artifact (not distributed): `runs/oracle/transport-continuation-20261026/motion-timelines/README.md`
- [Original worktree scope](transport-worktree-oracle.md) and [execution history](transport-continuation.md); historical incompleteness does not override latest evidence.
- Other owners' read-only references: [Dial plan](dial-gpt-preparation-plan-20261027.md), [Relay plan](relay-gpt-readiness-and-factory-parallel-plan-20261027.md). Recollect changing docs/uncommitted code before integration.
