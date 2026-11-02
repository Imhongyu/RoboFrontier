# Historical design: Claude Code multi-model harness migration

Recorded on **2026-10-28, Asia/Hong_Kong**. This is the original migration
proposal, translated into English with its design constraints and source links
preserved. It is not the current implementation or qualification checklist.
The original note reported an offline runner, role-bound MCP, preflight commands
and neutralized shared core, with a passing Haiku preflight; policy hosting,
supervision and delegation were still pending at that point. Later work has
superseded that implementation status. Consult the current
[engine comparison](../../engines/README.md),
[standing-team guide](../../engines/claude-code.md#standing-teams) and
[integration evidence ledger](../unified-main.md).

Provider compatibility, package versions and vendor policy statements below
are recorded research, not a fresh verification. Proposed files/commands are
identified as such. In particular, this proposal's old START/READY gate is not
the new direct-START protocol, and its proposed spending limits do not override
current explicit settings.

## 1. Goal and branch baseline

Design an independent Claude experiment system on `codex/claude-code-harness`,
starting from GitHub branch `codex/multimodel-handoff` at
`b3259aa817197f9bcb26ed7ccda02229b7c049ca`, in a separate worktree.

- Route every experimental policy model through Claude Code CLI, including
  Opus 5.5, other Claude models and compatible Chinese-provider models.
- Allow Claude Desktop, Claude Code, Codex or another authorized agent to be
  the outer engineering session. Engineering models must not make policy decisions.
- Make doctor, prepare, run and handoff independent of the `codex` executable
  and Codex authentication state.
- Target `claude-opus-5-5`, other Claude models, original GPT profiles, Kimi,
  Qwen, GLM and DeepSeek; later add Doubao, MiMo, MiniMax and Step. Each exact
  model must pass its own preflight.
- Retain the baseline published scenes: all nine Mosaic cases use R14, 81 mm,
  without R15's 15% color exchange.
- Leave the original GitHub handoff branch and other Codex/R15 worktrees intact.
- Reuse physics, evaluation, public tasks and action semantics; implement Claude
  sessions, tools, prompts, skills and scheduling natively.

The historical local CLI check recorded an upgrade from `2.1.96` to the then-npm
latest `2.1.312`, with version/help checked and no authentication or inference
invoked by that upgrade check. Formal trials should pin and record the verified
CLI/SDK version, and requalify after an upgrade.

## 2. Distinguish four entry points

| Entry point | Native capability | Proposed project role |
| --- | --- | --- |
| Claude Code CLI / Agent SDK | Claude Code loop, sessions, tools, permissions, compaction and subagents | First complete automation route; API-key billing preferred |
| Claude Desktop Code mode | Project-based Claude Code interaction, instructions, skills and MCP | Interactive development/management; independent CLI/SDK processes own batch policies |
| Ordinary Claude Desktop chat or another outer session | Authorized management commands or management MCP | May start/query experiments; is not the policy team |
| Claude Messages API / Client SDK | Model requests, images, tool_use/tool_result | Model-service protocol behind Claude Code; no separate policy executor bypassing CLI |

An API key selects authentication/billing. Messages API and Agent SDK are
different execution routes: Agent SDK runs the Claude Code binary; direct
Messages requests do not automatically provide its sessions, forks, skills,
hooks or compaction. Other providers need Anthropic Messages compatibility or
an explicitly verified translation service. A Responses URL cannot simply be
used as a Claude Code endpoint.
[Recorded official comparison](https://code.claude.com/docs/en/agent-sdk/overview).

Code mode and CLI may share project settings, with different Desktop discovery
precedence; load only the selected frozen materials. Ordinary chat MCP access
does not establish an official interface for creating, waking and monitoring
arbitrary chat sessions.
[Desktop Code](https://code.claude.com/docs/en/desktop),
[local Desktop MCP](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).

## 3. Proposed architecture

```text
Claude Desktop / Claude Code / Codex / authorized engineering session
                  |
       Management commands or management MCP
       prepare / start / status / stop / report
                  |
          Claude experiment supervisor
                  |
          Claude Code CLI / official Agent SDK
                  |
       Selected provider's Claude or compatible model API
                  |
       Robot MCP: authenticated operations and actual images
                  |
       Public task / work notes / mailbox / authority / IDs / scheduling
                  |
       Physics owner / MuJoCo / private evaluation and recording
```

The outer engineering session can change; the batch's frozen configuration
selects policy executor and model. Changing the outer session does not change
the in-task model. Management tools return authorized engineering status,
billing and error summaries, without action advice or hidden evaluator truth.
Policies start in fresh sessions without engineering chat, other trials or
Oracle history. Runtime SQLite remains authoritative for experiment state;
Claude transcripts are model-session evidence. Session resume does not imply
that a crashed physical world can be restored.

## 4. Native Claude capabilities to adopt

| Capability | Proposed use | Required verification |
| --- | --- | --- |
| Noninteractive execution/logging | CLI `-p`, stream-json or official Agent SDK | Native init/result/error, session ID, full usage and abnormal exit |
| Persistent turns | Resume an explicit session ID; native fork for branched history | Never use a shared latest-session shortcut; do not replay physical actions on recovery |
| Robot functions/images | Native MCP text and image content | Model receives the actual current image; a path string is insufficient |
| Instructions/knowledge | Run-frozen Claude prompts, skills and agent definitions | Actual child-loaded materials and rule recovery after compaction |
| Temporary division of work | Ordinary subagent or native fork according to history requirements | Ordinary subagents do not inherently inherit full history; fork/tool authority differ |
| Lifecycle observation | SDK events, native session/agent IDs and applicable hooks | A native turn ending is not task completion or return of control |

Recorded official references:
[headless execution](https://code.claude.com/docs/en/headless),
[sessions/fork](https://code.claude.com/docs/en/agent-sdk/sessions),
[MCP images](https://code.claude.com/docs/en/mcp#images-in-tool-results),
[skills](https://code.claude.com/docs/en/skills),
[SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents),
[hooks](https://code.claude.com/docs/en/hooks).

The research treated Agent Teams as experimental, with teammate recovery/task
state limitations, and excluded it as the first release's sole unattended
physical-experiment foundation. A later separate experimental mode was possible.
[Recorded limitations](https://code.claude.com/docs/en/agent-teams#limitations).

## 5. Separate prompts, skills and role configuration

These paths were **proposed**, not a statement that each now exists or is a
current command:

```text
prompts/claude/manager.md              Engineering preparation/start/monitor/report
prompts/claude/controller.md           Controller initialization and return duties
prompts/claude/delegate.md             Bounded temporary assignments/role changes
prompts/claude/worker.md               Optional standing Worker mode
.claude/skills/robot-experiment/       Claude-specific execution/recovery rules
.claude/agents/                       Native role-definition templates
configs/claude-models.json             Exact models, endpoints and budget settings
configs/claude-harness.json            Engine, topology and concurrency settings
scripts/claude_benchmark.py            Independent engineering commands
robofrontier/claude/                  Runner, supervision, MCP and session evidence
docs/claude-handoff.md                 Installation, credentials, Desktop and servers
```

Choose language/module boundaries after protocol verification, with one
implementation per responsibility. Evaluate Python Agent SDK first to reuse the
Python runtime. If only the pinned TypeScript version reliably provides needed
native identity/events, choose a TypeScript runner instead; do not maintain two
Claude Code loops.

The manager performs engineering work. The Controller chooses policy and
delegation. Delegates execute their own robots/goal/done_when/constraints.
Keep one authoritative action contract; Claude documentation adds native tool
names, image handling and recovery without copying a drifting protocol body.
Freeze actual adopted materials and their digests per run, avoiding later edits
to workspace templates.

Generate project `CLAUDE.md` and skill paths only within explicit engineering
or policy scope. Policy workspaces must not automatically load the outer
session's private memory, hooks, plugins or unfrozen instructions.

## 6. Robot MCP is an enforced interface

Reuse observe, move, gripper, job/pending, work, inbox, communication and
return_task semantics. Use fixed JSON schemas and actual image content.
Stable action IDs identify business requests; query the original ID after an
unknown receipt. The current host-generated-ID contract supersedes any
implication here that models must invent ordinary request IDs themselves.

Bind run and actor in the trusted MCP process/connection; runtime checks robot
ownership. A model cannot switch roles by supplying an arbitrary actor or private
connection path. Inheriting an MCP connection does not grant a new independent
role; fork does not automatically revoke parent authority.

Initial protocol qualification must establish reliable role binding through
native role-scoped MCP settings or separate role processes and authenticated
connections. Map native child identity, authority and lifecycle in the trusted
host. Self-reported identity, prompt injection or ordinary tool parameters are
not evidence of this mapping. Failure blocks the topology rather than silently
weakening authorization.

MCP/tool allowlists alone do not provide OS file isolation against a malicious
policy. The first proposal retained the benchmark's cooperative evidence
restrictions; stronger workspace/process isolation needs separate qualification.

## 7. Multi-agent, fork and scheduling design

- First qualify one Controller's tools, images, continuation and lifecycle.
  This interface check is not a formal adaptive result. A Controller may submit
  parallel actions on different arms without any delegate.
- Adaptive delegation remains the Controller's choice. Runtime checks disjoint
  authority and pending actions, records delegation, binds the child session,
  verifies history/identity, and then activates authority.
- Ordinary native subagents start with fresh context. Use native session fork
  when the task requires full prior history. A skill's `context: fork` is not
  a full session-history fork.
- Define Claude provenance using native session/agent/parent IDs, known source
  message boundaries, and request/confirmation events. Do not fabricate Codex
  ordinals or replace provenance with a child-created log line.
- Verify parent suspension/idle, actual child creation, matching source history,
  image history and role rebinding. If native interfaces cannot prove required
  history, record the gap. Explicit-context-package delegation is a different
  experimental condition, not equivalent adaptive behavior.
- Distinguish starting, active, waiting, idle, failed, unknown and ended. Native
  evidence advances session state; runtime return_task/finish decides business
  completion.
- Use verified hooks for lifecycle/event collection, not action idempotence,
  authorization or private evaluation.

This was the largest design gate: native fork support alone does not prove
matching history boundaries or authority. Recorded references:
[native subagents](https://code.claude.com/docs/en/sub-agents),
[skill context fork](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent).

## 8. Parallelism, models and budgets

Configure batch task concurrency, per-task policy/delegate count, account API
request concurrency and rate/cost admission separately. Four minimum-arm Level 1
cases mean four independent worlds, not four arms or four API requests. Each
world owns its records, mailbox, work notes and action IDs.

The proposed profile records engine, exact model, requested/effective effort,
context capabilities, compaction, output/time/cost settings, CLI/SDK version and
authentication-source type. Never record secret values. Other Claude/provider
models need independent settings; do not assume matching context, effort, image
limits or cache rules.

These were provider candidates, **not completed API preflights in that worktree**:

| Model | Recorded Claude Code / Anthropic entry evidence | Verification needed |
| --- | --- | --- |
| Original OpenAI profiles `gpt-6-astra`, `gpt-6-luna` | No directly usable Claude Code model endpoint verified in this research | Model/API access and Anthropic-compatible route; a separately verified translation gateway might be needed |
| Kimi `kimi-k3.1-pro` | [Kimi Messages / Claude Code](https://platform.kimi.com/docs/guide/claude-code-kimi) | Exact model, vision and tool-returned images |
| Qwen `qwen3.8-max-0902` | [Bailian Messages model table](https://help.aliyun.com/zh/model-studio/anthropic-api-messages) | Region, pay-as-you-go credentials and returned images; the recorded [Coding Plan rules](https://help.aliyun.com/zh/model-studio/coding-plan-faq) prohibited noninteractive batch scripts |
| GLM `glm-5.3-flash` | [Zhipu Claude Code](https://docs.bigmodel.cn/cn/coding-plan/tool/claude) | Examples used Coding Plan; verify ordinary metered keys and exact model |
| DeepSeek `deepseek-flash` | [Official integration](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/) | Pin Flash; avoid Claude tier aliases mapping to non-vision V4 Pro |
| Doubao `doubao-seed-2-1-pro-260915` | [Ark metered entry](https://docs.volcengine.com/docs/ark/integrate-third-party-tools?lang=en) | Example used an older snapshot; verify 260915 and image/tool behavior |
| MiMo `mimo-v2.6-pro` | [MiMo metered integration](https://mimo.mi.com/docs/zh-CN/tokenplan/integration/claudecode) | Images, subagents, actual model and tool returns |
| MiniMax `MiniMax-M3.1-Flash` | [MiniMax Claude Code](https://platform.minimax.cn/docs/m-plan/claude-code) | Examples used subscriptions; verify metered keys and image/tool chain |
| Step `step-5-preview` | [Step Claude Code](https://platform.stepfun.com/docs/zh/guides/developer/integrations/claude-code.md) | Separate Step Plan from ordinary metered endpoints; verify images/tools |

Pass a profile's endpoint/key environment only to its process, without changing
global user settings. Override/isolate inherited Claude model/endpoints to avoid
cross-provider routing. Verify setting precedence and credential conflicts for
the pinned CLI. Audit actual models used by aliases, auxiliary requests,
subagents and fallback. Missing trustworthy model identity means unverified,
not a verified target-model run.

The recorded Opus 5.5 target was `claude-opus-5-5`, with adaptive thinking and
supported effort rather than copied manual thinking-token budgets or forced
tool_choice settings.
[Recorded model note](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5).

Strict model trials disable automatic model downgrade. Report other-model or
unknown-model calls explicitly; a top-level `--model` does not prove every
background call used Opus. Include auxiliary/subagent usage by model.
Count cache reads, 5m/1h writes, ordinary input, output and auxiliary models
separately. Distinguish API usage from client estimates; avoid adding cumulative
cost again on resume. Verify account quotas before launching.

Codex/Responses cache pricing and hit behavior do not automatically apply to an
Anthropic-compatible endpoint. Recheck each provider, region, plan, protocol and
actual usage fields. API-key automation was preferred; ordinary Claude login
remained an explicit interactive choice. Do not copy Desktop login files or
call subscription allowance API balance. Auth diagnostics report state and
variable names only.

## 9. Outer session and provider delivery scope

Desktop Code can read Claude-specific materials and use the same prepare/run/
status commands. Ordinary Desktop chat could use management MCP for requests
such as four task families at N-way concurrency, while a supervisor owns the
experiment lifecycle. Closing chat is not task completion.

Any authorized outer session may run management commands or management MCP.
Independent native CLI/SDK sessions execute policies using Claude or verified
Anthropic-compatible providers. Engineering and policy sessions remain separate.

Local Desktop may use stdio MCP. Slurm/remote use should favor an SSH tunnel to
a local MCP bridge. A remote connector originates in Anthropic's cloud and
cannot reach a merely local localhost server. A separately deployed reachable,
authenticated endpoint is required for that route; do not expose cluster
services automatically.
[Recorded networking reference](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

Each provider needs an independent profile for metered key, endpoint, model and
quota. Verify subscription scope, vision and permission for noninteractive use;
interactive compatibility does not establish batch authorization. Record native
compatibility gaps first. A custom gateway is an explicitly labeled option only
after protocol, images, tool continuation and costs are independently verified.

## 10. Implementation stages and acceptance artifacts

| Stage | Work / artifact | Acceptance condition |
| --- | --- | --- |
| A: design/capability freeze | Pin CLI/SDK; verify session/fork, role-scoped MCP, images and authority | Capability matrix; failed capabilities block the corresponding mode |
| B: independent entry/run package | Claude catalogs, prepare/doctor, frozen prompts/skills | Model-free/physics-free preparation of four Level 1 cases; source/asset hashes verify |
| C: native tools/single-role loop | MCP, native events, real image round trips and stable IDs | Synthetic image recognition, a different tool-returned image, then another call; no textual color-answer leakage |
| D: sessions/delegation | Resume, post-compaction recovery, fork, binding/reclaim and communication | Provenance holds; unauthorized children and duplicate/unknown calls rejected; same world without resets |
| E: complete supervision | START, waiting/wake, capacity errors, stop, sealing and usage | No duplicate delivery into active sessions; no post-deadline actions; failures retain evidence without restart |
| F: bounded real preflight | Explicit model/budget check and independent receipt | Receipt binds actual versions, configuration, prompts/skills and tool protocol |
| G: formal minimum batch | One minimum-arm Level 1 case per family on explicit user request | Four independent runs with images, raw usage, actions and private evaluation |
| H: Desktop/handoff | Code mode, management MCP and other outer managers | Fresh-clone reproduction; no Codex install required; complete config/assets without old login files |
| I: provider integrations | Individual Messages endpoints, credentials, models and preflights | Per-model images/tools/identity/quotas/billing/concurrency qualified; one failure does not break other profiles |

Paid checks in A/C/D require an explicit implementation-stage budget; the design
phase makes no model calls. A text-only reply cannot pass F: the actual image
and tool continuation loop must be verified.

## 11. Coupling points and invariants

The original Codex coupling spanned `scripts/benchmark.py`,
`codex_policy_host.js`, `codex_rpc.js`, `codex_preflight.js`,
`meta_dispatcher.js`, Codex fork-file checks in `runtime_cli.py`, source
allowlists in `runtime_store.py`, frozen-source lists in `run_setup.py`, and
Codex-specific handoff doctor behavior.

Build a native Claude runner/supervisor, rather than injecting fake Codex tools
into the old dispatcher. Shared session-observation/delegation validation may
become a platform-neutral contract with separate native Claude and historical
Codex evidence validators. Do not broaden a trusted-source allowlist to arbitrary
strings merely to accept a new engine.

Preserve frozen public inputs, action idempotence/unknown outcomes, role authority,
per-arm exclusion, return of control, 24-hour deadlines, one physical owner per
world, terminal sealing, private scoring, R14 hashes and independently simulated
worlds sharing newly generated Dial puzzles for within-batch model comparisons.
The original proposal also preserved its START/READY protocol; new runs now use
direct START, with READY only a capability query. Automatic retries, fallback
and filesystem checkpoints cannot bypass physical invariants.

Tests cover actual image results, asynchronous arms, authority, same-history
delegation, unknown receipts, 429 waits, budget/time stops and sealing; reuse
FakeWorld/protocol fixtures where appropriate. Avoid literal mirror tests for
documentation or reversible configuration. Shared changes require original Codex
core regression acceptance, without reliance on ignored files or other runs.

## 12. Git and handoff

The original work belonged on `codex/claude-code-harness`, split into reviewable
preparation/configuration, MCP/native execution, delegation/supervision, and
Desktop/handoff commits without unrelated scene changes. Do not import R15,
Oracle outputs, old policy history, `.env`, login state, machine-specific paths
or another worktree's virtual environment by default. Reproduce dependencies
and R14 assets with installation/hash verification.

Rebuild/update a PR from the handoff branch after implementation; merge only
after shared-core regression review. Deliver ordinary Git commits and explicit
asset packages. A colleague should clone, initialize dependencies/credentials,
and choose model, families, level, min_arms, parallel and budget from an authorized
outer session. Final CLI/Desktop names follow the implementation; proposed paths
in this document do not establish available commands.

## 14. Post-review implementation breakdown, recorded 2026-10-28

The original numbering jumps from 12 to 14 and is retained for references.
This baseline investigation used
`b3259aa817197f9bcb26ed7ccda02229b7c049ca`. The table records a plan, not an
implementation claim or a guarantee for unverified third-party services.

| Existing file / directory | Baseline finding | Planned implementation |
| --- | --- | --- |
| `scripts/benchmark.py` | Selection, profiles, freezing, locking and scheduling; writes codex.json and checks preflight/version/host | Separate engine-neutral selection/batch responsibilities; add Claude commands/config; retain the old entry until regression passes |
| `scripts/codex_policy_host.js`, `scripts/codex_rpc.js` | App-server turns/threads and dynamic robot tool; host owns roles/actions/images | Native runner + MCP with true binding and single-execution semantics, without pretending to be app-server |
| `scripts/meta_dispatcher.js` | Codex-specific observation, fork, send and wake | Preserve scheduling rules; observe trusted Claude events/control native sessions; unknown states require inspection |
| `runtime_cli.py`, `runtime_store.py`, `delegation.py` | CODEX_HOME ordinal/prefix hashes, two Codex observation sources, transactional ownership | Typed/versioned real evidence; preserve ownership/transactions; keep adaptive closed without verifiable Claude provenance |
| `runtime_service.py`, `pipeline.py`, `pipeline_client.py` | Role tokens, world, observations, action queue, private scoring and idempotence | Reuse public contracts with trusted actor binding; do not replay pending actions or recover a lost world |
| `run_setup.py`, `run_seal.py` | Frozen public/private inputs; Codex-specific source/template lists | Freeze Claude runner, MCP, prompts, skills, profiles, dependencies and versions; exclude engineering/private context from policies |
| `configs/models.json`, `configs/harnesses/policy.json`, `configs/task_families/current.json` | Responses profiles and partial engine/release coupling | Separate Claude profiles with per-model verification; preserve task registry and R14 physics |
| `scripts/benchmark_handoff.py`, `docs/multimodel-handoff.md` | Reusable asset restoration but Codex-dependent doctor/install guide | Independent Claude doctor, credentials/environment, assets and fresh-clone documentation |
| `test_cli_benchmark.py`, `test_runtime_store.py`, `test_delegation.py`, `test_meta_dispatcher.cjs`, `test_codex_preflight.js`, `test_execution_contract.py`, `test_run_setup.py` | Existing tests do not prove Claude image/fork/identity/events | Preserve them; add native-shaped offline integrations, fault injection and authorized provider checks |

Minimum progression conditions:

1. **Baseline/capability inventory.** Freeze commit, CLI/SDK and config; check
   dependencies and published asset hashes. Use local help and official sources
   for MCP images, events, resume/fork, isolation and version boundaries. Record
   the capability matrix and unknowns.
2. **Clean prepare/doctor.** Create independent catalogs/commands, select four
   minimum-arm Level 1 cases, and freeze every input. Diagnose missing assets,
   dependencies and credential variables without requesting a model. Model-free
   preparation must work in an environment without a Codex executable.
3. **Minimal offline end-to-end route.** Use a controlled stub to test startup,
   actual image content in MCP results, binding, native session/turn events and
   stopping. Stub external interfaces must match the pinned version. This proves
   host behavior, not a real provider's compatibility.
4. **Physics/fault integration.** Test one Controller, concurrent arms, images,
   messages, real state and ending semantics in a local test world. Inject
   disconnects, unknown receipts, subprocess failures and duplicate requests.
   Never recreate a lost world and resume scoring. Use recoverable test assets
   and explicitly nonformal results.
5. **Roles/history/dynamic delegation.** Verify native inheritance boundaries,
   trusted provenance, actual child authority, observed parent/child state,
   handback and failure handling. Inject duplicate forks and unknown startup.
   Unproven original conditions keep the mode closed; alternatives must be
   labeled different experimental conditions rather than equivalent behavior.
6. **Bounded real-model preflight.** With usable credentials and authorized
   allowance, check the exact model's text, input image, tools, a new returned
   image, native resume and any required fork/compaction. Record identity, route,
   versions and costs without keys. A failed/unverified provider cannot launch
   formal trials.
7. **Delivery/real experiment.** Finish concurrency/resource/cost controls,
   interruptible supervision, docs and fresh-clone restoration. Present per-model
   preflight results first. Start a real four-case Level 1 batch only on explicit
   instruction; task count is not request concurrency.
8. **Return to main.** Commit only code/tests/key-free docs to the Claude branch;
   validate in an isolated worktree, push the dedicated branch, compare via PR,
   resolve conflicts and regress against main. Git does not merge physical
   worktree directories, `.env`, ignored assets or run evidence automatically.

Every stage must distinguish implemented, offline-only, real-provider-verified
and restricted/unavailable. A tool starting, CLI exit zero or model saying
"done" is not task success.
