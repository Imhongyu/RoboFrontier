# Transport branch merge handoff

This is the dated family-branch handoff. Its pending integration items describe
that stage; consult the [unified acceptance ledger](../../development/unified-main.md)
for implementation and qualification completed since then. Its hold-final
presentation plan was later superseded by the current independent-loop policy.

Transport's default was the physical half-opening R14. Current specifications,
entrypoints and evidence boundaries are in the [task guide](../../tasks/transport.md);
GPT guidance is `prompts/tasks/transport.md`. Family preparation/cleanup was
complete in this worktree; shared integration, formal R14 qualification and
combined Factory rendering remained with the main session.

## Merge scope and ownership

| Content | Authority |
| --- | --- |
| Scene/acceptance/controller binding | `configs/task_families/transport/half-opening-r14.json` |
| Nine-case catalog | `configs/suites/frontier-transport-r14.json` |
| New scene metadata | `configs/environments/cube_transport/frontier-v2-r14-transport-*` |
| Original R13 nine-case evidence | `configs/task_families/transport/r13-qualified.json` |
| Durable delivery paths/SHA/playback endpoint | `configs/task_families/transport/delivery.json` |
| Public inputs and asset materialization | `robofrontier/suite/transport_policy_package.py` |
| Native source edits and signal functions | `robofrontier/suite/transport_motion_edit.py`, `transport_motion_signals.py` |
| Build/edit/check | `scripts/build_transport_policy_package.py`, `edit_transport_recordings.py`, `check_transport_family.py` |
| Final task guidance | `prompts/tasks/transport.md` |

The branch also contained concurrency, grasp, recovery, collision-screening and
media changes from completed Oracle work. Transport's `transport_*` modules and
tests belonged in integration; shared files needed feature-by-feature merging
to retain other families. Shared Skill, role prompts and global catalog had
not yet loaded the new family guidance at this stage.

Shared changes requiring separate review:

- `suite/oracle.py`, `suite/oracle_budget.py`: reference execution, event/pause and budget records.
- `motion_recording.py`, `motion_timeline.py`: selective reads, legacy delivery timelines and default references.
- `factory_workstations.py`: frozen-source overrides, half-opening display and rigid station transforms.
- `render_frontier_oracle.py`, `replay_motion_in_factory.py`: 20x / 30fps and legacy edits.
- `build_factory_workstations.py`, `export_factory_recorded_pose.py`, `render_factory_blender.py`: provenance and geometry-display propagation.

Cleanup left these shared bytes unchanged; C1–C5 below remained open. Conflicts
must not be resolved by replacing entire files from one branch. Do not rename
old catalogs in bulk or rewrite original scene, controller or scorer report SHAs.

## Durable data and historical merge steps

The durable local root was `/Users/fanchangxuan/Repos/roomscript2`; this worktree's
`runs/` and `outputs/` were links. These directories, scene `assets/`, previews
and dependencies were ignored. **Git merge does not transfer them.**

1. Merge source, configuration, documentation and tests; retain the primary repository's durable `runs/` and `outputs/`.
2. Check report, stream, edit-array and video SHAs against `delivery.json`. Preserve the entire Transport batch, including unselected attempts, frozen code, action/process/recovery logs, unit checks and diagnostics.
3. In the integrated checkout, run `build_transport_policy_package.py --assets-only`. It restores new R14 assets from bound original witnesses, verifies existing assets and retains independent inodes without needing the old worktree.
4. Use a new `--output` when rebuilding public packages; never overwrite a frozen release.
5. Complete C1–C5 and checks, then launch formal GPT only under the user's instructions.

Packaging/editing used repository Python dependencies. Historical Oracle
execution additionally required greenlet from `requirements-oracle-transport.txt`.
The local `.oracle-deps/` was not mergeable source or the default controller for
new GPT trials. Frozen R13/R11/R12 manifests retained historical reproducibility;
new tasks selected R14 only.

## C1: Public input loading and freezing

Shared run_setup should load the family's public JSON and `transport.md` through
one family provider and freeze hashes. Public data includes actual table support,
openings, bounds, orders, mechanisms, camera mounting/calibration and completion
contracts. Oracle indexes, trajectories, engineering diagnostics and recovery
recipes remain private. The generic Skill needs one mechanism for following
per-task family references; family prompts supply the rules.

## C2: Formal qualification and source binding

Original R13 had nine independent complete witnesses, 216/216: three programmatic
and six engineering-assisted. R14 had compilation/model-consistency checks and
zero contact with newly added table material over six trajectories / 1,998,263
states, without a new complete physical trial. Retain the preview gate and
`formal_gpt_ready=false` until an explicit qualification path is established.

Controller/scorer changes require old/new source records and verification.
Model, effort, topology and budget come from the new shared configuration,
without inheriting an old 1200s probe or Oracle budget. Source matching must
compare more than case_id.

## C3: Edit adaptation

Native source format: `robofrontier.transport-source-edit.v1`, producer transport.
Each JSON binds original stream/scene/action/process/array hashes;
`selection.npz` stores original timestamps and bool keep.
`TransportEdit.at_video_time(T,speed=20)` returns original frame/time, effective
time and ended.

The shared layer must explicitly adapt actual structures. Transport's old
`robofrontier.motion-edit.v1` and identically named formats in other worktrees
may differ; schema text alone is insufficient. Background/material/camera changes
reuse the same source selection. Existing generator snapshots and hashes remain
unchanged. Cleanup only moved signal functions; it neither recalculated nor
replaced delivered selections.

## C4: Multi-table Factory and historical endpoint plan

Each table has an independent stillness-removal clock while synchronizing its
robots, fingers, objects, mechanisms and appearance. One Factory frame can use
different original times per table. After all mocap/appearance updates, perform
one whole-Factory FK/render. Factory `data.time` uses presentation time, rather
than the last station's source time.

**The then-requested policy held each exact final state and ended after all
tables finished, without looping.** Transport used 20x and 30fps; other families
selected their own speeds. Every frame should trace each station's source run,
frame, original/effective time, edit hash and completion state. Acceptance was
to start with two tables of different lengths/staggered waits, then nine tables
and the full Factory.

Original Oracle FK used frozen R13, displaying half-openings relative to R13 at scale 0.5.
Future GPT used physical R14 at scale 1 relative to R14. The shared renderer then still defaulted
to 0.5; integration had to consume source-specific family metadata to avoid
quarter-sized R14 holes. Existing single-table mappings/two-frame previews were
not full combined Factory videos.

## C5: Merge acceptance

Check actually frozen public inputs and READY capabilities, concurrency,
recording, uncertain actions, timeouts and failure retention. Before merging,
re-pin other worktrees' actual commits and uncommitted files rather than trusting
old HEADs in historical documents. Main-session responsibilities included Factory
appearance, camera demo sequencing, Robo Factory wall lettering and Codex context
settings.

## Cleanup record and verification

Audit directory: the durable batch's `engineering/transport-cleanup-20261027/`.

- `source-before/`, `legacy-media/`: original code and one-off legacy media scripts.
- `protected-before.json.gz`: per-file hashes of original experiments, final edits/videos and scenes.
- `shared-before.json`: shared-code baseline; `removed.json` / `deletion-candidates.json`: removal details.
- `verification.json`, `tests.log`, `family-audit.json`: post-cleanup checks.
- `merge.patch.gz`, `source-only-apply.json`: final branch diff and independent application to the primary repository.

The 9 historical plans moved into existing `docs/history/`; active guidance was
reduced to final state. One-off old editing/publication scripts left active
scripts, while reused signal/frame-check functions remained in family modules.
The 7 superseded draft-output directories were removed. Original experiments,
final media, half-opening audits, old videos' audit-v4/timelines and native
source v2 stayed. A one-off root handoff pointer was removed; this became the
common handoff, with a compact batch recovery entry retained.

Native edits retained 1,096,132 states and skipped 1,035,753. Existing 20x videos
still used the original reviewed edit, distinguished by delivery indexes and
manifests. The new native source edit had not been batch-rerendered.
