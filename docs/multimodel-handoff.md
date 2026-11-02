# Multi-model handoff and worktree collaboration

For new work use the [unified CLI](unified-cli.md), [Docker](docker.md),
[Slurm](slurm.md) and [evidence storage](evidence-storage.md) guides. This checkout
is integrating `integration/unified-main`; that work has not yet replaced the
published default branch. The native `scripts.benchmark` entry is retained for
Codex compatibility and has different defaults from the unified entry.

## Scope and provenance

The original `codex/multimodel-handoff` branch was created from
`codex/server-benchmark-prep`, commit
`3638e1c351b6e885ac94e3256f5782f8aecd46ee`. Forking a chat did not copy a Git
worktree; the code base was checked separately. The original Harness session's
running experiments remained its responsibility. This is historical provenance,
not a claim that every current integration file equals that original commit.

Current policy selection retains Transport R14, Mosaic R14, Relay's final goal
policy and BEST5 Dial R11. Mosaic R15 drafts are not a default. Frozen historical
recordings retain their own source/colors/physical parameters; new code must not
silently apply current physics or scoring to an old recording.

An optional outer coding-agent session can prepare, launch, inspect engineering
errors and collect results using commands. It need not use the same model or
engine as the evaluated policy. The selected engine profile and frozen runtime
configuration determine the actual policy, not the manager's chat model.
The [manager prompt](../prompts/benchmark-manager.md) defines its authority:
policy decisions, task images and robot actions belong to the evaluated roles.
An outer manager that changes inputs or injects strategy can invalidate a run;
command-based orchestration alone does not establish independence.

Native Codex and Claude Code use their respective supported authentication flows.
An official API profile and a subscription/OAuth profile are different choices;
a subscription in one product is not a transferable API credential for every
engine/provider. Cross-provider model names do not establish image, tool, fork,
compression, budget or authentication compatibility. Perform the matching native
preflight; keep the actual requested/observed configuration with the evidence.

## GitHub, branches and offline bundles

The repository is [changxuanfan/RoboFrontier](https://github.com/changxuanfan/RoboFrontier).
A worktree is a directory checked out on a branch. Committing there advances
that branch, not `main`. A branch can be shared without first merging main.
Cloning public code does not grant push permission; writers need the repository
owner's access invitation or their own fork/PR workflow. GitHub access settings
are separate from code, assets and model authentication.

The historical Codex handoff can be cloned explicitly:

```sh
git clone --branch codex/multimodel-handoff \
  https://github.com/changxuanfan/RoboFrontier.git RoboFrontier
cd RoboFrontier
git switch -c experiments/my-model
```

That command selects the historical branch, not this unpublished unified
integration. Use the reviewed published ref appropriate to the experiment.
For an existing checkout, inspect `git status --short`, `git branch --show-current`
and `git log -1` before updating. Do not discard local work to force a pull.

An offline Git bundle contains selected Git history/refs; it is not a running
worktree, dependency installer, model login, asset archive or synchronization
service. The original handoff called its bundle `roomscript2.bundle`. A receiver
can clone a verified bundle containing the intended branch:

```sh
git clone --branch codex/multimodel-handoff /path/to/roomscript2.bundle RoboFrontier
```

Later updates require a remote fetch or another bundle. Share only reviewed refs;
ignored credentials/runs do not enter a new bundle merely because they are in a
worktree, but Git history itself must still be reviewed before publication.

## Assets and local environment

Install Python 3.12, uv, Node.js and the chosen native CLI. The integration checks
use Codex 0.165.0 and Claude Code 2.1.312, not a claim about latest upstream
versions. The original handoff's `0.164.0-alpha.11.1` was a historical test pin;
do not treat its provider receipt as valid for another installed CLI.

```sh
uv sync --locked --extra oracle
.venv/bin/robofrontier bootstrap
.venv/bin/python -m scripts.benchmark_handoff init-env
```

`init-env` creates `.env` only if absent, with mode 600. Edit an existing file
locally. The loader reads literal values rather than executing shell syntax;
process environment values take precedence. Do not `source` an unreviewed file
or transfer someone else's native login. Relevant profile credentials include:

```dotenv
OPENAI_API_KEY=
OPENLUX_API_KEY=
ANTHROPIC_API_KEY=
KIMI_API_KEY=
DASHSCOPE_API_KEY=
DASHSCOPE_BASE_URL=
ZAI_API_KEY=
DEEPSEEK_API_KEY=
```

Configure only the selected profiles. A local manager controlling SSH does not
automatically forward its keys to the remote process. The tools target POSIX
macOS/Linux environments with file locks; graphics and sandbox prerequisites
must be verified on the execution machine.

Preparation automatically installs/verifies the policy package if needed; a
plain `git clone` cannot run an installation step. The pinned archive is
`policy-assets-rolling003-20261029.tar.gz` from the
[handoff-20261028 release](https://github.com/changxuanfan/RoboFrontier/releases/tag/handoff-20261028),
SHA-256 `1bb7420c38c44b7e2f469d3789a1c0096a4f5cf6d377894d1ae2c1b0a8de2d31`.
It supplies the required 36-task scene assets and Panda upstream source/licenses,
not user authentication, experiment results or prepared worlds. Do not replace a
missing asset with an approximate texture or alter an expected fingerprint.

Offline preparation can use a separately transferred verified archive:

```sh
.venv/bin/python -m scripts.benchmark_handoff setup-assets \
  --archive /path/to/policy-assets-rolling003-20261029.tar.gz
```

A receiver can also download that named asset with their own authorized `gh`
installation. Any private-repository access requirement is determined by the
repository's actual settings. The independent Factory package has a separate
lock/installer; it is not downloaded by ordinary policy bootstrap.

## Providers and preflight

The native Codex catalog is `configs/models.json`; Claude has
`configs/claude-models.json`. Profiles are not provider-availability certificates.
The dated [pricing research](archive/model-pricing-20261028.md) and
[compatibility comparison](archive/model-compatibility-20261028.md) are historical research,
not current price/rate-limit guarantees. Candidate models not in the catalog
cannot be launched merely because they appear in those tables.

For Qwen, set the actual workspace/region Responses-compatible base URL, such as
`https://<WorkspaceId>.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`, rather than
assuming an ordinary Chat Completions endpoint is interchangeable. Configured
third-party endpoints still require real account-specific verification. Codex
provider configuration uses `wire_api="responses"`; image declarations alone do
not establish that image content actually reaches the model. See the native
[Codex guide](gpt-policy.md) and its official documentation links.

Run local checks before a paid test:

```sh
.venv/bin/robofrontier doctor --engine codex --profile kimi --render native
.venv/bin/python -m scripts.check_codex_cli --output runs/engineering/local-cli-check
.venv/bin/robofrontier plan --engine codex --profile kimi --level 1 --min-arms --parallel 4
```

Use `--render cpu` on Linux OSMesa or the default NVIDIA backend on an equipped
Linux host. Doctor checks local prerequisites; it is not proof of account access.
The CLI stub check exercises local native interfaces, images and fork behavior;
it is not a successful call to Kimi/Qwen/GLM/DeepSeek.

With the account owner's authorization, a paid smoke-only test can check a small
synthetic image/tool round trip. A complete paid preflight additionally exercises
manual compaction and fork history/tool use:

```sh
.venv/bin/robofrontier preflight --profile kimi --render native --smoke-only --confirm-spend
.venv/bin/robofrontier preflight --profile kimi --render native --confirm-spend
```

Smoke receipts do not replace complete qualification. These checks do not stress
every context size, establish autonomous compaction under all loads, prove the
provider's actual backing model identity, or qualify every robot task. Change
model, endpoint, effort, catalog or CLI version only with a matching new check.
Native Codex compatibility reports remain under
`runs/engineering/model-smoke/<profile>/report.json` and
`runs/engineering/model-compatibility/<profile>/report.json` respectively.

## Select tasks and concurrency

New unified defaults are Luna/high, adaptive, 36 concurrent task hosts and a
24-hour limit from each task's persisted START. The retained native
`scripts.benchmark run` default is parallel 9. Always inspect a plan rather than
assuming two entries use identical defaults.

| Selection | Tasks per model | Four model profiles |
| --- | ---: | ---: |
| Level 1, minimum arms in each family | 4 | 16 |
| Level 1, every scale | 12 | 48 |
| All levels and scales | 36 | 144 |

Minimum-arm Level 1 selects Transport 4, Mosaic 4, Relay 8 and Dial 4 arms.
Level 2 selects 4, 4, 8 and 8 respectively. Dial's `n04` denotes dial count,
not necessarily arm count. Selection reads actual task metadata.

For one model's four Level 1 tasks, after matching preflight:

```sh
.venv/bin/robofrontier prepare --engine codex --profile kimi --render native \
  --level 1 --min-arms --parallel 4 --output runs/policy/kimi-l1-small-001
.venv/bin/robofrontier run runs/policy/kimi-l1-small-001
.venv/bin/robofrontier status runs/policy/kimi-l1-small-001
.venv/bin/robofrontier stop runs/policy/kimi-l1-small-001
```

Preparation freezes code, public task inputs, profile/configuration and independent
worlds without launching a model. Task concurrency is not native session count
or provider request concurrency; delegates, turns and forks add model requests.
Concurrent batches add their loads. CPU, RAM, rendering and account RPM/TPM can
all limit throughput. No setting silently guarantees successful 36-way execution.

For a deliberately shared Dial random instance across multiple Codex profiles,
the native compatibility entry retains one combined preparation:

```sh
.venv/bin/python -m scripts.benchmark prepare --models kimi qwen glm deepseek \
  --level 1 --min-arms --output runs/policy/native-four-model-comparison
.venv/bin/python -m scripts.benchmark run runs/policy/native-four-model-comparison --parallel 4
```

This selects 16 tasks that execute in batches of up to four. Independent
preparations can generate different Dial instances. It is a native compatibility
workflow, not a 144-task unified concurrency setting. Keep profile-specific
context/compaction thresholds and requested effort in reports: identical effort
strings do not prove identical compute. Do not infer current values from the
original handoff's 272,000/245,000 context/compaction snapshot.

Finish is subject to action/delegation safety checks and then evaluation; saying
"done" does not prove success. STOP requests a graceful shutdown rather than an
immediate kill. Unstarted tasks can be skipped. A crashed physical world is not
automatically restarted or replayed. Keep unsealed/uncertain outcomes for audit.
Use a fresh directory for another experiment. Level 2 is a new explicit selection,
not an implicit promotion by the runner. Task limits are not payment caps.

The host event file under each task's `private/outputs/` is distinct from native
session JSONL. Tool observations are rendered scene images, not automatic desktop
screenshots. Use the shared stopped-evidence collector/ZIP verifier for sessions,
motion, referenced JPEGs and scoring evidence; see [storage](evidence-storage.md).
Never monitor a live database across Docker/network filesystem boundaries.

## Worktrees and eventual merge

A linked worktree shares Git history but has its own checked-out branch and
working files. One branch cannot normally be checked out in two linked worktrees
at once. A coworker's independent clone can use a personal branch; a second
worktree in one clone can be created from the intended reviewed base:

```sh
git worktree add -b experiments/kimi-l1 ../RoboFrontier-kimi codex/multimodel-handoff
```

The example preserves the historical Codex base. Choose the reviewed unified
ref after it is published when the integration features are required. Worktree
creation does not copy ignored `.env`, Python environments, run directories or
untracked assets. Rebuild dependencies and use verified read-only assets; keep
new prepared worlds and runtime directories independent. Prepare on the target
machine/path rather than moving a frozen executable batch with absolute paths.

Commit only the reviewed code, push your branch, then open a PR. Before merging
into main, verify its branch/status, review the complete diff, resolve conflicts
and run the appropriate checks. Preserve teammates' commits and do not force-push
over their work. Git merges tracked code; ignored assets, credentials, native
sessions and experiment outputs require their own verified handoff. A merged
branch alone does not publish a new asset release or prove the entire integration
qualified.
