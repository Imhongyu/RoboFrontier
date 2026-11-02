> Historical archive. Current specification/status: [Transport task](../../tasks/transport.md).
> Merge procedure: [handoff](../plans/suite-v2/transport-merge-handoff.md).
> This record retains the original process and evidence.

# Nine-task Transport mathematical baseline

This work performed calculations only, without new physics trials.

The measured 1.68 speedup covered only F_slot2 and H_slot3 in twelve-arm L1.
F alone took 34.0s, H alone 46.8s and common settling 3.2s: ideal serial 84.0s,
independent parallel 50.0s; measured 83.98s / 50.10s.

## Uniform-unit resource model

Each grasp, handoff, placement or insertion costs 1 unit. Assumptions: the
supply's owning arm grasps, a target-region arm places, minimum ring hops,
no intermediate waits, holding occupies an arm and handoff occupies two arms.
These are calculation assumptions, not task permissions.

| Scale | N | H | Serial | Model-optimal parallel | Model speedup |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4 | 12 | 18 | 42 | 17 | 2.47 |
| 8 | 24 | 48 | 96 | 20 | 4.80 |
| 12 | 36 | 106 | 178 | 27 | 6.59 |

L1/L2/L3 have identical orders, so their uniform-unit models match. An integer
programming solver reported optimal schedules for all three groups, and those
schedules were saved. Physical optima also depend on alternative grasping arms,
direct handoff edges, joint trajectories, contacts and additional regrasping.

## Duration extrapolation: conditional-model simulation seconds

| Task | Serial | Parallel resource lower bound | Constructed schedule | Model speedup |
| --- | ---: | ---: | ---: | ---: |
| 4-arm L1 | 1183.0 | 479.7 | 545.1 | 2.17 |
| 4-arm L2 | 1010.6 | 419.9 | 471.9 | 2.14 |
| 4-arm L3 | 1005.6 | 418.6 | 469.8 | 2.14 |
| 8-arm L1 | 1877.3 | 434.8 | 534.4 | 3.51 |
| 8-arm L2 | 2175.0 | 452.2 | 608.9 | 3.57 |
| 8-arm L3 | 2423.4 | 551.7 | 670.8 | 3.61 |
| 12-arm L1 | 4010.0 | 642.0 | 901.5 | 4.45 |
| 12-arm L2 | 4741.2 | 744.7 | 1041.9 | 4.55 |
| 12-arm L3 | 4789.1 | 758.3 | 1051.0 | 4.56 |

These are not complete physical-task scores. Bounds constrain only this resource
model; actual execution may be slower, fail, or use a different faster strategy.
L2/L3 include unpassed actions, so these are not verified executable plans.
Some twelve-arm durations borrow eight-arm references; see the JSON provenance.

Data: runs/oracle/transport-r13-units-20261025/nine-task-math.json.
Recalculate: PYTHONPATH=. OPENBLAS_NUM_THREADS=1 .venv/bin/python runs/oracle/transport-r13-units-20261025/calculate_nine.py.

Historical page: http://127.0.0.1:56719/transport-r13-study/nine-math/index.html.

## Meaning of the eight unpassed categories

| Unit | Recorded reason | Boundary / alternative |
| --- | --- | --- |
| 4-arm L2 block ①: tabs upward | Lift passed; the candidate's final wrist pose failed screening, with link6/link7 near-table conflicts. | The same B_item1→B_slot1 passed after airborne transfer B→C before insertion. |
| 4-arm L2 block ②: lateral ① | Lift passed; no continuous carry/insertion route was found for the current single grasp. | This example is incomplete, without proving physical impossibility. |
| 4-arm L2 block ③: lateral ② | Another supply position/lateral grasp also lifted, but no final slot-entry route was found. | Joint-limit and collision-screening contributions were not individually isolated. |
| 4-arm L3 block ①: tabs upward | The top grasp could not connect to a screened insertion pose. | The same B_item1→B_slot1 passed spring-board insertion after regrasping. |
| 12-arm L2 cylinder ①: tabs upward | Lift passed; no direct insertion route was found while retaining this grasp. | The same H_item1→H_slot3 passed after airborne transfer H→G. |
| 12-arm L2 cylinder ②: lateral | Lift passed; no subsequent board-entry route was found for this side grasp. | This is not a failure to grasp; other grasps/branches still require comparison. |
| 12-arm L3 cylinder ①: tabs upward | This arm's direct insertion while retaining the grasp did not pass. | This does not exclude every regrasp/operator combination. |
| 12-arm L3: left cylinder present, then center insertion | Left placement was established; the second object had IK rejection and timeout. The latest side-grasp attempt produced actual H_hand/H_link5 self-collision. | This is a mechanical neighbor fixture, not a real order. Failure and unresolved H actions remain retained. |
