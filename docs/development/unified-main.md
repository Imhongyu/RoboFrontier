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
modes and formal scored execution remain closed. Factory commands now share
the versioned configuration; Oracle integration remains pending. Slurm staging has
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

The corrected `9352651995a8` image built and the actual unified container doctor
passed with explicit `unconfined` configuration. With Docker's default seccomp,
the same command returned exit 2, exposing the namespace denial while still
reporting a successful llvmpipe render. Both invocations made zero model calls.

A synthetic stopped collection containing a real 21-frame Transport motion
stream and one synthetic image-bearing session was archived by the native
container command. The wrapper copied a 5,225,812-byte ZIP to the host and
verified SHA-256 `0c6b78cf2ca0ff042f5d9d7eefc843f99d939a70dea69069be050ac3d8d1f367`.
Host extraction and archive verification restored the session byte-for-byte,
loaded the recording's own frozen model, and replayed every frame with finite
forward kinematics. A restored frame rendered at 1920 x 1080 using Apple M5 Pro
OpenGL/Metal, independently of the 896 x 560 policy-image format. This is plain
background reconstruction, not Factory qualification or a native model session.
Local evidence is under `runs/engineering/main-integration-container-20261101`.

The root README is now English and describes the actual unified entries,
authentication boundaries, defaults, data locations and open acceptance gates.
It does not yet make the rest of the repository English or replace the pending
Factory/Oracle/atlas/video documentation and integration work.

## Unified Factory configuration and actual CPU replay

Schema version 2 adds a separate `[factory]` section for data identity, Cycles
device, Blender executable, output dimensions, quality, presentation duration,
import speedup and render-array concurrency. Existing frozen version 1 policy
configurations retain their exact hashed shape. Factory video defaults to
1920 x 1080, independently of 896 x 560 policy observations. The full tour remains
210.5 seconds; an explicit positive duration caps only an engineering preview.

The unified command now supports setup, verify, doctor, recording import,
preparation, local execution, status and explicit Slurm submission. A prepared
plan freezes the effective configuration and code/input hashes. Existing render
plans keep their native legacy entry. CPU queues request no GPU; CUDA/OPTIX
queues require one GPU; Metal is rejected on the Slurm path. Queue submission
remains a dry run unless `--queue` is supplied. See `docs/factory.md`.

The focused Factory/configuration/container/Slurm group passed 53 tests. They
cover frozen settings, version 1 policy compatibility, independent observation
and video sizes, full-tour duration, legacy plans, mismatched bundle rejection
and explicit queueing. These tests made no model calls.

Actual native commands verified all 123,198 files and 36 stations of the pinned
R14 Factory package. Four minimum-arm Level 1 jobs then rendered three frames
each using Blender 5.1.2 CPU Cycles at 320 x 180, one sample and 30 fps. Transport,
Mosaic, Relay and Dial all passed complete video decoding, input/code checks and
result sealing; representative images were inspected. Maximum reported Blender
pose-position error was approximately 1.91 micrometers. This small diagnostic
does not validate full-length videos, new physics, GPU performance or task success.

The previously verified evidence ZIP was restored and its real 21-frame
Transport motion imported through the unified command. Import composed the desk
from that recording's frozen source, produced a distinct verified 1,217-file
bundle and retained `recorded_benchmark_presentation_only` qualification. Every
copied float32 state and timestamp matched the restored source exactly. All
21 frames passed Factory FK checks with physics stepping explicitly forbidden;
maximum positional error was below 5.1e-15 m. A separate three-frame CPU Cycles
render of this imported bundle also passed decoding and sealing. This is a
synthetic collection containing real motion, not a native model result. New
all-family recording import, full videos, GPU and real Slurm qualification remain
open. Local artifacts are under
`runs/engineering/main-integration-factory-20261101`.

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

## Curated R14 Oracle implementation

The integration extracts the R14 endpoint-worker, checkout-binding and
revision-aware runner changes through `a49880f`, plus the archived-executor cache
diagnostic correction from `76d87ed`. It does not merge the Oracle branch's R15
assets/selectors, balanced/direct-nearest source experiments or experimental
review scope refinement. The native Mosaic default is now explicitly R14; a
selected task's own revision must also agree with its catalog before a world is
constructed. Policy release inputs and locks are unchanged by this curation.

The focused group passed 98 tests, including actual serial/parallel endpoint
equivalence on the current R14 scene, frozen imports, source color mismatch,
worker errors, same-owner recovery and uncertain-action handling. Existing
equivalence tests now use the installed R14 scenes rather than missing R13
assets; their physical-array and task-contract assertions are retained.
`docs/oracle.md` documents native execution, assistance, evidence, stop and timing
boundaries. Unified Oracle configuration/supervision and new full physical
witnesses remain pending; these tests are not scored or full-case results.

The committed `9e088cc` executor then ran an actual two-goal R14 commissioning
trial with four planning workers and no internal physics worker pool. It
completed the two selected goals out of 72, with 58 robot actions, no failed
robot actions, no process violations, no unresolved actions and no assistance.
The report correctly keeps full-case `passed=false` and
`commissioning_passed=true`. Wall time including planning was 151.920 seconds;
simulation reached 87.88 seconds. The independent motion audit verified all
5,274 frames, checksums and 141 visual events with a maximum sample gap of
0.018 seconds. Compressed chunks totaled 3,038,141 bytes. This is an actual
partial physical reference, not a full-case success or an LLM run. Evidence is
under `runs/engineering/main-integration-oracle-20261101`.

## Shared runtime language follow-up

The shared scheduler wake notices, native Desktop delegation notice and run-audit
Markdown now use English. Wake triggers, role authority, ID isolation and the
legacy protocol branch are unchanged. This is only part of the repository-wide
English migration; legacy generators, pages and historical documents remain.

Three old Codex RPC assertions still matched Chinese bootstrap/recovery text
after the host had already changed to English. Their failed pre-update run is
retained locally; assertions now check the same process-event, legacy READY and
post-START recovery semantics in English. All 21 focused Codex Node tests, all
24 existing dispatcher scenarios and 23 scheduling/report/direct-start Python
tests passed. An additional opt-in smoke passed using the actual native Claude
CLI against a local synthetic model endpoint and actual MuJoCo. Its early-finish
path produced an incomplete evaluation, sealed evidence and the English
unqualified-engineering report. This does not qualify a real provider, adaptive
delegation or formal Claude scoring. None of these checks used paid inference.

## Unified native Oracle workflow

The CLI now exposes `oracle plan`, `prepare`, `run`, `status` and `stop` for the
existing Transport full-order, Mosaic R14, Relay live-pipeline and blind Dial
entries. It selects current released task scenes rather than the historical
`oracle` recording inventory, and pins source, harness/catalog, scene assets,
effective settings and dependency versions before one single-use launch.
Fresh Dial puzzles are evaluator-only; an optional explicit codebook remains
private and never becomes a solver input. Native typed recovery, evaluator
gates, intervention records and full-versus-commissioning scope are retained.

Schema version 3 adds a separate Oracle section. Frozen version 1/2 settings
remain exact and are validated without adding fields or changing their hashes.
The Oracle engineering elapsed limit includes launch/planning/review pauses and
is separate from the policy START clock. STOP and the deadline signal the
existing owner, followed by bounded process-group cleanup. Input mutation,
single-use replay, unknown actions, child writers and partial commissioning
cannot silently qualify as a clean full success. Monitoring uses atomic JSON,
not another process's SQLite database.

The focused checks passed 41 tests in 18.706 seconds, including actual
subprocess stop/deadline and leftover-writer tests, the four native command
bindings, current R14 selection, configuration/Factory regressions, source
snapshot/manifest integrity tests and direct standing-team START. No model was
called. Actual native physical smoke runs are the next qualification step;
this entry alone is not a full physical witness.

The first actual CLI smoke launched each current minimum-arm Level 1 native
Oracle with a 15-second engineering elapsed limit and 10-second cleanup grace.
Transport, Mosaic and Dial produced stopped native reports without forced
termination. Transport and Mosaic retained unresolved in-flight actions rather
than pretending to have sealed them. None is a task success. Relay exposed a
native stop/recovery bug: its recoverable-error catch intercepted
`ReferenceStopped`, entered live repair and continued stepping until the
supervisor killed it. The original forced-stop directory is retained without a
fabricated report under `runs/engineering/main-integration-oracle-cli-20261101`.

The Relay entry now latches an owner stop and propagates terminal stop and
commissioning-boundary exceptions past recoverable repair. Ordinary forward
repair and process-violation rejection are unchanged. The focused stop/recovery,
Relay batch and unified Oracle group passed 37 tests in 14.800 seconds. A new
physical attempt is required to verify native shutdown; the first trial is
never resumed or rewritten.

The new Relay attempt from committed source `496f83a` stopped at the same
15-second limit without forced termination and wrote its native report. Its
36 actions and four unresolved arms are retained; it is interrupted, not a
success or a fully reconciled physical stop. All four current native entries
now have real CLI load/action/stop/report evidence. The retained stream audits
decoded 1,707 Transport, 2,065 Mosaic, 2,123 Relay and 1,765 Dial frames, including
three Dial appearance events. Every committed chunk checksum and timestamp
decoded correctly. As interrupted streams, none passed the complete-recording
gate; Transport/Mosaic/Relay also exposed a final event after the last cadence
pose. Original files were not rewritten.

Controlled Oracle shutdown now captures the actual final live pose without
another physics step, retaining `interrupted` status. Invalid final state keeps
its verified prefix and an explicit capture-error field. The closing regression
checks exact float32 pose retention, unchanged controls/physics state, event time
coverage and invalid-state handling. All 17 motion/process/monitoring/stop tests
passed in 2.428 seconds. Six initially missing-asset errors came from the motion
test fixture selecting the obsolete generated v2 scene; that format-generic
fixture now resolves the current released scene, with all codec/source/corruption
assertions intact. New physical recordings still need to verify the revised
closing path; an old interrupted recording cannot retroactively gain a frame.
