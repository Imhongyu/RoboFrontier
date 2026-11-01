# Unified main integration

This document tracks implementation gates. It is not a statement that all gates
have passed. Work is isolated on `integration/unified-main`; existing worktrees
and `main` remain intact until the integration is reviewed.

## Product

**RoboFrontier: Benchmarking How LLM Agents Organize, Communicate, and Collaborate
in a Multi-Robot World**

Confirmed first author: **Changxuan Fan**, **Hong Kong University of Science and
Technology**. The full author list, author order beyond first author, copyright
holder, publication status, DOI, and paper URL are not finalized. Do not infer
these fields from Git history or the repository owner.

## Sources and provenance

| Source | Pinned source commit | Integration intent |
| --- | --- | --- |
| Main | `c8b41371fbc49aa014b2d36332c43529b3c6d4f4` | Existing shared benchmark |
| Codex | `b518bc164eb1cdcd5766435a6e49345a7f880557` | Native Codex policy engine and protocol fixes |
| Factory server | `d1e1b3d7e274fb001c1576f9876239601fc72647` | Portable assets, frozen-source replay and Slurm rendering; already contains the pinned Codex source |
| Luna | `907f4807eb43644e9db4621c5305fa3300017830` | CPU rendering, Docker, providers and command-line operation |
| Multi-topology | `c1d05e3426468322fc5e89141e0cb5f49e87a925` | Four topology modes and communication measurement |
| Claude | `3b3fd08e8220d486b004c9dc2d764f5ba0d27d8b` | Native Claude Code sessions, MCP and recovery |
| Oracle | `a0249a6977e8137442a3d1f323be903a64c3f8c9` | Curate validated R14 fixes; do not import R15 experiments as defaults |

## Acceptance gates

- [x] Preserve refs and uncommitted source work outside the integration worktree.
- [x] Fast-forward Codex and Factory server without duplicating their shared history.
- [x] Integrate Luna, multi-topology and Claude with targeted regression checks.
- [ ] Provide one validated TOML configuration and CLI; resolve defaults once and freeze the effective configuration per run.
- [x] Launch initial task hosts through one scheduler with a default 0.3-second interval.
- [ ] Isolate task runtime state, verify Codex initialization/authentication, and stage Slurm SQLite state on node-local storage.
- [ ] Preserve shared START, scoring, safe call-ID and stop semantics across native engines.
- [ ] Keep R14 as the Mosaic default; validate recommended physical candidates before publishing changed assets.
- [ ] Verify automatic pinned policy-asset installation from a fresh checkout.
- [ ] Verify old and compressed motion, image references, evidence restore and frozen-source Factory replay.
- [ ] Integrate qualified Oracle functionality without exposing private solutions to policies.
- [ ] Publish English-only current content, task atlas, editable full video project, detailed README and documentation.
- [ ] Exercise CPU, native macOS, NVIDIA/EGL and Slurm paths where hardware is available; record unavailable checks explicitly.
- [ ] Run offline suites and clean-checkout checks; record any remaining paid/hardware qualification separately.
- [ ] Review the integrated branch before publishing or merging it into main.

## Invariants

Task limits are measured from persisted START, normally 86,400 seconds. An
engineering stop is separate and must not silently replace the public task limit.
`ready` queries capability; it does not unlock START. Completion is evaluated by
an independent scorer; process events are reported separately. Dial completion
remains latched on unlock. Adaptive delegation remains optional and dynamic.

New requests receive host-generated IDs. Uncertain physical requests must not be
replayed under new IDs. Collection and archival run only after all writers stop;
source evidence is retained by default. Factory playback uses each recording's
frozen scene and assets, including legacy recordings. A successful restore or
render does not imply that the recorded task succeeded.

## Merge decisions

Luna's offscreen capture and capture timing are retained. Factory server's
array-based diagnostic Factory replay is retained, because it avoids requiring
production Cycles video rendering for pixel/FK comparisons. Luna's additional
call-ID query/uncertain-result tests are retained alongside Codex error tests.

## Initial regression inventory

The first full discovery run executed 1,272 tests in 118 seconds: 25 were
skipped, 179 errored, and one failed. This is a diagnostic inventory, not a
passing release gate. Most errors request historical scene/workstation assets
outside the current 36-case policy bundle. Other findings include missing Oracle
extras and script import paths, two synthetic robot fixtures missing their image
profile, a Factory fixture missing table metadata, and an outdated source
compatibility receipt. Do not update a provenance receipt merely to turn a test
green; verify the claimed equivalence first, or withdraw that claim.

The targeted engine/role/protocol checks are separate from this legacy inventory.
No live model calls were made by these checks. Claude's scored-run qualification
remains closed until its native lifecycle has passed the required real checks.

## Configuration and launch implementation

The first unified CLI stage is implemented in `robofrontier.cli`, with validated
`robofrontier.toml` settings and immutable per-run effective configuration.
`docs/unified-cli.md` documents actual supported options and pending interfaces.
The API path creates one home per task, serially initializes every home, then
launches hosts through one 0.3-second gate. Collection resolves per-task markers
while preserving legacy batch-home behavior. Native subscription refresh remains
an explicit qualification gap; credentials are never cloned automatically.

The native CLI wrapper can plan, bootstrap assets, prepare Codex runs or Claude
engineering drafts, explicitly preflight providers, run, read atomic status,
request stop, collect, ZIP, extract and restore evidence. Claude permanent-worker
modes and formal scored execution remain closed. Factory/Oracle commands
have not yet been folded into this configuration schema. Slurm staging now has
its own settings and entry, with real-cluster qualification still outstanding.

Six real Codex 0.165.0 app-servers were initialized in independent cold homes and
then launched at a 0.3-second interval. All acknowledged initialization and exited
cleanly; no model turn or robot world was started. This verifies local startup,
not subscription refresh, 36-task resource capacity or provider execution. Raw
local evidence is under `runs/engineering/main-integration-codex-offline-20261101`.

The new command independently prepared four minimum-arm Level 1 cases with zero
model calls. All current 36-case asset hashes also passed inspection. The existing
asset lock is unchanged; recommended physics candidates still need final gates.

The source compatibility receipt was reviewed rather than blindly rehashed:
the exact observation-profile initialization and reported camera-size changes
are normalized alongside the service wrapper, and every remaining pipeline AST
node matches the original unaffected digest. The unaffected non-Relay evaluator
AST also matches its original digest. This establishes the limited historical
source claim, not equivalent policy observations, current scoring or new physics.

The completed configuration-stage regression group passed 123 tests. Thirteen
Codex host/transport Node tests also passed. Renderer checks reject a Mesa
software context when NVIDIA is requested and record the actual GL vendor,
renderer and version. The GPU validation still needs real Linux NVIDIA hardware.
The old synthetic ready-capability and Factory fixtures were brought up to date
without reducing their physics/FK assertions. Full historical-asset coverage,
real Slurm hardware acceptance, English migration and product UI/video gates
remain outstanding.

## Slurm staging implementation

The new `slurm-submit` command freezes committed source, the staging launcher,
resolved public settings, pinned assets and the explicit provider receipt before
queue submission. Compute-node staging requires a verified local filesystem.
Runtime, task Codex homes and temporary files remain node-local. A separate
`srun` step contains all execution descendants; the batch shell returns evidence
only after that step exits and owner/supervisor locks are available.

Only atomic supervisor JSON is monitored. Normal stage-out returns one verified
evidence ZIP with payload SHA-256 hashes. A failed collection returns stopped raw
motion/session evidence for review, excluding CLI authentication/config stores.
No source is automatically deleted and no uncertain action is replayed. Node
failure/SIGKILL can still prevent stage-out; this is not checkpoint/resume.

The retired Luna sbatch entry now gives migration instructions instead of
placing active databases in shared storage or making implicit paid preflight
calls. `docs/slurm.md` documents commands, resource requests, assumptions, stop,
stage-out, credentials and recovery limits. The focused staging/collection/
configuration regression group passed 56 tests with no model calls. This does
not validate a site's Slurm process tracker, actual node storage, 36-task memory
capacity, NVIDIA EGL or its cluster network.

## Direct startup for standing teams

New standing-team Codex batches use `direct_team_v3`: all required roles must be
bound to distinct native sessions before one persisted START, followed by an
explicit started prompt to every role. No role must first run a READY model
turn. Single/Adaptive retain their direct Controller startup. Frozen legacy
READY inputs remain supported, without being rewritten.

The Single Controller, standing Controller and Worker role prompts no longer
unconditionally demand READY/yield. The shared policy contract now describes
initial roles rather than assuming every topology starts with a Controller.
The capability reference distinguishes an optional direct-start query from a
legacy readiness registration. Codex bootstrap/recovery text is now English.

Offline checks cover both standing-team topologies, actions before/after START,
distinct-session binding, optional post-START capabilities, unchanged ownership,
one task clock, failed binding/START, STOP during setup and legacy behavior.
The runtime group passed 55 tests; the configuration/compatibility group passed
18 tests; six further profile/bootstrap checks passed. Fourteen native host tests
and all 24 existing dispatcher scenarios passed. These are overlapping groups,
not a count of unique release tests. No model inference was used.

## Unified Docker implementation

The `container` command builds committed source through `git archive`, verifies
the image's source-revision label, creates persistent plain local Docker volumes,
and invokes the same native command-line interface. Image construction installs
both native CLIs, locked dependencies and pinned assets without model inference.
The entry checks runtime filesystem locality. API task homes and native sessions
remain separate from the host's existing authentication directories.

The wrapper reads a prepared batch's frozen renderer before requesting a GPU,
forwards only selected provider credential variable names, monitors JSON, and
requests orderly stop on interruption. A still-live/disconnected container is
retained for review. After closure, automatic evidence ZIPs are copied to the
host and verified against the terminal command's SHA-256. Native session/auth
volumes are never removed automatically. Explicit native authentication commands
are available without cloning the host's Desktop/Keychain credentials.

The focused container/configuration/Slurm group passed 31 offline tests. The
actual `e51fa4b94315` image then built successfully with the pinned assets and
both CLI versions. Its unified plan returned all 36 tasks, Luna high and adaptive
with zero model calls. A real OSMesa context rendered RGB using Mesa llvmpipe.

The actual Codex sandbox failed under Docker Desktop's default seccomp profile
with a user-namespace permission error. The same fixed local probe passed when
the container was explicitly started with `seccomp=unconfined`, without privileged
mode or added capabilities. This establishes only the local sandbox prerequisite;
it does not qualify a complete native model/robot lifecycle.

The CLI now provides an offline `doctor`, checks native prerequisites before a
confirmed paid provider preflight, and checks native prerequisites/rendering
before task launch. A failed probe blocks model calls. The container seccomp
choice is explicit, validated, frozen and documented; its default remains the
Docker default. The focused diagnostics/configuration/container/Slurm group
passed 39 tests. Provider/subscription lifecycle, actual NVIDIA and 36-task
resource qualification remain outstanding; no paid test was started.

The `4210bf575eb5` image also prepared all four minimum-arm Level 1 tasks through
the container command, without models. An engineering-only probe loaded each
frozen world, stepped 0.2 simulation seconds, and called the actual policy capture
implementation for three cameras per case. All 12 JPEGs decoded at 896 x 560;
all states remained finite and all frozen input hashes stayed unchanged. This
is a loading/observation check, not sustained physical stability or task success.

The first actual doctor invocation exposed its own missing temporary Codex-home
directory, before any model call. The directory is now explicitly created for
both native CLIs and the regression test asserts that it exists. The independent
archive command now returns the ZIP SHA-256 as well as its path, matching the
container export verifier. The focused follow-up group passed 23 tests including
byte-exact session/image/motion restoration and terminal receipt verification.

## Second full regression inventory

After the source/fixture corrections and added integration checks, full discovery
executed 1,355 tests in 715.670 seconds. There were no assertion failures, 177
errors and 25 skips. Every recorded error was a missing file/scene asset or a
missing historical evidence dependency; none establishes an acceptable release
test result. Historical scene assets, Oracle witnesses and source-preservation
receipts still need explicit installation/Legacy treatment. Current 36-case
asset verification is separate and must not be used to claim that this full
suite passed. Raw diagnostic output remains in local engineering artifacts;
the historical asset/evidence gates remain open.
