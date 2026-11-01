# Privileged Oracle execution

An Oracle is engineering reference code with access to the physical scene and
evaluator. It is separate from both native policy engines and their controllers.
An Oracle result is not an LLM benchmark result. A successful historical witness
does not qualify a changed scene, controller, solver or physics release.

This guide documents the current native entries. Oracle preparation, resource
settings and supervision have not yet been folded into the unified TOML/CLI.
The root configuration's policy deadline must not be assumed to configure a
native Oracle command. That integration remains an explicit acceptance gate.

## Install and select inputs

```sh
uv sync --locked --extra oracle
.venv/bin/robofrontier bootstrap
```

The policy asset package supplies the current task scenes. Historical reference
recordings and their private review evidence are separate data; bootstrap does
not manufacture those witnesses. A Factory presentation package is not permission
to claim that every historical Oracle has been rerun on current physics.

Mosaic uses `configs/suites/frontier-mosaic-r14.json` by default. Case IDs are
reused across revisions, so identify a run by its catalog, scene and executor
hashes as well as its case ID. The runner verifies the selected case, scene hash
and matching catalog/task revision before constructing a physical world. Keep an
old executor with its historical inputs when reproducing a legacy result.

## Mosaic commissioning and full execution

Start with an explicitly partial engineering check:

```sh
.venv/bin/python scripts/run_mosaic_oracle.py \
  --case mosaic-a04-6x12-d1 \
  --output runs/oracle/my-r14-commissioning \
  --planning-workers 4 --physics-workers 0 \
  --max-goals 2 --wall-s 600
```

`--max-goals` is commissioning, even when all selected goals pass. It is not a
full-case success. To attempt the complete task, omit the goal limit, choose a
new output directory and set any intended explicit wall/simulation/action caps.
The native Mosaic entry has no default wall cap. The normal policy benchmark's
86,400-second START deadline is a different protocol.

Commit the executor before physical execution. The native runner rejects a dirty
checkout, records its Git commit and freezes Python code, harness and catalog
before re-executing. It binds imports to that frozen checkout, avoiding a shared
virtual environment silently importing another worktree. Scene assets remain
revisioned inputs, verified separately and frozen with the recording; this is
not a physical restart checkpoint.

Planning workers reconstruct independent scratch models and IK references. They
never own the live physics data or submit robot actions. `--planning-workers 0`
uses available CPUs; a positive number is an explicit process count, bounded by
the number of items. The serial planner remains available with `1`. Worker loss
is reported rather than leaving a silently missing pool result indefinitely.
`planning-status.json` distinguishes elapsed planning from time since progress.

`--physics-workers N` explicitly enables MuJoCo internal worker threads in the
single live world. Zero leaves the pool disabled. More threads or processes do
not prove greater throughput, especially with multiple Oracle worlds. Endpoint
screens are candidates; they do not prove collision-free travel, successful
grasps or task completion.

## Review, assistance and stopping

The owner publishes atomic `runner-status.json` and `planning-status.json`.
At a supported known execution boundary, Mosaic review publishes privileged
state in `review/observation.json`. Its `world_id` and `review_id` identify the
current world and review epoch. Recovery requests and results remain under
`review/requests/` and `review/results/`; rejected requests are retained.

A supervising human or coding session can inspect this engineering evidence and
submit a supported bounded recovery. Such an intervention is recorded as
assistance. It does not modify the frozen solver, reset the scene, remove old
events or transfer physics ownership. Known held payloads must be completed or
physically reconciled before rematching. Uncertain/in-flight actions cannot be
blindly replayed. Requests have idempotent IDs bound to their original content.

An acknowledged request is not proof that a physical recovery succeeded. Read
the resulting action feedback and independent evaluator, retaining failed
commands and review history. The original Oracle reference has stricter
process-violation continuation gates than terminal-outcome policy scoring; do not
interpret an Oracle stop as the policy scorer automatically ending an agent.

Create a `STOP` file in that trial's output directory, or send SIGTERM to its
owner, to request controlled termination. Preserve its report, unresolved action
status and motion before collecting it. Killing the process or losing a node can
leave an incomplete tail and cannot be called a sealed success. Do not replace a
running executor's source or synthesize a restart from visual motion.

The cache diagnostic reads the trial's archived solver to determine whether its
own code prunes stale graph metadata. It does not treat a comment, another
function, or the current checkout's behavior as authority for an older executor.
The diagnosis alone never authorizes motion or certifies a safe recovery.

## Evidence and Factory replay

Retain the frozen executor snapshot, catalog/harness, `report.json`, controller
actions, process/trace events, review requests/results, source assets and motion.
Report `assisted`/`oracle_mode` and commissioning scope without dropping their
provenance. A source-bound concurrent execution needs equivalent inputs and its
own physical validation; borrowing a source does not borrow its success flag or
erase assistance in the source's history.

Closed `robofrontier.motion.v1` recordings can be imported using the
[Factory workflow](factory.md). That composes the desk from the recording's own
source and replays saved poses without physics. Video completion remains separate
from Oracle acceptance. Compression does not authorize stripping events, source
identity, intervention evidence or unresolved actions.

## Curated integration scope

The first R14 curation takes the reviewed endpoint-worker, checkout-binding and
input-identity changes through source commit `a49880f`, plus the frozen-executor
cache diagnostic correction from `76d87ed`. Main also checks the task revision
against the catalog and makes R14 the native default. The 71-mm Mosaic R15 scenes,
15-percent color experiments, R15 selector and experimental source-order/scope
changes were not imported. Relay's independent revision numbers are unrelated.

Focused tests cover actual R14 serial/parallel endpoint equivalence, unchanged
live state, worker initialization failures, frozen imports, revision mismatches,
changed stock colors, protected goals, recovery ownership and uncertain actions.
Passing these tests does not establish every full-case Oracle or a new physical
release. See the [integration ledger](development/unified-main.md) for actual
checks and remaining unified-entry and operational gates.
