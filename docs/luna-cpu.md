# Luna CPU execution on Linux and Slurm

This guide describes the unified `integration/unified-main` checkout. It has
not yet replaced the published default branch. Start with the [unified CLI](unified-cli.md)
and use the [Slurm staging guide](slurm.md) for queue execution. The native
`scripts.luna_cpu` wrapper remains a compatibility entry, with different Codex
home behavior; it is not the new cluster submission mechanism.

New-run defaults select Luna/high, official OpenAI API authentication, adaptive
organization, all 36 R14 task selections and 36 requested concurrent task hosts.
CPU rendering is an explicit override of the unified Linux NVIDIA default.
MuJoCo dynamics always use CPU; Linux CPU images use Mesa OSMesa/llvmpipe.
Adaptive delegates may create more native sessions/model requests than tasks.
No outer LLM session is needed to prepare, launch, monitor, stop or collect.

A task's default 86,400-second limit starts at its persisted START, separately
for every task. The host does not impose another fixed 24 hours from process
creation. The initial launch interval is 0.3 seconds. Startup timeout, scheduler
allocation lifetime and cleanup allowance are separate. A 36-task capacity or
long-running provider qualification has not been demonstrated on your cluster.

## Install and verify

Use Python 3.12, the locked uv environment, Node.js, and Codex CLI. The integration
checks use Codex 0.165.0; this is a reproducibility pin, not a latest-version
claim. Linux CPU rendering needs Mesa OSMesa and an operating environment that
supports the native Codex sandbox. Configure software according to the site's
rules; a site may not provide Docker or permit installing system packages.

```sh
uv sync --locked --extra oracle
npm install --prefix "$PWD/.codex-tools" @openai/codex@0.165.0
export PATH="$PWD/.codex-tools/node_modules/.bin:$PATH"
cp .env.example .env
chmod 600 .env
# Edit OPENAI_API_KEY locally; do not print or commit its value.
.venv/bin/robofrontier bootstrap
.venv/bin/robofrontier doctor --render cpu
```

Do not replace an existing `.env` with the template. On Debian-family systems,
`libosmesa6` supplies the relevant software GL library. Doctor checks local CLI,
sandbox and actual rendering prerequisites without calling a model. Native
macOS does not support this OSMesa mode: use `--render native` for Mac rendering,
or use the [Linux container flow](docker.md) for CPU OSMesa.

Policy bootstrap automatically restores the approximately 186 MB pinned archive,
checks its SHA-256, and verifies referenced assets. The package is
`policy-assets-rolling003-20261029.tar.gz` in the
[handoff-20261028 release](https://github.com/changxuanfan/RoboFrontier/releases/tag/handoff-20261028),
SHA-256 `1bb7420c38c44b7e2f469d3789a1c0096a4f5cf6d377894d1ae2c1b0a8de2d31`.
Release and asset upload dates need not match. Correct installed files are reused;
`already_complete` does not imply a new download/cache file. A conflicting file
or wrong package fails verification rather than being approximated or relabeled.
For an offline machine, transfer the pinned package and run:

```sh
.venv/bin/python -m scripts.benchmark_handoff setup-assets \
  --archive /path/to/policy-assets-rolling003-20261029.tar.gz
```

The separate multi-gigabyte Factory recording package is not needed for policy
execution. API credentials are local per user; a local SSH driver does not
implicitly transmit its environment to a remote machine.

## Configure and run without Slurm

Create an operator TOML on a filesystem local to the executing machine:

```toml
# luna-cpu-site.toml
[render]
device = "cpu"

[slurm]
gpus = 0
```

The root defaults supply Luna/high, adaptive, 36 tasks, 36 concurrent slots and a
24-hour task clock. For a 12-hour task, set `batch.task_wall_limit_s = 43200.0` in
the appropriate `[batch]` table. The scheduler allocation must also cover setup,
execution and stage-out. This task clock is not a monetary cap.

```sh
.venv/bin/robofrontier --config luna-cpu-site.toml plan
.venv/bin/robofrontier --config luna-cpu-site.toml preflight --confirm-spend
.venv/bin/robofrontier --config luna-cpu-site.toml prepare \
  --output runs/policy/luna-all-36
.venv/bin/robofrontier run runs/policy/luna-all-36
```

Only run a paid preflight/execution with the account owner's authorization. A
small smoke receipt does not replace the required complete provider receipt.
Preparation itself freezes inputs and calls no model. Use a new output directory
for each batch. A changed CLI/model/provider/configuration needs a matching new
preflight. The foreground runner waits for its batch; it is not detached merely
because a chat tool returned. Use an appropriate persistent process/job manager.

For a small Level 1 engineering selection, add `--level 1 --min-arms --parallel 4`
to `prepare` and inspect the four-task plan first. Change task duration in TOML,
not by editing a frozen task or altering source hashes.

```sh
.venv/bin/robofrontier status runs/policy/luna-all-36
.venv/bin/robofrontier stop runs/policy/luna-all-36
```

The 24 hours are a maximum, not a requirement to keep a completed task alive.
Controller may finish after completion or a publicly justified unrecoverable
state, once actions/delegates are resolved. Finish triggers evaluation; a claim
of success alone cannot pass the scorer. Incomplete or interrupted tasks retain
that outcome. No automatic physical-world restart or replay follows a crash.

## Queue on Slurm

Active SQLite WAL files, Codex homes/sessions, temporary data, observations and
motion must live on verified **node-local storage**, not Lustre/NFS. Shared
storage can hold the committed source, read-only assets and stopped stage-out
packages. Do not write large data into quota-limited home directories. The
[Slurm guide](slurm.md) specifies node-local filesystem checks, descendant-process
tracking, API credential handling, stop warnings and verified stage-out. Real
allocation, x86_64/NVIDIA and site-specific capacity qualification remain open.

From the Linux login node, after the explicit preflight and site resource review:

```sh
.venv/bin/robofrontier --config luna-cpu-site.toml slurm-submit \
  --output runs/submissions/luna-all-36
.venv/bin/robofrontier --config luna-cpu-site.toml slurm-submit \
  --output runs/submissions/another-luna-all-36 --queue
squeue -u "$USER"
```

The first example only freezes a submission. The second freezes a different new
submission and explicitly queues it. Do not reuse the same output directory to
submit a second experiment. The snapshot pins committed source, settings,
launcher and verified assets. It does not rely on later checkout edits. Resource
requests are not proof that 36 tasks plus delegates fit available memory/API
limits. Slurm time includes setup and cleanup, independently of task START.

Both old sbatch files, `scripts/slurm_luna_cpu.sh` and
`scripts/slurm_luna_l3_max_test.sh`, exit with migration instructions. They do not
create shared active databases or run a hidden paid preflight. Their old
`RF_BATCH_OUTPUT`, `RF_WALL_LIMIT_S` and `RF_PARALLEL` workflow is retired.

### Four maximum-arm Level 3 tasks

Copy [`configs/examples/luna-l3-cpu.toml`](../configs/examples/luna-l3-cpu.toml) to
an untracked site TOML and review partition/account/CPU/memory/scratch settings:

```sh
cp configs/examples/luna-l3-cpu.toml l3-cpu-site.toml
.venv/bin/robofrontier --config l3-cpu-site.toml plan
```

| Family | Task | Arms |
| --- | --- | ---: |
| Transport | `transport-a12-d3` | 12 |
| Mosaic | `mosaic-a08-12x24-d3` | 8 |
| Relay | `relay-a16-d3` | 16 |
| BEST5 Dial | `dial-best5-n08-d3` | 16 |

The example requests exactly these four tasks, parallel 4, Luna/high/adaptive,
CPU observations, one hour per task after START, and a two-hour Slurm allocation
ceiling. Other resource requests inherit the root defaults until you edit them;
they are not measured requirements. For a 30-minute task cap, set
`batch.task_wall_limit_s = 1800.0`. Keep setup/stage-out allowance in the allocation.
Use the same explicit preflight and `slurm-submit --queue` flow as above. This
engineering selection is not a replacement for the 36-task/24-hour defaults.

## Evidence and resource metrics

New unified API runs isolate task-native Codex state; the batch records actual
home/session paths. The native Luna compatibility wrapper instead records its
batch home in `codex-home.json`, generally under
`.codex-luna/<batch-name>-<path-hash>/sessions/`. Neither location is the shared
server user's default `~/.codex` unless explicitly configured that way. Docker
uses persistent local volumes and exports stopped results; inspect that flow's
own recorded paths rather than guessing a host path.

`private/outputs/codex-host.jsonl` contains host scheduling/tool/timing events,
not the complete native session. Native `<session-id>.jsonl` traces retain model
turn evidence. Motion, frozen source, process events and referenced JPEGs have
separate output paths. Realtime MP4 is off by default; later offline video can
use another resolution/background. The [evidence guide](evidence-storage.md)
explains compression, image references, collection manifests, verified ZIPs,
restore and provenance. Collection copies originals; it does not silently delete
source evidence or turn engineering errors into model failures.

Inspect metrics in the same execution context, using stopped evidence when a
command opens SQLite. Do not read a live container database from the Mac host,
or an active node database across a shared mount. Native compatibility commands
include `scripts.luna_cpu usage`, `performance` and `collect`. Usage deduplicates
recorded responses and reports missing traces; it is not the provider bill.
Completed-response TPM is not a provider admission/rate-limit counter. Model
turn duration includes tool waits; action and model intervals overlap and must
not be summed as disjoint cost/time categories. Owner counters are not a complete
continuous CPU/RSS profiler. Where configured, Slurm can report:

```sh
sacct -j JOB_ID --format=JobID,State,Elapsed,AllocCPUS,MaxRSS,TotalCPU
```

Site accounting determines metric scope. Inspect missing sessions/evaluations,
unsealed outcomes and stage-out receipts before sharing a collected package.
A backup is a separately retained verified copy, not merely an ignored run folder.

## Native compatibility commands

For a local Linux filesystem and an existing compatible environment, the native
wrapper retains `setup-assets`, `doctor`, `preflight`, `prepare`, `submit`, `run`,
`status`, `stop`, `usage`, `performance`, `collect`, and `l3-max-test`. Its profiles
include `luna`, `openlux-luna` and `openlux-terra`; changing profile changes the
required API key and provider preflight. It does not stage live state to Slurm
scratch. Prefer the unified entry for new task-isolated/concurrent deployments.

The following remains a model-free way to inspect the legacy L3 preparation:

```sh
.venv/bin/python -m scripts.luna_cpu l3-max-test --prepare-only \
  --output runs/policy/legacy-l3-draft
```

Its native one-hour default, optional `--wall-limit-s`, parallel-4 selection and
private `codex-home.json` marker remain compatibility behavior. An already
prepared directory is executed with its separate native `run` command after a
matching preflight, not by invoking `l3-max-test` over it again. Never move a
prepared live batch between machines/absolute paths or mix native and unified
configuration markers. Old Docker commands/image defaults are documented as
Legacy; new work should use the frozen [Docker commands](docker.md).
