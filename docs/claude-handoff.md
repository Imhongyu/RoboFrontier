# Native Claude Code engineering handoff

The unified integration retains the native Claude CLI/MCP implementation beside
Codex. It does **not** admit scored Claude tasks. Current Single/Adaptive
engineering entries can start real simulation and potentially billable inference
only when explicitly invoked. Provider profiles are candidates, not compatibility
certificates. Permanent Worker topologies remain an implementation/qualification
gate; see [the component map](claude-codex-parity.md),
[harness alignment](harness-alignment.md) and
[the current acceptance ledger](development/unified-main.md).

## Current startup, time and finish contract

New Single/Adaptive policy inputs use direct Controller START. Once the world is
ready and the Controller's native session is bound, the host persists START and
sends an explicit started prompt. Initial task reading, observation and planning
count toward the task clock. `ready` is an optional capability query; it is not
a readiness barrier. Frozen `ready_barrier_v1` runs keep their historical
READY/idle startup and must not be reinterpreted as direct-start experiments.

The default task limit is 86,400 seconds from persisted START. A separately
selected engineering stop does not rewrite that public limit. Normal policy
turns have no separate default timeout; startup, RPC, tool waits and tool-free
fork creation still have their own bounds. Host creation time is not a second
24-hour experiment clock. `run-engineering --startup-timeout-s` defaults to
120 seconds; the unified TOML startup default is 600 seconds. Record the entry
and its frozen settings rather than treating these as one parameter.

The shared [policy rules](../prompts/policy-rules.md) require continued work and
recovery while unfinished. Use `finish` after public evidence supports completion,
or explain publicly supported unrecoverability. The runtime independently checks
actions and delegation closure, and the private scorer evaluates the terminal
world. Accepted finish does not imply success. Ending a CLI turn or returning a
child does not itself finish the task. Dial retains unlock-once completion.

Realtime MP4 is off by default. Observations and motion are still recorded.
Legacy `prepare-draft --record-video` enables MP4 and requires FFmpeg/ffprobe;
engineering sealing checks the stream and decodes its first frame. This is not
full-file decode qualification. Requested video that cannot be verified requires
review; expected absence when disabled is not a task failure.

## Configuration and installation

Use the checked-out integration's [README](../README.md) and
[unified CLI guide](unified-cli.md). Integration has not yet replaced GitHub main.
The earlier public `codex/claude-code-harness` branch is a historical source;
cloning it does not acquire all newer unified features automatically.

Install Python 3.12, uv and the native Claude CLI on macOS/Linux. Observed local
checks use Claude Code 2.1.312. Requalify changed versions. An outer manager may
be Codex, Claude, another coding agent, or ordinary shell commands; selecting the
Claude policy engine does not require the outer manager to be Claude Desktop.
A native Claude-only path does not require the Codex CLI. The unified Docker
image installs both pinned CLIs.

```sh
uv sync --locked --extra oracle
claude --version
.venv/bin/robofrontier bootstrap
.venv/bin/robofrontier plan --engine claude --profile haiku --level 1 --min-arms --parallel 4
.venv/bin/robofrontier prepare --engine claude --profile haiku --level 1 --min-arms --parallel 4 --render native --output runs/engineering/claude-current-l1
```

The renderer example is for macOS. On Linux select `--render nvidia` or
`--render cpu`. Preparation restores pinned assets automatically, creates no
world or model session and does not authorize inference. Mosaic uses R14. Use
`configs/policy-assets.json` for the exact archive/hash; offline installation is
`python -m scripts.benchmark_handoff setup-assets --archive /path/to/archive`.
Do not approximate missing labels or silently substitute another asset revision.

The model catalog is `configs/claude-models.json`. Create the ignored `.env`
without replacing an existing file, then edit it locally:

```sh
.venv/bin/python -c 'import os; from pathlib import Path; fd = os.open(".env", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600); os.write(fd, Path(".env.claude.example").read_bytes()); os.close(fd)'
```

`haiku` and `opus` use `ANTHROPIC_API_KEY`. Other profiles use their catalog's
credential variable; Qwen additionally uses `DASHSCOPE_ANTHROPIC_BASE_URL` matching
the actual account/region. Existing process environment values take precedence.
An empty template value is neither a login nor a compatibility check. Keep keys
out of chat, TOML and Git.

API profiles pass only their selected credential/endpoint into the native CLI;
`--bare` avoids reading native OAuth. The candidate `opus_subscription` path uses
`CLAUDE_CODE_OAUTH_TOKEN`, disables project/user setting sources and automatic MCP
discovery/tool search, and permits that token only at the official Anthropic
endpoint. It does not copy Claude Desktop login. Its real subscription behavior,
credits/cost reporting and refresh are not qualified. The native loopback tests
used a synthetic token. Follow the current
[Anthropic authentication documentation](https://code.claude.com/docs/en/authentication)
for account setup; do not share a generated token in chat or Git.

Check current provider account terms, allowed batch use, model mapping, endpoint,
vision/tool support, quota and pricing before paid prechecks. An editor-compatible
coding plan does not automatically authorize unattended parallel benchmarks.
Do not mix coding-plan and pay-as-you-go keys/endpoints. Historical source links:
[Qwen Claude Code integration](https://help.aliyun.com/zh/model-studio/claude-code),
[DeepSeek Claude Code integration](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/),
[Kimi Code integration](https://www.kimi.com/code/docs/en/third-party-tools/claude-code.html).
`kimi` and `kimi_code` are distinct candidates with different credential variables
and endpoints. A configured URL or model name is not provider qualification.

The engine-specific doctor only checks local CLI/assets, credential presence and
FFmpeg/ffprobe availability. It does not validate authentication, an encoder,
model responses or a complete video. The unified doctor additionally checks a
real renderer; neither calls a provider. A missing local permission should be
resolved in the intended environment rather than bypassed.

## Optional engineering cost allowances

`--turn-budget-usd` and `--task-budget-usd` are optional and unset by default.
Without a turn allowance, `--max-budget-usd` is not injected into the Claude CLI.
Reported cost is still retained. Adaptive Controller, children and fork setup
share one run-local ledger. Missing cost without a ceiling is recorded as
unreported rather than zero, and does not alone block a confirmed normal turn.
Unknown execution, uncertain cancellation or failed fork provenance still needs
review regardless of whether a budget exists.

With explicit allowances, reservations and remaining estimated task funds bound
new turns. A task-only allowance may reserve the entire remainder for one turn,
so another role can be denied concurrently; set a suitable per-turn allowance
when intending concurrency within a task budget. Unknown/invalid/overspent cost
under an allowance blocks further allocation. Reservations from uncertain or lost
processes are not automatically released. These are CLI-reported estimates,
not hard provider billing caps, subscription credits or one shared batch budget.

## Provider prechecks and historical evidence

The following records preserve the conditions and limitations of earlier
engineering work. Dates, costs and source commits describe those attempts; they
are not qualification for every later profile, CLI, account or public protocol.
Some original attempts used the historical READY barrier. New direct-start runs
must use their own prepared inputs and evidence.

After `uv sync --locked --extra oracle`, use:

```sh
.venv/bin/python -m scripts.claude_benchmark models
.venv/bin/python -m scripts.claude_benchmark doctor --models haiku opus kimi qwen glm deepseek
.venv/bin/python -m scripts.claude_benchmark plan --models kimi --level 1 --min-arms --parallel 4
.venv/bin/python -m scripts.claude_benchmark prepare-draft --models kimi --level 1 --min-arms --output runs/engineering/claude-draft
.venv/bin/python -m scripts.claude_benchmark prepare-draft --models opus --level 1 --min-arms --record-video --output runs/engineering/claude-video-draft
.venv/bin/python -m scripts.claude_offline_probe
```

Real precheck (spends money; needs a credential and an explicit cap):

```sh
.venv/bin/python -m scripts.claude_precheck --profile haiku --max-budget-usd 0.5
.venv/bin/python -m scripts.claude_precheck --profile haiku --max-budget-usd 0.5 --confirm-spend
.venv/bin/python -m scripts.claude_precheck --profile haiku --max-budget-usd 0.5 --check-fork --confirm-spend
```

Without `--confirm-spend` it only prints the plan. With it, it makes three
calls on one explicit session: a text reply, a robot tool call whose returned
image must be identified, and a resumed turn. The receipt is `receipt.json`
in the output directory; it records CLI version, requested and reported model,
cost and per-check results, never key values. A profile passes only if all
three checks pass within the cap. Choose the intended profile explicitly for
each engineering draft and obtain the relevant precheck evidence for that
profile; a Haiku precheck does not establish Opus or other provider readiness.

The image color is chosen randomly from six colors for each new precheck; the
receipt records the chosen color after the checks. A single correct answer can
still be a lucky guess and does not establish general visual capability. The
earlier Haiku receipt listed below used a fixed green image.
Each local precheck server keeps its own image and request count, so concurrent
checks do not share that state; this is not a provider concurrency guarantee.
The check also requires the CLI event stream to show an `observe` call selecting
the `top` view, a matching non-error tool result containing an image, and an
`observe` request received by the local service. This is still not independent
proof that a real provider processed the image. Older receipts lacking the
new view-request or image-result evidence will not pass `claude_readiness`;
the historical Haiku receipt has not been rerun under these checks.

`--check-fork` adds a fourth paid call: a tool-free native fork of the idle
session that must recall the image color and have a matching native transcript
prefix. The receipt includes a profile fingerprint and whether the fork was
checked. This idle-session check does not establish compatibility with a parent
blocked in a tool call, concurrent delegate execution, or a real robot task.
The cap is based on CLI-reported cost and is not a provider billing limit.

For an additional paid check of the adaptive fork boundary:

```sh
.venv/bin/python -m scripts.claude_blocked_precheck --profile opus --max-budget-usd 1
.venv/bin/python -m scripts.claude_blocked_precheck --profile opus --max-budget-usd 1 --confirm-spend
```

It uses a synthetic local robot service and three CLI turns: initialize the
parent, block the parent at an image tool call, and create a tool-free fork
while that call is blocked. It verifies the native history prefix, releases the
parent, and checks its image response. One turn can generate multiple provider
requests. The two concurrent turn allowances share the remaining estimated
budget. A receipt with `cost_complete: false` does not account for every turn;
neither this check nor the CLI-reported budget proves a provider billing cap,
physical execution, or scored-run qualification.

On 2026-10-28, the `opus` profile also passed both real-provider prechecks
using CLI 2.1.312: text, image/tool round trip, resume, idle fork, and fork
while the parent was blocked on an image call. The CLI reported $0.030570
and $0.021293 respectively; these are estimates, not the provider invoice.
The local receipts matched the profile and CLI in `claude_readiness`.
They do not qualify a physical task or a scored run, and the Chinese profiles
remain unverified. Receipts and transcripts are local run artifacts, not part
of the Git handoff.

A subsequent separately authorized, unscored Opus adaptive transport engineering
trial reached READY and received two observation images, but the startup turn
did not end before the 120-second startup timeout. The owner sealed and exited
with no unresolved actions; no physical action had started. The interrupted CLI
turn did not produce a complete cost report, so actual charges require checking
the provider invoice. Its event stream showed continued thinking progress after
the observation; this alone does not establish the cause or a remedy. Do not
replay the claimed run or treat this as a qualified benchmark result.

A separately authorized second Opus engineering trial used a 600-second startup
timeout and a $0.20 CLI turn allowance. Before START, the CLI exited nonzero
with `error_max_budget_usd` and reported $0.4755318 for the turn. This exceeds
the requested per-turn allowance and is not a provider invoice; the ledger
retained the cost as uncertain. The physical owner sealed and exited with no
unresolved actions and no robot actions. This observation demonstrates that
the CLI allowance is not a hard spending cap, and the trial does not qualify a
scored benchmark or explain the earlier interrupted turn's actual cost.
The final CLI event reported per-model aggregate `modelUsage`: 13,707 output
tokens including 13,299 thinking tokens, 39,118 cache-creation input tokens,
and 28,889 cache-read input tokens. Its separate `usage` field contained lower
counts; it should not be mistaken for the aggregate. New summaries retain both
fields and the result subtype as reported, without converting them to a bill.

A separately authorized Haiku 5.5 adaptive transport trial reached START and
made physical tool calls through the real CLI and provider. It reached the
300-second wall limit without a finish call, then sealed and exited with no
unresolved actions. The runtime recorded 14 completed physical actions and one
failed action; two further move requests were rejected before execution. No
delegate was created and no task-success evaluation was produced. The CLI
reported $0.011251435 for the completed startup turn; the interrupted active
turn had unknown cost, requiring provider billing review. This unscored trial
demonstrates live observations and actions, not task completion or full
adaptive qualification.

After obtaining both real receipts, compare them with the current profile and
CLI version without making model calls:

```sh
.venv/bin/python -m scripts.claude_readiness --profile opus --precheck /path/to/receipt.json --blocked-precheck /path/to/blocked/receipt.json
```

This checks required observations, session relationships, cost completeness,
model/profile fingerprint and CLI version. `precheck_evidence_matches` is only
receipt consistency: it cannot authenticate a receipt, distinguish accounts
sharing the same profile, establish provider model identity, or authorize a
scored benchmark. `formal_execution_available` remains false.

The doctor checks locally only. It reports whether credentials are present,
not whether they work. If a sandbox denies the provider host or writes under
`runs/`, allow it in your own environment rather than bypassing the sandbox.
For local credentials copy `.env.claude.example` to
`.env` with permissions 600; existing environment variables take priority.
Do not commit credentials. The Anthropic-compatible Qwen endpoint must match
your actual account and region.

The runner redacts exact occurrences of the selected credential (including
JSON-escaped forms) from its event file, summary and stderr tail, and writes
event files with owner-only permissions. This does not sanitize Claude's native
session files or detect transformed/partial secrets; treat the entire run
directory as private and inspect it before sharing.

First Haiku preflight record (historical, before the Opus checks above):

- `haiku` (`claude-haiku-5-5`, CLI 2.1.312) passed on 2026-10-28 with a total
  cost of $0.000541 under a $0.5 cap. Its receipt is local at
  `runs/engineering/claude-precheck/haiku-20261028-194259/receipt.json`
  (`runs/` is gitignored). This covers only that profile, CLI version and cap.
- The first Haiku record did not establish Opus readiness; the later separately authorized Opus checks are recorded above. Other providers remain unqualified.

`robofrontier.claude.robot_mcp` is an experimental role-bound MCP server. Its
offline probe checks Claude CLI tool discovery, simulated tool-image forwarding and
fork history against local stub servers. It does not validate real provider image
handling, trusted session provenance, dynamic delegation or production physical runs.
Do not launch it against an actual scored world. The draft prepare command freezes inputs for engineering inspection only; it is
not a scored batch. Experimental engineering run/status/stop commands exist, but
the real-provider preflight and full runner still require qualification; the Codex-to-Claude
component map and verified CLI facts are in [claude-codex-parity.md](claude-codex-parity.md).
Mosaic remains the released R14 scene in this branch.

On 2026-10-28, a fresh local clone at commit `aa0473d` independently created
its Python environment with `uv sync --locked --extra oracle`, downloaded the
published `handoff-20261028` asset archive, verified its SHA-256 and restored
3,467 files. It planned and prepared the four minimum-arm Level 1 Opus drafts;
all four frozen-input checks returned no changes. The Claude test suite ran
104 tests successfully with two opt-in physical tests skipped. The clone came
from the local branch, not GitHub, and no real provider or scored run was tested.
The same clone subsequently passed the opt-in four-way physical smoke: four
distinct MuJoCo owners overlapped, camera images reached a synthetic loopback
model, each delegate completed its synthetic motion and returned control, and
all four worlds sealed. This is an engineering integration check, not evidence
of real model capability or scored benchmark qualification.

At commit `0b81cb5`, a new local clone again installed its own dependencies,
downloaded and SHA-256-verified the GitHub Release archive, and restored 3,467
files. It prepared the four minimum-arm Level 1 Opus drafts and verified all
four frozen inputs. Claude-focused discovery completed 123 tests with six
skipped. This was a clone of the local branch, because the Claude branch was
not yet published; it did not call a real provider or run a scored task.


## Reports, frozen inputs and provenance

`scripts.export_run_report` reads only the current Claude run's role/turn
summaries, not unrelated Codex homes. A CLI-reported model name remains an
observation; `all_requested_models_verified` stays false. It cannot rule out
provider mapping or auxiliary requests. JSON audit reports declare
`benchmark_qualified: false`; Markdown also labels the unqualified state.
Task success and permission to claim a scored benchmark are different facts.

New drafts freeze their actual shared imports `benchmark.py`,
`benchmark_handoff.py` and `tasks.py`, alongside native engine code and inputs.
Reprepare after source changes. Older drafts do not gain that check retroactively.
At historical Claude commit `85f9b91`, a merge preview against main `c8b4137` had
no text conflicts; this was not a completed merge or behavioral proof. That
branch descends from Codex handoff and brings its ancestors. Eight engine-neutral,
ten benchmark and 24 Node dispatcher checks passed then; current integration
must use its own source comparison and regressions.

## Native sessions, tools and internal delegation

`ClaudeSessionHost` owns one role's unique native session, fixed MCP connection,
turn exclusion, explicit resume, evidence and cancellation. Unknown turn outcomes
never automatically start another turn. A host's lifecycle result is not a task
score. Public bootstrap text is packaged from allowlisted frozen inputs because
policy file-reading tools are disabled.

`robot public_image` returns only reference paths explicitly listed by the
current public task, within its public input directory. It also accepts the
listed `target.reference_image`, used for the Mosaic target. Historical public
reference inputs remain PNG and retain their signed bytes; runtime camera
observations use their separately frozen image profile. This distinction does
not authorize rewriting source textures or old reference hashes.

The 2026-10-28 offline Level 1 preparation covered twelve drafts. Three Mosaic
scales each exposed a target image; three Dial scales each exposed three reference
images. A real CLI/local synthetic model check confirmed exact image bytes for
the smallest Mosaic and Dial cases through MCP. It did not test real model
understanding. Opt-in recheck:

```sh
ROBOFRONTIER_MOSAIC_IMAGE=1 .venv/bin/python -m unittest discover -s tests -p 'test_claude_mosaic_image_integration.py' -v
```

General Claude `delegate-bind` is closed. The internal Adaptive engineering path
claims a delegation, binds it to the unique unmatched native tool call, creates
a tool-free native fork, verifies unchanged parent/prefix/session evidence, then
binds scope and enables child MCP authority. Native transcript writes can lag;
the bounded match wait pauses on timeout/ambiguity. Prefix equality alone does
not establish trusted creation or authorization. Failed/uncertain setup is not
automatically reforked. Role hosts, original transcripts and referenced parent
`tool-results` must stay available during the run.

A returned child's authorized report is available to the Controller via
`robot work` with `{"delegate_id":"Delegate_..."}` in `delegate_report`.
The report is model-authored public evidence, not private evaluation. Missing
return, mismatched references or an oversized report does not expose a body.

## Engineering run, status and stop

The unified entry uses frozen settings:

```sh
.venv/bin/robofrontier run runs/engineering/claude-current-l1 --engineering
.venv/bin/robofrontier status runs/engineering/claude-current-l1
.venv/bin/robofrontier stop runs/engineering/claude-current-l1
```

Run is potentially billable; invoke only with explicit authorization. The
engine-specific multi-profile entry remains available for engineering inspection:

```sh
.venv/bin/python -m scripts.claude_benchmark run-engineering RUN_DIR --parallel 2 --wall-limit-s 1200 --startup-timeout-s 600
.venv/bin/python -m scripts.claude_benchmark status-engineering RUN_DIR
.venv/bin/python -m scripts.claude_benchmark stop-engineering RUN_DIR
```

The first command is a dry plan unless `--confirm-engineering-spend` is added.
Use optional `--turn-budget-usd`/`--task-budget-usd` only when an allowance is
intended. An engineering wall stop is measured after START, excludes startup
and sealing, and requests orderly stop rather than an exact provider cutoff.
The shorter of the applicable persisted task deadline and engineering stop
controls execution. Waiting longer for startup changes neither allowance nor
physical/model qualification.

The launcher validates a draft, claims it once, starts an independent physical
owner and supervises existing role sessions. It never automatically restarts a
world or an uncertain task. Sealing must explicitly report no unresolved actions;
process exit alone is insufficient. If finish ended the world, a readable private
`evaluation.json` with boolean `task_success` is required for clean engineering
closure. `task_success: false` may be a normally sealed unsuccessful task.
Missing/corrupt evaluation remains `needs_review`.

Batch startup prechecks all tasks, respects concurrency and does not restart
claimed tasks. Useful status values include:

| State | Meaning |
| --- | --- |
| `stopped_before_start` | Stop arrived before a task was launched. |
| `stopped` | Stop skipped unstarted tasks or sealed active tasks. |
| `closed` | Engineering batch closure, not successful task scoring. |
| `needs_review` | At least one task has unresolved execution/sealing/cost evidence; takes precedence over normal closure. |
| `claim_without_status_needs_review` | A launch claim exists without a status file; do not treat it as a fresh unlaunched batch. |
| `supervisor_lost_needs_review` | Supervisor loss needs inspection; claims remain and replay is refused. |

`stop_requested` is marker existence, not confirmation the owner received it.
`claim_record_present` is likewise a file snapshot. Recorded `owner_pid` is not a
live-process check and may be reused by the OS. When Controller state is unknown
or failed, limited `session_evidence` records allowance status, recognized CLI
result subtype and reported turn cost; a number does not reconcile an uncertain
bill or authorize retry. A run with unknown execution, unresolved reservations
or cost uncertainty under an allowance remains review-required even if its
physical world sealed. Historical statuses are never retroactively rewritten.

Ctrl-C/SIGTERM requests batch stop, skips pending launches and waits for active
models/owners to stop and seal. Wait for exit and inspect status. SIGKILL, node
loss or supervisor crashes can leave physical processes; do not infer sealing
or blindly relaunch. A prelaunch cancellation check avoids creating the CLI when
already canceled, and can release its unused reservation. A cancellation racing
with process creation can still launch a request and incur cost; its outcome and
reservation remain uncertain. Role/delegation state still needs inspection.

Only conclusively ended, matching-session structured capacity failures permit
bounded recovery, under the [current recovery checks](harness-alignment.md#capacity-and-rate-limit-recovery).
Ordinary nonzero exits, unknown actions, uncertain fork creation and unknown
identity remain review-required. Provider retries never replay physical actions.

## Historical local integration and physics checks

Early local synthetic model/robot checks verified native session launch, image
forwarding, resume, fixed role connection, READY/START and deterministic
scheduling. They did not prove provider compatibility or real physics. Two old
execution/action tests initially lacked `mosaic/four-arm-10x10/assets`; restoring
the exact main-worktree scene let them pass then. This does not establish all
historical assets for a new clone.

The optional physical checks below use real MuJoCo owners and Claude CLI, but
only a loopback synthetic model with a synthetic key. They make no paid calls
and do not measure model ability. Install current pinned assets and choose a
working graphics environment first.

```sh
ROBOFRONTIER_PHYSICS_SMOKE=1 .venv/bin/python -m unittest discover -s tests -p 'test_claude_physics_smoke.py' -v
ROBOFRONTIER_PHYSICS_BATCH=1 .venv/bin/python -m unittest discover -s tests -p 'test_claude_parallel_physics_smoke.py' -v
ROBOFRONTIER_PHYSICS_FINISH=1 .venv/bin/python -m unittest discover -s tests -p 'test_claude_finish_physics_smoke.py' -v
ROBOFRONTIER_PHYSICS_SIGNAL=1 .venv/bin/python -m unittest discover -s tests -p 'test_claude_signal_physics_smoke.py' -v
```

The single-run check defaults to minimum-arm Level 1 Transport; set
`ROBOFRONTIER_PHYSICS_CASE` for another released case. It verifies images reaching
the synthetic model, Adaptive delegation/return, a synthetic 5 mm A-arm movement,
deadline stop, sealing and owner exit. On 2026-10-28, each minimum-arm Level 1
family passed separately. Setting `ROBOFRONTIER_PHYSICS_VIDEO=1` additionally
checks recorded stream/first-frame decode; the historical Transport check
passed but did not decode the entire video.

The four-way check verified four independent MuJoCo owners alive concurrently,
images, child displacement/return and sealing. It passed at `9f8709d` and again
at `2972dba` after prompt changes. Predetermined synthetic responses are not
real model collaboration or provider concurrency/rate/billing evidence.

The finish check deliberately ended an unfinished centralized Transport case.
Private evaluation correctly reported failure, exported audit retained it and
requested-model identity remained unverified. It checks failure closure and
scorer isolation, not successful completion or scored eligibility.

Single- and four-task SIGTERM checks verified supervisor exit and each owner
seal/exit under the tested timing. After cancellation-reservation changes,
`9d58b2a` passed both checks; its Claude group ran 127 tests with seven optional
checks skipped. A separate supervisor-loss test used fake tasks, retained launch
claims and refused rerun; it does not prove that real physical children stop
or seal after supervisor loss. None of these tests covers every crash, provider
error, interruption boundary or long-run concurrent task.

Real-provider successful task completion, true multi-role stability, current
subscription operation and formal scored qualification remain required. Use the
integration ledger for newer source-specific acceptance; preserved historical
counts and receipts do not certify changed code automatically.
