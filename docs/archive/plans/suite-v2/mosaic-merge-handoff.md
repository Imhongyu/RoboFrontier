# Mosaic branch merge handoff

This is the dated branch-receiving record, separating delivered family work from
then-pending shared integration. Consult the [acceptance ledger](../../unified-main.md)
for later implementation. The endpoint/scoring plans below remain historical;
later independent-loop and terminal-outcome requirements take precedence.
Current task rules are in the [task guide](../../../tasks/mosaic.md). This cleanup
started no new GPT/Oracle and did not change the shared harness.

## Receiving entries

| Content | Entry |
| --- | --- |
| Purpose and delivery commands | `configs/task_families/mosaic/delivery.json`, `python -m scripts.mosaic` |
| Nine GPT cases | `configs/task_families/mosaic/r14.json`, `configs/suites/frontier-mosaic-r14.json` |
| Nine original Oracle cases | `configs/task_families/mosaic/r13.json`, `configs/suites/frontier-mosaic-r13.json` |
| Public GPT materials | `outputs/policy-packages/mosaic-r14-local-colours-20261027/public/` |
| Original public review package | `outputs/policy-packages/mosaic-r13-20261027/public/` |
| Original Oracle summary | `runs/oracle/mosaic-continuation-20261026/FINAL.md`, `evidence-summary.json` |
| Videos/source edits | `outputs/oracle/mosaic-continuation-20261026/videos/video-index.json`, including its original edit-timeline index |
| R14 private color-design evidence | `runs/engineering/mosaic-local-colours-r14-20261027/` |
| Private unused-interval proposals | `runs/engineering/mosaic-motion-review-20261027/` |
| Cleanup protection/change lists | `runs/engineering/mosaic-merge-cleanup-20261027/` |

R13 passed all 1566 cells, retaining 7 failed actions and in-world recovery.
Three selected 4-arm runs were pure_program; the other six were
privileged_assisted. R14 had only color-variant design/geometric-equivalence
evidence, without inheriting R13's completed-color Oracle qualification.
Formal policy_launch_ready remained false.

Daily checking defaulted to gpt; original Oracle review required explicit purpose:

```sh
python -m scripts.mosaic check
python -m scripts.mosaic check --purpose oracle
python -m scripts.mosaic check --verify-recorded-chunks --verify-protected \
  --report runs/engineering/NEW-report.json
```

Commands checked inputs only. Only explicit `--report` created a new report,
refusing overwrite. `package --output NEW_DIRECTORY` exported the verified frozen
package without recoloring or recalculating Oracle. Color-design builders and
the original R13 package module retained their original bytes for version checks,
rather than serving as daily default entries. `docs/history/mosaic-*` records
history, not a new execution protocol.

## Data/assets outside Git

The worktree's `runs/`, `outputs/`, `.venv` and `vendor` pointed to the primary
repository's durable directories. Merge commits neither copied them nor restored
ignored `assets/` meshes/textures. JSON/MJCF for 18 R14/R13 scenes traveled through
Git; assets required separate materialization.

Historical primary-repository materialization commands:

```sh
python -m scripts.mosaic assets \
  --destination /Users/fanchangxuan/Repos/roomscript2 --dry-run
python -m scripts.mosaic assets \
  --destination /Users/fanchangxuan/Repos/roomscript2
```

The materializer checked each workstation manifest/asset SHA, reused identical
targets and refused differing bytes. Sources were existing assets, original
Oracle self-contained `motion/source/assets`, then durable content caches.
R14 changed only XML/metadata colors; original R13 frozen assets could restore
the same meshes/textures without the retiring worktree. No model, IK or physics
integration started.

Bound absolute paths in private R14 design files then pointed to durable primary
`runs`, outside the worktree. Migration to another machine required explicit
path mapping/new delivery manifests, retaining original hashes/provenance.

Some `_executor_launches` aliases pointed to the old worktree. These were
historical launch caches. Selected trials' `executor-source`, `motion/source`
and state chunks were the protected review/replay sources; launch caches were
not physics-world restart state. Original experiment paths remained provenance,
and manifests identified aliases. This branch neither deleted worktrees nor
rewrote old frozen sources/aliases.

## Family cleanup scope

Active documentation converged on the task guide and this handoff. Old R13
protocols, package preparation, R14 color design and early GPT/Factory planning
moved into existing `docs/history`. Version-bound R13/R14 prompts/shared skill
retained original bytes so delivered review packages still verified.

Completed diagnostics, fault injection, parallel probes and old staged-video
entries left the active worktree. Original bytes remained in commit `a66e183`
and trial-frozen sources. `retired-code.json` recorded individual hashes/frozen
copies. Coverage, recovery execution and meaningful regression tests imported
by R14 remained.

Removal candidates were limited to superseded drafts, duplicated timeline
reexports and reproducible caches. Full-content SHA deduplication hardlinked
videos while preserving paths, encoded bytes, historical videos and all indexes.
Useful recovery logs, failure feedback, source chunks, original scenes, edits
and review reports remained.

`protected-files.json` bound 103823 original files, including selected complete
Oracle trials, the original 496-file protection set, R14 scenes/assets/delivered
galleries and version evidence. delivery.json pinned its SHA. Cleanup reports
recorded actual removal/deduplication. Early physical-unit paths totaled about
77GiB logically, with substantial hardlink sharing. That was not reclaimable
space and did not justify whole-directory removal.

## Historical shared-integration plan

The main session's receiving order was merge/data-integrity acceptance, shared
wiring/Factory integration, multi-table Oracle camera-demo checks, then freezing
new GPT protocol and parallel execution. GPT batches needed independent run
databases, credentials, physical owners and outputs; the new protocol had to
specify model concurrency, CPU and spending budgets.

1. **Execution gates/version selection.** Generic `v2.cases()` still defaulted Mosaic to R10, and the old minimum probe fixed R10/1200s. Select all nine cases explicitly through purpose registries, recognizing R14 color-evidence boundaries. Freeze new model, effort, topology, cost and execution protocol, without inheriting pilot limits. Connect `validate_task`/`World.start_trial` preview restrictions through the shared protocol, rather than pretending to run an old probe.
2. **Public loading/sealing.** `run_setup` then copied only generic roles/skill, without Mosaic materials. Allowlist public completion, static geometry and guidance; record files/hashes before sealing. Family public task data is supplementary and must not overwrite new formal gates through preview fields. Start clean policy contexts; engineering registries, pairings, truth and repair experience stay private.
3. **Controller/scorer equivalence.** Original servo2/pd1000-v1 matched frozen records. The physical fingerprint hashed all of `pipeline.py`, so gate-only changes also changed its hash. Analyze impact and prove limited compatibility first. Preserve old fingerprints; neither hide differences nor automatically require rerunning every Oracle.
4. **Unified edit protocol.** Mosaic/Dial/Transport used identically named v1 formats with different structures/boundaries. Design a new version and explicit legacy adapters, preserving case/scene/stream/events identity, exact output frames and full-sampling-rate retained intervals. Keep source, edited and output-frame clocks separate; do not interpolate across removed intervals.
5. **Independent station clocks.** Each station consumes source states/events using its own edit mapping/speed. After all updates, set common presentation time and render once. The historical plan held exact final states and ended when the longest finished, without looping. Permit different scene/run bindings for the same case_id to avoid mixing Oracle/GPT colors. `FactoryPlayback.apply` then set global data.time, requiring handling by the shared orchestrator.
6. **Scene and filming.** Oracle-matched scene: `outputs/robo-factory/v6-mosaic-recorded-20261027`; old v6 Mosaic R10 bases did not match. Integrate each family from exact frozen station sources, using rigid translation/horizontal rotation without scaling. GPT uses its own frozen R14 source. Shared work included Factory detail, Robo Factory wall-lettering removal, overview/local orbit/per-table difficulty shots, material/resource reuse and near/far views. Measure complexity/render cost at equal settings; the user's desired increase was below 100x.
7. **Semantic unused-interval review.** Existing Mosaic labels remained proposals. Review protected actions, commanded grasp lifetime, progress and completion; whole-window aggregation was conservative, and prolonged oscillation still required task-purpose review. Force settings/pose were not measured contact forces. The 135 idle proposals were not automatically applied.

Shared diffs required feature-wise integration:
`robofrontier/motion_edit.py`, `scripts/render_frontier_oracle.py`,
`scripts/replay_motion_in_factory.py`, `scripts/export_factory_recorded_pose.py`
and related regressions. A branch's latest file must not overwrite other families.
Re-pin commits and uncommitted data before merging because worktrees may advance.

The then-proposed shared README text was:

> Nine complete R13 Mosaic Oracle runs and independent action audits passed,
> totaling 1566 cells. Later GPT uses R14 locally mixed supplies, retaining
> positions/physics; formal shared wiring remained pending. Oracle Factory replay
> stays bound to original R13 motion. Presentation prefers 30x/30fps, independent
> wait removal per station, exact final-state holding and exit after all finish.
> See docs/tasks/mosaic.md for specification/data entries.

## Recorded merge checks

Family cleanup passed 58 related tests, both R13/R14 nine-case review packages,
original action-chunk checks, 103823-file protection and restoration/compilation
of 18 scenes / 1332 bound assets without worktree assets.
Reports: `runs/engineering/mosaic-merge-cleanup-20261027`.

- Original R13 tasks/motion/failure recovery/audits stayed unchanged. All nine R14 cases conserved color/target counts; purpose versions stayed separate.
- Assets for 18 scenes could be restored without the old worktree, reused on repeat and protected against conflicting overwrite.
- Both review packages passed, with public boundaries matching their prompts/skill; every protected-file check passed.
- All nine historical 30x videos/source mappings remained readable, retaining all old paths/hashes.
- No new Oracle/GPT start or old experiment rerun was introduced; shared control, scorer, READY and role permissions were unchanged.
- Shared-stage checks still needed staggered-wait multi-table playback, hold_final/end after the last table, source/version mismatch rejection and source-state mapping across cameras/backgrounds.
