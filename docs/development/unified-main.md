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
- [x] Provide one validated TOML configuration and CLI; resolve defaults once and freeze the effective configuration per run.
- [x] Launch initial task hosts through one scheduler with a default 0.3-second interval.
- [ ] Isolate task runtime state, verify Codex initialization/authentication, and stage Slurm SQLite state on node-local storage.
- [ ] Preserve shared START, scoring, safe call-ID and stop semantics across native engines.
- [ ] Keep R14 as the Mosaic default; validate recommended physical candidates before publishing changed assets.
- [x] Verify automatic pinned policy-asset installation from a fresh checkout.
- [ ] Verify old and compressed motion, image references, evidence restore and frozen-source Factory replay.
- [ ] Integrate qualified Oracle functionality without exposing private solutions to policies.
- [ ] Publish English-only current content, task atlas, editable full video project, detailed README and documentation.
- [ ] Exercise CPU, native macOS, NVIDIA/EGL and Slurm paths where hardware is available; record unavailable checks explicitly.
- [x] Run offline suites and clean-checkout checks; record any remaining paid/hardware qualification separately.
- [ ] Review the integrated branch before publishing or merging it into main.

## Latest scoped acceptance snapshot

As of 2026-11-02, the Oracle repair regression group passes on macOS and Linux
(391 checks each). Full macOS discovery passed 1,501 checks before addition of
the fixture installer. An independent Linux-local clone of `4f9cd85`, supplied
only the explicitly pinned optional historical fixtures and an existing
dependency image, passed 1,512 checks: zero failures/errors and 26 conditional
skips. All JavaScript/dispatcher and portable-link checks passed. Subsequent
palette/task/report display translations have separate text-invariance checks;
the Linux receipt is not relabeled as a full run of those later commits.

The optional historical fixture installer and separate local bundle now support
independent installation. Public bundle distribution, final current-source image,
remaining English migration, final review and main publication are still open.
Real-provider/subscription lifecycle, 36-task capacity, NVIDIA observations and
the unified Slurm execution/stage-out path remain distinct qualification gates.
Slurm resource discovery alone does not satisfy them. Claude formal scored
execution remains closed. The user's deferred full video rerender stays deferred.

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
request stop, collect, ZIP, extract and restore evidence. All four Claude modes
now have native engineering entries; formal scored execution remains closed.
Factory and Oracle commands share the versioned configuration, with their
scoped acceptance evidence recorded below. Slurm staging has
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

An actual new five-second Transport execution from `24a4b41` verified the revised
shutdown path. It returned a native stopped report without forced termination;
all 759 motion frames, checksums and 70 events decoded, with 0.018-second maximum
sample spacing. No event extended beyond the final recorded pose. The complete-
recording audit still correctly rejects its `interrupted` status. Its original
source-scene hash is unchanged. Evidence and the separate read-only motion audit
are retained beside the earlier four-family smoke outputs.

## Manager prompts and remaining English migration

Both outer-manager prompts now use English. The Codex prompt uses the unified
one-profile configuration/CLI, explicit paid-stage authorization, frozen launch
settings, direct role startup and stopped collection. It explains combined
concurrency for separate profiles rather than implying one supervisor controls
all of them. The Claude prompt retains the native multi-profile engineering
entry, optional cost limits, explicit precheck estimates, unqualified status and
separate subscription qualification. Neither outer manager injects robot
strategies or claims its own model is the measured policy.

Legacy Transport startup text and Dial design display titles also use English;
physics, geometry and installed asset fingerprints were not regenerated.
The active `robofrontier/` and `prompts/` trees now have no Han characters.
This does not complete the repository-wide language gate: historical docs,
scripts, generated pages and some metadata still require migration.

The presentation/legacy Dial contract group passed all 22 tests in 2.766 seconds.
Its first run exposed missing legacy `facing-04` assets, not a new runtime error.
The synthetic policy group now builds its own isolated legacy XML/textures and
initial keyframe using the real generator and compiled model. Its preview and
runtime measurements remain explicitly synthetic; no physical qualification is
claimed. Tests retain every existing privacy, symbol mapping, role/fork return,
sampling and success-latch assertion, without installing/overwriting a published
scene or loosening production scene-path checks.

A combined regression run after these changes passed all 100 selected tests in
25.125 seconds, including the generated legacy Dial fixture followed by current
motion/Oracle tests in the same process. The temporary fixture roots were
restored correctly. This is the focused integration group, not the still-open
full historical discovery gate. Its log is
`/tmp/robofrontier-unified-oracle-final-regressions.log`. The policy/Factory asset
locks and scene files were unchanged, `main` remains at `c8b4137`, and none of
these integration commits has been pushed or merged into main.


## All-family current compressed-motion Factory acceptance

Four actual new native engineering recordings were imported through the unified
Factory CLI, using their own frozen inputs. A read-only all-frame audit checked
5,274 Mosaic, 759 Transport, 1,765 Dial and 1,716 Relay frames (9,514 total).
Imported float32 states and timestamps were bit-exact; original chunks, events
and assets were unchanged. Factory playback had zero dynamic/control dimensions
and performed no physics steps. Every mapped geometry's pose matched within
5.1e-15 metres, and all three Dial appearance events were retained and applied.

Each imported case also produced a three-frame, 320 x 180, one-sample Cycles CPU
preview. All four MP4 files were fully decoded and inspected. This validates
new compressed-motion background import, all-frame pose/appearance replay and
small CPU renders; it does not qualify complete videos, NVIDIA, Slurm or task
success. Mosaic is a two-goal partial commissioning recording; the other three
recordings retain their failed/interrupted status. Evidence is under
`runs/engineering/main-integration-factory-new-motion-20261101/`.

The first import exposed a CLI presentation defect: exporter progress and the
final result both went to stdout. The completed first import was retained.
The unified Factory entry now routes exporter progress to stderr and emits one
JSON result on stdout. A regression reproduced the previous parse failure;
subsequent native imports parsed successfully without regenerating Mosaic.

## Isolated operational physics and final failed-state retention

The committed `scripts.commission_transport_contacts` entry compares compiled
models before running a selected reference operation. Only declared contact-cone
and selected cylinder rolling changes are permitted. Candidate fingerprints
include the cone; old metadata and qualification are not silently inherited.
The released source and all declared asset hashes remain unchanged.

Actual side-cylinder pickup/lift, full-route handovers and socket operations
were compared for released, elliptic/30 mm and elliptic/1 mm variants. The 1 mm
candidate and released control both completed a local direct socket placement.
The maintained candidate command additionally verified post-release settling
and retained goal acceptance. Long multi-handover operations failed at different
finite planning/contact gates in all three variants; none qualifies a complete
Transport task or proves the candidate universally better. No candidate was
published as the new default. See [physics commissioning](../physics.md).

A five-second maintained trial retained a typed `ReferenceStopped` and its last
measured pose. A separate ordinary finite planning failure exposed an older
recording gap: its last event could follow the last cadence sample. Oracle
closure now captures the measured final state on an ordinary error as well as
an interruption, without stepping physics or replaying an action. Failed status
remains failed. The regression checks exact float32 final pose, event coverage
and unchanged live controls/state. A new actual failed trial retained all 1,126
frames and covered all 21 event timestamps. Original failed recordings were
never rewritten. Evidence is under
`runs/engineering/main-integration-physics-20261101/`.

The final focused integration group passed 106 tests in 28.045 seconds, including
motion, stop/recovery, all four Oracle entries, direct standing-team START,
configuration, Factory, snapshots and contact commissioning. These overlapping
regression groups are not a passing full historical discovery run.

## Fresh checkout and automatic asset repair

A new shallow local clone of committed integration source `caa341b` installed
with `uv sync --locked --extra oracle`, without copying the original environment,
authentication or assets. Bootstrap restored 3,467 files with zero reused files
from the pinned archive, whose SHA-256 was verified. Every expected scene/Panda
asset hash was then checked.

One ignored Relay label was deliberately moved out of this fresh fixture.
The ordinary unified `prepare` command restored it automatically and prepared
all 36 tasks. Every frozen input verified; defaults were Codex/Luna/high,
Adaptive, 36 concurrent slots, a 0.3-second initial launch interval and 86,400
seconds per task. On this Mac the explicit renderer was `native`. No environment
file, model calls or native model session transcripts were created. The actual
native doctor also passed CLI/sandbox, a 64 x 64 RGB render and a CPU physics
step. The clone remained clean.

The detailed receipt is
`runs/engineering/main-integration-fresh-clone-20261101/verification.json`.
This is local clean-checkout/bootstrap/preparation evidence, not GitHub branch
publication, provider compatibility, concurrent subscription refresh, 36-task
resource capacity, Linux NVIDIA or Slurm qualification. The policy and Factory
release locks remain unchanged, and integration has not been merged into main.


## Tracked English public atlas

The current public task atlas is now reproducible, tracked under
`docs/task-atlas/`, with editable templates under `web/task-atlas/` and the
`scripts.build_task_atlas` build/verify/ZIP entry. It regenerated all 72 top/front
JPEG views from the actual current 36 scenes at their initial keyframes, without
physics stepping or model calls. The package binds each file and generator to
release `b432892f`; it uses the same reviewed public contracts and terminal
scoring overlays as new policy runs. Raw private puzzles, Oracle solutions,
local paths and live runtime databases are excluded.

Eight artifact/public-contract tests passed in 2.710 seconds. They cover exact
current contract selection, private-field rejection, corrupted images/unlisted
files, stale completion semantics even with a rewritten payload hash, refusal to
overwrite an existing artifact, and deterministic ZIP creation/restoration with
byte-exact file checks. The generated site is 4,367,839 bytes and its ZIP is
2,998,888 bytes (SHA-256
`fdb1da0519f76ace7da90398128b7c2e385e1ce35c3d6009929fca88a43504df`).

Actual browser checks exercised combined family/level/arm/ID filters, empty
results, reset, front-camera switching and family-card navigation. A real
initial navigation bug, caused by a reset-button ID masking `form.reset`, was
found and fixed before delivery. The corrected 390 x 844 layout has one-column
task cards with no horizontal overflow; desktop layout and loaded images were
also inspected. Direct `file:` navigation is blocked by this browser tool's
protocol policy, so it is not claimed as an executed browser check. Structural
relative-link checks, self-contained JavaScript/CSS and actual ZIP restore are
verified separately. Evidence is under
`runs/engineering/main-integration-task-atlas-20261101/`.

The Pages workflow validates relevant pull requests and supports an explicit
manual publication, disabled by default. It uploads only the verified atlas;
there is no push-triggered deployment. Neither this workflow nor the current
integration branch has been published. The repository layout guide is now
English and distinguishes tracked code/atlas from ignored original recordings,
collections and historical local delivery layouts. Repository-wide English,
full editable promo and the other outstanding gates remain open.


The committed atlas source `c68becf` also passed all eight artifact checks in a
network-disabled Linux container (1.990 seconds), using an extracted Git source
archive and the previously installed pinned dependency environment. This is
Linux artifact/contract verification, not a newly built current policy image or
a provider/Slurm/GPU run. The first check allocated only 512 MiB to its temporary
source filesystem and failed while extracting the 654 MiB source archive; it
never reached tests. A new attempt with an explicit 1 GiB temporary filesystem
passed. Both logs are retained with the atlas evidence.


## English native-engine and evidence handoff

The Claude handoff, Codex/Claude component map, harness-alignment guide and
evidence-storage guide are now English. They preserve dated native CLI/provider
observations, costs, source commits and qualification limits, while separating
current direct START from historical READY. The stale first-Haiku preflight
paragraph no longer contradicts the later separately authorized Opus checks.
Budget defaults remain unset, structured recovery remains bounded, and no new
model/provider capability is asserted by translation.

The evidence guide now leads with the unified ZIP path and explicitly separates
ZIP extraction (compressed objects) from restoration (ordinary motion/session
files). It distinguishes the unified retention of stopped incomplete evidence
from the lower-level directory archiver's complete-by-default mode, and explains
that reversible image extraction retains image bytes. Historical PNG transcoding
is not silently described as lossless. Local links and English-only content
passed inspection; the documented offline Claude plan selected four tasks with
zero model calls. Current Claude discovery passed 164 tests in 31.704 seconds,
with seven opt-in checks skipped. This is not full repository or real-provider
physical qualification.

## Native Claude physical lifecycle and stopped-evidence recovery

On committed integration source `430d390`, five explicitly enabled native checks
passed in 53.429 seconds. They used the real Claude CLI 2.1.312 and real MuJoCo
worlds with a synthetic loopback model service, not a paid provider. Coverage
included an Adaptive observe/move/delegate-return operation, four simultaneous
physical owners for the four minimum-arm Level 1 cases, an unfinished Controller
finish followed by independent unsuccessful scoring, and SIGTERM finalization
of one and four actual owners. All tested physical owners exited, seals reported
no unresolved physical actions, and the world-stop assertions passed.

The opt-in command was:

```sh
ROBOFRONTIER_PHYSICS_SMOKE=1 ROBOFRONTIER_PHYSICS_BATCH=1 \
ROBOFRONTIER_PHYSICS_FINISH=1 ROBOFRONTIER_PHYSICS_SIGNAL=1 \
PYTHONPATH=tests:scripts .venv/bin/python -m unittest \
  test_claude_physics_smoke test_claude_parallel_physics_smoke \
  test_claude_finish_physics_smoke test_claude_signal_physics_smoke
```

The three retained stopped batches were then collected, archived to ZIP and
verified using the production collection/archive entries. This inspection did
not restart a native owner or call a model. All issues remain in their collection
manifests. Each batch is incomplete because interrupted native turns left
reported costs uncertain under these tests' explicitly configured budgets.
The four-owner signal batch also contains two delegates stopped before a valid
native session ID was bound. Their missing-session findings remain visible;
this evidence is not a claim that all delegates completed or that these are
cleanly accounted benchmark results.

| Retained test batch | Collection bytes | ZIP bytes | Recorded policy sessions |
| --- | ---: | ---: | ---: |
| Four-family Adaptive operation | 303,697,498 | 10,511,344 | 8 |
| Single-owner SIGTERM | 73,466,937 | 6,413,736 | 2 |
| Four-owner SIGTERM | 294,465,627 | 8,582,069 | 6 |

The four-family ZIP was extracted and restored into a new ordinary collection.
All 1,829 file payloads were byte-exact. All 4,928 recorded float32 states and
timestamps and all motion/appearance events were exact. First/middle/last
simple-background render samples matched pixel-for-pixel for all four cases.
No physics was stepped during replay. Original stopped batches and collections
were retained. The 96.5% storage reduction in this synthetic short-run fixture is
measured archive behavior, not an estimate for a long real-model batch.

The first local verification helper failed before collecting anything because
it imported a nonexistent `restore` symbol. It was corrected to the archiver's
actual atomic `verify(..., output=...)` restore API. No production code or source
evidence was changed to bypass verification. Logs, ZIPs and the detailed receipt
are under `runs/engineering/main-integration-task-atlas-20261101/`, including
`claude-native-physics.log` and `claude-evidence-verification.json`.

## English Factory handoff and historical boundaries

The Factory design/rendering guide, native Linux/Slurm handoff and dated server
acceptance are now English. All local Markdown links resolve. The current guide
leads to the unified configuration; historical V9/V10 sampling, cleanup policies,
performance, paths and scope remain dated rather than becoming new defaults.
The server guide separates policy execution from render-array execution and
explains that cloning remote main before integration publication does not obtain
these changes. No source scenes, release fingerprints, historical acceptance
receipts or published data locks were regenerated by this documentation change.

## Native Claude standing-team engineering implementation

The earlier permanent-Worker implementation gap is now resolved for engineering
execution. `StandingTeamPolicyHost` creates one independent native session per
frozen initial role, confirms every binding, persists one `direct_team_v3` START,
and then sends public role/task prompts. Controller + Worker preserves the
coordinating Controller's lack of arm authority and hierarchical message routes.
Worker-Worker has no Controller role and preserves direct peer communication.
Standing roles do not use Adaptive fork setup. The shared runtime, mailbox,
permission checks, safe action IDs and private evaluator are unchanged.

Unified preparation and the native engineering batch/run now accept both modes.
All roles share one run-local optional budget ledger. Unknown binds are not
repeated; uncertain wake dispatch pauses rather than resends. Team-wide
observation checks precede recovery or new wake dispatch, so a known unavailable
teammate cannot be hidden behind another role's capacity recovery. Stop cancels
all role turns and uses the existing physical seal. Existing Single/Adaptive
hosts and frozen READY-barrier inputs retain their paths.

Six new runtime-level tests exercise direct startup, independent identities,
authorized/forbidden routes, wakes, lost bind/send acknowledgements and recovery
with unknown teammates. The final selected configuration/engineering/direct-START
group passed 49 tests in 10.218 seconds. Full current Claude discovery then
passed 174 tests in 36.932 seconds, with eight opt-in checks skipped. These
counts overlap and do not replace the open full-repository historical discovery.

An actual Claude CLI/MCP loopback check exercised both modes with a synthetic
world, independent transcripts, a Worker action, messages and resumed wakes.
The first fixture incorrectly assumed that a coalesced user message's last
block identified the tool boundary, causing its scripted endpoint to loop on
inbox. It was replaced with a bounded per-role script. A second assertion
incorrectly required a wake to remain `sent` after its receipt had already
advanced it to `observed`; it now accepts both actual lifecycle states. Failed
logs remain retained. The corrected two-mode native check passed in 4.759
seconds and also passed inside the final full Claude regression run.

The explicitly enabled `test_claude_standing_physics_smoke` then exercised real
MuJoCo Transport A04-D1 under each mode for 20 seconds from START. Both obtained
an RGB image through MCP, completed one Worker A gripper action, exchanged
messages and continued bound sessions. Every role saved its work; none needed
READY. Both tasks reached their engineering stop, had sealed worlds with no
unresolved actions, and exited their physical owners. Both reported finished
engineering lifecycle with the shared ledger still tracking. This one test with
two topology subcases passed in 45.593 seconds. The model endpoint was synthetic;
there were no genuine provider calls and no task-solving qualification.

Both stopped batches were collected using the production collector. Collections
were complete, with all five Controller + Worker sessions and all four peer
sessions. Their ZIPs restored every file byte exactly; each recording's 1,230
states/timestamps and events were exact, and three simple-scene render samples
matched pixel-for-pixel without physics integration.

| Mode | Verified files | Collection bytes | ZIP bytes |
| --- | ---: | ---: | ---: |
| Controller + Worker | 524 | 76,810,027 | 7,082,657 |
| Worker-Worker | 516 | 76,470,926 | 7,018,607 |

Reading the restored host evidence through the common metrics exporter recovered
all five/four role keys, 14 tools and six completed CLI turns per test, with
complete synthetic usage fields. No synthetic token/cost value is a real
provider bill or caching measurement. Original batches and collections remain
retained. Receipts, failures, native logs, ZIPs, restores and replay reports are
under `runs/engineering/main-integration-task-atlas-20261101/` with the
`claude-standing-` prefix. These runs freeze the actual implementation inputs;
they were conducted before committing this implementation.

The README, unified CLI, component map and handoff now describe four native
engineering modes and link the new [standing-team guide](../claude-standing-teams.md).
It explains task versus role concurrency, initial role counts, native names,
resource implications, clock semantics, recovery, evidence and reproducible test
commands. Formal scored Claude execution, genuine provider lifecycle/ability,
all-family/all-scale standing physical checks and cluster/subscription
qualification remain open; no release lock or production physics changed.

## Linux image and publication-boundary checks

The committed `849b5c1ea10502baebbc85d4265fc59a9e932440` source built successfully
through the unified container command. Image `robofrontier:849b5c1ea105` carries
that exact revision label; its image ID is
`sha256:51d42e40eab7bc0fbd4111103f2bd1cf1e2c8f62097319bc1d5530e5696a242b`.
The build used no model calls. A network-disabled Linux aarch64 container passed
native Claude CLI and actual RGB doctor checks with Mesa llvmpipe. This does not
qualify NVIDIA, x86_64, a real provider, Slurm or 36-task execution capacity.

Actual unified `prepare` commands in that image prepared four minimum-arm Level 1
cases for each engine/topology combination: 32 independent frozen runs across
Codex/Claude and Single/Adaptive/Controller + Worker/Worker-Worker. Every input
manifest verified; CPU rendering, JPEG observations, 24-hour public task limits,
0.3-second startup spacing and the corresponding direct-start protocols matched.
No model or physical world was started by these preparations.

The first Linux selected group exposed a process-loss test race: the fake worker
had entered before the supervisor's `starting` JSON publication. Killing the
supervisor then legitimately retained `queued` in its last published snapshot.
The test now controls the actual publication seam and exercises both sides of
it. Both cases preserve run/batch claims, report the lost supervisor, support
STOP, and refuse replay. All 18 engineering-batch tests passed on macOS and
Linux after this change. Production supervision was not altered.

The initial Linux full Claude discovery ran 175 tests with one failure and eight
skips. Its standalone native-fork test attempted resume immediately after an MCP
HTTP handler was entered, before the native parent history was guaranteed to be
written. Production delegation already waits for its recorded pending-tool
boundary in `fork_setup._pending_history`. The standalone test now also requires
its actual observe tool-use row in the native transcript before creating a fork.
The corrected native test passed on macOS (1.465 seconds) and Linux (1.340 seconds).
The initial failing logs remain retained; a complete post-fix discovery is still
required before claiming that whole Linux group passes.

The engineering index and Linux policy guide are now English and lead to the
unified CLI, pinned bootstrap, explicit render backends, node-local execution,
credential isolation and stopped evidence collection. Stale permanent-Worker
unavailability statements in the current architecture, Docker, Slurm and manager
guides were updated to the implemented engineering capability, retaining the
formal qualification boundary. Historical interfaces are explicitly Legacy.

Local evidence uses the `linux-`, `supervisor-publication-` and `fork-boundary-`
prefixes under `runs/engineering/main-integration-task-atlas-20261101/`. Linux
post-fix tests used the committed image with only the identified test files
replaced inside disposable containers; no production image file or original
run evidence was overwritten. Source changes will need a new committed image
for exact-revision final acceptance.

## Exact-revision Linux native standing acceptance

After the test-boundary corrections, source
`b0129eb665918c9353dfa6e52ccf31941ee55a87` was committed and built through the
unified container command. Image `robofrontier:b0129eb66591` has that exact source
label and image ID
`sha256:ead76e49acd4898218dabaa075642d806a3d83491ec2767d709b01075d4515fb`.
Full Claude discovery ran 175 tests, with zero failures/errors and eight skips,
on both macOS (41.540 seconds) and the network-disabled Linux image (31.715
seconds). These are 167 executed passing checks per platform, not 175 independent
provider or physics qualifications. The corrected Linux run used the committed
image unchanged, without the earlier test-file overlays. One preceding command
used a mistyped image tag and failed before container creation; its separate log
is retained and does not count as a test run.

The opt-in standing-team physical smoke also passed in that exact Linux image:
one test/two topology subcases, 45.552 seconds. Each used real MuJoCo Transport
A04-D1 with OSMesa/llvmpipe, the native Claude CLI/MCP, and a synthetic loopback
model. Both bound distinct sessions before START, delivered an actual image,
completed Worker A's gripper action, exchanged messages, resumed bound roles,
and stopped after 20 seconds from START with sealed worlds, no unresolved action
IDs, and exited physical owners. The test container exited zero without OOM.
There were no genuine provider calls and no claim of task-solving success.

After that container was authoritatively stopped, its test data was copied as a
23,674,591-byte gzip transport tar. A separate network-disabled container restored
the unchanged original absolute paths onto local storage, then ran the production
collector, ZIP archiver, atomic restore, and replay verifier. No live database
was read across a container boundary. Both collections were complete:

| Mode | Native role sessions | Verified files | Motion frames | ZIP bytes |
| --- | ---: | ---: | ---: | ---: |
| Controller + Worker | 5 | 527 | 1,179 | 7,076,133 |
| Worker-Worker | 4 | 516 | 1,235 | 7,019,079 |

Every collected file restored byte-for-byte. All states/timestamps and appearance
events matched exactly; three sampled simple-scene images per recording matched
pixel-for-pixel without physics integration. The exported sample JPEGs were also
visually inspected. Both stopped containers and the transport copy remain
retained. The verified ZIPs, hashes, replay samples/reports, and receipt were
copied out only after the verification container exited zero. They are under
`runs/engineering/main-integration-task-atlas-20261101/linux-standing-verified-b0129eb/`.
Logs use the `linux-claude-regressions-b0129eb-exact`,
`linux-standing-physics-b0129eb`, and `linux-standing-evidence-b0129eb` prefixes.
These checks do not establish Factory replay of these particular new streams,
NVIDIA rendering, subscription refresh, Slurm, x86_64, or real-model capacity.

## English task and native execution guides

Transport, Mosaic, and BEST5 Dial specifications are now English. They preserve
geometry, numerical tolerances, historical qualification counts, edit/video
provenance, and native script identities while distinguishing new policy
terminal scoring from unchanged strict historical Oracle reports. Mosaic clearly
selects R14/81 mm for new policy and unified Oracle runs; original R13 recordings
keep their colors/source. Dial explicitly retains unlock-once completion and
separates the device's READY indicator from harness startup. Historical
Unicode-named artifact basenames are represented with exact JSON escapes rather
than renaming original recordings or dropping their location information.

The native Codex guide now leads to the unified Luna/high API defaults while
labeling the retained native entry's Astra/parallel-9 defaults separately. It
explains task-isolated homes, optional capability READY, safe request identities,
JPEG observations, compressed motion, explicit render selection, API versus
subscription qualification, and independent offline video quality. Its provider
catalog table remains an explicitly dated 2026-10-28 snapshot, not a new ranking
or availability assertion. The official OpenAI configuration and app-server
references were fetched to confirm Responses-only provider configuration and
source-kind filtering; canonical links are retained in the guide.

The original four-family Oracle integration guide is now an explicitly dated
English acceptance snapshot. Its 1,008-test result, asset scan, 48 pre-existing
broken links, 36 source recordings, timing observations, and unfinished work
remain historical facts rather than claims about the current larger suite.
These documentation changes do not modify the asset lock, physics, public
policy templates, evaluators, source motion, or archived compatibility hashes.

## Full-length Factory movie audit and remaining editorial work

The preserved `factory-promo-r14.mp4` under the original Factory worktree's
`outputs/robo-factory/promo-r14-427210/` was inspected without modification. Its
134,315,571 bytes have SHA-256
`9c83e1d0ad17c3f6d4a7ed4b7d806322160f5d61d1e58e2471f0d3b300b86f96`.
ffprobe confirms H.264, 1920 x 1080, 30 fps, 6,315 frames, and 210.500 seconds.
Four derived inspection JPEGs at 0, 16, 66, and 162 seconds are retained in
`runs/engineering/main-integration-task-atlas-20261101/promo-audit/`, with the
media receipt. Opening and Dial samples were visually inspected.

That delivery folder contains the full movie and a preview, not a complete
editable editorial project with title/subtitle sources and a source-bound camera
plan. A filename containing R14 does not establish that every source scene or
contact parameter matches the current release. The existing full movie remains
historical evidence; it has not been relabeled as a newly rendered current
release. Native promo generation already exports camera plans, pose frames,
source clock traces, reset events, and hashes. The remaining work is to expose
editable English titles/subtitles and camera controls through a reproducible
source-bound project and verify the full-length deliverable. This audit is not
that implementation or final-video acceptance.

## Editable English Factory project and media verification

The source-bound full-tour project is now tracked at
`assets/robo_factory/tour-project.json`, with 73 camera waypoints, five English
title cues, 34 subtitle cues, and the existing licensed Barlow font. It spans
210.5 seconds/6,315 frames at 30 fps. Task subtitles use the actual inspection
camera/task metadata. Camera positions, targets, FOV, timing, SRT text and style
are editable; camera edits do not implicitly retime existing subtitle tracks.
The [editorial guide](../factory-editorial.md) documents the complete workflow.

Unified and native commands now expose `factory project`, `prepare --project`,
and `edit-video`. New promo plans generate or copy the complete project into a
frozen plan. Preparation publishes atomically; incomplete 36-station inputs or
invalid edits cannot publish a partial plan. Native pose export consumes the
frozen camera plan. Cycles retains its raw movie; the compositor retains the
editable project and generates a captioned movie, source/project/output hashes
and a full-decode report. Completion requires both raw and captioned media,
matching project bytes, original source movie identity, dimensions, rate and
frame count. A changed camera/subtitle during rendering, changed retained
project, missing editorial result, or compositor failure prevents successful
completion. Legacy plans without editorial inputs retain their raw-media
contract; they are not implicitly upgraded.

The final Factory regression suite discovered 60 tests on each platform:
55 executed and passed, five historical generated-data tests skipped. macOS
took 9.495 seconds; Linux aarch64 took 4.674 seconds. The Linux run used the
existing `robofrontier:b0129eb66591` dependency image with the current checkout
mounted read-only at `/work`, a writable temporary filesystem, and networking
disabled. This is not a claim that that older image contains the new source.
Checks include the actual FFmpeg/libass CLI path, source immutability, pixel
changes in title and subtitle regions, portable font/project retention,
preparation rollback, attempt failure/no-seal behavior, changed-during-render
rejection and both new and legacy completion paths. The first fixture attempt
failed because its new synthetic Mosaic task omitted R14 scale metadata; that
fixture was corrected without weakening production bundle validation.

The checked-in project also completed an actual unified `prepare`/`run`/`status`
round trip against the pinned 36-station R14 bundle, using CPU Cycles at
320 x 180, one sample and an explicit 0.1-second preview. All three raw and
captioned frames were decoded, sealed and input/code hashes verified. Status
returns both final `video` and original `source_video`. This verifies a small
current-source render, not full-length current-source GPU/Slurm rendering.

The preserved historical full movie was separately composited without another
Cycles render: 1,920 x 1,080, 30 fps and all 6,315 frames. Output is 133,064,566
bytes, SHA-256
`86f0111abf2c94c7d508f223d841ffdf2541a955882dd341f133798d0e84a876`.
Full decoding passed, and inspection frames at 0, 16, 66 and 162 seconds were
viewed. The original SHA-256 remains
`9c83e1d0ad17c3f6d4a7ed4b7d806322160f5d61d1e58e2471f0d3b300b86f96`.
The full video's report explicitly qualifies text/media processing only; it
does not establish that this historical movie depicts current physics or its
project's declared scene. It is not given a current-source render-plan seal.
The complete new-source full-length delivery gate therefore remains open.

Logs, projects, raw/final preview media, full edited historical movie, inspection
JPEGs and `factory-editorial-acceptance.json` are retained under
`runs/engineering/main-integration-task-atlas-20261101/`, using the
`factory-editorial-` prefix. No model calls or physics steps were performed.

## English compatibility dashboards and configuration index

Three compatibility dashboards now use English labels, status/error text and
locale formatting. The shared-world view displays Controller while retaining
the historical `Coordinator` role ID for routing/sorting. The two-session pilot
is explicitly labeled Legacy and keeps its original READY/START experiment gate;
it is not documentation of the new direct-START benchmark protocol. Existing
message/event payloads and archived snapshots are not rewritten.

All three inline JavaScript programs parse with Node. The existing four mailbox
pilot lifecycle/snapshot tests passed in 0.207 seconds. An initial text scan
caught one untranslated camera filter label, which was corrected before the
final parse/English check. These checks do not claim new browser visual or
native-engine qualification. The configuration index is now English and clearly
separates the unified TOML, engine catalogs, asset locks, native baseline JSON,
frozen Factory inputs and editable video project. These changes do not modify
physics, asset fingerprints, task selection or startup behavior.

The remaining tracked-text English inventory is 133 files/126,853 Han characters,
recorded in `english-inventory-after-editorial.json`. Repository-wide English
migration remains unfinished.

## Luna/Slurm handoff migration and remaining legacy entry closure

The Luna CPU and multi-model handoff guides are now English and lead to current
unified commands. They distinguish the unpublished integration from the original
Codex/Luna branches, task-isolated API state from the native Luna batch home,
unified parallel-36 defaults from native parallel-9 defaults, START task time
from allocation time, explicit paid preflight from model-free preparation, and
stopped evidence from unsafe cross-filesystem live SQLite inspection. Historical
source commit, CLI pin, archive name/hash, offline bundle behavior, multi-profile
Dial comparison, native compatibility entries, and worktree/PR instructions are
retained with clear scope. They do not claim current provider prices or model
compatibility from the dated research tables.

Review found that `scripts/slurm_luna_l3_max_test.sh`, unlike the already retired
general Luna sbatch entry, still created `runs/tmp` in the shared checkout and
automatically ran paid preflight/execution. That remaining unsafe legacy path
now exits with migration instructions before writing runtime state. Both retired
scripts are regression-tested by executing them with synthetic Slurm variables
in an empty directory: they exit 2, describe the node-local replacement, start
no model/simulator, and leave the directory empty.

The equivalent new explicit selection is
[`configs/examples/luna-l3-cpu.toml`](../../configs/examples/luna-l3-cpu.toml):
Luna/high/adaptive, CPU rendering, parallel 4, four maximum-arm Level 3 cases,
3,600 seconds per task and a 7,200-second Slurm allocation ceiling. The actual
unified plan confirmed Transport 12, Mosaic 8, Relay 16 and Dial 16 arms, with
zero model calls and no simulator. The sample retains the existing scene
qualification labels and does not change the 36-task/24-hour root defaults.
Operators must review inherited CPU/memory/site resource requests before queueing.

The combined Slurm/Luna group passed all 26 tests on macOS (0.736 seconds) and
Linux aarch64 (0.286 seconds). Linux used the existing dependency image and the
current checkout mounted read-only, with networking disabled. Both shell scripts
and all shell blocks in the rewritten guides parse. Local Markdown links resolve;
the Level 2 minimum-arm values were independently checked against current task
metadata. Logs and the four-task plan are retained under the existing engineering
evidence root with `luna-slurm-migration-` and `luna-l3-unified-` prefixes.
This remains offline submission/staging acceptance, not real Slurm allocation,
provider capacity or NVIDIA qualification.

## Historical loop plan and editorial guide alignment

The three-arm 2026-10-20/21 work-loop plan is now English and explicitly Legacy.
It retains all trial outcomes, retired evidence locations, stock/origin rules,
19-operation/38-phase/16-slot resource result, bottleneck assumptions, authority
boundaries, deferred features and acceptance stages. Its READY/START gate is
clearly historical and superseded for new direct-START runs. Old coordinating
role IDs are not renamed in evidence. The root README, native Factory guide,
Factory overview and unified configuration guide now distinguish the implemented
editable project from the still-open full newly rendered current-source movie.
They also distinguish raw-frame cleanup after successful Cycles encoding from
a subsequent subtitle failure, which retains the raw movie and failed attempt.

English scans and local Markdown link checks passed for these edited guides.
No execution semantics, asset fingerprints or archived evidence changed. The
remaining tracked-text migration is 130 files/119,355 Han characters, captured
in `english-inventory-after-slurm-guides.json`; this remains an open release gate.

## Dated provider research translation

The four-profile pricing and eight-provider compatibility research snapshots are
now English. Both retain the original 2026-10-28 review date, distinguish recorded
figures from current account access/pricing, and point to current handoff commands.
The compatibility guide distinguishes the raw Codex catalog seed's lite/code-mode
fields from the native launcher's effective Responses/function-tool overrides.
It does not claim that offline configuration proves real-provider image/tool,
compaction or fork compatibility.

The verification receipt `english-provider-snapshot-verification.json` under the
existing engineering evidence root compares the edits against their HEAD source:
all 14 and 41 distinct source URLs are preserved, as are numeric cells in the
price, quota and funding-tier tables. Both documents are free of Han text, local
Markdown links resolve, and `git diff --check` passes. This is a translation of
historical research, not a fresh vendor-price audit or a paid preflight. No model
profile, asset fingerprint or experiment was changed.

## Legacy transport catalogs and generated startup guides

All three retired Cube Transport series (v2 spheres, v3 cones, v4 cylinders)
now have English guides, seed-0 catalogs and 30 English startup guides. They are
explicitly separate from the current 36-case suite. Review found that the old
v2/v3 reproduction instructions misleadingly described commands as generating
those old shapes, although the maintained generator now targets v4 cylinders.
The guides now identify that boundary, original generator archives, ignored
run-report locations and the difference between historical recorded claims and
new qualification. The generator's catalog text and startup title are English
so regeneration preserves the language and Legacy designation.

The source comparison verified all 30 displayed orders, 255 semantic/numeric
table rows, 30 demand histograms, and every startup guide's station stock,
numeric fields and adjacency. An independent output directory generated all
ten sizes (3-12 arms) and 30 seed tasks. Every task JSON equals the existing
source task; all actual MuJoCo load/support/spacing/endpoint-IK/initial-contact/
one-second-settling checks passed. Generated cylinder startup/catalog sections
match the translated checked-in guides. No previews were rendered, and none
of the 5,169 checked source files under configs/benchmarks/vendor changed during
generation. Original historical manifests and current release fingerprints were
not rewritten.

The original checkout's ten-test Cube Transport group produced eight passes
and two errors because ignored historical `assets/label_A.png` files are absent.
The same ten tests passed without skips against the newly generated isolated
scene fixture, using original preview JSON metadata for its camera/label tests;
this does not claim new preview-image rendering. Neither outcome qualifies old
cone/sphere transport, multi-arm dynamics or current-suite physical candidates.
Receipts, raw failure log, generated fixture and successful derived-fixture log
are retained with the `legacy-transport-` prefix under the existing engineering
evidence root. No model calls were made.

The remaining tracked-text migration is 91 files /
97,564 Han characters, recorded in
`english-inventory-after-legacy-transport.json`. This remains an open release gate.

## Full released-case preparation matrix

At source `abd700e`, the actual unified CLI prepared all 36 released cases for
each combination of two engines (Codex/Luna and Claude/Haiku) and four topologies
(Single, Adaptive, Controller + Worker, Worker-Worker): eight batches / 288 runs.
Every run passed frozen input verification and the complete frozen policy-release
projection check. Per-family counts are nine and per-level counts twelve in
every batch. Role counts/arm authority match each topology, including maximum
arm counts; Single/Adaptive use direct_controller_v2 and both standing modes
use direct_team_v3. Each effective config retains parallel 36, startup interval
0.3 seconds, START task limit 86,400 seconds, startup timeout 600 seconds, high
effort and task-scoped API runtime settings. Observation settings are
jpeg_896x560_q85 with realtime video disabled. Public textual inputs across all
288 prepared runs contain no Han text.

These checks ran on macOS with CPU observation settings, without starting a
simulator, model process, API request or runtime rendering backend. They prove
preparation coverage, not 288-task execution, API quota, GPU readiness or
physical completion. Claude batches deliberately remain prepared_not_qualified
with execution_available false; Codex batches remain prepared_not_started.
An initial verifier wrongly expected the Codex batch status for Claude. Its
assertion stopped after preparation, not during a trial. The corrected verifier
reused and verified existing frozen batches, then prepared the remaining ones;
no worlds or model sessions were restarted. Both logs and the complete final
`full-preparation-matrix.json` are retained under the engineering evidence root.

## Historical Claude migration proposal

The 2026-10-28 native-harness proposal is now English and clearly historical,
with links to current implementation/qualification guides. It preserves all
23 original source URLs, model IDs, baseline commit, recorded CLI versions,
stages A-I, eight implementation progression conditions and original section
numbering (including its missing section 13). It distinguishes proposed paths,
recorded third-party integration claims and obsolete READY gating from current
commands/direct START. It does not relaunch the old proposal, assert current
provider access, or make a new paid preflight. Local Markdown links resolve;
`english-claude-plan-verification.json` records the source comparison.

Remaining English migration: 90 files / 91,957 Han
characters, recorded in `english-inventory-after-claude-plan.json`.

## Container help must not execute work

While building the current committed delivery image, the command
`container build --help` unexpectedly performed the build. The resulting image
`robofrontier:aad3cf2691ce` is a successful source-frozen build of
`aad3cf2691cef90f41512b28b515deae1fb660c7`, image ID
`sha256:462afc173c44b0eb51ce1e61a92ec0913853fe24a8337442e06a6e1759085629`.
It restored all 3,467 policy asset files against the pinned archive/release;
no model calls occurred. This image predates the help fix described below.

A deterministic regression reproduced the bug in 0.025 seconds: nested help
reached the Docker subprocess boundary. Differential probes showed that top-level
container help stayed local while nested build help and unknown build flags
were forwarded. Root cause: REMAINDER parsing passed those tokens unchanged,
and the wrapper's parse_known_args settings extraction ignored them before
unconditional build dispatch. The existing native argument-parser construction
is now reusable; nested native commands are validated with that same parser.
Build accepts no arguments, and auth has local wrapper help plus early action
validation. Both the CLI boundary and direct Python wrapper validate before
Docker operations; the CLI does so before configuration loading. Authentication
options still reach their native CLI unchanged, and no policy protocol changes.

The regression now covers build/native/auth help, nonexistent config with help,
misspelled options, missing arguments and direct wrapper invocation without
Docker execution. The actual installed CLI also returned only help for a missing
config path. The combined container/configuration suite passed 26 tests on
macOS (5.588 seconds) and Linux aarch64 (12.249 seconds). Linux used the
aad3cf image's dependencies with current source mounted read-only, no network,
and tmpfs test fixtures; this is not yet a new-source image build. Before/after
logs, differential receipt and actual help output use the `container-help-`
prefix under the engineering evidence root.

## Current-source Docker and Linux preparation acceptance

The committed help fix was built using the production git-archive wrapper as
`robofrontier:8b47962499c1`, source
`8b47962499c169921f890dd931566a925882ba1f`, image ID
`sha256:bc87fe3e1e63fdbe9d527a1d02e84e9d18672f100dc19078d06111afd7d4261d`.
Unlike a dependency image with host code mounted, the subsequent Linux checks
ran the code contained in this image. All eight fresh combinations of engine
and topology prepared/verified all 36 cases: another 288 preparations, with
no model calls, no simulation and no public Han-text findings. Source identity,
per-case release projection, role allocation, 24-hour START clocks, JPEG settings
and defaults passed. The arm64 container exited zero without OOM. Its verified
receipt and state were copied after it stopped; the disposable model-free
preparation container was then removed. Existing benchmark containers and real
session evidence were not touched. No x86/NVIDIA/provider qualification is
implied. The additional CLI consumer suite passed 33 tests on macOS (10.210 s)
and 33 inside the new image (4.231 s), covering evidence ZIP, Factory/editorial,
portable benchmark and diagnostics. The initial Mac invocation lacked the tests
fixture import path; its two import errors are retained, followed by the
correct PYTHONPATH invocation and passing results.

## Factory Metal preview and user-deferred full render

A fresh complete check verified all 123,198 files of the pinned 36-station R14
Factory bundle and identified Blender 5.1.2 / Apple M5 Pro, 16-core Metal GPU.
The actual unified 1920×1080, 64-sample, three-frame Metal preview completed
with the checked-in English project, full raw/captioned decode and complete
sealing. The inspection JPEG was viewed: opening title and subtitles are legible.
Cycles took 28.442 seconds including setup/encoding; warm frames averaged
6.673 seconds. That opening-view measurement is not a reliable whole-tour ETA.

The full 6,315-frame plan was prepared and launched at lower CPU priority.
The user then explicitly requested stopping new rendering and publishing the
original movie instead. Only the verified owner of that exact plan received
SIGTERM; it stopped its child, retained the attempt and exited 2. The attempt
is interrupted with signal 15, no running receipt and no complete seal. It is
not counted as a completed new movie. New full rendering is now deferred by
user instruction, while the overall integration continues.

The original full movie was rehashed, fully decoded and published unchanged at
[Original Factory tour](https://github.com/changxuanfan/RoboFrontier/releases/tag/factory-tour-media-20261102).
It is 134,315,571 bytes, 1920×1080, 30 fps, 6,315 frames / 210.5 seconds; SHA-256
`9c83e1d0ad17c3f6d4a7ed4b7d806322160f5d61d1e58e2471f0d3b300b86f96`.
The release includes the original MP4, extracted JPEG poster, media receipt and
checksums. All four GitHub asset digests/sizes were checked against local files.
The media release does not replace the latest Factory data release or change
asset locks. It is explicitly historical and does not establish current-scene
equivalence, model success or physics qualification. README has a linked poster;
its integration-branch edit has not been merged into main. Evidence prefixes are
`factory-metal-`, `factory-editorial-metal1080p-`,
`factory-editorial-current-full-` and `factory-video-`.

## English engineering notes and remaining checker findings

The MuJoCo/Panda interface notes, harness-coverage guide and communication
research notes are now English. The interface review retains all 16 source
URLs, seven numeric joint-range rows and six section numbers, and distinguishes
interactive reset advice from prohibited policy-world restart. The harness guide
labels coverage rather than claiming a green release and distinguishes legacy
READY tests from current direct START. The communication review retains all five
paper links and explicitly labels protocol suggestions as hypotheses. These are
local translations, not fresh upstream/vendor research. Source comparisons and
local Markdown links passed; no motion, asset fingerprint or policy protocol was
changed.

A broader protocol-only checker ran with MuJoCo entrypoints explicitly blocked.
It is **not green**: 187 Python tests had two errors, and link checking found one
retired historical output link. Zero assertion failures were reported; details
remain in `protocol-acceptance-after-container-help.json/.log` for diagnosis.
Its dispatcher scenario count is still a hardcoded historical 23, while the
actual JavaScript suite reports 24; do not treat that metadata as a fresh count.
No failures are hidden or waived by the narrower passing CLI suites.

Remaining English migration: 87 files / 87,491 Han
characters (`english-inventory-after-engineering-notes.json`).

## Portable protocol acceptance and English operations cleanup

The protocol-only checker initially failed for two reproducible fixture reasons:
legacy Beam freezing required missing ignored textures, and the spring-Dial
fixture compiled a model despite the no-physics guard. Those groups now use
self-contained synthetic XML/previews and FakeWorld measurements. They retain
all task validation, input freezing, role routing, scoring and privacy assertions;
no real Panda/contact qualification is inferred from their primitive fixtures.

The original dispatcher program actually invoked 28 top-level scenarios while
its console label claimed 24 and the checker hardcoded 23. The runner now counts
its executed scenario list, and the checker requires/parses that result. No
scenario was removed. Three historical absolute Mac links also appeared valid
only because those artifacts existed on the developer's machine. They are now
explicit retired local references. Link validation rejects absolute paths,
outside-checkout traversal and symlink escapes even when those targets exist.
Two regression tests cover portable encoded/anchor/external links and those
machine-dependent false positives.

Current Mac and Linux runs both passed 199 Python protocol tests with zero
failures, errors or skips, all 28 dispatcher scenarios, the remaining JavaScript
checks, syntax checks and portable documentation links. Linux used the pinned
8b47962499c1 dependency image with this checkout mounted read-only, network
blocked, and writable temporary test directories; it is a mounted-source check,
not a newly built image qualification. Bypassing the normal image entry initially
left its TMPDIR uncreated, then a noexec tmpfs prevented a synthetic Python helper
from executing. Both failed invocation logs are retained. Setting TMPDIR to the
existing executable test tmpfs resolved that test-launch configuration without
changing production code or omitting tests.

Evidence is in `runs/engineering/main-integration-task-atlas-20261101/`:
`protocol-fixture-reproduction.log`, `protocol-portable-final-mac.json`, and
`protocol-portable-final-linux-exec-tmp.log`. The full historical discovery suite
and real native/provider/physics/cluster acceptance are separate gates.

OpenLux operations, Relay task/replay guides, the historical README and selected
archive redirects are now English. The OpenLux guide uses the actual unified
TOML/CLI, explicit paid preflight, task-local homes and maintained Docker/Slurm
flows rather than the old batch-shared and privileged-container examples. The
Relay guide distinguishes terminal completion from stricter historical process
and Oracle requirements. Historical frame rates, source-time mapping, exact
track schemas and all Relay media command blocks were retained. Original
external URLs in the ten translated documents were checked for preservation.

Five Unicode test fixtures now spell their non-ASCII samples with Unicode
escapes; parsed Python ASTs are identical to their predecessors. Their 62-test
regression group passed. The literal-Han inventory dropped from 87 files/87,491
characters to 72 files/81,751 characters. This is progress toward the English-only
repository, not a claim that the remaining history, scripts and asset UI are done.
No model calls, new scene renders, release physics edits or asset-pin changes
were made for this work. The original Factory video remains the published media;
its deferred replacement was not restarted.

## Atlas presentation refresh with preserved capture evidence

The static atlas now describes all four native Claude engineering entries while
keeping scored qualification closed. No scene rendering was used to update it.
The new `build_task_atlas refresh` command accepts an existing publication, a new
output path and its full source commit. Before writing, it compares the exact
incoming manifest and original generator/templates with immutable Git objects,
then validates every existing payload, JPEG and current public contract.

A refreshed v2 manifest binds the new browser presentation to current sources and
retains the first v1 capture manifest, its SHA-256 and source commit. Its images,
per-case JSON, aggregate task JSON, release, backend and capture metadata must
remain identical. Verification and ZIP delivery do not need historical Git
objects or an OpenGL context; creating a refresh does need the source history.
The Pages validation checkout now fetches that history for regression fixtures.
There is no Pages deployment or automatic publication change.

All 72 original JPEGs and 37 task JSON records remained byte-identical. The
original publication was verified at commit
`5c33ea3f14a3e833535e9f88f4db00a10a888267` before template edits. Only its HTML and
manifest changed in the tracked artifact. Total artifact size changed from
4,367,839 to 4,381,495 bytes, retaining the original capture proof. The offline
ZIP is 2,999,909 bytes, SHA-256
`89e7b3c6a7b28871befd034e6d7ce14054ebf77d61efd9109083189722d452ae`.

All 12 atlas tests passed on Mac (7.057 s) and Linux (6.779 s), including actual
committed-publication refresh, explicit no-model/no-renderer guards, original
input retention, overwrite/nesting rejection, tampered/rehashed image rejection,
private-field exclusion, current contracts and deterministic ZIP restoration.
Linux used read-only current source and only the Git objects/refs/HEAD required
for the immutable publication fixture; it copied no credentials and made no
network calls. The normal current-source artifact verifier also passed.

Evidence is under `runs/engineering/main-integration-task-atlas-20261101/`:
`atlas-refresh-before.log` records the missing-interface reproduction;
`atlas-refresh-regression-mac.log`, `atlas-refresh-regression-linux.log`,
`atlas-refresh-publication-verification.json`, and
`task-atlas-refreshed-offline.zip` record the completed checks and delivery.
This is presentation/provenance acceptance, not new task physics or provider
qualification. The complete Factory render remains user-deferred.

## Saved-run viewer and legacy display language

The optional local policy batch viewer now reads only existing batch JSON, saved
runtime snapshots and recorded images/video. The previous implementation could
instantiate RuntimeStore and create a SQLite database just by opening the page;
an actual HTTP fixture reproduced that behavior before the change. The new
viewer opens no SQLite database, performs no writes and starts no model or world.
It supports both engine metadata layouts, repeated cases across profiles, stale
or absent snapshots, JPEG MIME types and existing-video Range requests. Its UI
labels the batch state as saved metadata, not proof of a live process. Usage and
namespace limits are documented in `docs/local-viewer.md`.

Seven legacy analysis/generation/viewer scripts also have English display text.
Their non-text Python ASTs are unchanged; no generator or renderer was executed.
The literal-Han inventory is now 64 tracked files / 80,990 characters. The
English-only release gate therefore remains open.

Seven HTTP/viewer regressions and four mailbox regressions passed after the
final UI wording change. Earlier full protocol runs with the viewer module
included passed 206 Python checks on both Mac and Linux, plus 28 dispatcher
checks. Evidence is under
`runs/engineering/main-integration-task-atlas-20261101/`; these are offline
protocol checks, not new model or task qualification.

## Oracle terminal recovery and final local regression

New schema-4 Oracle preparations freeze an explicit execution protocol with
`task-reference` terminal semantics; `strict-process` remains available. Old
schema-1/2/3 configurations and frozen executions keep their original shape and
rules. Source scenes, score tolerances, asset locks and historical reports are
unchanged. Reports expose task completion, process cleanliness, resolved
execution, valid physics and strategy completion separately. Privileged Oracle
work remains distinct from a scored model trajectory.

The recovery audit removes historical-process vetoes from task-reference
Mosaic/Relay paths, distinguishes current support from old drop/custody flags,
and uses measured separation instead of preferred aperture as a release fact.
Transport retains force-off release phases across rejected exits. Its empty-hand
screen requires real upward board support, compares identical geometry-distance
queries, bounds finger contact across the whole phase and rejects new/worsened
penetration without falling back to insertion tolerance. Final scoring and normal
arm/world guards are preserved. See [recovery boundaries](../oracle-recovery.md).

The previously failing Linux Dial pressure-requalification test was reproduced
unchanged. Nominal 20 mm regrasp failed at a measured 26.709 mm aperture. At that
boundary the tilted stem's projection on the fingers' closing axis was 21.906 mm.
Changing only the requested grasp width to the measured projection made the
original physical test pass on macOS and Linux. The 5 mm actuator tolerances and
actual bilateral airborne-support checks remain unchanged. Invalid projections
still require geometry review. This fixes a reference geometry assumption, not
the task evaluator or the physical drive's acceptance thresholds.

The audit also reproduced a permanent historical-uncertainty veto after original
terminal feedback was known. Resolution now matches the original call ID and
robot without editing the uncertain history. Adapter acknowledgement fences need
explicit execution-owner review of the adapter's own terminal result; no pending
sequence is replayed. Legacy/strict behavior is retained. A separate regression
reproduced partial-start acknowledgement loss escaping the action log; attempted
IDs are now recorded as uncertain and unissued calls as `not_started` before
another batch ID can be allocated. Invalid physics blocks new actions.

The final selected group passed 391 tests on macOS (73.111 seconds) and Linux
aarch64 (88.236 seconds), with no failures, errors or skips. It covers the four
Oracle families, original physical Dial fault injection, real Panda owner-review
and stop feedback, archived-pose socket screening, configuration versions,
workflow supervision, Factory and source snapshots. These are overlapping
engineering checks, not full task or real-provider qualification. Linux used
the existing `8b47962499c1` dependency image with current source mounted read-only,
network disabled and local temporary fixtures; it was not a newly built image.
The first concurrent Linux run had two source-asset read-permission errors;
that failed log is retained, followed by the complete passing isolated run.
Both platforms additionally passed 235 protocol-only Python tests and 28
dispatcher scenarios, with physics entrypoints blocked. Linux's first protocol
invocation lacked writable fixture/bytecode directories and failed before a
complete report. A new invocation used local executable temporary directories for
the legacy fixture and Python cache while retaining read-only source; it passed
without changing tests or production code. Both invocation logs remain retained.

An independent new controlled Transport probe, `archived-pose-exit-v9`, completed
three withdrawal actions and 8.040 simulation seconds, established separation
and retained original acceptance of the selected material. Execution was resolved,
physics valid and the scene hash unchanged. It explicitly reports the full
24-goal task incomplete. Initialization used archived state 73 and new holding
references; this is neither exact episode continuation nor a new physics-release
qualification. Earlier attempts remain unchanged.

Evidence is in `runs/engineering/main-integration-oracle-final-20261102/` and
`runs/engineering/oracle-terminal-recovery-20261102/`. No paid model calls or new
video rendering were performed. Full repository, real hardware/provider and
publication gates remain open.

## English archival and robot-interface notes

The 2026-10-30 evidence synchronization receipt, 2026-10-19 VLA action-space
review and 2026-10-22 robot-interface audit are now English. Their dates, every
source URL and numeric value remain preserved. The force-interface audit keeps
the pre-grasp-v2 findings separate from the later implementation update; the
archive receipt keeps its historical test counts, interrupted Claude status,
pixel/float32 scope and then-unverified deadline/Slurm boundaries. No vendor
research was refreshed and no historical trial was relabeled.

Local links resolve and the three files contain no Han characters. The current
tracked-text inventory is 61 files / 75,375 Han characters, so the English-only
gate remains open. Verification is in
`runs/engineering/main-integration-oracle-final-20261102/english-operations-verification.json`.

## Committed native Oracle protocol smoke and English historical entries

Committed source `87cf155` prepared and ran the four current minimum-arm Level 1
native Oracle entries through the unified CLI, each with a 15-second engineering
limit and 20-second cleanup allowance. All four native owners exited without
forced kill or descendant cleanup and released their owner locks. Every entry
wrote `robofrontier.oracle-report.v2`, with valid physics and incomplete tasks.
Transport/Mosaic/Relay retained their unresolved in-flight actions; Dial resolved
its stop. No interrupted run was promoted to full success.

Read-only stream audits decoded 1,405 Transport, 1,601 Mosaic, 1,909 Relay and
1,493 Dial frames (6,408 total), checking every chunk, timestamp and visual event.
Maximum sample gap was 0.018 seconds, and all events fit within retained final
poses. Each complete-recording gate correctly rejected only the interrupted
status. These checks did not solve full tasks, call a model or render new videos.
Native status/report and motion receipts remain under
`runs/engineering/main-integration-oracle-final-20261102/`.

The current Dial/environment entries, dated Oracle integration plan, Transport
R11/R12/R13 history, early RGB/NoSlip records and three historical redirect
headers now use English. Historical commands, numerical results and source URLs
are retained, with old demo defaults and preview-only checks labeled by date.
All edited local links resolve. The tracked-text inventory is now 50 files /
72,002 Han characters; the English-only gate is still open. Translation source
comparisons are in `english-history-verification.json` beside the Oracle evidence.

## Historical fixture closure and full local discovery

Full discovery first ran 1,495 tests with no assertion failures, 41 errors and
26 skips. Most errors were absent ignored historical data; a hardware-capability
test also constructed World without its current observation-image profile.
That fixture now initializes the same declared profile without changing either
hardware-width assertion or production World behavior.

The preserved primary checkout supplied 3,643 absent assets from identical-XML
scenes, 1,295 original previews and 87 files from the unchanged source-preservation
receipt. Workstation checksums were required wherever declared. Independent
copied objects were shared only inside the new fixture store, with no links to
the originals. Pinned closed Dial/Transport reports, streams and original harness
files were copied byte-exactly; all 36 historical Oracle-presentation sources
were restored against their existing metadata/asset hashes. No approximate
regeneration, source-scene edit, raw-report rewrite or new rendering occurred.

The Dial family review had additional actual compatibility defects after these
files were present: absolute selection paths did not relocate; the legacy
builder incorrectly required the current explicitly unqualified physics
candidate to equal its older successful witness; and it compared the historical
report with the changed current scorer. It now selects only the pinned local
report with the exact logical suffix and SHA-256. Current metadata is separately
bound to the release and registered hashes. A source mismatch requires both the
existing explicit historical-evidence caveat and the unqualified-candidate
release label. Public geometry uses the current source, and images use verified
existing reviewed public files. Formal readiness remains false and all original
qualification/assistance labels are preserved.

The old report's evaluator is verified from its own frozen bytes. No equivalence
is claimed for current terminal scoring. The only newly admitted controller
compatibility change is the exact role-label/engine/direct-START validation in
load_harness: removing those reviewed checks yields the identical AST from
pinned commit `d3e5916`, including every control and timing function. Its raw
historical hash is unchanged. Mutation tests reject changed control/timing,
unreviewed source, invalid report relocation/hashes, missing candidate caveats
and changed historical evaluator bytes.

The focused handoff/source group passed 32 checks on network-disabled Linux
aarch64 using read-only current source and the existing dependency image. Full
macOS discovery then ran 1,501 tests in 329.983 seconds: 1,475 passed, 26 skipped,
zero failures/errors. All 28 dispatcher scenarios, other JavaScript checks,
syntax checks and portable links also passed. The first failed full run remains
retained. This passing discovery used the restored local historical fixtures;
it is not automatic fresh-clone fixture delivery or Linux/NVIDIA/Slurm qualification.
The full group includes native CLI tests with synthetic loopback endpoints;
the checker's descriptive scope now states that explicitly. The raw earlier
report is retained. Protocol-only validation with source-compatibility guards
also passed 239 tests and 28 dispatcher scenarios on macOS.

See [testing](testing.md). Logs, data restoration receipts, exact control-AST
comparison and passing/failing reports remain in
`runs/engineering/main-integration-oracle-final-20261102/`. No paid inference
or new full video was started. Remaining fixture packaging, English migration,
hardware/provider qualification and final publication gates stay open.

## English historical display generators

Eight historical collection, contact-sheet, video-index, concept-preview and
Dial/Relay/Mosaic display generators now emit English captions. Original status
labels still distinguish selected success, incomplete/user-paused runs and older
scene revisions. Concept sketches remain explicitly labeled as concepts.

Each edited Python file parses, and its AST is identical after replacing string
constants only. Numeric drawing coordinates, execution paths, input/output paths,
record selection and physics are unchanged. No generator, renderer, world or
model was executed for this text migration, so no newly rendered layout is
claimed. The comparison receipt is `english-display-verification.json` under the
2026-11-02 Oracle engineering directory. Tracked text now contains 42 files /
70,259 Han characters; the repository-wide English gate remains open.

## Optional historical fixture installer

The preserved test inputs now have a separate local delivery archive and
per-file manifest: 43,678 files, 757,780,223 compressed bytes. Both delivery hashes
are recorded in the testing guide; individual file identities remain unchanged.
The standard-library installer requires the independent manifest pin, validates
all members before installation, rejects source overwrites, traversal and
unverified links, reuses only exact existing files and supports retry after an
interrupted install. Hardlinks share only newly staged copies. Ten focused
macOS tests pass, including late corruption with no partial installation.

An initial isolated Linux staging driver was stopped before running tests:
its random-access extraction repeatedly decompressed hardlink targets. Its
original log and staging volume are retained. The maintained installer instead
reads sequentially and resolves hardlinks only to already verified staged files.
Independent Linux full-discovery and actual large-bundle installation results
are still pending at this commit. This local bundle does not add a public
historical-fixture download or change the ordinary policy bootstrap.

## English early communication pilots and slip diagnosis

The early shared-world trial, two-session mailbox pilot and 2026-10-19 slip
diagnosis now have English archival text. The desktop driver's controlled role,
actual idle versus self-report, original permission limitations, protocol-only
scope and separation of offline truth-assisted diagnosis from model results are
retained. Obsolete commands are labeled historical. All numeric tokens and
source URLs match the originals, and local links resolve; the comparison is
`english-pilot-verification.json` in the Oracle engineering evidence directory.
The English migration remains open, with 39 tracked files / 67,326 Han characters.

## English historical Factory viewer and V7 record

The legacy empty-building viewer and V7 rendering record now use English. The
viewer still identifies its reserved zones as an empty-building preview; it
cannot be mistaken for the later populated Factory delivery. HTML structure,
non-text JavaScript, template expressions and numeric values are unchanged, and
the inline script parses. No renderer was started. The V7 record retains all
numeric values, commands, historical limitations and local links. Verification
is in `english-factory-legacy-verification.json` in the Oracle evidence root.
The remaining English inventory is 37 files / 66,203 Han characters.

## English original environment notes and Transport math

The early eight-arm beam-handoff and four-arm Mosaic environment notes now use
English, retaining geometry, contact/IK boundaries, measured results and the
legacy READY/topology protocol. The latter is explicitly separate from current
direct START. Missing original beam-run reports remain identified by their exact
historical paths instead of unusable links. No historical reference is promoted
to current qualification. The Transport nine-task mathematical baseline retains
every schedule value and all eight unpassed categories, including unresolved
execution. Numeric tokens, source URLs and local links were checked in
`english-early-environments-verification.json`. The remaining tracked English
inventory is 34 files / 63,299 Han characters.

## Independent Linux discovery exposed a fixture packaging omission

Source `53db653` was cloned from its Git bundle into a Linux-local Docker volume,
without the live worktree, active databases, credentials or network. The v2
fixture installer verified and installed 43,678 files in 10.744 seconds. Full
discovery ran 1,511 tests in 232.246 seconds: zero assertion failures, one error
and 26 conditional skips; all JavaScript and documentation-link checks passed.
The error was a missing registered Relay Oracle source under `outputs/oracle`,
which the original export's `configs/environments` / `runs/oracle` roots omitted.
This failed full-discovery report is retained in `linux-isolated-results-v2/`.

The v3 optional bundle adds all nine registered dated Relay source directories:
858 original metadata/asset files, verified against unchanged release source
pins and workstation asset checksums. It now holds 44,536 files / 759,710,326
compressed bytes. The installer admits only those dated source metadata/assets
under outputs, with unrelated paths rejected. Eleven focused macOS checks pass.
The testing guide contains the new independent manifest and archive pins. The
v2 bundle/report remain retained; neither is silently relabeled complete.
An independent v3 installation and complete Linux discovery are pending.

## English palette labels and legacy task prose

Five pattern/task JSON sources now use English display labels, descriptions,
objectives and execution-context prose. Parsed values outside those text fields
are identical: palette IDs/hex values, every lattice cell, object/goal constraints,
control limits, friction and scoring thresholds remain unchanged. The original
frozen scene pattern copies and recorded run inputs were not rewritten; only
future generation/preparation reads the translated source text and its new raw
hash. Original/translated hashes are in `english-pattern-task-verification.json`.
Existing inventory/schedule and petal-symmetry/round-crank checks pass (three
checks). The remaining tracked inventory is 29 files / 63,012 Han characters.

## English historical report output

The original trial exporter, Mosaic local-color preview and deterministic
Transport program summary now produce English text. Their original limitations
remain explicit: a single pilot does not compare architectures; sampled geometry
does not qualify parallel paths; truth-assisted program execution is not an RGB
policy baseline; unpassed physical references cannot attribute failure to model
intelligence. All three Python files parse and retain identical non-text ASTs.
No exporter, renderer or simulation was run. The source comparison is retained
in `english-legacy-report-verification.json`. English migration remains open at
26 tracked files / 61,812 Han characters.

## Independent Linux full discovery passed with v3 fixtures

The independent Git-bundle clone of `4f9cd85` installed all 44,536 v3 historical
fixture files in 10.446 seconds on its Linux-local volume. Full discovery ran
1,512 checks in 227.561 seconds: 1,486 passed, 26 conditionally skipped, zero
failures/errors. All 28 dispatcher scenarios, other JavaScript checks, syntax
checks and documentation links passed. Stopped-container receipts and logs were
copied to `linux-isolated-results-v3/`; the original v2 failure stays retained.
No source assertions, physics thresholds or original evidence hashes were
weakened. Network was disabled; no credentials or active host database were
mounted. Native loopback test sessions are engineering checks without real
provider inference. The existing arm64 dependency image and pinned Panda assets
were reused, so this is independent current-code Linux CPU discovery, not a new
image build, x86/NVIDIA qualification or automatic public fixture distribution.

Slurm was discoverable after loading the site's `slurm/slurm/23.02.6` module.
Read-only queries reported debug and llm partitions with GPU resources; several
SSH attempts failed before a later successful query. No allocation, provider
trial or unified stage-out qualification is claimed by this discovery receipt.

## English historical suite previews and policy-batch report

The early Frontier v2 preview, five-valid-setting Dial preview and historical
minimum-scale policy-batch report now emit English. Preview text retains static
initial-state and non-qualification caveats. The policy report explicitly labels
its original 20-minute budget and process-compliance requirement as historical,
rather than changing the current 24-hour/terminal-outcome protocol. Numeric tokens
and non-text Python ASTs are identical; no previews, models or worlds were run.
The comparison is in `english-preview-batch-verification.json`. Remaining tracked
English migration: 23 files / 60,692 Han characters.
