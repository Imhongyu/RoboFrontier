# RoboFrontier minimum runnable prototype plan

Historical status: 2026-10-19 delivered the first Human keyboard-practice stage.
Dependencies, Panda scene, end-effector IK/joint control, initialization restore,
recording and three reference-grasp checks were complete. README.md described
actual usage/scope. Remaining sections preserved the proposed full experimental
prototype; tool takeover, step protocol and formal RGB/Oracle separation were
not yet implemented. They are not the current unified execution contract.

## Delivery scope

First deliver one local MuJoCo desktop window: Panda 7 DoF, table, three free
red/blue/green blocks, fixed camera, keyboard teleoperation, scene reset,
MP4 recording and action logs. The user operates first; later Codex submits
local commands to the same running simulation.

The first version excludes a website, experiment matrix, statistics reports,
paired player and independent GPT API client. First establish real-contact grasping.

## Technical approach

- An independent Python 3.12 environment with versions locked after actual checks, without modifying system Python.
- MuJoCo and Menagerie's `franka_emika_panda`; fetch only needed models/assets and record upstream commit/license.
- Native MuJoCo `mjv` / `mjr` rendering in a small GLFW window. Window/OpenGL run on the macOS main thread, directly receiving key-down/up/focus changes. This supports multi-key input without global keyboard listeners or a passive viewer's private window.
- Small NumPy damped-least-squares IK, retaining official position servos without ROS / robosuite.
- FFmpeg encoding, decoupled from physics/input so encoder load cannot change action duration/timestep.
- A running simulation command service bound only to `127.0.0.1`, with a CLI client. Only the simulation thread may mutate `MjData`.

## Scene and physics starting points

These are proposed engineering values, not calibrated real-robot parameters.
Keep them in one configuration and freeze after acceptance.

| Item | Starting value / rule |
| --- | --- |
| Coordinates | SI; world Z up; visible world X/Y/Z axes and direction-key labels |
| Table | 1.2 × 0.8 m, thickness 0.05 m, top at world Z=0.40 m |
| Robot base | Fixed at world (0, 0, 0.40) m; table covers base/grasp region |
| Blocks | Side 0.04 m, mass 0.05 kg; independent freejoints; box geometry/mass derive inertia |
| Initial block centers | Blue (0.45, -0.09, 0.42), red (0.45, 0, 0.42), green (0.45, 0.09, 0.42) m |
| Gravity | (0, 0, -9.81) m/s² |
| Physics step | 0.002 s, 500 Hz; never enlarge for dropped display frames |
| Control update | 100 Hz, 5 physics steps per control cycle |
| Render/video | Display target 60 FPS; fixed-camera video 1280×720, 30 FPS |
| Integrator/solver | `implicitfast` / Newton, iterations=100; start from model soft-contact settings and adjust through tests |
| Contacts | Objects/table/gripper/model-defined arm collisions; retain upstream self-collision exclusions |
| Initial block contact | friction=(1.0, 0.005, 0.0001), condim=4; verify effective geom/pair-combined parameters |
| Robot dynamics | Retain upstream masses, inertias, joint damping, actuator PD gains and torque limits; do not arbitrarily increase grasp force |
| Grasping | Actual two-finger contact/friction; no attachment, weld or direct object transport after grasp |
| Initialization | Start from upstream home and solve a collision-free downward-gripper pose above blocks; save actual solved values |

Color relations initially use one fixed layout. Define camera-left/world-left
and multiple seeded layouts before formal R0/R1 trials.

At startup, run fixed control references for about 1 s to settle contacts.
Check penetration, drift, initial finger spacing and reachability, then save the
settled episode snapshot. Arbitrary initial joints are not a validated setup.
After adding freejoints, rebuild keyframes rather than retaining robot-only
qpos lengths.

## Keyboard controls

### Default: end-effector movement for grasp practice

Keep the gripper downward. Arrows translate world X/Y, W/S move world Z and
A/D adjust yaw. Show signs explicitly; fixed camera/world axes help calibration.

- Slow / normal / fast translation: 0.01 / **0.03** / 0.06 m/s.
- Slow / normal / fast yaw: 5 / **15** / 30 °/s.
- Simultaneous directions allow diagonal motion. Limit the combined translation norm; three keys must not multiply speed by the square root of three.
- IK outputs remain constrained by all seven joints' velocity, acceleration, position and actuator torque limits. Stop target accumulation near singularity/unreachable motion and display the reason.
- Initially exclude arbitrary roll/pitch to reduce keyboard workload.

### Joint mode: independent or concurrent control of seven joints

Tab switches end-effector/joint mode and clears all keys/old velocity commands.

| Joint | Positive / negative | Default command speed | Slow / fast |
| --- | --- | --- | --- |
| J1 | Q / A | 15 °/s | 5 / 30 °/s |
| J2 | W / S | 15 °/s | 5 / 30 °/s |
| J3 | E / D | 15 °/s | 5 / 30 °/s |
| J4 | R / F | 15 °/s | 5 / 30 °/s |
| J5 | T / G | 15 °/s | 5 / 30 °/s |
| J6 | Y / H | 15 °/s | 5 / 30 °/s |
| J7 | U / J | 15 °/s | 5 / 30 °/s |

- All seven joints accept concurrent commands, subject to keyboard rollover. Display recognized keys/velocity vector; tools can submit the complete seven-dimensional vector.
- Opposite keys on one joint cancel; different joints do not overwrite each other.
- `[` / `]` select slow/normal/fast. Display the mode and each joint's commanded/measured speed.
- Initial reference acceleration is 60 °/s² for every joint; use rad/rad/s internally. Per-joint configuration is supported, with one conservative value initially.
- Soft position limits intersect model joint range and actuator ctrlrange with 0.02 rad margin. Slow before boundaries instead of stopping on hard limits.
- These are defined **reference-trajectory speeds**. Upstream position PD actuators have no transferable default movement speed. Contact, load and tracking error change actual speed. Stop/log excessive speed or tracking error; reference limits are not a hard actual-speed guarantee.

### Common controls

- O / P: open/close. Default total aperture ramps from about 80 mm to 0 mm over about 1 s; contact need not reach actual zero. Retain upstream actuator mapping 0…255.
- Space: pause physics immediately and clear commands. Resume holding the current pose, without continuing old keypresses.
- Backspace: end the episode, restore frozen initialization and create a new episode. Close recording before reset; never concatenate both sides as one trajectory.
- F9: start/stop recording. Esc: save normally and exit.
- Key release cancels that direction's velocity request, decelerating within limits to hold. Focus loss clears keys/pauses to prevent missed key-up causing motion.
- No persistent action queue; stalls must not accumulate delayed old keypresses.

## One control core, two uses of time

Initial real-time practice means hold to move/release to stop. Physics continues
without input, allowing natural slip/drop.

A later step mode was proposed for comparable Human/GPT operation. Default
actions advance 0.20 s simulation time, accepting 0.10…1.00 s aligned to 0.01 s.
After each action, freeze physics and return observations until the next action.
`wait` is explicit, and gripper motion also requires physics time.

In step mode, keyboard directions/joint vectors are composed before Enter
submits an action. Both operators share duration, speeds, limits and observation
updates. Mark real-time practice explicitly; it does not by itself establish
fair comparison with stepwise GPT operation.

## Proposed Codex connection, outputs and execution ownership

Execution chain:

```text
Keyboard events ───┐
                  ├→ Action → Validate / limit → Schedule → Controller → mj_step
Codex local CLI ───┘                                            ↓
                                                    Observations / logs / video
```

Chat text does not directly drive joints, and each action must not restart a
script. One persistent simulation process owns state; the CLI submits JSON and
waits for results.

Proposed common Action contract:

```json
{
  "request_id": "episode001-action004",
  "expected_observation_id": 3,
  "type": "joint_jog",
  "velocity_rad_s": [0.0, 0.12, 0.0, -0.08, 0.0, 0.0, 0.0],
  "duration_s": 0.2
}
```

Other actions: `tcp_jog(linear_m_s[3], yaw_rad_s, duration_s)`,
`gripper(open|close, duration_s)`, `wait(duration_s)`, `observe()`.
Reset/recording are separately logged session-management operations.

Validate fields, lengths, finite values, duration, current control owner and
observation_id. Reject invalid input, explicitly return any valid-input limiting
and deduplicate request_id against timeout replay. Human/Codex takeover is
exclusive, clearing commands and returning to hold on switches.

The proposed shortest integration reused Codex command/image tools:

1. Invoke the project CLI through existing commands, for example the then-proposed `uv run python -m robofrontier.cli action --json-file action.json`.
2. The CLI submits to the running local service. A bounded queue transfers work to the simulation main thread; network threads never touch physics.
3. The shared controller generates smooth joint references; MuJoCo position actuators produce torques and physics integrates contact/motion.
4. Return JSON with request_id, actual duration, limiting/errors, new observation_id, robot state, absolute RGB path and log paths. Task and communication failure remain distinct.
5. Codex views that image through its existing image tool before choosing another action. Initial Oracle debugging precedes RGB truth filtering; internal logs still retain full truth.

This would form an actual tool loop without first requesting a GPT API key.
An independent GPT client could later wrap the same Action as a function tool/MCP.
Tool registration alone does not execute physics; the local simulator does.
The chat does not acquire a newly registered robot MCP tool automatically.
These were integration proposals, not claims of deployed features at that date.

## Initialization, logging and video

Per episode, save model/dependency versions, configuration/hash, seed, fixed
camera intrinsics/extrinsics, task, operator, mode, initial physics snapshot and
controller state.

Reset restores qpos, qvel, act/ctrl, simulation time, integration state, applied
forces, controller references/filter state. Clear input/queue/previous action/
success timer and regenerate observation_id. Use matching-version/layout
MuJoCo state APIs and forward afterward.

Every action logs submitted/limited values, before/after state, timing,
observation references and errors. Video-sample state snapshots support
rerendering; cross-version/platform re-simulation is not promised bit-exact.

Default recording uses the fixed MuJoCo camera and mode/speed/simulation-time/
action-ID HUD, without macOS desktop-recording permission. Save MP4, JSONL and
snapshots in one episode directory. Real-time practice video uses wall time;
step video uses simulation time, with an explicit metadata timebase and separately
logged thinking waits. Encoding is asynchronous/bounded; dropped frames must
be recorded/reported.

## Proposed implementation order and checks

1. **Show a window:** independent environment, dependency lock, selected model, table/three blocks and fixed camera. Run 30 s without input, numerical divergence or obvious drift; check initial table/robot penetration.
2. **Usable controls:** shared joint trajectories/gripper, then keyboard/small IK. Check single/multiple joints, speed modes, release, focus loss, soft limits, pause/resume and reliable default end-effector approach.
3. **Actual grasp:** deterministic shared-Action approach/descent/close/lift, repeated 3 times from fixed initialization. Raise object center at least 5 cm and retain it under gravity for at least 1 s, checking bilateral finger contact. Advance physics; paused time does not count. Diagnose model/control/contact failures instead of hiding them with attachment.
4. **User operation and saving:** verify complete reset state, one keyboard grasp from initialization, playable F9 MP4, action logs/snapshots and clean video finalization on exit.
5. **Later takeover entry:** local CLI observe/joint_jog/tcp_jog/gripper/wait through the same executor as keyboard, request_id deduplication/observation-version checks and one reference sequence in step mode.

The proposed full first-version gate was all five steps, with README documenting
one launch command, controls, parameter/recording locations and takeover.
Formal Human/GPT experiments, extra layouts and paper metrics would follow.

## Original references

- [Menagerie Panda model](https://github.com/google-deepmind/mujoco_menagerie/tree/main/franka_emika_panda): model, actuators, joint limits and gripper mapping.
- [MuJoCo Python](https://mujoco.readthedocs.io/en/stable/python.html): API, native viewer and macOS thread constraints.
- [MuJoCo visualization](https://mujoco.readthedocs.io/en/stable/programming/visualization.html): native scene/render interfaces.
- [GLFW input guide](https://www.glfw.org/docs/latest/input_guide.html): key state, simultaneous input and focus.
- Further historical checks: `docs/mujoco-official-notes.md`.
