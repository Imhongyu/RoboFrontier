# RoboFrontier four-family environment and Oracle expansion plan

Date: 2026-10-24 (Asia/Hong_Kong). Historical specification/implementation plan,
not evidence that the following 36 configurations were generated or passed.
GPT experiments were stopped at this checkpoint; environments, frozen inputs,
Oracles and model runs were preserved. These historical dimensions and rules
are not current defaults; see the [integration ledger](../../development/unified-main.md).

## 1. Initial scope: 36 configurations

Each family combines 3 mechanism levels × 3 scales, 9 cases; four families total
36. The user paired Mosaic arm counts with dimensions, rather than a full cross
product. 12-dial tasks were excluded for now.

| Family | Level 1 | Level 2 | Level 3 | Scale |
| --- | --- | --- | --- | --- |
| Transport | Cube pick/place/handoff | Two-peg cubes into fixed socket boards | Same pegs into centrally spring-supported boards | 4/8/12 arms, initially 3 objects each, 12/24/36 objects |
| Airborne Relay | Original timber | Weight on short rings at one end | Same weight on flexible cord at same end | 8/12/16 arms, 4/6/8 facing pairs |
| Rocket Mosaic | Physical pockets | Painted grid | No table grid | 4 arms 7×7, 6 arms 7×14, 8 arms 7×21; 49/98/147 blocks |
| Dial combination lock | Fixed white dial/red gear knob | Lift blue support/turn red gear | Lift blue support/turn red eccentric crank | 4/6/8 dials; level 1 uses 4/6/8 arms, levels 2/3 use 8/12/16 |

Scale increases workload and sometimes route complexity; it measures system
scaling, not an arm-count-only causal ablation. Comparisons of single/hierarchical/
peer/adaptive within one case use identical scenes/goals/initial states/physics.
A fixed-workload arm-count control would be a separate study outside these 36.

Dial scale is 4/6/8 dials, fixed N arms versus airborne 2N. These are nine
combinations on two axes, not identical arm counts at every level. Single means
one Agent controls all physical arms, without reducing them or forcing serial work.

Families cover logistics/resources, continuous shared load/handoffs, spatial
assembly/protecting completed work, and partial-information feedback puzzles/state
holding. Do not invent external approval rituals to force communication.

Increasing difficulty is a design aim, not an empirical conclusion from labels.
Engineering verifies meaningful new constraints and complete solvability; model
pilots measure difficulty. Better poses/order/concurrency may reduce constraints:
loading symmetrically, orienting support for crank clearance, or smooth transport
reducing sway are desired planning abilities, not loopholes to forbid.

## 2. Dial family

Fixed layouts: 4 dials in two rows/two columns; 6 in three rows/two columns per
user correction; 8 as 3×3 without center, rows 3–2–3. Arms operate from the
perimeter without a center robot obscuring the scene.

Airborne: 4 retain four straight groups at 70cm spacing; 6 begin with two rows/
three columns of modules, each with facing arms and full base/arm clearance
between middle robots; 8 use a ring with arms inside/outside each module. Set
radius from inner-base clearance, reach and full trajectories, not a copied70cm
arc length. Mark unproven motion unqualified; successful rendering is insufficient.

Secret symbols only 1/2/3, repeats allowed; existing 0/1/2/3 and white-dial-relative
angle semantics unchanged. Candidate counts for 4/6/8 are 81/729/6561, not required
attempt counts. Feedback shows only total correct, dash if any invalid input;
panel expands to00–08 with explicit total dials. Airborne support/clearance must
precede red-part contact.

Check prolonged zero rest, eccentric gravity, both directions/half-turn reach,
continuous support, exit and spring return. Prior60cm Oracle proves one path only;
70cm, additional modules/new layouts need checks. Preserve failed in-place opening;
not every opening pose is promised. If zero drifts, compare real counterweights/
passive springs during engineering, freeze/publicize apparatus; no live parameter
or angle changes in model trials.

Audit first red contact, sustained operation, support loss/reestablishment and
resumed operation. Distinguish passive return from continued robot driving;
define numeric tolerances/rules first. Separate public scene seed from private
combination generation; filenames/public seeds must not reveal combinations.

## 3. Transport and sockets

Levels share inventory/orders/identity/targets/transport graph/seeds. Do not
replace cubes with cylinders when adding pegs, which would confound shape with
mechanism. Three same-type supplies per arm; balance local/neighbor/distant demand
across the graph, not identical per-arm templates. Conserve inventory/orders,
balance long routes, and mark identities visibly for repeated colors so nearby
same-color stock cannot bypass assigned distant demand.

Initial unverified peg proposal:40mm cube,8mm peg diameter,10mm length,20mm centers,
10mm hole clearance. Calibrate before qualification. Supply/transfer supports
need peg clearance, such as raised open cradles, not penetration through tables.
Raised boards can contain real blind holes with explicit depth/length. Build
holes from convex collision parts enclosing real gaps, not painted holes on one
convex body.

Level3 defaults to one board per arm bearing three targets and one central elastic
support, not three independent small boards. Permit damped/limited vertical,
pitch/roll motion; a vertical slider alone does not model tilt. Explain visual
spring versus equivalent mechanics without claiming turn-by-turn finite elements.

Two holes per target, six per three-target board:4/8/12 arms give24/48/72 target
holes. Fixed/elastic boards share sockets/depth/chamfers. Chamfers, if used, are
actual shared geometry, not automatic attraction. Consider peg clearance/finite
buffers across supply/temporary placement/targets; exclude unsolvable cyclic occupancy.

Calibration goal: visible recoverable one-sided tilt, about20°–25° under offset
load, protection near30°; vertical settlement millimeters to about10mm, no board
edge/table collision. Do not require25° on every insertion. Actual load determines
tilt/settlement. Start vertical stiffness250–500N/m, estimate rotational stiffness
Kθ≈m g r / θ, then calibrate board mass/post geometry/load center/dynamics and
damping without suppressing all sway. Do not immobilize it to pass. Private
acceptance uses current board-local coordinates, not returned to policy.

Calculate total tilt from board normal. Separate pitch/roll limits30° do not
bound total tilt30°. Check empty, one-sided and full three-object loads plus
post-release dynamics; simple statics do not replace center-of-mass/gravity stability.

## 4. Mosaic

User-confirmed:40mm blocks, about51mm pitch,50mm pocket opening, about1mm walls,
depth one-third block height. Flat levels retain centers/design gaps rather than
seamless tiling. All levels share target/supply initial states; only physical
or visible guidance changes. Gridless gives no hidden cell-alignment feedback.

Four colors B/R/Y/W including physical blocks for every white background cell.
Draft turns the7×7 rocket rightward;14/21-column versions extend body/repeat blue
windows, without noninteger whole-image scaling or multiple rockets. See
rocket-targets.png/json. This editable draft had not replaced old7×7 tasks.

4 arms:one per edge;6:two top/two bottom/one each side;8:three top/three bottom/
one each side. Four-arm supplies one color each; six repeats the two highest-demand
colors; eight has two supplies per color. Split stock by target counts, not equal
per-arm counts or permanent color ownership. Start with tidy single-layer arrays,
not extra random-pile difficulty.

Largest board≈0.36×1.07m; do not assume every arm reaches all cells. Every cell
needs a full approach/place/release/retreat solution, cooperating adjacent zones
and feasible stock transport, without isolated undeliverable colors. Heatmaps
cover goals, supplies and optional transfers.

Publish target/pitch/assembly reference pose consistently; these are goals, not
live truth. Gridless does not mean guessing an undisclosed absolute location.
Check color, unique matches, planar pose, release/stability; pockets also full
containment/floor seating. Calibrate/freeze tolerances before experiments; separate
strict diagnostics from task acceptance, without post-failure relaxation.

Gridless assembly has no target outline/grid/fiducials or per-cell world-coordinate
table. Same target image/pitch/reference let Agents derive positions. Specify
whether global pattern registration is allowed rather than choosing favorable
alignment during scoring. Respect symmetry: equivalent cube right-angle rotations,
identical twin-peg half-turn symmetry, Dial±180° same symbol; no componentwise
comparison with initial quaternions.

## 5. Airborne Relay

8 arms:four straight pairs;12:six pairs along turns, preferably roomy L/U routes;
16:eight ring pairs.16 arms are not16 pairs. Facing direction follows local route.
Verify receiving grasp, shared holding, sender opening and retreat, beyond endpoint IK.

Closed-loop task is finite: visit all groups/one full lap with actual custody
progress, preventing no-motion success when start=end. Group order/endpoints are
rules; grasps/poses/schedule belong to Agent. More laps are future parameters,
not infinite execution.

Initial candidates:retain≈1.458kg timber;levels2/3 add≈250g at the same end.
Try short-ring10–20mm, long cord≈200mm; freeze mass/attachment/length after bench
checks. Ring connection is preassembled and swinging, not onsite robot hooking.
Document equivalent-joint differences from real ring contacts; object connection
is not welding timber to a robot.

Long cord must bend/swing; test a small segmented ball-joint rope/official cable,
not rigid rod or animation. Match level2 weight/attachment without easier friction,
force limits or solver settings.

All levels use raised start/end supports with clearance for weight/cord; lift
height covers cord length/weight/safety margin. Full payload participates in
collision/process audits. Only legal sender may recover a drop; receiver pickup
cannot bypass handoff. Test one explicitly recoverable drop, without universal
recoverability promises or automatic reset.

Ordinary Transport permits table buffers; Relay requires continuous shared load
during transfer. This is a task rule, not a claim one Panda cannot physically
carry the timber by mass alone.

## 6. Common engineering and policy responsibilities

- Reuse four parameterized generators, not36 copied controllers or a new agent framework.
- Replace hardcoded four-arm/four-dial/square/straight assumptions in generators,
  checks, displays/private samplers with robot/device/grid/route iteration. Most
  changes belong to generation/adaptation/evaluation/Oracle; only demonstrated
  capability gaps justify execution Harness changes.
- Task docs carry goals/mechanisms/geometry. Common Skill covers rolling plans,
  concurrency, support/operation coupling, exits and experience management, not
  successful grasps/turn poses/insertion recipes or one Agent per arm mandates.
- Keep move/joint targets/aperture/bounded force/observe tools corresponding to
  real robots. No auto-attract/insert/object locking/successful-turn macros;
  policies cannot change friction/solver/springs/mass/combination.
- Freeze every case for single/hierarchical/peer/adaptive. Retain existing role/
  delegate lifecycle; Oracle planning stays outside task Agent context.
- Named fixed global front/rear/top/local cameras, clear robot/device labels,
  selective loading. Truth-based auto-tracking requires declared extra observation.
  Prefer synchronized front/rear recording; private full state is engineering
  replay, not what Agents actually observed.
- Freeze friction/mass/grasp ranges/solver/timestep across compared protocols.
  New mechanism physics gets explicit versions/revalidation, never silent changes.
- Check compiled total mass/inertia/center of mass; visual stickers/labels must
  not accidentally add mass. Match parameters to compiled MuJoCo values, not
  nominal block/timber mass alone. Calibrate contact stiffness/damping to avoid
  penetration-based grasp stability.
- Use actual current capability contracts, not old audit gaps. Position/joint/
  aperture/bounded grasp force already exist; do not claim unavailable hardware
  modes. Actual Oracle contact force remains private, not default Agent sensing.

## 6.1. Appearance, labels and cameras

Bright robotics bench:cool light-blue/neutral background, matte brown wood,
natural white/black Panda, restrained contrasting mechanism colors. No silver-only
scene/yellow background/black decorative panels/clutter/gloss obscuring contacts.
Yellow reserved for task blocks.

Suggested palette:background#DFEAF2,table#9A7558,fixtures/dials#F1EFE8,text#17202B;
red gears/cranks,blue supports,orange pointers. Bold dark labels must be checked
in actual camera images, not textures alone. Use edges/lighting to distinguish
white blocks from fixtures without blown highlights.

Tables fit bases/supply/sweeps/hanging clearance, symmetric sides without wasted
space. Rings need real inner mounting surfaces. Boards/supports/displays have
thickness/support, not visual levitation. Relevant legs/tabletops collide;
never disable physics for Oracle success.

Robots A–P, dials independent01–08 to avoid ambiguous B labels. Physically visible
base/module labels do not obscure grasps/cells/dials. Initial layout/key/camera
diagrams contain no undeclared live coordinates.

Fixed eight-dial rows3–2–3; airborne eight-dial/sixteen-arm Relay rings need top
and oblique review, especially inner crowding.70cm belongs to current four-dial
straight layout, not every installation.

Global views show identity/direction/concurrency; local views show slots/fingers/
marks/cables without requiring millimeter judgments from panoramas. Fixed named
cameras; readable in-table displays outside sweeps, English/zero-padded numbers,
e.g. CORRECT03/08.

Deliver front/rear/top/key local previews for each case. Review small/large
representatives before bulk generation. Rocket draft must clearly show nose/body/
windows/tail; draft is not frozen official target.

## 7. Directories and order

Retain configs/environments,configs/tasks,runs ownership. A lightweight suite
manifest indexes configuration/status/evidence rather than duplicating parameters/
rules. Keep generation/task/frozen-run responsibilities and old files in place.

Variant names should include family/scale/level, e.g.dial-n06-floating-crank,
mosaic-a08-7x21-grid. Preserve directory depth/Panda relative assets. Append-only
attempts in separate runs/oracle directories. Each case needs preview/specification/
scene hash/task/status/trace/video index; distinguish planned,built,layout_checked,
primitive_verified,oracle_passed and retain failures.

1. Freeze plan/36-case index/pattern drafts and meanings of arms/devices/pairs/
   routes. Audit baseline hashes and distinguish complete traces/local tests/
   previews; old success does not transfer automatically to new geometry/mechanisms.
2. Bench new twin pegs/spring board/ring weight/flexible rope and existing crank
   rest/release constraints. Engineering Oracles are not model pre-learning.
3. Check large skeletons early:16-arm inner/outer rings,eight-arm long Mosaic,
   12-arm logistics geometry/performance. Parameterize generators, then all36
   previews/collisions/initial states/local cameras; label unqualified work.
4. Whole-scene reach/collision/rest/solver screening; fix layout/mechanism as
   necessary. Point IK is not a complete feasible path.
5. Small scale/three levels first, then medium/large. Every full case needs
   continuous initial-to-complete physical Oracle covering all targets/handoffs/
   dials, not one block or one turn called a complete pass.
6. First full witness, then three independent runs/small perturbations after
   freezing (same-version first witness may count). Report attempts/failures,
   not best-of-picked reliability. Boundary/drop recovery separately, without
   changing formal policy initial states.
7. 36-row status/video page:success/quality/actions/simulated time/actual overlap/
   collision/support/landing/stability/compute wall cost. Reference schedules are
   not optimal without proof, nor is faster-than-LLM reference a model-efficiency result.

Before GPT, check engineering per case; unfinished cases remain development,
without claiming all passed. Then compare architectures with matching seeds and
include model exploration cost. Oracle programs/reference data remain engineering-only.

Separate motion from useful holding:airborne support/Dial holding are work, not
idle merely because stationary. Report useful support, idle/wait causes,
throughput/planning/communication. Single Agent can command concurrently; do not
force serial execution to create advantages. Privileged truth/offline fast-forward
cannot represent LLM-achievable planning efficiency.

Measure large-scale real-time factor, control/render overhead. Report separately
if16 arms/ropes run slower than wall clock. Oracle/model physical-speed comparisons
need matching interfaces/action constraints/clock protocols; distinguish inference
wall time and simulated execution, without blaming engine slowness on Agent.

## 8. Oracle implementation and delivery

Engineering Oracle may use private poses/contacts/board state/full geometry for
candidates, but actual execution uses the same bounded Panda action layer.
Keyframe writes only at initialization; afterward no object/dial state writes,
hand welding, injected forces, auto-attraction or live material/mass/solver edits.
Solvability does not establish GPT understanding/execution.

One planner per family driven by configuration, not36 hardcoded routes:logistics
graph/finite buffers; Mosaic coverage/supply/order; Relay feasible receiving/exit
grasps with closed-loop prefixes; Dial actual white-relative arcs/support.
Heuristics are allowed, without unproved optimality claims.

Dial has mechanical checks of three nonzero marks/release per dial and full puzzle
witnesses using only configuration/total-score feedback decoders. Secret stays in
independent evaluator; reading it is not puzzle solving. Bind feedback to stable
actual inputs/timestamps; stable intermediate inputs count as attempts. Decoder/
strategy never enters GPT Prompt/Skill.

| Family | Complete success | Required additional checks |
| --- | --- | --- |
| Transport | All3N targets, correct identity/color/station, stable released placement | Both pegs/depth/local board/full-load stability/end-to-end logistics |
| Relay | Every required handoff/final landing, legal process | Receiving support before sender exit, all-arm collision/full hanging load/legal recovery/all ring groups |
| Mosaic | All49/98/147 cells uniquely correct and stably released | No later disturbance, pocket seating/free-board pose, remaining grasp/exit space |
| Dial | Score N with valid inputs/process | Simultaneous N-dial input, continuous support/zero/return/all nonzero marks, secret/feedback separation |

Sample required process, not final frame alone. Define expected fixture/object
contacts versus forbidden arm/self collisions with fixed public tolerances.
completed commands/stopped aperture/is_grasped inference do not replace actual
support/placement evidence. No reset after a fall counted as the same success;
recovery follows explicit family rules.

Distinguish planned,generated,layout_checked,primitive_verified,
oracle_witness_passed,repeatability_checked. Separate full witness from three
predeclared seeds/perturbations. Identical deterministic replay is not robustness.
Record all failures/parameter versions; changed parameters require affected
witnesses again rather than borrowing old PASS.

Deliver36-row status, frozen scenes/parameters/mass checks/tasks/rules/cameras/
previews/reach reports, full actions/process/results, synchronized front/rear
video or labeled framewise rerenders, repeatability/performance. Framewise visual
replay does not establish crash recovery of the same physical world.

Unfinished development entries are allowed, but formal first-version acceptance
requires all36 full witnesses, not static loading or a started run. Three physical
levels must have observable effects; later independent pilots measure model success/
difficulty. Do not promise untested50%–70% model success.

## 9. Technical basis

- Convex collision geometry requires actual decompositions for holes/rings:
  [Collision computation](https://mujoco.readthedocs.io/en/latest/computation/).
- Passive springs, reference positions, damping/limits:
  [XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html).
- Official cable uses inextensible ball-jointed segments for flexible suspension:
  [Composite objects](https://mujoco.readthedocs.io/en/stable/modeling.html#composite-objects).

These references support modeling methods, not qualification of these mechanisms/layouts.
