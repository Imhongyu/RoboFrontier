# Visible Codex two-session communication pilot

This historical pilot used a local standard-library loopback service, without
MuJoCo or a separate model API. Actual inference ran in two new tasks in the
Codex desktop project, both fixed to `gpt-6-luna` / `xhigh`.

See the [current communication protocol](../../prompts/skills/robot-collaboration/references/communication.md)
for the later tree Meta–Worker and distributed Worker–Worker design. That
protocol has since changed; its capabilities must not be attributed to this pilot.

## Scope

The pilot checked the READY/START gate, continued background work in B while A
sent a message, B's actual handling and reply, mailbox-triggered resumption after
B's Codex turn actually ended, and a common timeline.

**The development session was the driver.** Through the Codex application
interface, it created tasks, read actual platform state and resumed B only after
confirming an unhandled mailbox message and B's idle state. It neither sent A/B's
business messages nor chose their replies. This was a controlled demonstration
with connected desktop tasks, rather than an unattended file-watcher daemon
connected to the desktop backend. Files alone do not wake a model whose turn
has ended.

## Local mailbox and overview

```sh
python3 scripts/session_mailbox_demo.py serve --run-dir runs/session-mailbox-NEW
```

The printed localhost URL showed live A/B status, independent work timers, raw
messages, actual model verification and complete events. The corresponding run's
`state.json` / `report.md` identifies the actual tasks and settings.

Each run used a new directory. Public rules and role prompts were in
`public/common_rules.md`, `public/roles/robot_A.md` and `robot_B.md`. The first
desktop message supplied these explicit paths, without forking development history.

Historical client examples:

```sh
python3 scripts/session_mailbox_demo.py call --run-dir runs/session-mailbox-NEW --agent A --op ready
python3 scripts/session_mailbox_demo.py call --run-dir runs/session-mailbox-NEW --agent A --op watch --data '{"condition":"start","timeout":15}'
python3 scripts/session_mailbox_demo.py call --run-dir runs/session-mailbox-NEW --agent A --op send --data '{"to":"B","key":"example","text":"Please confirm the processing order for work item X7"}'
python3 scripts/session_mailbox_demo.py call --run-dir runs/session-mailbox-NEW --agent B --op inbox
```

## Two-stage workflow

1. A/B each reported READY. The development driver verified model/effort in the actual turn_context, then published START.
2. B started an independent 150-second background timer. The call returned immediately; the timer did not wait for the model.
3. A confirmed the work was running, then sent `during-work`. B chose its own text reply, sent `during-work-ack` and marked the original handled. A acknowledged receipt.
4. B's work completed naturally. B sent final `B_IDLE_WAIT` and ended its turn. The driver verified idle through Codex platform state and recorded evidence.
5. The driver resumed A's original session, asking A to send `idle-wake` and end its turn.
6. After confirming the mailbox event, the driver notified the original B session that new mail was available. B had to read its mailbox and reply `idle-wake-ack`.
7. A resumed and confirmed receipt; the driver ran `verify`.

## Message and concurrency semantics

- Every message had an independent ID, sender, recipient, business key, optional reply_to and handling state.
- Reading and handling were distinct: inbox reads retained messages; only the recipient's handled operation acknowledged processing.
- Retrying the same sender/key/content produced no duplicate. Reusing the key with different content failed.
- One mailbox service serialized all state commits, avoiding concurrent model writes to a shared file.
- READY/START, background work, group messages, agent-reported stages and platform confirmations were logged separately. Self-reported waiting was not proof of actual platform idle.
- Business messages used the mailbox only. Trial sessions did not directly call Codex cross-task messaging tools or create other agents.

## Evidence

- `events.jsonl`: sequential IDs, precise UTC timestamps, event source and details.
- `messages.jsonl`: original sends; events and state retained handling status.
- `state.json`: run state, thread IDs and requested/actual model settings.
- `verification.json`: timing and lifecycle checks.
- `report.md`: complete readable timeline.
- `report.html`: independent static overview generated at verification, readable after server shutdown.

Historical test command:

```sh
python3 -m unittest discover -s scripts -p 'test_session_mailbox_demo.py' -v
```

This pilot checked neither robot actions nor strict permission isolation. Later
robot trials should separately identify initial policy information, subsequent
RGB/proprioceptive observations and any additional state feedback.
