# VLA action spaces and RGB/Oracle information: primary-source review

Date: 2026-10-19. This is a dated research/design note, not a new simulation or
an updated upstream survey. Each cited paper/repository describes a particular
implementation; its choices do not apply to every vision-language-action model.

## Verified examples

| System | Model input | Action representation | Primary evidence |
| --- | --- | --- | --- |
| RT-2 | Camera image and text task | End-effector 3D translation delta, 3D rotation delta, gripper and termination flag | [Original paper §3.2](https://arxiv.org/html/2307.15818v1#S3.SS2) |
| Original OpenVLA | Image and language instruction | 7-dimensional robot action; training data filtered for single-arm end-effector control, not seven joints | [Paper Fig.2, §3.2–3.3](https://arxiv.org/html/2406.09246v3) |
| π0 paper | Multiple RGB views, language and joint-angle proprioception | Joint positions for the authors' internal data; mixed training also includes different action representations | [Paper §IV](https://www.physicalintelligence.company/download/pi0.pdf), [author Kevin Black's official repository explanation](https://github.com/Physical-Intelligence/openpi/discussions/302) |
| Later openpi-related models | Defined by the particular model and data adapter | Authors describe joint, world-frame end-effector and end-effector-relative actions; these are not uniformly joint outputs | [Official author discussion #302](https://github.com/Physical-Intelligence/openpi/discussions/302) |

OpenVLA's seven dimensions commonly mean three translation, three rotation and
one gripper component. RT-2 additionally has a termination flag. A seven-DoF
robot and a seven-dimensional action vector are distinct concepts. Conclusions
about original OpenVLA image inputs do not automatically apply to later
extensions such as OpenVLA-OFT.

The π0 paper explicitly includes joint angles in observations. The official
ALOHA adapter defines state from both arms' angles and grippers and supplies it
alongside images: [aloha_policy.py](https://github.com/Physical-Intelligence/openpi/blob/main/src/openpi/policies/aloha_policy.py).
A visual robot therefore need not restrict both its model and its lower-level
controller to camera information alone.

These primary implementations do not share a single action space. End-effector
and joint commands are both ordinary designs. Report the actual representation,
frame, units, frequency, normalization and actuator rather than interpreting a
"VLA standard" as a requirement to output every motor command.

## IK and privileged object state are independent questions

LeRobot documents joint and end-effector representations and URDF-based
`RobotKinematics`, `ForwardKinematicsJointsToEE` and
`InverseKinematicsEEToJoints`: [Action Representations](https://github.com/huggingface/lerobot/blob/main/docs/source/action_representations.mdx).
Its kinematic conversion uses the robot model and joint state, not simulated
cube ground truth.

The following is a system-design interpretation of that evidence:

1. **Perception/decision** determines where a cube is, which cube to choose and
   where the end effector should move. A visual policy decides from images;
   an Oracle may receive precise object coordinates.
2. **IK** determines joint configurations for a desired end-effector pose and
   known robot geometry. Numerical solvers commonly initialize from current
   joint configuration to find continuous, reachable solutions.
3. **Low-level control** tracks references using measured joint feedback. A model
   that does not receive joint state can still use a controller that reads encoders.

RGB and Oracle policies can consequently share the same IK. Their distinction
is the information used to choose targets/actions. IK does not recognize a blue
cube or replace a wrongly estimated target with the correct cube coordinate.

For physical hardware, Franka's `Robot` API supports CartesianPose,
CartesianVelocities, JointPositions and JointVelocities; `RobotState.q` is
measured joint position in rad: [Robot API](https://frankarobotics.github.io/libfranka/latest/classfranka_1_1Robot.html),
[RobotState API](https://frankarobotics.github.io/libfranka/latest/structfranka_1_1RobotState.html).
An official example sends Cartesian pose goals to the interface to solve IK:
[joint_impedance_control.cpp](https://github.com/frankarobotics/libfranka/blob/main/examples/joint_impedance_control.cpp).
These interfaces do not require the grasped cube's true position. A real robot
uses its known structure and its own measurements without knowing the whole world.
See also the [official FCI overview](https://frankarobotics.github.io/docs/doc/libfranka/docs/overview.html).

"Move down 2 mm after viewing an image" need not explicitly reconstruct the
whole world. Recovering exact cube coordinates from one RGB image requires
visual estimation, calibration, depth, multiple views or task priors; it is not
an IK capability. A monocular feedback loop does not guarantee exact 3D recovery
in arbitrary scenes.

## End-effector control does not always mean IK

Robosuite distinguishes WholeBodyIK from OSC_POSE. The former converts
end-effector targets into joint-angle targets; the latter computes joint torques
from end-effector error and the robot model: [controller documentation](https://robosuite.ai/docs/modules/controllers.html).
Showing that a VLA outputs end-effector actions therefore does not prove that
its controller uses a particular IK implementation.

## Recommendations for the early demo: design judgments

- Define RGB as **RGB plus the same robot proprioception**. Define Oracle as
  that information plus object position, orientation and attributes.
- Share end-effector deltas, gripper commands, IK and trajectory limits. Using
  joint control in one condition and end-effector control in the other changes
  two experimental factors.
- The RGB IK/controller must not read cube body poses, target sites or simulated
  depth. It may read robot geometry and proprioceptive joint state. The physics
  solver necessarily has full state; that does not expose it to the operator.
- Select proprioception explicitly by robot joint/site names. Do not pass the
  whole `qpos`, including free-object poses, to an RGB policy or its IK. Full
  state belongs to physics, the evaluator and logging.
- `move(dx,dy,dz)` and `grasp(object_id)` are different abstraction levels. If the
  latter queries object truth and plans a grasp internally, it bypasses visual
  decisions and cannot be presented as an ordinary RGB action.
- A pure-pixel policy without proprioceptive feedback is a separate condition.
  Declare whether the policy sees joints and whether its controller reads
  encoders; that differs from RGB versus an object-state Oracle.

## Verification outstanding at the snapshot date

Panda IK continuity, joint limits, physical contact, action scales and visual
operability still needed measurement. Real-robot papers using end-effector
actions do not establish that an untrained general GPT can grasp reliably.
Control-interface feasibility and model execution ability require separate checks.
