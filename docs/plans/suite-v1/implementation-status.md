# Historical 36-scene engineering progress and continuation entry

This is the original first-suite progress snapshot, not current unified-main
acceptance. See the [current ledger](../../development/unified-main.md) for later
results. At this stage, complete Oracle acceptance was still in progress.
The user authorized environment/physical Oracle work; **no GPT / Codex policy
sessions had started**. Previews, compilation and endpoint IK were not full-task passes.

## Scope and directories

- Specification: `plan.md`, `matrix.json`; 36-row index: `configs/suites/frontier-v1.json`.
- 4 families × 3 mechanisms × 3 paired scales: Transport 4/8/12 arms; Relay 8/12/16; Mosaic 4 arms 7×7, 6 arms 7×14, 8 arms 7×21; Dial 4/6/8 dials, fixed N arms and floating 2N arms.
- Resolve scene directories through `suite.scenes.case_directory(case)`; retain old versions in sibling `-vN` directories. Do not overwrite assets with successful physical witnesses.
- Generator: `robofrontier/suite/scenes.py`; rules/public projection: `tasks.py`; private process evaluation: `evaluate.py`.
- Shared restricted actions: `robot_control.PandaArm`; private references: `suite/oracle.py` and placement / relay / dial_oracle. References read truth but execute actual robot-driver command types only.
- Scripts: `build_frontier_suite.py`, `revise_frontier_scene.py`, `verify_frontier_suite.py`, `check_frontier_layouts.py`, `preview_frontier_suite.py`, `frontier_suite_gallery.py`, `render_frontier_oracle.py`.
- Append witnesses only under `runs/oracle/frontier-v1/<case>/seed-<seed>/attempt-*`. The intended final gate was complete witnesses and seeds 0/1/2 under one frozen version for every case; this was not yet achieved.

## Key corrections already implemented at that stage

- All 36 cases had passed initialization, settling and endpoint checks. New Dial/ring-Relay revisions still needed rechecking.
- Joint targets shared progress, acceleration scaling and velocity feedforward. Cartesian motion also used common scaling, limiting reference lead/integration. This fixed reachable vertical descent sweeping sideways through blocks; see `cartesian-retimed-reference-001.log`.
- IK contained only the arm's 7-joint chain, excluding objects. FK/Jacobians for all 4 families and rotated bases matched complete models to 1e-12. Isolated FK was about 5.7 times faster, without establishing equal full-simulation speedup.
- Grasp drive followed speed-limited approach → encoder-width stability → requested force establishment → hold. The 70 N cap, actual mass, friction and passive damping were not increased. **The earlier 20 kg transmission-inertia counterfactual was not adopted.**
- Position-gripper actions also checked each finger's position window. Failure/stop retained actual aperture instead of continuing old targets. Motion prechecks copied model/gripper history without mutating live drive state.
- The last complete regression had passed 299 tests; later focused drive/evaluation groups passed 14, 30 and 38. Latest full logs still needed inspection; old counts could not replace them.
- Executing-action overlap and actual joint-motion overlap were distinct, with holding recorded separately. Old `motion_overlap_sim_s` used active jobs and could not compare real parallelism.
- Asset identity included XML, referenced meshes/textures and task/environment contracts, with program sources independently snapshotted/hashed. Transactional index merging prevented late old results overwriting newer outcomes. XML-only old reports were development evidence.
- Generator material dependency ordering was fixed. An unordered resource sort had rewritten the old fixed-four-dial v2; original XML/contracts were restored byte-exactly from the frozen report before creating a new revision.

## Scenes and rules at that stage

- Transport v2 used four-corner supply/transfer support; paired pegs did not hit solid supports during quarter turns. Fixed holes/spring boards shared geometry; spring boards permitted Z compression and roll/pitch with damping/limits.
- Mosaic used 40 mm cubes, 51 mm pitch, 50 mm clear pockets, 1 mm walls and depth 1/3 block. Other levels had printed/no grid. Supplies stayed on the table at 80 mm pitch, reserving transfer space first.
- Mosaic references considered nonexclusive supplies, direct reachable transfers, later goal orientation, 24 equivalent cube orientations and direct joint paths before forced high planes. Hold/withdrawal used the task-surface normal, not a rotated cube's local Z.
- New neighbor-clearance calculations used known hand geometry. Transport slots allowed full opening before withdrawal to avoid dragging seated objects. These newest changes still needed complete rechecks.
- Relay 8/12-arm scenes restored previously demonstrated normal beam layouts. The 16-arm v3 used tangential beams, facing-pair lateral spacing 1 m and longitudinal offset 0.30 m. References allowed staged handoff with two valid grasps throughout, exploring receiver order/spacing; the full ring remained incomplete.
- Relay support counted only valid beam grasps, not grabbing weights/ropes. The full suspended assembly had to clear the table. Final completion required actual separation from all robot contacts.
- Latest Dial revisions: fixed 4/6/8 dials at 4/3/3; floating gears at 4/4/4; floating cranks at 5/4/4. All restored 2 ms steps. Gripper holding did not rely on altered inertia.
- **Dial feedback v2:** retain the same nonzero mark within 4° for 0.25 s, allowing small within-band vibration. Angular velocity was diagnostic only; an extra unrequested speed gate was removed. New rules required new witnesses, without relabeling old failures.
- The decoder used only its own inputs and currently visible total score, without unobserved historical scores. Half-turns could use either direction, targeting ±179.5°. All held inputs were continuously rechecked, not only changed dials.

## Positive development evidence and unresolved items

- The 4-arm pocket Mosaic had completed 49/49 at seed0 attempt027. Both flat levels had reached 40/49 before final approach/withdrawal-pose failure. Larger patterns still had path/supply-access issues.
- Old/current development Transport versions had complete passes for all levels at 4/8 arms and base/spring-board at 12 arms. The latest 12-arm base was attempt003; fixed paired holes still had occasional post-release shifts. PASS could not move across versions.
- Relay had complete development witnesses for all three 8-arm levels and 12-arm base/short-ring/rope. The 16-arm run reached its second handoff but failed sender exit.
- New-rule Dial had successes for fixed 4/6/8 and floating-gear 4 dials. A 4-dial floating-crank independent counterfactual completed, but still needed a canonical current witness. Floating 6/8 remained under recheck.
- `calibrate_dial_stiffness.py` ran independent counterfactuals with `passed` always false. `mechanical_passed`/complete goals were separate fields and **did not automatically promote the catalog**. Modes covered timestep, drive, dense-contact, full-task and retention.
- Retention had to distinguish airborne from qualified blue-handle grasp. `floating-current-driver-retention-001` stayed airborne for 60 s but H aperture reached 80 mm, without a valid grasp pass; an addendum recorded this. New tests separately measured qualified blue grasp while exploring deeper actual grasp points.

## Historical execution and closeout plan

- Inspect real processes/logs first: running processes used code imported at launch, without hot updates. Main batches were `dial-rule-v2-witnesses-001` and `dial-continuous-input-hold-001`, with newer geometry/hand-release/ring batches. Actual processes/reports were authoritative.
- `dial-frozen-three-seeds-001` had stopped, retaining partial NPZ and `dial-old-driver-stop.json`; it did not validate the current executor.
- Reference batches supported `--jobs`, `--record-hz 4/15` and cooperative parent SIGINT/SIGTERM, saving in-flight worlds and skipping unstarted cases. `cooperative-stop-smoke-001` checked this. Older batches without worker signal setup could print misleading final stop summaries; individual reports were authoritative. See `pool-cleanup-correction.json`.
- Final recording used `--record-hz 15`, rerendering actual saved states with sample-rate/speed captions, not re-simulating success. Synchronized front/rear outputs needed complete decoding. The 8-arm short-ring Relay had readable views under attempt002/video.
- Gallery: `docs/generated/frontier-suite/index.html`; historical local service: `http://127.0.0.1:56718/`. New revisions still needed updated previews/status; old images were not latest-version evidence.
- Do not declare 36-case completion before all pass. Remaining gates were complete current-version witnesses, three seeds, parameter/actual-contact audits, latest four-topology freeze/load, public projections, front/rear videos and an accurate 36-row status table.
- Future GPT needed a fresh Controller reading public role materials only. **Do not fork the research session into a policy:** it had read private Oracle state/control experience. Adaptive delegates should fork a clean policy Controller. Regenerate formal private codes and pair them across comparison instances, without Oracle's fixed random stream. Protocol isolation was not OS filesystem isolation.
