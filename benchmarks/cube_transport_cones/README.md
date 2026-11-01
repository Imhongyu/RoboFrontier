# Legacy Cube Transport v3: cubes and cones

This historical series replaces v2 spheres with full pointed cones. Original
scenes, orders and videos remain in `cube_transport`; v2 generator sources are
archived in `benchmarks/cube_transport/history/v2-generator-source.tar.gz`.
The current legacy generator outputs **v4 cylinders**, not this cone series.
Neither offline collection is the current 36-case benchmark; see the
[task atlas](../../docs/task-atlas.md) for current cases.

## Scenes and tasks

The 3-6-arm cases use solid six-color cubes. The 7-12-arm cases reuse those
colors: A-F initially hold three red, blue, green, orange, purple or cyan cubes;
G-L hold three cones in the same order. Cones point upward on flat bases,
with base diameter 4 cm, height 4 cm and mass 50 g. Visualization and collision
share a closed convex mesh with a 64-sided base approximation. Mesh-derived
inertia places the center of mass 1 cm below the bounding-box-centered body origin.

Layout, supply/demand, initial positions, goals, cameras and scene-wide distance
distribution preserve v2. Orders change sphere requirements to cone. Same-color,
same-shape items are interchangeable; each arm has three goals, whose slot IDs
do not prescribe execution order. See [tasks.md](tasks.md). Ten sizes each have
three order seeds, changing orders without changing initial geometry.

The background is pale blue and table warm wood. Front/side views per arm plus
global/global_side/top make 2N+3 fixed cameras. Physical base IDs and A-L preview
border labels identify robots; static images do not replace runtime observations.
`startup.md` / `startup.json` contain initialization, not a solution. Initial
coordinates may be public; runtime policies should receive only RGB, robot
proprioception and action state.

## Published physics and validation scope

The table is 0.4 m high; the step is 0.002 s and gravity 9.81 m/s². Original
friction `[1,0.005,0.0001]`, condim 4, NoSlip 10 and Panda gripper actuators are
unchanged. No rolling resistance, attraction, hidden support or fixation was
added. These values are historical, not the current suite's
[physics release](../../docs/physics.md).

The original ten-size report recorded loading, support, initial penetration,
point IK / endpoint contacts and one-second settling, with maximum cone
settling displacement about 0.075 mm. This does not establish successful dynamic
grasps, handovers or multi-arm collision avoidance.

**The recorded reference cone grasp did not pass.** A known-pose three-arm A cube
pick/place passed; seven-arm G and 12-arm L cones were not lifted stably. Probes
with different grip heights and slower lifts also failed. Results/videos remain
historical `validation` artifacts. Mass, friction and grip strength were not
changed to hide those failures. Shape replacement does not prove full-task
feasibility; suitable grasps or other objects still required validation.

The local grasp check additionally requires released cone tilt below 15 degrees.
Task scoring retains v2 position, linear-speed, support, release and one-second
window requirements; **no task orientation score was added**. Failed grasps
are not counted as passes.

Local grasp checks use known poses and IK, without an LLM; they are not
vision-model scores. This publication launched no model experiments and changed
no communication harness or planning skill. Offline scheduling checks capacity
and dependencies, excluding actual motion time. Phase counts match v2 and do
not establish physical speedup.

## Files and reproduction boundaries

```text
configs/environments/cube_transport_cones/<environment>/
  environment.json / scene.xml / assets/
  startup.json / startup.md
configs/tasks/cube_transport_cones/<environment>/seed-0.json ... seed-2.json
benchmarks/cube_transport_cones/
  README.md / tasks.md / manifest.json
  previews/     Initial images and label/camera metadata
  references/   Abstract schedules, lower bounds and distance counts
  validation/   Geometry, point checks, settling, local grasps and videos
```

The following retained commands target the generator's **current cylinder
collection**. They do not reproduce cones. For cone reproduction, inspect the
preserved `history/v3-generator-source.tar.gz` sources and original assets in
an isolated checkout; do not overwrite current or historical evidence:

```sh
.venv/bin/python -m scripts.generate_cube_transport
.venv/bin/python -m scripts.verify_transport_objects --record
.venv/bin/python -m unittest tests.test_cube_transport -v
.venv/bin/mjpython -m scripts.view_cube_transport --count 7
```

The historical cone grasp checker returned nonzero on the recorded failures;
this was expected, not a passing result. The viewer applies `initial` and runs
physics, without the old pipeline action service, keyboard control or recording.
Use the same environment's Python instead of `mjpython` outside macOS. Partial
generation overwrites collection summaries, so a full offline publication needs
all sizes. Old program playback scripts retain their old directory targets.
Ignored historical videos and validation assets may need their original archive;
the current policy release does not promise to install these retired series.
