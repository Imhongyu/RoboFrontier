# Historical NoSlip configuration and actual RGB grasp

Date: 2026-10-19. After the user requested NoSlip and a video without the cube
slipping, `configs/noslip.json` (profile `noslip-10-v1`) was added and became the
early demo's default; `config.json` retained the NoSlip=0 baseline. This is a
dated demo record, not the current benchmark CLI/defaults.

## Configuration change

Only `noslip_iterations=10` and a profile label were added. Friction, cube mass,
gripper PD gains/force limit, arm speed and gravity were unchanged. NoSlip is
contact-solver postprocessing, not adhesion, a weld or object-pose assignment.

## Reference-program verification

Historical command:

```sh
uv run python scripts/verify_demo.py --config configs/noslip.json --hold-seconds 30
```

3 consecutive two-finger grasps from the same initial state lifted 11.99 cm.
Each held for another 30 s with approximately 0.051 mm displacement. Idle
stability, reset, multi-joint input, key release and mode-switch checks passed.
This fixed-coordinate reference verified a physical control loop, not an RGB
policy score.

## Actual RGB policy operation

The demo was restarted with randomized cubes using the historical command:

```sh
uv run robofrontier --config configs/noslip.json --bridge --blind --record --camera side
```

The entry did not return the new layout; internal truth logs/initialization were
not read to choose actions. Front/side RGB and robot proprioception were used.
The conversational policy selected actions incrementally through the same IK
and keyboard controller; physics continued during reasoning.

- 14 robot actions, 1 closing attempt.
- TCP height after closing: 0.4250 m; after final lift: 0.5216 m, a 9.66 cm rise.
- RGB showed the blue cube rising with the gripper and remaining held.
- Lift ended at simulation time 219.27 s; a stability image at 257.26 s showed
  the cube still held after 37.99 s.
- No object truth measured exact cube lift; 9.66 cm is the proprioceptive TCP rise.
- Original-speed recording continued to approximately 290 s, including closing,
  lifting and the complete hold. Camera switching did not affect physics.

This was one success, not a success rate across layouts or a guarantee for every grasp.

## Retained artifacts

Episode: `runs/20261019-222926-883522/`.

- `success-realtime.mp4`: from second 150 to the end of the complete recording,
  original speed, 140.27 s; starts with open fingers, then closing/lift/hold,
  without splicing or acceleration.
- `recording-01.mp4`: complete 290.27 s original-speed recording.
- `policy.jsonl`: policy-visible requests, robot feedback and RGB paths,
  separate from internal truth logs.
- `public-summary.json`: derived only from robot feedback/action counts in `policy.jsonl`.
- `rgb-0015-*.png`, `rgb-0016-*.png`: two views at hold start and about 38 s later.

## Historical usage boundary

At this date, `Launch Demo.command` and `uv run robofrontier` used NoSlip by
default. The original baseline required `--config config.json`. Human/GPT
comparisons had to use the same settings; old failures could not be pooled with
new-configuration results. Use the current README for today's benchmark and
explicit demo entry rather than assuming those historical defaults still apply.
