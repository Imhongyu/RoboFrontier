# Native Claude standing teams

Claude engineering execution supports all four shared collaboration modes.
`single` and `adaptive` retain their existing hosts. `controller-worker` and
`worker-worker` use native independent Claude sessions, the same role-bound robot
MCP, and the existing runtime's durable mailbox, permissions, action IDs, wake
leases and private evaluator. No Codex session interface is fabricated and no
standing Worker is represented as an Adaptive fork.

These are **engineering entries**, not qualified scored Claude benchmarks. A
configured provider/profile and a local synthetic test do not prove a real
provider's capability, throughput, billing or task success. See the
[acceptance ledger](development/unified-main.md) for current evidence.

## Select and prepare

Choose topology and model through the ordinary TOML or CLI. For example, prepare
the four minimum-arm Level 1 tasks without model calls:

```sh
.venv/bin/robofrontier plan --engine claude --profile haiku \
  --topology controller-worker --level 1 --min-arms --parallel 2
.venv/bin/robofrontier prepare --engine claude --profile haiku --render native \
  --topology controller-worker --level 1 --min-arms --parallel 2 \
  --output runs/engineering/claude-standing-l1
```

Use `--render nvidia` on Linux NVIDIA or explicit `--render cpu` for Linux
software rendering. A preparation freezes the chosen mode, provider profile,
shared task inputs, public Claude role prompts and source hashes. Changing TOML
after preparation does not change this batch. Use a new output path to change
settings. Pinned policy assets are installed automatically when needed.

When authorized to spend against the selected credentials, execute:

```sh
.venv/bin/robofrontier run runs/engineering/claude-standing-l1 --engineering
```

Substitute `worker-worker` to prepare peer Workers. The underlying native
`claude_benchmark prepare-draft --topology` spellings remain `hierarchical` and
`peer`; the unified names describe the same roles. Native `run-engineering` also
supports those drafts. Neither entry admits formal scored execution. Provider
preflight remains a separate explicit operation; it is never a side effect of
planning or preparation.

## Initial roles and START

| Mode | Initial native sessions | Robot and finish authority |
| --- | --- | --- |
| Controller + Worker | One Controller plus one Worker per arm | Workers control only their own arms; Controller coordinates and may propose team finish |
| Worker-Worker | One Worker per arm, with no Controller session | Workers control their own arms, communicate directly and may propose team finish |

Controller + Worker routes business messages through Controller. Worker-to-Worker
business messages are rejected in that mode. Worker-Worker allows authorized
peer messages. The runtime, rather than prompt wording alone, enforces these
routes and robot authority. The old serialized `coordinator` kind is retained
for compatibility; its public actor name is Controller in current defaults.

The host creates all initial native session IDs, binds each role once, and asks
the existing physical owner to START only after every binding is confirmed.
IDs must be distinct. START persists the task's start time; each role then
receives its own public task/skill/role prompt with an explicit started statement.
Reading, model startup turns, observation, planning and subsequent communication
are inside this clock. Initial model replies are not a READY gate.
`ready` remains an optional capability query. Old frozen READY-barrier runs keep
their previous behavior; new standing drafts require `direct_team_v3`.

The host never fills a Worker's plan or decides allocations. Shared collaboration
rules describe standing local authority. Workers remain available after local
completion until the team ends. Their end of a model turn is an idle native
session, not a completed task. Messages, self-selected review deadlines and
saved work can wake that same session again. Controller is also a normal bound
policy role for mailbox and wake purposes.

## Resource and timing implications

A batch's `parallel` limits simultaneous **tasks**, not role CLI processes.
With N arms, a standing task has N or N+1 initial sessions. The four smallest
Level 1 cases have 4, 4, 8 and 4 arms: all four at once mean 20 peer Workers, or
24 roles with Controllers. A 36-task Adaptive resource estimate does not qualify
36 standing tasks. Commission concurrency with actual memory, provider limits
and process observations before increasing it.

The default 0.3-second interval gates initial task-host launches. It is not a
pause between robot operations, a message latency or a guarantee of serial model
turns inside one team. All roles operate independently after START, subject to
shared runtime authority and the provider. Native configuration is per task;
each role has its own native session and transcript within that task's store.

The task deadline is the persisted START plus the frozen limit, normally 24
hours. A separately selected engineering stop does not silently shorten that
public task definition. Status and stop use the same commands as other batches:

```sh
.venv/bin/robofrontier status runs/engineering/claude-standing-l1
.venv/bin/robofrontier stop runs/engineering/claude-standing-l1
```

Stop first cancels every role's model turn and waits, then uses the existing
physical seal. Unknown physical outcomes remain unresolved rather than being
replayed. Inspect seal and final owner status before collecting.

## Errors, budgets and evidence

A lost bind acknowledgement blocks bootstrap instead of rebinding. A lost wake
acknowledgement marks that wake uncertain, pauses dispatch and prevents automatic
resend. An unavailable/mismatched role also pauses the team. Confirmed provider
capacity errors use the existing bounded same-session recovery. One role's
recoverable error cannot hide another role's unknown or fatal outcome.

Standing roles share one task-local cost ledger. Dollar caps are optional and
unset by default. An explicit task allowance must cover simultaneous turn
reservations; it is not a per-role allowance or provider-enforced spending cap.
Unknown costs under configured allowances stay review findings. Model stop and
physical sealing do not invent missing cost or session records.

The normal stopped collection includes all role-bound native transcripts and
linked auxiliaries, motion, action/message/wake records and reports. Collectors
identify roles from runtime metadata, so no Controller is required in peer mode.
The normal ZIP archive, restore and replay path also applies. See
[evidence storage](evidence-storage.md) for locations and retention.

## Measured coverage

The native loopback integration runs actual Claude CLI/MCP with a synthetic
model endpoint and synthetic world. Both topologies verified independent native
sessions, an authorized Worker action, mailbox messages, wake dispatch and
continuation of the same sessions. A confirmed wake may already be `observed`
when inspected; it is not required to remain transiently `sent`.

An explicitly enabled real MuJoCo test then ran each topology on Transport
A04-D1 for 20 seconds after START. Both exercised an RGB observation, a completed
Worker A gripper operation, messages and resumed native roles. Both stopped with
sealed physical state, no unresolved actions and an exited owner. The tests did
not ask a genuine model to solve Transport or claim a success rate.

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m unittest \
  test_claude_standing_team test_claude_standing_team_integration
ROBOFRONTIER_PHYSICS_STANDING=1 PYTHONPATH=tests:scripts \
  .venv/bin/python -m unittest test_claude_standing_physics_smoke
```

The opt-in test needs installed current assets, a renderer and Claude CLI, but
uses only a local synthetic endpoint. It retains stopped physical evidence.
These scoped checks do not qualify all families/scales, concurrent subscription
refresh, production providers, cluster hardware or formal scored execution.
