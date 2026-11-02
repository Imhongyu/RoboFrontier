# Legacy plan: three-arm transport and autonomous work loops

This is the 2026-10-20/21 plan and its historical progress, not the current
36-task configuration or a new-run instruction. In particular, the READY/START
handshake described below belongs to that experiment. New unified runs use the
direct-START protocol. Consult the current [architecture](../architecture.md),
[runbook](../meta-runbook.md), assigned public task and
[collaboration skill](../../prompts/skills/robot-collaboration/SKILL.md).
The historical coordinating role was named `Coordinator`; current naming uses
Controller. The role descriptions below use Controller for readability without
renaming original session IDs or stored evidence.

## Historical progress

Task/algorithm work (A), physical reference work (B), and offline interaction
checks (C) were completed; the model comparison remained incomplete. Three-arm,
nine-block configuration, tool-boundary inbox batching, `wait_events` and optional
nonblocking actions were connected. The engineering report is a retired artifact
at `../runs/autonomous-loop-engineering-20261020/report.md`. This phase kept the
three existing Panda robots and did not add a fourth arm.

Trial04 was sealed after a user-requested pause without completing the task.
The retired `../runs/trial04-efficiency-audit-20261020/report.md` identified batch
barriers, tool intervals and stale notes. Targeted fixes in
`../runs/efficiency-fixes-20261020/report.md` added timestamps/independent execution
facts, optional same-return delivery of results and images, and a total agent
waiting deadline. Trial05 still waited for handover conditions before preparing
its own region. The retired `../runs/trial05-concurrency-audit-20261020/report.md`
identified dependency/authorization granularity. Its process exited after the
user paused it and was recorded as interrupted.

The rules revision in the retired
`../runs/dependency-boundaries-20261020/review.md` changed only the skill and
role/communication guidance: conditions attached to actual dependent steps while
preserving authority, safety and preparation-value constraints. It changed no
harness and started no experiment. A short behavioral test was still needed;
text inspection could not demonstrate better parallelism.

On 2026-10-21, paper planning showed that the model used explicitly supplied
independent spaces/dependencies. This was not closed-loop speed evidence.
General motion-evidence rules, `robot_model` and `check_motion` were added.
The last performs read-only, finite-horizon nominal cross-arm sampling. It does
not execute candidate actions or cover continuous time, payload, table contact
or dynamics errors. This work was offline engineering, not old-world recovery.

Trial06 used the new interface and again exhibited global serial execution. It
was paused/sealed at the user's request without completing nine goals. The
retired `../runs/pipeline-coordinator-nine-20261021-trial06/private/outputs/efficiency-audit/report.md`
recorded zero transport overlap, single-arm checks and authorization gaps.
Input changes in `../runs/coordination-objective-fixes-20261021/report.md` added
only task-efficiency/simulation context, resource-exclusion scope, teammate
evidence and grouped decisions. No new behavioral improvement was demonstrated.
The next proposed step was short real transport rather than another full trial.

READY's existing `robot_facts` startup context was also expanded. The retired
`../runs/robot-facts-context-20261021/report.md` recorded actual base/TCP bounds,
capability summaries, a shared skill and a shorter coordinating prompt. No new
session or physical trial established a model improvement.

## Evidence and the proposed comparison

Trial02 and Trial03 completed all six goals but had zero overlapping two-arm
transport. The retired reports are:

- `../runs/pipeline-coordinator-20261020-trial02/private/outputs/report.md`
- `../runs/pipeline-coordinator-20261020-trial03/private/outputs/report.md`

After a policy update, messages changed from 57 to 42 and coordinating-role
turns from 56 to 41, while wall time changed from 20m44s to 26m52s. Prompt text,
wake frequency and peak concurrency were not evidence of greater efficiency.
One sample per condition supported no general causal conclusion.

The proposed checks separated whether the environment provided usable pipeline
windows from whether an agent anticipated/prepared work and exploited them.

## Fixed three-arm task

Origin was defined by the initial region; passing through another region did
not change origin. Initial stock and final slots were separate, so a local part
still required a pick/place.

| Arm | Initial stock | Three final slots | Origin requirement |
| --- | --- | --- | --- |
| A | Three red blocks | One red, two green | One local, two from C |
| B | Three blue blocks | One blue, one red, one green | One local, one from A, one from C |
| C | Three green blocks | One red, two blue | One from A, two from B |

Color encoded initial origin. There were no patterns, stacks or assemblies.
Reachable shared table areas permitted temporary placement chosen by policy.
No transport order, fixed handover point or automatic transport program was
prescribed. A free shared region, an empty gripper and a finished order remained
different facts.

The reproducible search in `scripts/check_transport_schedule.py` used 19
pick/place operations: local 2, A-to-B 2, A-to-C 3, B-to-C 4, C-to-A 6 and
C-to-B 2. Each operation had equal-duration pick-and-clear and place-and-clear
phases: 38 serial slots versus an achievable optimum of 16. Arm A/B/C workloads
were 10/16/12 phases; B's 16 gave a matching lower bound. Shared-area capacity
of either one or two parts could achieve 16.

This resource model assumed successful grasps, full-arm clearance after each
phase and separable motion in independent regions. It omitted real trajectory,
collision, inference, communication and observation costs. It did not promise a
physical 2.375-times speedup.

## Role autonomy and authority

- Meta managed environment, versions, monitoring, fixed transport/necessary
  continuation and audit. It selected no parts, assigned no policy work and
  controlled no robot.
- Controller maintained rolling global plans, assignments and authorization
  scope, and could plan while workers acted. It chose when to continue, wait or
  end its own turn.
- Hierarchical workers anticipated local work, executed within authority,
  prepared independent steps and proposed improvements through Controller routing.
- Peer workers identified needs, negotiated priority and maintained commitments
  directly with affected teammates. They did not await Meta assignments or need
  every peer's vote on every step.

The plan retained one message format and the
[shared communication principles](../../prompts/skills/robot-collaboration/references/communication.md).
Agents chose plans, anticipation depth, waiting dependencies and check deadlines.
The harness did not interpret business meaning or produce task schedules.
Ending a reply did not leave the team. Ordinary waiting did not justify immediate
fault recovery; saved continuation work, relevant events or a deadline did.

Both modes let every agent choose continued work, event waiting or saved-state
turn completion. The harness supplied reliable continuation without choosing the
cadence. In the hierarchy, effective authorization could cover multiple actions;
a condition-change report was not inherently another approval request. New
approval depended on scope and actual changes, not a mandatory per-object ritual.
Peers negotiated commitments for supply, relay, spatial occupancy and changed
plans with affected workers, without a coordinating role or unrelated voters.

An advance plan/authorization did not automatically execute. Conditional action
queues were deferred: after an event, the agent checked conditions and issued an
action, so model response cost remained.

## Minimal interaction changes

The historical proposal allowed multiple decision cycles inside one native turn
without requiring either one reply per cycle or one endless turn. Bounded event
batches arrived at tool returns or explicit reads. New messages queued during
processing instead of steering each one or cancelling a physical tool.

Optional `wait_events` waited for relevant messages, execution events or an
agent-chosen check deadline. It did not block the simulation thread or hold a
long database transaction. Existing IDs, receipts and deduplication protected
the read-then-sleep wake race. Saved notes/continuation restored missing context
without forcing a complete reread of history/images on every turn.

For this historical experiment only, the existing READY/START gate remained:
it required READY plus actual idle. Entering an active wait before START could
deadlock that handshake, so autonomous loops began afterward. This is superseded
for new direct-START runs and must not be copied into their startup prompts.

Optional `wait:false` let a worker plan/communicate while its arm moved. It kept
original action IDs, same-arm exclusion and explicit status. Running could not
be cached as completed, unknown results could not be replayed automatically, and
observation/communication did not authorize a conflicting second arm action.

Automatic conditional language/actions remained out of scope. No private object
truth released a natural-language condition. Independent background scheduling
had not gained write authority over Desktop sessions; Meta's fixed bridge could
carry the existing connection but did not prove continuation after its own host
exited. The plan reused the established native session/model framework.

## Proposed implementation and acceptance order

| Stage | Artifact and acceptance |
| --- | --- |
| A: task/algorithm | New task, origin/count/color conservation, reproducible resource search and witness replay with explicit model assumptions |
| B: physical feasibility | Three slots per arm; stock/staging reachability, gripper space and full-arm paths; a reference executor using the same action interface completes the order with real transport/restocking overlap |
| C: offline interaction | Synthetic sessions/executors check bounded batches, wait races, deadlines/re-wait, resume after turn end, busy/idle, unknown actions, authority, START and cleanup; unimplemented tools must not appear in runnable role instructions |
| D: real same-task comparison | Fix three-arm task, physics/observations/controls/model; compare old turn cadence with autonomous loops; request and verify Luna/xhigh; let agents choose order/authorization |
| E: topology comparison | Compare hierarchy and peers on that same task/tools; add single-agent later rather than compare architectures on different tasks |

The reference executor only demonstrated that environment/interfaces permitted
parallel work. Its schedule was not placed in policy prompts or treated as a
time target guaranteed to an equally informed LLM. Researchers could use
engineering truth for verification; policy retained public initial information,
RGB, proprioception and execution feedback without dynamic object truth.

A/B design and C interaction engineering could proceed separately. Real-agent
experiments required both acceptances first. One pilot diagnosed problems;
repetition and changed layouts were needed for stronger conclusions.

## Required evidence and interpretation

- Nine goals, initial origins, release and final clearance; independent evaluation
  separate from agent claims.
- START-to-team-finish wall time, each arm's actions and failures/retries/useless
  moves; action completion was not proof of grasp success.
- Actual action overlap, separately for local/transport phases; distinguish
  parallel model thinking, peak concurrent actions and sustained transport overlap.
- Message creation-to-delivery-to-decision/authorization-to-next-action latency;
  queries, repeated confirmations, anticipation and rejected requests. Do not
  attribute all stillness to the dispatcher.
- Reasoning/observation/tool costs, video frame loss and trimming error; freeze
  source, prompts, skill, tasks and parameters per run.
- Cleanup races: Trial03 rejected C's completion report after team finish. This
  was not an authority or physical failure and could not be silently omitted.

The [architecture](../architecture.md) assigned one authoritative SQLite runtime
state and one note per role, with fixed inputs and retained evidence. Old runs
were neither migrated nor rewritten. Physical restart recovery remained outside
this phase. The intended order was to prove safe executable parallel work, then
assess whether agents used it. B was the workload bottleneck; reasonable A/C
idle time was not failure. Keeping every arm permanently busy was not the goal.

## Historical exclusions

This phase added no robots, degrees of freedom, VLA, complex objects or multiple
task families. It added no hidden planner, automatic conditional language,
large message taxonomy, vector memory or duplicate plan/todo stores, and did
not first rebuild an independent Desktop scheduler. Four-arm bidirectional
batch transport was deferred as a later family extension.
