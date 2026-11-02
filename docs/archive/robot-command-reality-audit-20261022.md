# Robot parameters and the Franka hardware interface: historical audit

Status update, 2026-10-23: READY's `robot_facts.control_profile` explicitly lists
pose/joint targets, aperture/grasp modes and parameters, along with unavailable
independent velocity, torque/end-effector force, impedance, homing, calibration,
collision-threshold and some mechanical-feedback interfaces. Synchronized
submission and geometry screening are software capabilities. Software speed and
workspace limits do not establish the complete hardware capability boundary.
No calibrated physical driver or mechanical model is claimed. The body below is
an early audit snapshot, not the current agent tool reference. READY here is a
historical capability entry; new benchmark startup follows the current protocol.

Implementation follow-up: after the pre-grasp-v2 audit below, the shared multi-arm
controller gained `gripper.mode=grasp`, requested force of 30..70 N, width
tolerances and explicit drive feedback; total aperture speed was limited to
0.10 m/s. Position mode remains available. Continuous end-effector force control
remains unavailable. See the [current tool reference](../../prompts/skills/robot-collaboration/references/tools.md)
for behavior. Related validation and Oracle physics records are in the ignored
`runs/beam-handoff-grasp-20261022/`. This is not a completed hardware calibration.

Audit date: 2026-10-22. Scope: then-current Panda/Franka Hand task actions, the
eight-arm beam scene, original Menagerie MJCF gripper and existing Oracle lift
records. The audit changed no tools, skills, prompts, scenes or actuator
parameters and ran no new handover experiment.

## Findings at the audit date

1. Pose/joint targets, motion speed, gripper aperture and opening/closing speed
   have hardware counterparts. The simulated controller was not a completed
   physical-driver adaptation.
2. Franka Hand provides a requested grasp-force argument, `Gripper::grasp.force`.
   The project then lacked that grasp mode and used original MJCF position control.
3. Requested grasp force, controller output limits and collision thresholds are
   different quantities. Renaming MuJoCo `forcerange` or a collision threshold
   to `force_n` does not implement physical grasp-force control.
4. The previously observed approximately 2.25 N was tendon drive force in that
   simulated grasp. It was not the Hand's rated gripping capability and could
   not be compared directly with manual values without defining transmission.

## Official evidence retained from the audit

- [Franka Hand manual 220010/1.2/EN, page 10](https://download.franka.de/documents/220010_Product_Franka%20Hand_1.2_EN.pdf#page=10):
  adjustable continuous grasp force of 30–70 N, 80 mm stroke and 50 mm/s per
  finger. These are that manual version's specifications, not universal limits
  for every gripper or firmware.
- [libfranka Gripper](https://frankarobotics.github.io/libfranka/0.20.4/classfranka_1_1Gripper.html):
  `move` takes aperture/speed; `grasp` adds force and two width tolerances. Its
  width is the expected object size, not "close to zero and accept any obstacle."
- [GripperState](https://frankarobotics.github.io/libfranka/0.20.4/structfranka_1_1GripperState.html):
  standard feedback includes aperture, calibrated maximum aperture, `is_grasped`,
  temperature and time, without per-finger object identity or measured normal force.
- [FCI overview](https://frankarobotics.github.io/docs/overview.html): joint
  position/velocity, Cartesian pose/velocity and joint-torque modes are executed
  by the real-time control layer.
- [Control interface requirements](https://frankarobotics.github.io/docs/robot_specifications.html):
  trajectories also have acceleration/jerk constraints. Simulation speed limits
  do not replace them; FR3-specific figures are not treated as old Panda ratings.
- [Robot configuration](https://frankarobotics.github.io/libfranka/0.20.4/classfranka_1_1Robot.html):
  impedance, TCP/frames, load model and collision behavior have separate settings.
  A load model changes compensation assumptions, not actual object mass;
  collision thresholds change detection triggers, not requested gripper force.
- [MuJoCo general actuator](https://mujoco.readthedocs.io/en/stable/XMLreference.html#actuator-general):
  `forcerange` clamps an already computed actuator force.

## Parameter classification at the audit date

| Field/configuration | Hardware counterpart and audit judgment | Recommended agent authority |
| --- | --- | --- |
| `move.target_m`, `delta_m`, `quaternion_wxyz` | Cartesian motion/trajectory interface; not an instantaneous pose jump | Ordinary actions; control layer generates bounded trajectories |
| `joint_rad`, `joint_speed_rad_s` | Joint-motion counterparts; 0.9 rad/s was a project limit, not a Panda rating | Select within configured ranges |
| `speed_m_s`, `angular_speed_rad_s` | Meaningful motion-speed choices; TCP 0.005–0.15 m/s was software configuration | Retain; hardware adapter checks actual model constraints |
| `gripper.width_m`, `state` | Physical aperture control; 0–0.08 m corresponded to the reviewed Hand stroke | Retain; use actual fingertips and homed `max_width` |
| `gripper.speed_m_s` | Hardware opening/closing speed; project field meant total aperture rate | Align units, definitions and range with the driver |
| Then-current 0.16 m/s maximum aperture reference | Symmetric fingers imply 80 mm/s each, above the reviewed 50 mm/s rating; load may lower actual speed but does not align the reference limit | Correct later; default total aperture 0.08 m/s did not exceed that figure |
| Proposed `force_n` | Requested physical grasp force; tool then lacked the field/mode | Expose after implementation and verification within hardware limits |
| `epsilon_inner_m`, `epsilon_outer_m` | Grasp-width acceptance tolerances, not adhesion, pose correction or force amplification | Provide defined ranges/defaults in grasp mode |
| `forcerange`, `ctrlrange` | Simulated actuator output/input bounds, not equivalent to `grasp.force` | Fixed calibrated drive configuration, not an action increasing rated capability |
| XML `gainprm`, `biasprm` | Simulated motor/position-servo parameters, not public Hand grasp arguments | Engineering calibration; agent cannot edit MJCF |
| Joint/Cartesian impedance | Available on hardware; not arbitrary simulated gain edits; no corresponding mode was exposed | Define separately when needed; do not substitute for grasp force |
| Hard joint limits, rated speed/torque, maximum aperture | Device/installation constraints; software may tighten them | Keep fixed; XML edits cannot establish stronger hardware |
| `setLoad` mass/COM/inertia | Must describe the actual payload; differs from changing MuJoCo `body_mass` | Model configuration; incorrect calibration cannot reduce real weight |
| Contact friction and beam mass/inertia/dimensions | Object/surface properties; changing material or object defines a new scene | Freeze task physics |
| `noslip_iterations`, `timestep`, `solver`, `solref/solimp` | Numerical simulation/contact settings, not ordinary hardware actions | Engineering settings, unavailable to task agents |
| `stop` | Has a physical counterpart; controlled braking/holding is neither an emergency stop nor automatically identical to `Gripper.stop` grasp consequences | Define driver holding/release semantics |
| `check_motion` | Software calculation on a robot model, not new hardware capability | Optional computation; no promise of physical whole-scene collision freedom |

At the original audit date, `robofrontier/robot_control.py` validation/start/control
lacked a force field. Motion, speed and state were reasonable abstractions, but
physical hardware still required real-time trajectories and constraint checking;
a 50 Hz MuJoCo servo loop could not simply be connected to FCI. The later status
update above supersedes that historical statement about the field's absence.

## Hardware features not exposed to the agent at the audit date

| Capability | Gap and purpose |
| --- | --- |
| Grasp force and width tolerances | Most direct Hand interface gap; distinguish from aperture `move` |
| Gripper homing | Calibrates maximum aperture for installed fingers; simulation used configured initial state |
| Direct joint/Cartesian velocity commands | Position targets plus speed were not independent continuous velocity modes |
| Joint torque/contact control | FCI provides torque control; adding a force field alone does not implement end-effector force control, which differs from Hand grasp force |
| Joint/Cartesian impedance | Hardware configuration existed without a defined verified agent tool |
| TCP/stiffness frame | Tool/frame calibration; not motion of the actual structure |
| Load model | Payload mass/COM/inertia description; cannot make the object physically lighter |
| Collision thresholds | Contact detection configuration, not grasp strength or rated capability |
| Joint torque/external force and torque estimates | Then-current observe exposed joint positions/velocities, TCP and aperture, not these mechanical-feedback fields |

Whether to expose each feature is a separate engineering choice; this audit did
not request implementing everything at once. Standard Hand state has no exact
normal-force measurement for each contact. Oracle MuJoCo contact truth cannot
be presented as an ordinary physical-gripper sensor.

"Unavailable on hardware" also needs precision: NoSlip iterations and contact
solver parameters are numerical settings; mass, friction and inertia are real
physical properties that cannot be rewritten through a robot command. IK damping,
step sizes and planning budgets are controller-software choices, not extra
hardware capability.

## Does raising a force limit increase force?

A controller computes output before the output limit clamps it. Raising a limit
can increase output only if the old output was clipped and the controller asks
for more. Motor drive without object contact is not the object's gripping force.

The original position servo, with static zero closing input, produced tendon
force approximately −100 times tendon length. At the previously measured
22.49 mm tendon length, that was approximately −2.249 N.

More fully, the unclipped model was
`F_raw = 0.01568627451*u - 100*L - 10*L_dot`. Closing input `u=0`, static
`L_dot=0`, and `L≈0.02249 m` gave `F_raw≈−2.249 N`, then `forcerange` clamped
that value. Here L is fixed-tendon length and each finger transmission coefficient
is 0.5. Tendon drive and one-/two-finger contact-force values are not interchangeable.

Friction does not enter that fixed-pose actuator calculation. It influences
available tangential contact load, bounded by normal force and friction. Raising
friction can improve slip resistance but cannot turn the same-pose 2.249 N drive
into a larger value. Replacing physical pads and requesting grasp force are
likewise different actions.

An independent in-memory model copy, at identical pose/input, produced:

| Symmetric actuator force limit | Absolute tendon drive output |
| --- | --- |
| 1 N | 1.000 N |
| 2 N | 2.000 N |
| 100 N (original model) | 2.249 N |
| 200 N (counterfactual) | 2.249 N |

The 100/200 N figures tested MuJoCo clamping semantics; they were not recommended
Hand commands. Original scenes were unchanged and no physics trial was started.
The retained local reproducer is
`runs/beam-handoff-oracle-20261022/audit_force_limit.py`, with
`force-limit-audit.json` beside it.

Increasing `forcerange` therefore did not solve that weak-grasp case. Increasing
requested grasp force required an actual grasp-force mode. Contact force also
depends on transmission, contact, drive capability and tracking error. A
`force_n` command cannot stand in for a measurement.

## Proposed minimum interface at that date

Separate aperture movement from grasping: aperture/speed for the former;
expected object width, speed, grasp force and width tolerances for the latter.
Use the official force meaning instead of treating `force_limit_n` as a direct
Franka mapping.

The reviewed Hand ranges could seed a configuration for verification, with the
specific gripper, fingertips, firmware and units fixed. A bounded drive/grasp
controller would accept ordinary agent targets; calibration would compare
requested force, simulated tendon output and fingertip contact response.
Supporting a grasp command would not guarantee every grasp or replace lift and
handover checks.

Expose only feedback available on the corresponding hardware. If force sensing
is unavailable, mark it unavailable; do not return simulated per-contact normal
force as a physical sensor. Earlier Oracle contact truth remains engineering
diagnostics.

The original audit implemented none of those proposals and did not rerun a
successful trial with a new force controller. Its conclusion was an interface/
model alignment gap, not proof that a Franka arm cannot transport a 1.458 kg beam.
