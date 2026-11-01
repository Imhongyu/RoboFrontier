# Post-failure slip diagnosis

2026-10-19. This offline diagnosis used simulation ground truth and contact
forces. It was separate from the earlier RGB policy actions and did not change
the three previous failures. The formal configuration, original recordings and
window settings were unchanged during diagnosis. The user subsequently requested
NoSlip and a successful recording; that separately versioned validation is in
`noslip-validation-20261019.md`.

## Reproduction and outcome

The third post-close integration state and joint references were restored from
`runs/20261019-220952-187535/trace.jsonl` (sim time 425.03 s). The same
`Simulation.control()` replayed the following three lift actions.

```sh
uv run python scripts/diagnose_slip.py --case baseline
```

Two consecutive invocations reproduced the same result: after lift, the block
lost bilateral finger contact, the gripper closed to nearly zero aperture and
the block returned to the table. The assertion failure was the expected failure
reproduction signal.

Removing model-thinking pauses and executing the same three lifts consecutively
retained the block briefly; an additional 30 s hold caused a drop. Waiting time
therefore mattered. The older reference test held for only about 4.6 s and could
not establish the long-duration retention needed by this interaction.

Minimal timing reproduction:

```sh
uv run python scripts/diagnose_slip.py --case baseline --compact --hold-seconds 30
```

## One-factor comparisons

Each row restored the same post-close state and used the same actions, changing
only one factor. These compact-mode comparisons ended with a 30 s hold:

| Diagnostic configuration | Final drop? | Final block lift |
| --- | --- | --- |
| Original | Yes | About 0 cm |
| Sliding friction coefficient only ×3 | Yes | Back on table |
| Gripper position stiffness only ×4, with proportional target remapping | Yes | About 0 cm |
| Torsional friction parameter only ×5 | No complete drop, but continued downward slip | 3.91 cm |
| `noslip_iterations=10` only | No | 6.90 cm |

With the original real waiting intervals retained and an additional terminal
30 s hold, `noslip_iterations=10` still retained the block, at a final lift of
6.89 cm. The original configuration dropped it with the same waits. This supports
slow soft-contact slip as a key environmental factor in this reproduced case;
it does not establish reliability for every pose or grasp location.

```sh
uv run python scripts/diagnose_slip.py --case noslip_10 --hold-seconds 30
```

The contemporary interpretation of the [MuJoCo Modeling solver documentation](https://mujoco.readthedocs.io/en/stable/modeling.html#solver-settings)
was that soft-contact regularization does not guarantee perfectly stationary
sticking. NoSlip postprocesses friction dimensions and can reduce drift, but
is neither a zero-slip guarantee nor real-robot calibration evidence.

## Continued gripper effort

The controller continuously retained a closed position reference. It did not
send a single pulse and turn off, and it did not command constant force.

- `gripper_goal=0` persisted after close.
- `data.ctrl[7]` ramped from its current value to 0. Every later movement/wait cycle continued writing 0; only open changed it to 255.
- After the third close, initial effective sliding friction was 1.0. The measured normal contact-force sums for the two fingers were about 0.999 N and 0.998 N.
- Tendon actuator force was about -1.996 N. The upstream tendon transmission coefficient was 0.5 on each side; `forcerange=-100..100` was a limit, not a continuous 100 N per finger.
- Gripper control 0 meant a closed reference, not 0 N. Once the object was lost, the aperture and position error approached zero, and actuator force naturally did too.
- Quadrupling position stiffness raised initial contact force to about 3.9 N per finger, but the block still fell. Greater closing force alone did not resolve this case.

## IK and actual MuJoCo output

The entire trial used end-effector mode. The policy sent only XYZ increments
and durations, translated at entry into the same direction/speed requests as
the keyboard controls.

Every 10 ms, the controller advanced a small TCP target and ran damped
least-squares IK initialized from the nearby seven-joint reference. IK returned
seven target joint positions. After velocity, acceleration and position limits:

```python
data.ctrl[:7] = q_ref       # Seven joint-position references, rad
data.ctrl[7] = gripper_ref # Gripper closed=0, open=255
for _ in range(5):
    mujoco.mj_step(model, data) # Each step is 2 ms
```

All seven targets updated in one control cycle. Upstream position actuators
produced torque from joint errors and velocities; MuJoCo integrated the actual
motion. Execution did not overwrite `qpos` with the IK answer or schedule joints
one after another.

## Scope and follow-up

Artifacts are in `runs/slip-diagnosis/`. The script reproduces this recorded state
segment, rather than a general benchmark. Original failure signals and each
one-factor comparison were retained.

This diagnosis recorded findings without increasing friction or grasp force in
the original configuration. The subsequent NoSlip configuration was independently
versioned and passed a long hold plus RGB operation in one new layout, as
recorded separately above. More locations and poses still require testing.
Offline ground-truth replay success must not be counted as model success.
