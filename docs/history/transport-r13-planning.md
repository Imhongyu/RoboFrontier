> Historical archive. Current specification/status: [Transport task](../tasks/transport.md).
> Merge procedure: [handoff](../plans/suite-v2/transport-merge-handoff.md).
> This record preserves the original process/evidence.

# Transport R13: grasp continuation, forward recovery and independent progress

Scope: minimum Transport units and a twelve-arm L2 two-goal comparison.
This ran neither nine complete orders nor the Codex fork stopped by the user.
Oracle was an engineering reference using private geometry and actual control
commands, not a GPT policy trial.

## Corrections

- `robofrontier/suite/oracle.py`: retained old error prefixes and added rejection counts for approach IK, near-socket IK/clearance, direct carrying and elevated carrying. Finite search failure no longer produced only a height error.
- `robofrontier/suite/transport_unit_motion.py`: included insertion-pose constraints in grasp selection, adding oblique candidates such as 30° and 45°. Ranked source/target palm clearance; cheap source pruning preceded insertion/open/withdrawal/approach/lift checks. Candidates still required execution; IK endpoints were not passes.
- `robofrontier/suite/transport_socket_motion.py`: checked full arm, carried object, continuous IK branches and sampled joint edges in an independent planning copy. Finite descent sampling was 2 mm, rotation 0.025 rad and joint edges 0.01 rad, without continuous-collision/contact-dynamics certification. Pre-execution screening also covered actual fine adjustments.
- Reread object/gripper relations and board pose after carrying. One actual side grasp showed about 4.1° relative rotation and 1 mm translation, invalidating indefinite reuse of the pre-grasp rigid relation.
- Handoff candidates could screen receiver-grasp insertion/open/withdrawal. After sender release/withdrawal, the actual receiver continued insertion, without mandatory table storage or sender regrasp.
- `scripts/verify_transport_units.py`: allowed changing to handoff in the same scene only with known-idle actions, actual support, no violations and real load/board separation. Geometric candidates selected receiver/grasp angles/points. Only search failure before any action for that candidate allowed another candidate family.
- Recovery eligibility used actual object/board geometry distance, not height above an infinitely extended board plane. Inserted/near-wall objects, uncertain actions or prohibited contact did not trigger automatic withdrawal, replay or history clearing.
- Failed opening that missed target aperture remained failed. Withdrawal could be screened/executed only after known feedback and cancellation of force holding. Planning left the supported object in place, then checked actual separation/final seating. A sufficiently wide aperture was not relabeled successful opening.
- `scripts/verify_transport_parallel_unit.py`: added ready queues for independent single-arm sequences. An arm continued after its own action/wait rather than waiting for the other arm's batch. One physics thread remained. This executed reviewed independent programs, without automatic assignment, two-arm handoff or full-task planning.

Changes were confined to engineering Oracle/validation drivers, without new MCP,
database, agent communication protocol or permission system. Generic Prompt/Skill
received no private grasp points or task solution.

## Resolution of the original eight gaps

A pass meant one actual segment for its specified target, not a whole order.
Handoff examples were not counted as same-arm single-grasp insertion.

| Unit | Verified strategy | Scope |
| --- | --- | --- |
| Four-arm L2 upward-tab block | B lifts, hands to C, C inserts directly into B_slot1 | Original order identity |
| Four-arm L2 lateral block ① | 45° oblique grasp, same-arm direct insertion | Original order identity |
| Four-arm L2 lateral block ② | 45° oblique grasp, loaded joint speed cap 0.18 rad/s, same-arm insertion | Original order identity |
| Four-arm L3 upward-tab block | B→C handoff, then C inserts | Original order identity |
| Twelve-arm L2 upward-tab cylinder | H→G handoff, then G inserts | Original order identity |
| Twelve-arm L2 lateral cylinder | 45° oblique grasp, same-arm insertion | Original order identity |
| Twelve-arm L3 upward-tab cylinder | Receiver inserts after handoff | Original order identity |
| Twelve-arm L3 left cylinder present, then center insertion | Establish actual left object, select a continuable H grasp/joint branch, insert center | Mechanical fixture; identities differ from original order and earn no order score |

Candidate searches for lateral block ① and the lateral cylinder took about
1.3 s and 3.3 s respectively. These were neither full-task times nor general
search caps. Lateral block ② once hit its own palm after fast carrying, then
passed at a lower legal action speed. Friction, force limits and acceptance
were unchanged.

The previously passed four-arm L3 side-laid block was also rechecked: a new
oblique grasp/direct insertion passed while retaining one
`Requested aperture exceeded` failure. Screened withdrawal then verified actual
separation/stable seating. The failed command was not rewritten as completion.

## Twelve-arm L2: identical goals and per-arm commands

Goals: F_item2→F_slot2 and H_item2→H_slot3. Three worlds began at identical
standard initialization, excluding common initial homing but including the same
terminal settling. Original acceptance simultaneously accepted both goals,
with zero violations/unknown actions.

| Execution | Segment simulation time | Actual two-arm motion overlap | Relative to serial |
| --- | ---: | ---: | ---: |
| Serial | 100.92 s | 0.00 s | 1.00× |
| Batch parallel | 60.72 s | 34.72 s | 1.66× |
| Independent arm progress | 52.64 s | 40.82 s | 1.92× |

Independent progress saved 8.08 s versus batch waiting. Frozen programs took
49.44 s and 48.24 s, plus common terminal 3.20 s, giving the independent reference
`max(49.44,48.24)+3.20=52.64 s`. This concerns these two programs only, without
full-task global optimality. Batch synchronization, arm-motion concurrency and
multi-agent reasoning concurrency are distinct.

## Physics, recovery and recording boundaries

R13 environment files, object dimensions/masses, board positions, materials,
2 ms steps, pd1000-v1 and original acceptance were unchanged. Hashes matched all
1,197 frozen environment files. Loaded-speed changes were legal reference-program
parameters through the existing interface.

All actual segments began at declared standard initialization; only ordinary
robot commands changed the world within a segment. Failed worlds were neither
rolled back nor score-stitched, and uncertain actions were not replayed.
Failed attempts stayed independently sealed; later fresh starts were explicit
new attempts.

The 60 Hz float32 full-joint stream retained all objects, arms and spring-board
motion. Every chunk checked source, hash, initialization and timeline for offline
rendering/Factory import. This was not an exact physics-execution restart
checkpoint. This round performed no Factory migration.

## Full-task work remaining at that stage

Old complete `solve` still required declared fixed routes and could not directly
handle R13 without transfer boxes. Unit checks and two-goal queues did not prove
nine complete tasks.

The next phase should connect qualified recipes into actual job stages,
tracking object/arm occupancy, both handoff sides' readiness, target-board pose
and downstream exits. The same candidate/event logic should serve 4 / 8 / 12 arms
with broader candidates/reservations, without reintroducing whole-team batch waits.

L1 should compare actual carrying/handoff counts and receiver availability.
L2 should select receiver grasp/insertion joint branch along with route.
L3 should update board pose, neighbors and contact paths after load changes.
Resource schedules may choose only verified or explicitly unverified candidate
edges; combined motion and real execution still require checks.

Independent queues covered only single-arm programs with disjoint arm ownership.
Airborne handoff is coupled and cannot become two command streams without
handshake conditions. Full scheduling should separately verify safe shared-space
concurrency and A→B→C pipelines, without requiring all arms to begin holding objects.

## Evidence and tests

Run directory: `runs/oracle/transport-r13-planning-20261025/`. All attempts,
failures, source snapshots, chunks and three execution controls remained.
Final unified-code rechecks used `qualification-2/` and `final-executor-2/`;
passing recipes from different development stages could not be combined into
a claimed unified-version pass.

All eight final types passed under one executor snapshot, with zero prohibited
collisions/unknown actions: seven original-order goals and one mechanical
fixture. Four types used airborne handoff, three same-arm insertion and one
continuous operation with an existing neighbor. The fixture was not counted
as an original-order goal, nor handoff as single-grasp insertion.

The round contained 39 independent segments, including development failures,
two unified rechecks and three execution controls, with 27 local passes.
All chunks/timelines/standard initial states for 145,445 motion frames verified.
Control/acceptance fingerprints matched across segments and all 1,197 original
environment files stayed unchanged. Details: the run's `summary.json`.
Segments cannot be stitched into one complete task.

The 53 Transport planning regressions plus two environment/real-opening checks,
55 total, passed. They covered pre-execution rejection of an archived
self-collision, joint-branch jumps, intermediate collisions, blocking on uncertain
feedback, actual release verification, forbidding handoff during partial insertion,
airborne board-side recovery and fast-arm progress without waiting for slow arms.

Expanded environment tests exposed one existing Relay layout assertion expecting
`upper_semicircle`, while the frozen scene was `upper_arc_90_degrees`. It did not
call the changed Transport planner. This round changed neither Relay scenes nor
that historical assertion and did not claim a full-project pass.
