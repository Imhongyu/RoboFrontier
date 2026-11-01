# Historical Relay worktree pre-merge cleanup plan

2026-10-27. **This round only inventoried and planned; it deleted, moved or
rewrote no runtime/shared data.** It added this document and aligned the previous
playback plan to each table's own speed, without changing executables. Previous
plan: [relay-gpt-readiness-and-factory-parallel-plan-20261027.md](relay-gpt-readiness-and-factory-parallel-plan-20261027.md).
Later implementation is recorded in the [acceptance ledger](../development/unified-main.md).

## 1. Cleanup objective

Retain `robofrontier/`, `scripts/`, `configs/`, `prompts/`, `.agents/`, `tests/`,
`assets/`, `docs/`, `runs/` and `outputs/`. Make the final Relay task, default
entry, nine-case evidence, shared merge changes and unfinished work clear to
the receiving main session.

One final default meant one authoritative definition/current entry, not merging
necessary 8/12/16-arm × L1/L2/L3 inputs into one geometry. Do not rewrite history
as final rules or claim unfinished integration is complete.

The user's future main-session task was handoff context. This round did not
merge/remove worktrees, refactor the shared harness, enrich/film the Factory,
change wall lettering or adjust Codex context settings.

## 2. Inspection scope and inventory

Inspection covered branch/main file/commit differences, directory links,
task/public projections, Relay build/planning/recovery/launch/review/render code,
references/test responsibilities, key executor dependency links and media/motion
packages. The session JSONL's user messages were traversed line by line and
cross-checked with handoffs. Reading relevant modules/entries was not represented
as line-by-line review of the entire project or other three sessions.

Branch HEAD was `16e8e16`, main baseline `d3e5916`. The preceding GPT plan was
uncommitted and had to remain preserved.

| Content | Read-only inventory | Implication |
| --- | --- | --- |
| Git-tracked files | 5773 | Many were historical environments, not new temporary branch files |
| Tracked `configs/` | 4434 files, about 526MiB | Relay cleanup must not remove other families/shared baseline |
| Relay-named historical environments | 153 directories, about 180.8MiB tracked | Only nine defaults, but old versions still supported builds/tests/reproduction |
| Six R16 / six R17 scenes | About 10.2MiB tracked each | Not interchangeable duplicates; dependencies/semantics differed |
| Identical tracked R16/R17 content | 24 files, about 3.8MiB logical | Could already share inodes/COW; logical size was not promised disk savings |
| Local Python caches | 88 pyc, about 1.8MiB | Reproducible, unmerged, low-risk removal candidates |
| Long handoffs | `relay-continuation.md` about 52KB; compact checkpoint about 35KB | A concise final entry should replace searching successive latest updates |

Logical size was not reclaimable storage. Ignored assets, APFS and hardlinks
also affected usage.

## 3. Protect first

### 3.1 Shared directories are not branch garbage

`runs/`, `outputs/`, `.venv/`, `vendor/` and `docs/generated/` linked to primary
shared directories. Cleanup must not follow them recursively or use global
`git clean -fdx`. Untracked scene `assets/` may be independently materialized
required resources, not reproducible caches.

### 3.2 Oracle evidence

- Final selections: L1 from `relay-nine-ab1abec-20261026-032833`; L2/L3 from `relay-r16-38b5423-20261026-171651`.
- Each original 60Hz motion/chunk/index/hash, frozen source model/assets, original task, actions/events/reports, actual completion cutoff and prefix proof.
- `USER-GOAL-ALL-NINE-COMPLETE.json`, user acceptance and original native results. Native failures must not become a cleaned-up claim of nine native successes.
- Actual failures, recovery requests/results, control-correction source, hot-loaded source hashes/acks and intervention classification. Final success does not justify deleting failure/recovery evidence.
- Regression fixtures/tests, especially flipped grasp, final aperture/withdrawal, support and uncertain actions.
- Original session files and Git history in place, unchanged.

### 3.3 Media and reusable data

| Important primary shared directory | Logical size | Retention reason |
| --- | --- | --- |
| `outputs/oracle/relay-20x-20261027/` | 98 files, about 501MiB | Paired videos, per-frame mappings, checks, endpoint images/reports |
| `outputs/oracle/relay-edited-tracks-20261027/` | 1043 files, about 730MiB | Nine edited 60Hz streams, source models/events/retained intervals/hashes |
| `outputs/oracle/relay-nine-videos-20x-20261027/` | 9 files, about 192MiB | User-requested consolidated simple-background videos |
| `outputs/robo-factory/relay-nine-videos-20x-20261027/` | 9 files, about 278MiB | User-requested consolidated Factory videos |
| `outputs/robo-factory/relay-recorded-20261027/` | 603 files, about 51MiB | Factory model/assets exactly matching recorded sources |

Frozen sources, asset-cache and source directories could already be hardlinked;
730MiB cumulative size did not justify repeated deduplication. Retain old complete/
4x comparison videos while removing them as defaults. Without original video/time
mapping, accelerated copies alone are insufficient. Consolidated folders are
not disposable duplicates. For exact same-hash copies, investigate hardlinks/COW
while retaining user paths. Inventory shared-data changes separately from code removals.

## 4. Surviving worktree removal

This was more urgent than saving a few MiB.

`suite/source_snapshot.freeze_executor` froze Python/harness/catalog bytes but
linked configs, assets, docs and .agents, rather than producing a fully independent
archive. Each of the two key batches had 8 executor links directly into this
Relay worktree: `executor/configs`, `assets`, `docs`, `.agents`, `config.json`
and runs/outputs/vendor reached through the worktree. Removal could break them.

Latest video reports/package README also linked to this worktree's
`docs/relay-recorded-video.md`, requiring stable primary/archive navigation.

Inventory dependencies in three groups:

- Historical provenance strings: retain them; do not cosmetically rewrite reports/hashes.
- Required files/links: export exact dependencies to durable storage, verify hashes and create separate derived archives/migration indexes. Never redirect every link to changed main content blindly.
- Current delivery navigation: move to stable merged/package-local guidance instead of temporary worktree paths.

An executor directory alone did not establish a self-contained archive.
Breaking links also did not justify copying the entire worktree/all old outputs.

## 5. Specific cleanup/retirement candidates

### A. Low-risk cleanup candidates

- Actual worktree `__pycache__/` and `*.pyc`, already covered by ignore rules.
- Enumerated tool leftovers/empty partials only after writer exit and excluding failure evidence. No newly disposable large temporary file had been found; do not widen scope for a larger deletion count.

### B. Retire only after explicit replacement

| Then-current file | Proposal | Required before removal |
| --- | --- | --- |
| `scripts/run_relay_oracle_batch.py` | Retire old timed/pilot batch entry, preserving frozen executors | Document/static-test the sole replacement; historical review no longer depends on host files |
| `scripts/declare_relay_goal_contacts.py` | Consolidate declarations, then retire one-off append migration | Generate final family rules once and align public tasks |
| `scripts/render_relay_progress.py` | Leave the active media path; archive for historical reproduction | New export retains source/cutoff/actual motion/frame mapping and old provenance |
| `scripts/render_relay_underslung.py` | Retire proposal/design-preview-only entry | Formal builder covers final mechanisms and retains important images/parameters |
| `scripts/revise_relay_scenes.py` | Remove iterative migration from default builds | Load/rebuild final environments directly without upgrading through each revision |

These were review candidates, not completed deletions. No Python import did not
mean no reference: CLI commands, docs, saved commands and snapshots also counted.

### C. Temporary-sounding names that still mattered

- `scripts/diagnose_relay_descent.py` was imported by final-record review/user endpoint checks. Move reusable read-only loading into the family module before making a thin CLI/retiring a name.
- `relay_contact_escape.py`, `relay_user_goal_policy.py`, `relay_donor_staging.py`, `relay_observation_state.py` retained real corrections; `install()` alone did not justify deletion.
- `relay_live_recovery.py` owned typed recovery, provenance, IDs and uncertainty, rather than useless logs. Consolidation had to retain those constraints.
- `rigid_relay.py` still built final L2/L3 rings/springs; an early filename did not make the behavior obsolete.
- `relay_oracle.py` remained referenced by old suite verification/calibration. The family branch could not unilaterally remove shared historical support.

### D. Keep old scenes/generated data until dependencies are removed

R17 built from R16; R16 used 8/16-arm R13 and 12-arm R15 sources. Nine defaults
loaded 3 L1 and 6 R17 scenes directly; nondefault did not mean dependency-free.
Old compiled-physics/workstation registries still supported identity checks,
so large JSON files were not automatically disposable.

A later self-contained default could build from final parameters alone. Only
after removing chained-upgrade/test/doc dependencies could unused versions leave
active inputs. Archive exact sources, licenses/assets and hashes independently
first; Git does not preserve ignored assets. Shared-baseline environment cleanup
belonged to the main session, avoiding broad Relay deletion conflicts.

## 6. Consolidate actual final defaults

### 6.1 Rules and guidance

Replace layered base/R16/R17/50mm-addendum explanations with one complete task
specification: equipment, static layout, goal, handoff/allowed contacts/stacking/
near-table release, 50mm edge tolerance, actual release/landing and violations/
recovery. Do not add velocity/stillness gates or treat Oracle template centers
as targets. The 20/30mm release discrepancy required actual code alignment,
not merely deleting contradictory prose. Parameters express nine-case variation;
task/public-task/evaluator share one authority.

Public inputs contain final task facts, not version history, search traces,
repair IDs or Oracle answers. Old versions/reports retain their own semantics.

### 6.2 Default code path

- Select one Relay entry with explicit family catalog, tracked configuration and actual model. Do not implicitly load `runs/oracle/relay-key-units-20261025-213449/inputs/harness.json`.
- The nine-case entry called the live runner but did not default-enable pipeline and related paths. Final recovery installs were not all connected. Declare the intended default and run static/local regressions; a successful hot-patched world did not prove nine cases reproducible from HEAD.
- Integrate verified corrections into normal family calls, replacing layered `_before_*`/revision installers. Retain frozen hot-load source/acks as evidence without deleting useful behavior.
- Keep module paths and consolidate calls/functions before broad renaming/directory changes.
- Obsoleting an implementation was insufficient to delete its tests. Retain regression coverage for the underlying risk; do not manufacture green results by removing failures. Preserve honest scope of resource-missing tests.

### 6.3 Documentation entries

Proposed concise active guidance:

1. `docs/relay.md`: task facts, nine-case selection, default entry, evidence index and explicit unfinished work.
2. Existing `docs/relay-recorded-video.md`: motion, editing, Factory migration and actual capabilities.
3. One merge handoff: shared patches/conflicts, important data/path migration and GPT readiness gaps.

Long continuation/compact notes and R8/R9/R11 evolution would move into existing
`docs/history/`, retaining full contents/traceable references before shortening
active navigation. Stop prepending successive latest updates. Other families'
shared README/architecture status was not this branch's authority; supply an
accurate Relay summary for main integration. These paths were proposals, not
newly created/moved documents in this round.

## 7. Main-session handoff

- Independently mergeable final Relay definitions/modules/tests/evidence index and explicit retired-file list.
- Separate shared changes: v2 projection/readiness/Relay evaluation, shared catalogs and Factory playback interfaces.
- Semantic resolution of Relay/Mosaic `motion_edit.py`, same-schema/different-meaning and test-name collisions.
- Independent station edit clocks and prolonged useless passive-oscillation removal remained pending; final-state holding was then agreed. Retain all source times/frames/cut boundaries instead of asking main to infer stillness from video again.
- Preserve exact Factory source replacement, material/resource/texture provenance and near/far/camera capability. Cleanup must not discard assets/licenses/references needed for later detail.
- Robo Factory wall-lettering removal, fixed-baseline render-cost comparison, 30fps, family-specific speeds and aerial demos were later main-session work, not global changes here.
- Requested Codex 400k context/350k automatic compaction concerned host settings, not Relay merge files. This round neither changed nor claimed active repository configuration for them.

## 8. Proposed order and acceptance

1. Protect/index original evidence, assets, source snapshots, session provenance and references; repair dependencies that worktree removal would break, retaining hashes/history.
2. Consolidate final rules/default config/entry/verified corrections and complete static/read-only family checks.
3. Retire replaced scripts, duplicate declarations and ineffective installer layers, updating references/tests.
4. Keep active guidance about final state, archive history and supply a concise main-session handoff.
5. Only then remove confirmed unreferenced reproducible caches/derived copies; do not destructively reduce important data.

Acceptance required readable nine-case frozen sources/records, unchanged important
media/edit hashes, no implicit old-run default dependencies, matching rules/
implementation, unchanged historical/assisted classification, passing family
regressions, separate shared patches and replay independent of retiring worktrees.
Pure cache deletion needed no extra tests; rule/loading/behavior consolidation
needed meaningful regressions.

The plan reduced receiving-session decisions/conflicts; fewer files alone did
not establish correct cleanup.
