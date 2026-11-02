# Three arms in a shared world: historical v1 trial

This records a completed legacy trial. Its Meta was the participant coordinator,
then called Coordinator (now Controller). Current engineering Meta and the newer
harness are described in the [runbook](../../meta-runbook.md). Commands and limits
below describe that trial, rather than the current default workflow.

The implementation used one MuJoCo process, one visible GLFW window, three Panda
arms, nine physical-contact blocks, independent IK/action state for each arm,
a directed tree mailbox, video and a timeline. It retained the Menagerie
actuators, original block friction and NoSlip=10, with no attachment or automatic
pick/place.

## Historical setup

```sh
uv run python scripts/create_pipeline_run.py runs/pipeline-NEW
uv run python -m robofrontier.pipeline --run-dir runs/pipeline-NEW
```

Startup printed a local URL and created each role's connection file. Global,
global_side and each arm's front/side views shared the same model and state.
Meta could not move/gripper; Workers could control only their own arms. Messages
were limited to Meta ↔ Worker.

The measured trial directory was `runs/pipeline-meta-20261020-trial01/`.
`runs/pipeline-meta-20261020/` held earlier engineering setup and previews and
must not be counted as a model trial.

## Engineering checks

```sh
uv run python scripts/verify_pipeline.py
uv run python -m unittest discover -s scripts -p 'test_pipeline.py' -v
```

The reference program used Oracle only in an independent temporary world for
engineering checks: all three arms physically grasped blocks concurrently, then
A placed and B regrasped. `runs/pipeline-preflight.json` records this check, not
a model score. Tests covered tree routing, Meta's motion permissions, batch
receipt/reply correlation, wait/wakeup markers and concurrent action acceptance
by different arms.

## Trial sessions and lifecycle

Four real Codex desktop sessions belonged to the roomscript2 project: one Meta
and three Workers. All requested gpt-6-luna / xhigh. Verification of actual
turn_context settings was saved in private/model-verification.json.

The research session created sessions through the Codex application interface
and checked actual active/idle state. After every participant reported READY,
research called START and notified Meta; Workers resumed according to Meta's
mailbox assignments.

During execution, research polled actual session state and the server's mailbox
and deadline checks. It resumed the original session only when idle. Results
for active Workers included their mailbox; Meta read accumulated messages on its
next turn. Native notifications from research described only mailbox/deadline
events. They supplied no assignment or motion advice; participant agents
created their own business messages.

**This was controlled desktop scheduling by the research session, rather than
a persistent daemon that could operate Codex independently of that session.**
private/driver.jsonl records actual state and wakeup evidence. The desktop
sidebar showed the individual sessions, and the local overview showed messages
and actions.

## Permissions and information

Initial material positions/sizes, target-slot coordinates and workspaces were
public. Subsequent tools returned RGB, robot proprioception and execution state,
without dynamic object ground truth. After Meta requested completion, the
Evaluator privately checked object attributes, positions and heights in six
slots. It did not return ground-truth answers to the policy.

Messages required to/text and optional reply_to; the server added IDs and sender
identity. Message deduplication and action-ID caches were process-local. Complete
recovery after a process crash was not implemented.

Engineering and role files were SHA256-pinned at START, and detected edits caused
an explicit abort. Roles used independent tokens. All sessions nevertheless ran
under one operating-system user with general file access. These were protocol
constraints and integrity checks, **not operating-system isolation against a
malicious agent**. Agent rules required reading only the assigned role files,
using that role's tools and leaving engineering files unchanged.

## Evidence and evaluation scope

- `public/`: role rules, connection settings and actual RGB observations.
- `private/manifest.json`: frozen engineering hashes and control parameters.
- `private/episode-start.npz`: integration state at actual START.
- `private/events.jsonl`: raw actions, messages and tool results, each with wall/simulation time.
- `private/runtime.json`: continuously updated runtime snapshot.
- `private/threads.json`, `model-verification.json`, `driver.jsonl`: actual session settings and scheduling evidence.
- `private/evaluation.json`: terminal evaluator result.
- `global-realtime.mp4`: global recording after START, 15 FPS; encoder errors and dropped frames require inspection.

The task placed objects into six target slots, without stacking or precise block
edge alignment. Acceptance required center error <25 mm on each XY axis, height
error <12 mm and matching target attributes. Final release/withdrawal also needed
image and execution-log review; the slot check alone was not a complete grasp
stability evaluation.

Only one pilot was run. It cannot establish overall architecture superiority or
a completed benchmark.
