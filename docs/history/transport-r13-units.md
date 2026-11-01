> Historical archive. Current specification/status: [Transport task](../tasks/transport.md).
> Merge procedure: [handoff](../plans/suite-v2/transport-merge-handoff.md).
> This record preserves the original process/evidence.

# Transport R13: review, minimum units and parallel plan

Later engineering corrections/unified-code rechecks are in
[Transport R13 grasp continuation and independent progress](transport-r13-planning.md).
This preserves the earlier round; statements such as the 8 unpassed types
below are not final conclusions from the later rechecks.

The session independently executed this round under the user's request,
without resuming forks or running full tasks. R13 used 143×396 mm boards,
84 mm target markers and 36 mm clear marker spacing. Nine scene inputs,
2 ms steps, pd1000-v1, materials and original acceptance stayed frozen.

## Code and old-trace review

- R10 L1 four/eight/twelve-arm actual motion overlap was about 0.239%, 0.080%, 0.034%, mainly common initial homing. Transport was nearly serial; peak active-arm count did not establish transport parallelism.
- `deliver` and full-task loops synchronously processed orders/hops. Transfers placed on the table and regrasped. Default handoff cleanup could also make receivers store objects for regrasp by the original arm.
- Ring-route logs showed no example exceeding minimum hops for the same endpoints. Direction alone could not explain all inefficiency. Grasp/handoff redundancy, direction, receiver availability and subsequent reachability still required comparison.
- With R13 fixed transfer points removed, old full `solve` refused missing declared routes. Points were not reintroduced into scenes. New unit drivers proposed private handoff candidates; event scheduling for the complete executor remained future work.

## Minimum-unit outcomes

There were 49 independent physical segments, including serial/parallel controls,
covering 29 unit definitions. Specific frozen recipes passed for 21 types:
20 order-matching units and 1 mechanical-neighbor fixture. The remaining 8 types
were unpassed. Each of nine scenes had at least one local pass. Goal counts
across different worlds cannot be summed or inherited as whole-task success.

| Capability | Recorded outcome |
| --- | --- |
| L1 local direct placement | Four/eight/twelve-arm blocks and eight/twelve-arm cylinder examples passed |
| L1 direct placement after airborne handoff | Four/eight/twelve-arm blocks and eight/twelve-arm cylinders passed; the four-arm corner needed side grasp, receiver clearance and reduced loaded speed |
| L2 insertion after airborne handoff | Four/eight-arm blocks and eight/twelve-arm cylinders passed; the receiver retained the actual object into insertion, without table storage or sender regrasp |
| L3 insertion after airborne handoff | Block and cylinder examples passed; targets updated from actual board pose during insertion |
| Same-arm insertion from one grasp | Four-arm L3 side-laid block and twelve-arm L3 side-laid cylinder passed; finite candidates for other orientations still failed, without proving global physical impossibility |
| Left block present, then middle/right insertion | Both units passed, establishing the left block through actual actions and retaining both original order goals |
| Left cylinder present, then right insertion | Mechanical fixture passed; left identity differed from the order and was explicitly excluded from order completion |
| Left cylinder present, then middle insertion | Unpassed: IK rejection, timeout and H_hand/H_link5 self-collision occurred; failed collision and unresolved H action stayed retained |

Side-grasp candidates screened approach, grasp points and gripper/arm endpoints
at subsequent goals. Airborne handoff optionally screened later slot endpoints.
These were planning filters, not full-trajectory/dynamic-load guarantees.

## Actual serial/parallel comparison

Within the same R13 twelve-arm L1 scene, execute F_item1→F_slot2 and
H_item1→H_slot3. Separate runs started from identical standard initialization
and used exactly the same per-arm action sequences.

| Mode | Task simulation time, excluding common initial homing | Transport-motion overlap | Original acceptance |
| --- | ---: | ---: | --- |
| Serial | 83.98 s | 0 s | Both goals passed, zero violations/unknowns |
| Batch parallel | 50.10 s | 27.52 s | Both goals passed, zero violations/unknowns |

This minimum comparison was about 1.68 times faster. It demonstrated effective
physical parallelism through the existing batch interface, rather than full
twelve-arm-task speedup or multi-agent model performance. Source actions and
both measurements are in the run's `parallel/` directory.

## Route/concurrency draft, not executed

Adjacent arms initially formed a candidate ring, not a task-permission boundary.
Prefer minimum-handoff directions, breaking equal-length ties using receiver
reservations. Waiting created solely by draft reservations did not justify a
detour. Discovered feasible direct edges could skip unnecessary relays.
Four-arm L3 D→B gave one non-adjacent example, without generalizing to every
payload/scene.

The planning atom was one bounded object-transport chain. Reservations covered
all holding and both handoff participants, not just moving-arm time. Verify
receiver/downstream exit before pickup to avoid everyone holding objects in a
cycle. Initial pickup by every arm was not mandatory; receivers could prepare
safely empty-handed.

The conditional resource model below used measured macros at the same scale,
explicitly falling back to eight-arm references when absent. Other positions
still required extrapolation. It ran no full orders, omitted complete combined
trajectories/shared-space conflicts/perception/decision/communication costs
and did not prove optimality.

| Scale | Same-macro serial model | Conditional parallel draft |
| --- | ---: | ---: |
| 4 arms | 1183.0 s | 578.6 s |
| 8 arms | 1877.3 s | 549.1 s |
| 12 arms | 4010.0 s | 935.3 s |

Plan: `runs/oracle/transport-r13-units-20261025/parallel-plan.json`.
Plots use blue for grasp, orange for handoff and green for placement. Predicted
ratios are not measured MuJoCo speedups.

## Code changes and boundaries

- `transport_oracle_v2.py`: private candidate handoff centers, receiver grasp points/angles and optional later-goal screening. Retained old defaults to protect frozen R10 references; new units explicitly retained the receiver's object.
- `transport_unit_motion.py`: finite side-grasp/later-operation endpoint screening, without starting new physics worlds.
- `verify_transport_units.py`: independent standard initialization, budgets, original acceptance, real neighbor establishment, frozen provenance and 60 Hz full-state recording.
- `verify_transport_parallel_unit.py`: reused `Trial.execute` batches for the two-arm comparison. No multithreaded world writes, new MCP or persistent service.
- `plan_parallel.py`: a conditional scheduling prototype in this run directory, outside the generic Harness/Agent Skill.
- The 44 Transport reference regressions passed. R13 physics inputs were unchanged, control/acceptance hashes matched the old identical configuration and all physical processes exited.
- All chunks of 171,332 motion frames passed source/initial-state/time-monotonicity/2 ms checks. The 60 Hz stream supported offline reconstruction, not physics rollback checkpoints.

## Planned implementation sequence

1. Resolve the unpassed middle-cylinder contact segment: recheck wrist, self-collision and joint margin under actual load/board pose, changing grasp/operator if needed. High-hover checks alone, increased force or relaxed acceptance are insufficient.
2. Split qualified grasp/handoff/insertion into resumable small phases, with one physics thread handling ready actions through existing batch/nonblocking interfaces. Avoid synchronous full-order blocking or one world-writing thread per arm.
3. Before every phase, verify actual holding, receiver preparation, later insertion/withdrawal, and compare waiting, airborne handoff and storage. Avoid pointless homing/regrasping without demanding constant motion from all arms.
4. Integrate one/two physically independent job pairs before more combinations/full orders. This stage had not started in this round.

Engineering Oracle used private geometry/coordinates. Test recipes must not
enter future GPT Prompt/Skill automatically. Generic guidance may retain
look-ahead planning, clearance for later grasping and feedback-based replanning.

## Evidence entries

- Historical local report/videos: `http://127.0.0.1:56719/transport-r13-study/index.html`.
- Complete JSON, failures, source snapshots and chunks: `runs/oracle/transport-r13-units-20261025/`.
- Videos: `outputs/oracle/transport-r13-units/`, rendered offline from actual saved states. UNIT PASS was not a whole-task pass.
