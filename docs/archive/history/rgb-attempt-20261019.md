# Historical RGB/proprioceptive operation: 2026-10-19

The Codex session observed images, chose actions incrementally and called the
local entry through the same keyboard controller/robot IK. This was not a
previously successful fixed-coordinate reference script.

## Protocol

- `--blind` used an independent random source to place three cubes before the
  first observation, avoiding known coordinates of the previous default layout.
- Inputs were front/side RGB, TCP, joint angles/velocities, aperture and execution state.
- Decisions did not read object pose, depth, contact truth, success timers,
  private initial snapshots or internal physics logs.
- The blue cube was selected visually; images informed alignment/grasp timing.
  The interface provided small end-effector velocity requests, gripper, wait and
  observe, without automatic alignment or pick.
- Original dynamics, friction and grasp settings remained. Three attempts used
  one continuously running episode, without reset or parameter changes.
- Physics continued between reasoning/tool calls; objects were not frozen for reasoning.
- Two RGB views were permitted, so this was not a single-camera test. Robot-model
  and fixed-workbench priors still existed.

## Observations

There were 27 robot actions and 3 closing attempts, without a stable grasp:

1. After the first close, aperture was approximately 4 cm. A small lift closed
   it to zero while RGB showed the cube remaining on the table.
2. After fore/aft correction, the cube briefly rose, then tilted and slipped
   during further ascent.
3. Realignment and proprioceptive compensation for horizontal lift drift again
   produced a brief lift followed by slipping.

These were observations from images/robot feedback, not hidden object-truth
acceptance. They did not meet stable 5 cm lift/1 s hold criteria or establish an
overall model success rate. Grasp location, orientation and tracking could have
contributed; the cause had not been diagnosed.

## Retained evidence

Episode: `runs/20261019-220952-187535/`.

- `recording-01.mp4`: complete recording including waits/failures, 1280×800,
  30 FPS, approximately 8 minutes 35 seconds.
- `demo-4x.mp4`: the same complete sequence at four times speed, retaining failures.
- `rgb-0001-*.png` through `rgb-0028-*.png`: front/side images at each observation.
- Internal `trace.jsonl`: physics audit containing truth, unused for action selection.

A separate `policy.jsonl` writer was added after this episode and took effect on
subsequent launches. Original tool requests/results remain in the conversation
and internal event log.
