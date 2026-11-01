# Historical four-arm block Mosaic environment

Four inward-facing Franka Panda 7 DoF arms are fixed around a physical wood-colored
1.6×1.6 m table: A south, B east, C north, D west. Table height is 0.4 m. A central
10×10 grid occupies 40×40 cm; grid pitch and block side length are both 4 cm.
Grid lines and row/column numbers are visual printing only, without collision
dividers, attachment or automatic alignment.

The 100 free blocks each weigh 50 g. Draft target color counts are blue 40 near
A, red 30 near B, yellow 14 near C and white 16 near D. Supply is arranged in
spaced single layers. Supply locations do not restrict arms to a particular color.

The scene has a light-blue background and warm wood table. Its 12 fixed cameras
are global, global_side, top, board_top and front / side for A–D. board_top is a
grid closeup. In top view north is up and east right; rows run north to south,
columns west to east. initial-* files are initialization images, not live observations.

## View and reset

From the repository root:

```sh
.venv/bin/mjpython -m scripts.view_mosaic
```

F6 cycles global / top / board_top / global_side; F7 restores the initial keyframe.
On Mac, use Fn+F6 / Fn+F7 if needed. `--camera board_top` chooses the initial
view. Mouse navigation uses native MuJoCo controls.

Physics runs continuously while robots retain initial actuator targets. This
command is a viewer without an action service. The separate preparation/start
steps below allow the agent service to load the same scene. Four-arm keyboard
motion and an automatic placement policy were not implemented. Apply the saved
initial keyframe after loading; raw qpos0 is not a usable initialization pose.

## Draft goal and verification boundaries

assets/reference-original.png stores the user reference. task-draft.json and
target-pattern-draft.png define a regularized four-color 10×10 draft. Row 7 of
the original has a half-cell offset; this draft places the central blue block
in column 6 and treats dark/light blue as one color. The matrix still required
confirmation before evaluation. It is stored as PATTERN in robofrontier/mosaic.py;
changes require regeneration, which overwrites this directory's derived files.
This historical draft is separate from the current released Mosaic specification.

validation.json records initialization penetration, one-second settling and
robot-point IK checks. No initial penetration exceeded 1 mm; maximum block
displacement during settling was about 0.073 mm. Each arm's own supply center
passed IK. The union of reachable target cells covered all 100 cells, with
86 cells per arm at a fixed downward orientation.

These were geometric endpoint checks. They established neither grasping,
approach/withdrawal, finger clearance, dense zero-gap insertion, continuous
trajectories nor concurrent multi-arm safety. Private action-service scoring
checked the shared goal, 2 mm XY center error, 3 mm height error, about 2° axis
alignment, release and table support, with one continuous second of stability.
The goal remained a draft; complete dense placement feasibility was unverified.

Gravity, the 0.002 s timestep, NoSlip 10, friction and Panda position actuators
were retained from the existing environment. Grasp strength was unchanged and
no attachment was added. scene.xml references vendor/panda/assets through
relative paths; loading requires the complete repository.

Historical generation command:

```sh
.venv/bin/python -m scripts.build_mosaic --reference /path/to/reference.png
```

## Historical agent action-service integration

Generation also updated configs/tasks/mosaic-four-arm-v1.json with a shared goal,
without assigning target cells to individual robots. Prepare in a new directory:

```sh
.venv/bin/python -m scripts.create_pipeline_run runs/NEW --task configs/tasks/mosaic-four-arm-v1.json
.venv/bin/python -m robofrontier.pipeline --run-dir runs/NEW
```

The first command froze inputs, scene, grid textures and robot meshes, and created
role connections. Only the second started the shared physical world and local
authenticated service. This legacy integration retained role READY/session
binding/START gating; arms could not move before START. It is not the newer
unified direct-START protocol. One physical process owned a run; other roles
controlled that same world through their own connections rather than starting
independent simulators.

Controls included position plus world-frame quaternion, joint targets, continuous
gripper aperture/speed and controlled stop on the original action ID. The
controller retained joint velocity/acceleration, tracking and actuator force
limits. Gravity compensation used the robot model, without object-state-based
action selection. Gripper width control was not constant grasp-force control.
Complete parameters came from READY and the frozen Skill tool contract.

Runtime RGB was 1280×800, with camera settings returned by READY. Static previews
here were originally 1280×900; bordered previews also had viewport offsets
recorded in initial-top.json. These pixel coordinate systems are distinct.

Session scheduling and communication topology were retained. Changes covered
the robot action adapter, run preparation, shared-goal evaluation and generic
Prompt / Skill. No new model trial or prescribed placement/grasp sequence was run.
