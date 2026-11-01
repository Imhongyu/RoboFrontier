# Native Codex and Claude harness alignment

This guide describes newly prepared runs in the unified integration. Existing
frozen inputs and sessions are not migrated automatically. The normal task clock
is 24 hours from persisted START; an engineering stop is separate. Evaluation is
independent of policy execution: accepting `finish` begins closure/evaluation and
does not establish task success. Current implementation and hardware/provider
qualification are tracked in the [acceptance ledger](development/unified-main.md).

## Files and responsibilities

| Area | Files | Responsibility |
| --- | --- | --- |
| Claude tool IDs | `robofrontier/claude/robot_mcp.py` | Generate/return new request IDs, retain an ID across retransmission of the same MCP request, and return structured conflict/uncertain errors |
| Claude delegation identity | `request_identity.py`, `fork_setup.py` | Bind the generated delegation ID to one unmatched native tool call, then create and verify the fork |
| Public tool instructions | `prompts/claude/controller.md`, `.agents/skills/robot-collaboration/references/tools.md` | Distinguish new requests, status queries and retries of uncertain requests; retain explicit-ID compatibility |
| Claude provider errors | `recovery.py`, `runner.py`, `session_host.py` | Recognize structured capacity failures and retain original-session recovery, backoff and retry evidence |
| Claude scheduling | `supervisor.py`, `dispatch.py`, `adaptive_dispatch.py` | Recover within the existing deadline; a recovering role does not claim ordinary wakes while other runnable roles continue |
| Shared reporting | `robofrontier/run_metrics.py`, `scripts/export_run_report.py` | Emit common `host_metrics`; resolve isolated Codex homes and collected session maps |
| Host timing | `scripts/codex_policy_host.js`, Claude `runner.py` and `robot_mcp.py` | Record turn/tool/fork setup intervals without adding another image Base64 log |

The engine-specific modules remain native implementations. Common statistics,
public protocol and scoring do not make Codex app-server forks identical to
Claude CLI creation turns. See the [component map](claude-codex-parity.md).

## New requests, queries and delegation

Omit the outer `call_id` for an ordinary new request, then retain the generated ID
from the result. To query an existing action, send a new `job` request with the
old action ID in `data.call_id`. If retrying an uncertain original request is
necessary, use its original outer ID and exactly the same operation/arguments.
Confirm the old outcome before choosing another physical action. A known ID
conflict means rejection; an uncertain transport outcome does not prove rejection.

A Claude MCP JSON-RPC request ID is not the native `tool_use.id`. Before an
automatic delegation, the host reads the Controller's native record and finds
the unique unanswered tool call whose parameters match exactly. It persists this
association under `private/state/claude-tool-bindings/` before submission and
checks it again before forking. Native transcripts can lag behind an MCP request;
matching waits at most ten seconds. Missing or ambiguous evidence rejects the
submission rather than guessing provenance. The explicit delegation-ID path
remains compatible. Preserve parent/child transcripts and tool-result directories.

## Capacity and rate-limit recovery

Candidate recovery requires all of the following: the CLI has conclusively
exited; its returned session matches the original; the result subtype is
`error_during_execution`; and its structured code is `rate_limit`,
`rate_limit_error`, `overloaded_error` or `server_overloaded`. The string "429" in
model prose or stderr is insufficient. The native CLI may already have retried;
this host layer acts only after the CLI returns a recognized failure.

Before recovery, check native history, run state, stop markers, actions and
delegations. Accepted/executing requests must settle first. Unknown actions,
fork creation in progress, uncertain identity, a paused run or a stop request
prevent automatic recovery. When an explicit dollar allowance is set, a turn
whose cost is unknown still requires review.

At most three extra attempts follow consecutive capacity failures, after 10,
20 and 40 seconds. A successful turn resets the consecutive count. Defaults live
in `recovery.py`; host construction can lower the attempt count. Waiting does not
block the supervisor or extend START time. Recovery sends a continuation to the
original session; it does not resubmit motion or recreate a delegate. Exceeding
the limit or failing the checks retains stop/seal/review behavior. Cancellation,
process crashes and unknown outcomes are not this recoverable error class.
Synthetic error tests cannot establish every real provider failure behavior.

## Reports and metric definitions

After all writers stop, run in the original execution environment:

```sh
.venv/bin/python -m scripts.export_run_report RUN_DIR
```

The output is `RUN_DIR/private/outputs/report.json`; common statistics are in
`host_metrics`. For historical Codex logs, `--codex-home PATH` selects a home
explicitly. Otherwise the resolver prefers collected session mappings, then
run/batch `codex-home.json`, and finally the environment default. An unavailable
known batch home never authorizes substituting sessions from another home.
Collected mappings take priority over stale paths to the original server.

| Field | Meaning and missing-data handling |
| --- | --- |
| `usage.input_tokens` | Total input. Claude sums uncached input, cache reads and cache writes; Codex reported input already includes cached input. |
| `cached_input_tokens` | Cache-read input; `cache_hit_rate` is reads divided by total input. |
| `cache_write_input_tokens` | Claude-reported cache creation. This Codex interface does not separately report it, so its value is `null`. |
| `output_tokens` | CLI/app-server reported output; do not add thinking tokens a second time. |
| `reported_cost_usd` | Subtotal of reported costs. Missing cost is not zero; no assumed price is applied. |
| `usage_complete`, `cost_complete` | Whether fields are complete in the observed evidence scope. Unfinished turns, damaged logs and incomplete older evidence remain incomplete. |
| `known_usage_subtotals` | Known usage only; incomplete turns prevent interpretation as a complete total. |
| `by_actor`, `rows` | Per-role aggregates and deduplicated details. `row_unit` distinguishes Claude CLI turns from Codex usage updates; row counts are not equivalent API request counts. |
| `model_process_seconds_sum` | Sum of turn durations, including tool waits and CLI overhead. |
| `model_process_wall_seconds_union` | Union of those intervals, avoiding double-counting overlapping wall time. |
| `tool_seconds_sum` | Host tool durations, which may overlap model-process time. |
| `fork_setup_seconds_sum` | Claude tool-free snapshot/fork creation turns or Codex native fork RPC time. These perform different work. |

Claude prefers final `modelUsage`, aggregated across the turn's models, and uses
`usage` only as a fallback; the two are not added. Older summary-only records are
labeled `legacy_policy_only` and may omit setup. For Codex, the first usage update
uses `last` to exclude inherited parent usage; subsequent updates use cumulative
differences, with duplicate updates removed. These are host observations, not a
recalculation of full transcript history or a provider invoice.

Missing fields are `null`. Check completeness, evidence scope and original logs.
Model, tool and setup times overlap and include waits; summing them does not give
elapsed time percentages or pure API latency. Native host events live in
`private/outputs/codex-host.jsonl` or `claude-host.jsonl`. They supplement, rather
than replace, native sessions, motion, private evaluation and archive validation.

## Regression and qualification boundaries

Common offline checks:

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m unittest test_run_metrics test_run_report test_benchmark_collection test_policy_archive
node --test tests/test_codex_rpc.js tests/test_tool_errors.js tests/test_codex_wall_limit.js
```

Claude-specific checks:

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m unittest discover -s tests -p 'test_claude_*.py'
```

The opt-in physical group requires current assets, a working graphics backend
and the observed native Claude CLI. It uses real MuJoCo/CLI processes with a local
synthetic model service, no paid provider, and does not evaluate model ability:

```sh
PYTHONPATH=tests:scripts ROBOFRONTIER_PHYSICS_SMOKE=1 ROBOFRONTIER_PHYSICS_BATCH=1 ROBOFRONTIER_PHYSICS_FINISH=1 ROBOFRONTIER_PHYSICS_SIGNAL=1 .venv/bin/python -m unittest test_claude_physics_smoke test_claude_parallel_physics_smoke test_claude_finish_physics_smoke test_claude_signal_physics_smoke
```

These cover generated IDs, native fork/return, resumed actions, independent
scoring after `finish`, deadline/SIGTERM stop and collection. The synthetic
`finish` case deliberately leaves the task unfinished; evaluation must remain
unsuccessful. It tests scorer isolation, not successful task completion. Real
model task completion, concurrent roles, current provider behavior and scored
Claude qualification remain separate acceptance requirements.
