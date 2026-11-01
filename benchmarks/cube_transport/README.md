# Legacy Cube Transport v2: cubes and spheres

This historical offline MuJoCo series contains a three-arm line and four- to
12-arm rings: ten sizes and 30 orders. It is separate from the current 36-case
benchmark described in the [task atlas](../../docs/task-atlas.md). Its original
publication launched no model sessions and changed no communication harness,
runtime service or planning skill. These scenes were not connected to the old
pipeline service, which only supported bases on a line. The current unified
CLI does not select these legacy directories as benchmark cases.

## Materials and orders

The 3-6-arm cases use solid cubes. The 7-12-arm cases reuse six colors and add
spheres, with no stripe or dot patterns. Stations A-F initially hold red, blue,
green, orange, purple and cyan cubes; G-L hold spheres in that same color order.
Each station has three physical items of its type. Each present type has total
supply and demand of three items; each station must finally receive three items.

Orders specify color and shape. Matching physical items are interchangeable;
tasks impose no target `object_id` or source restriction. Private records still
use entity IDs to track physical state, and one item can match only one goal.
Slot numbers determine final positions, not action order. The policy chooses
routes, allocation, scheduling and parallel execution.

Seed 0 retains the agreed 3-6-arm orders. The three-arm order is A receiving
`a,c,c`, B receiving `b,a,c`, and C receiving `a,b,b`. The other two small-case
order seeds use graph-distance-preserving mappings and slot permutations.
For 7-12 arms, minimum handover distances are balanced across **all scene demand**
by minimizing the sum of squared histogram counts. Local demand combinations
are varied; stations need not have identical recipes.

The balancer uses deterministic random search and checks the integer count
lower bound. On an even ring, the number of odd-hop demands must be even, so
the ten-arm case cannot have five items in each of six distance bins; it allows
the smallest integer imbalance. This proves the selected demand-balancing
objective, not schedule optimality.

Each size has three order seeds. **Seeds change orders, not initial geometry or
object positions.** See [tasks.md](tasks.md) for seed 0 and
[references/summary.csv](references/summary.csv) for all seeds and distance counts.
Model completion rates and difficulty were not calibrated by this publication.

## Layout and visual identity

The ring's side counts are listed south, east, north, west:

| Arms | Stations per side |
| --- | --- |
| 4 | 1, 1, 1, 1 |
| 5 | 2, 1, 1, 1 |
| 6 | 2, 1, 2, 1 |
| 7 | 2, 2, 2, 1 |
| 8 | 2, 2, 2, 2 |
| 9 | 3, 2, 2, 2 |
| 10 | 3, 2, 3, 2 |
| 11 | 3, 3, 3, 2 |
| 12 | 3, 3, 3, 3 |

Station numbering begins on the south side and follows the perimeter. Bases
face inward and do not occupy corners. Four coplanar solid table strips surround
an open center, with supports below. Each station has three goals and two parking
positions. Each adjacent pair has a handover position of capacity one. The
adjacency graph defines permitted handovers, not complete collision boundaries.

The ground is light sky blue, the distant background pale blue, the matte table
warm wood, and supports dark brown. Enlarged physical station IDs supplement
upright A-L preview labels placed in a separate border with thin leaders to the
bases. Label boxes stay outside the scene viewport. **Overlays use fixed robot
base geometry only, not object ground truth.** Global labels were checked for
completeness, overlap and viewport exclusion. Readable labels do not establish
reliable model operation. Files ending `-raw.png` retain unannotated views.

World +X is east, +Y north, +Z up; local +X is inward and +Y is robot-left.
The top camera is north-up/east-right. Each scene's `startup.md` / `startup.json`
lists IDs, neighbors, initial stock, cameras and its initial top image, without
providing a transport solution.

The three-arm scene uses this series' new positions, not a coordinate-identical
copy of the earlier three-arm experiment. Line versus ring is not a controlled
comparison of arm count alone; six versus seven arms also changes object shapes.
Interpreting scale effects requires same-shape controls.

## Cameras, initialization and observations

Each arm has fixed front/side oblique cameras. Two global oblique cameras and a
top camera bring the total to 2N+3; there are no wrist cameras. Local views may
include neighbors. Raw renders are 1280×900; bordered previews are 1536×1152
without resizing the scene viewport. Calibration uses raw resolution; add the
viewport offset `[128,126]` for bordered pixels. Image JSON and `startup.json`
record the details. Initialization previews never replace live observations.

The historical startup contract supplied the selected `startup.md`, `startup.json`,
labeled top image and one seed order, after which the policy chose cameras.
A runtime adapter still needed to attach upright IDs, camera names and time to
live image returns. These overlays were offline previews, not a connection to
the original runtime or native viewer.

Initial object positions may be public. Runtime policies should receive RGB,
robot proprioception and action state. Simulation files, engineering checks and
mathematical references contain ground truth and must not enter default policy
observations. File conventions alone are not OS-level access isolation.

MJCF includes an `initial` keyframe for robots, fingers, free items and actuator
targets. Apply it after loading; default `qpos0` is not the prepared posture.
The following historical viewer uses the generator's current cylinder collection,
not this preserved v2 sphere collection; it does not reproduce v2 by itself:

```sh
.venv/bin/mjpython -m scripts.view_cube_transport --count 8
```

Use `mjpython` on macOS or the same environment's Python elsewhere. The viewer
accepts `--camera top`, runs physics, connects no policy and records no video.
Realtime performance was not calibrated.

## Published physics and completion rules

The table is 0.4 m high. Cube edges are 0.04 m; sphere radius is 0.02 m; each item
weighs 0.05 kg, with shape-derived inertia. Gravity is `[0,0,-9.81]`; the step is
0.002 s, with implicitfast integration, Newton solving and 100 iterations.
Friction `[1,0.005,0.0001]`, NoSlip 10, gripper actuator strength and finger limits
retain the original settings. Spheres are free bodies, without attraction,
fixed joints, hidden cradles or added rolling resistance. These legacy values
are not the current suite's contact release; see [physics.md](../../docs/physics.md).

`task.completion` requires a different color/shape-matching item in every slot:
XY center error at most 2 cm, Z error at most 1 cm, linear speed at most 1 cm/s,
table support and release from all robots, continuously for one simulated second.
Orientation and sphere spin direction are not scored.

Private `evaluate_placement_window` matches semantics over the final one-second
sample window, with gaps at most 25 ms. A missing window or sampling gap cannot
pass. Each matched item must satisfy its slot throughout the window; equivalent
entity IDs can differ between executions. Instantaneous `match_placement_sample`
is diagnostic only. Offline evaluator tests did not replace the need for actual
support, release and velocity samples from a runtime adapter; object state is
not exposed to the policy.

## Engineering checks and abstract references

Published checks cover loading, marked support/spacing, initial penetration,
IK at source/goal/parking/handover hover and grip positions, endpoint contacts,
and one-second settling. Endpoint IK uses peers at home, initial material
positions and open grippers, allowing contact penetration below 1 mm. It is not
a swept-path or concurrent collision proof.

`verify_transport_objects` added three known-pose physical references: a
three-arm A cube, seven-arm G sphere and 12-arm L sphere. Local pickup, holding,
release and retreat check bilateral finger contact, lift, support and stability
in the final second; see `validation/object-fixtures.json`. **These are not model
trials, and do not validate every station, full transport or simultaneous arms.**

Offline scheduling selects interchangeable entities as witnesses and chooses
minimum-handover routes, breaking equal ring paths toward increasing IDs.
A route with h handovers visits h+1 stations, each with pick-clear and place-clear
phases. Serial work is `2×Σ(h+1)`. The parallel reference tries up to 256 no-wait
priority insertions; receiving begins in the phase after sender placement.
No-wait is a reference-algorithm choice, not a policy constraint.

Artifacts retain a feasible upper bound, fixed-route load/item-chain lower
bounds and independent replay. `optimality_proven` is true only when bounds
meet. **Phases are neither seconds nor tool calls.** Geometry, inference,
perception and communication time are excluded; the reported ratio is not a
measured physical speedup. References are not default policy context.

## Files and reproduction boundaries

```text
configs/environments/cube_transport/<environment>/
  environment.json / scene.xml / assets/
  startup.md / startup.json
configs/tasks/cube_transport/<environment>/seed-0.json ... seed-2.json
benchmarks/cube_transport/
  manifest.json / tasks.md
  previews/       Initial images, camera/label metadata and overview
  validation/     Geometry, stability and local object-reference checks
  references/     Abstract schedules, lower bounds and distance counts
  history/v1-assets-20261021.tar.gz  Earlier v1 configs/references/generator
```

Panda meshes use relative references into `vendor/panda/assets`; copying only
`scene.xml` is insufficient. Historical generation archives are retained for
reproduction. The commands below now target `cube_transport_cylinders`, not v2:

```sh
.venv/bin/python -m scripts.generate_cube_transport
.venv/bin/python -m scripts.verify_transport_objects
.venv/bin/python -m unittest tests.test_cube_transport -v
```

The generator accepts `--counts 4 8 12` and `--no-render`. Partial generation
limits its manifest, summary and overview to that subset. Generate every size
for a complete offline publication. Local grasp verification is separate from
static generation. Do not regenerate or rewrite historical experiment results.

## Later end-to-end program reference

The historical data root `runs/program-transport-v2-20261021/` recorded CP-SAT
optimal round counts for all ten sizes under fixed routes and unit phases, with
independent replay. Original `references/` retain earlier feasible upper bounds;
these newer discrete proofs do not establish minimum continuous physical time.
That ignored run directory is not guaranteed to exist in a fresh clone.

Its `index.json` / `report.md` distinguish discrete proofs, physical acceptance,
failed attempts and playable videos. The program can use object ground truth,
continuous controls, motion prechecks and release corrections; it is an
engineering feasibility reference, not an RGB-policy-equivalent performance
baseline. Sphere relay still needs full-order end-to-end acceptance; a local
pick/place result cannot substitute for it.
