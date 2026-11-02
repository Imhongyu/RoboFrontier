# Native Codex policy execution

For new experiments, use the [unified CLI](unified-cli.md) and its versioned TOML.
This guide explains the native Codex path and the retained
`python -m scripts.benchmark` interface. See the [Linux guide](server-benchmark.md)
for environment choices, and the [multi-model handoff](multimodel-handoff.md) for
the original branch handoff. Claude has a separate native runner and
[component map](claude-codex-parity.md).

An outer Desktop session, another coding agent, or a shell can invoke and monitor
the command. The measured policy runs in independent native Codex app-server
sessions; an outer chat does not have to remain inside a tool turn. The manager
performs engineering operations, not private task strategy or physical recovery.

Each model/case has an independent run, MuJoCo world, SQLite state, authenticated
connections, policy history, and work notes. Adaptive is the default: only its
Controller decides when and how to delegate within the task. The host does not
choose grasp/placement routes. Single, Controller + Worker, and Worker-Worker
have their own authority and initial-role contracts. New runs use explicit
[direct START](unified-cli.md#startup-in-all-four-modes); capability `ready` does
not require a waiting turn.

Parallelism counts whole tasks. Adaptive delegates and standing Workers add
model requests within each task. For a shared prepared multi-model batch, each
Dial case uses the same newly sampled private puzzle across models, with
independent worlds and work notes. A new batch samples a new puzzle. Task
parallelism is not a provider quota guarantee.

## Model catalog and authentication

Profiles are in `configs/models.json`. The unified default is `luna`,
`gpt-6-luna/high`, through `OPENAI_API_KEY`. The retained native CLI still defaults
to its historical `astra` selection and parallelism; do not confuse that with
the unified TOML. Process-local model/provider settings do not overwrite the
user's global Codex defaults or sign-in.

The following is the **2026-10-28 catalog/documentation snapshot**, retained for
provenance rather than a current model ranking or provider availability promise:

| Provider | Catalog vision candidate | Original documentation |
| --- | --- | --- |
| DeepSeek | `deepseek-flash`; the referenced V4 Pro was text-only, with V4.1 Flash identified as the visual candidate | [Model/pricing documentation](https://api-docs.deepseek.com/quick_start/pricing/), [Codex integration](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/) |
| Qwen | Fixed `qwen3.8-max-0902` snapshot | [Vision](https://help.aliyun.com/zh/model-studio/vision-model), [Responses](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses) |
| Zhipu | `glm-5.3-flash` native-multimodal candidate; the referenced GLM-5.3 was text-only | [Text model](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3), [Vision candidate](https://docs.bigmodel.cn/cn/guide/models/vlm/glm-5.3-flash), [Responses](https://docs.bigmodel.cn/cn/guide/develop/responses/introduction) |
| Kimi | `kimi-k3.1-pro` | [Model guide](https://platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart), [Codex integration](https://platform.kimi.com/docs/guide/codex-kimi) |

A provider's flagship label is not our measured ranking. A text-only model is
not silently combined with a different vision model under one score. A coding
subscription does not establish the pay-as-you-go API permissions, image support,
Responses transport, or tools required here. Verify the actual account/profile
through preflight; catalog configuration alone is not qualification.

Use the ignored local `.env` or process environment. Existing environment values
take precedence. Literal `.env` parsing executes no shell. The provider variables
include `DEEPSEEK_API_KEY`, `DASHSCOPE_API_KEY`, `ZAI_API_KEY`, and `KIMI_API_KEY`.
Qwen additionally reads `DASHSCOPE_BASE_URL` for the actual workspace/region
endpoint supplied by the provider, for example
`https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`.
Never commit keys, put them in model JSON or command arguments, or share them in
chat. Use `benchmark_handoff init-env` to create a private template if absent.

For a third-party provider, the native process-local configuration has this
shape; the harness generates it rather than replacing global configuration:

```toml
[model_providers.deepseek]
name = "DeepSeek"
base_url = "https://api.deepseek.com"
env_key = "DEEPSEEK_API_KEY"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
```

The retained Kimi endpoint is `https://api.moonshot.cn/v1` with `KIMI_API_KEY`;
Zhipu uses `https://open.bigmodel.cn/api/v1` with `ZAI_API_KEY`; Qwen uses the
operator's workspace endpoint and `DASHSCOPE_API_KEY`. The matching catalog,
provider address, image modalities, tool mode, and context settings are frozen.
Simply changing `-m` or having a Chat Completions endpoint does not prove that
Codex can receive images or call robot tools. The supported runner uses Responses;
changing `wire_api` to `chat` is not a compatibility fix. See the
[official configuration reference](https://developers.openai.com/codex/config-reference/).

Native subscription profiles use Codex's own authentication rather than pretending
a subscription credit is an API key. The isolated API-home path does not clone
OAuth state. Concurrent subscription refresh/isolation remains a separate
qualification boundary; see the current unified authentication guidance.

## Preflight, preparation, and launch

Prefer the unified commands, which use current TOML defaults:

```sh
.venv/bin/robofrontier bootstrap
.venv/bin/robofrontier plan
.venv/bin/robofrontier doctor
# Billable provider compatibility check, separately authorized.
.venv/bin/robofrontier preflight --confirm-spend
.venv/bin/robofrontier prepare --output runs/policy/NEW_BATCH
.venv/bin/robofrontier run runs/policy/NEW_BATCH
```

Use the explicit Linux CPU or macOS native renderer when appropriate; the default
is Linux NVIDIA. A prepared batch keeps its frozen backend. Preparation calls
no model, starts no physical world, and requires a new output directory.

The retained native interface is useful for reproducing its original workflows:

```sh
.venv/bin/python -m scripts.benchmark models
# Billable: images, tools, manual compaction and native fork checks.
.venv/bin/python -m scripts.benchmark preflight --models astra
.venv/bin/python -m scripts.benchmark prepare --models astra \
  --families mosaic --output runs/policy/NEW_NATIVE_BATCH
.venv/bin/python -m scripts.benchmark run runs/policy/NEW_NATIVE_BATCH --parallel 9
.venv/bin/python -m scripts.benchmark status runs/policy/NEW_NATIVE_BATCH
.venv/bin/python -m scripts.benchmark stop runs/policy/NEW_NATIVE_BATCH
```

Omitting family/case filters prepares all 36 cases per selected model. The native
entry accepts up to 36 task slots, but local CPU, memory, disk, rendering, native
sessions, delegates, and provider capacity remain real bounds. Prepare a new
batch after changing execution source or frozen inputs; never restart a previously
started physical world to reuse its result directory.

Execution checks the compatibility receipt against the actual profile, provider
address, context, effort, generated model metadata, and native CLI version. The
full check exercises image/tool round trips, manual compaction, and inherited
fork history followed by tools. It does not establish the complete context window,
automatic compaction threshold, provider's internal model identity, task ability,
or long-term stability. A smoke-only receipt does not qualify a scored run.

The current release selects policy Mosaic R14. Historical Oracle/Factory
recordings retain their frozen R13 source colors. Unified new Oracle executions
select current released scenes independently. Another worktree's R15 draft does
not silently enter this registry or replace historical evidence.

## Time, capacity recovery, and context

The public default is 24 hours from each task's persisted START, including policy
reading, reasoning, tools, communication, fork setup, and capacity waits. The
physical service enforces its deadline: bar new actions, request braking, evaluate
the cutoff, and seal recording. Settling after the deadline is not timely success.
The host does not add a second fixed deadline from process creation. Startup
readiness and an operator's engineering stop are separate. Slurm allocations
must cover startup and cleanup as well as task execution. Ended worlds never
silently restart.

Explicit failed capacity/rate-limited turns wait at least ten seconds and can
continue the same native session only under the safe runtime conditions. They
do not replay robot motion, reset the world, or extend the deadline. Authentication,
quota exhaustion, and ordinary task errors are not blindly retried as capacity
errors. Unknown creation/fork/send acknowledgements retain evidence and stop
automatic replay. For uncertain physical operations, query the original request
ID; a new ordinary request normally omits the outer `call_id` so the host assigns
it. Querying an old job uses that old action ID inside `data.call_id`.

The catalog requests a 272,000-token context window and 245,000-token automatic
compaction threshold. Settings do not enlarge the provider's real context.
System/output reservations and the native catalog's effective-window allowance
can change the displayed available size; the historical 95% example was about
258,400 tokens. Preserve the actual requested/reported values, tokenizer,
compaction behavior, effort, response model identity, and date. Equal effort
names do not establish equal computation across providers or engines.

## Images, motion, and later video

The policy receives real selected-camera RGB through MuJoCo and its explicit
OpenGL backend. Tools return JSON and selected image content; a file path alone
does not prove the model saw an image. Current observations use JPEG
896 x 560 at quality 85. Hidden service operation does not continuously draw a
preview; real-time video encoding is optional and disabled by default.

The recorder samples physical state at 60 Hz, independently of screenshots,
including arm/object motion and appearance events. Sampling at physical substeps
does not preserve arbitrary changes above that bandwidth. Current float32/XOR
compression retains states and timestamps; old streams remain readable. Removing
idle or unproductive intervals is an editable presentation derivative and does
not overwrite the original evidence. Native session collection externalizes
image payloads into shared objects for portable archives; it does not change
what was sent to the API. See [evidence storage](evidence-storage.md).

Later [Factory rendering](factory.md) replays recorded motion without dynamics,
with independent 30 fps/1080p or configured output quality. It need not use the
model-observation resolution. Each recording uses matching frozen geometry,
parameters, appearance events, and edits.

## Native sessions and Desktop

The host uses native `thread/start`, `turn/start`, and `thread/fork`, binds real
session IDs, and verifies fork lineage through parent ID, source ordinal, and
history hashes. Initial task sessions are clean; only an authorized in-task
delegate inherits its own Controller's allowed current-task history.

Subscription batches share one dedicated home, `~/.robofrontier/codex-home`
(or `CODEX_HOME` when set), never the personal `~/.codex`, so personal
configuration, MCP servers, apps and sessions stay out of trials. Log in there
once with `CODEX_HOME=~/.robofrontier/codex-home codex login`; a batch refuses to
start without that login. The policy permission profile denies the home.

New API runs isolate Codex homes per task. That task's Controller, snapshots,
and delegates share its home to retain native lineage. Different tasks have
different homes. The resolved home is recorded in the run's Codex home marker;
original transcripts are under its `sessions/` directory, and run-v6 runs also
keep verified copies in `private/engine/transcripts/` ([evidence storage](evidence-storage.md#session-transcripts)). Legacy shared-home
runs keep their recorded location. Collection preserves the relevant native
traces without exporting authentication/config/state databases.

Status reports native IDs and observed states. A separate Desktop's `notLoaded`
label does not establish that an app-server stopped. Do not manually start a
competing turn in a live task's session. Desktop visibility can depend on source,
provider, sign-in, and project filters; automatic visibility of every third-party
session is not qualified, and the host does not forge Desktop private databases.
When auditing native `thread/list`, include the relevant app-server/exec sources
rather than assuming the interactive default covers every session. See the
[official app-server guide](https://developers.openai.com/codex/app-server/).

Local real-CLI checks use a synthetic Responses service without external billing:

```sh
.venv/bin/python -m scripts.check_codex_cli --output runs/engineering/NEW_CLI_CHECK
.venv/bin/python -m scripts.check_codex_snapshot
```

A passed offline check is evidence for its exact protocol/version, not acceptance
of every external provider or a formal task score. Current check scope is in the
integration ledger. Role permissions and authenticated tools define the benchmark
interface; they are not a claim of operating-system containment against malicious
policy code.
