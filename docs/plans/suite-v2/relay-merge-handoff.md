# Relay branch merge handoff

This is the dated family-branch handoff. Pending work describes that stage;
current integrated progress is in the [acceptance ledger](../../development/unified-main.md).
The then-planned hold-final playback was later superseded by independent loops.
Current task/default entries are in [docs/relay.md](../../relay.md), without
requiring reconstruction from dozens of continuation logs. Full history remains
in `docs/history/`.

## Completed family cleanup

- Added a Relay-specific nine-case catalog using the repository's formal servo2 settings, without implicit old-run configuration dependencies.
- `relay_contract.py` became the single rule authority; all nine tasks/public tasks matched final guidance. Relay evaluation included 50mm tolerance, permitted stacking, low 30mm release and no extra stillness/velocity gate. Only explicitly versioned tasks used these rules; old frozen records retained original semantics/scores.
- Goal handling, bounded exit, sender parking and exact-state corrections became normal function calls, replacing 4 install wrappers.
- Retired 4 scripts: old timed batch, one-off rule appender, old progress movie and mechanism-proposal preview. Original bytes remained in `runs/engineering/relay-cleanup-20261027/retired/`.
- Renamed analysis to `analyze_relay_motion.py`, producing edit tables only; the sole new video entry remained 20x / 30fps.
- Renamed Relay editing/tests to `relay_motion_edit.py` / `test_relay_motion_edit.py`, avoiding Mosaic's generic filenames. New schema: `robofrontier.relay-motion-edit.v1`. Delivered old packages stayed unchanged. Readers must validate Relay trajectory fields, not just old v1 text.
- Replaced 16 worktree dependency links for key executors in two batches with durable dependency archives; retained 21 related scenes. `manifest.json` recorded old/new targets and original hashes. Original reports/frozen Python bytes were unchanged.
- Moved long continuation notes to `docs/history/` and left short navigation entries. Scene-evolution dependencies and other families' directories were retained.

## Merge scope

Independent changes: Relay contracts, task/public task files, catalog,
reference/recovery/edit modules, tests and current guidance.

Shared changes requiring main-session review:

| File | Family change and integration requirement |
| --- | --- |
| `suite/evaluate_v2.py` | Read explicit rule parameters for Relay only; preserve other families and old-task semantics |
| `suite/v2.py`, `rigid_relay.py` | Existing Relay version/public-projection/build changes; retain other branches' new catalogs |
| `factory_workstations.py` | Exact source binding and vectorized read-only placement; integrate with other family players |
| `.gitignore` | Ignore only local/generated data; do not remove untracked materials |

Do not replace shared catalogs or choose entire files with ours/theirs. Each
worktree's latest family catalog is authoritative; shared R10 directories do
not describe other families' current state.

## Work remaining before formal GPT at that stage

1. Integrate final task/Prompt/Skill inputs/loading across all four families. Readiness must bind rules, control, source and evidence. Relay remained `environment_preview_only`; do not bulk-flip oracle_verified or inherit an old bounded-probe budget.
2. Regress generic harness, roles/concurrency/freezing/observations. This cleanup neither changed the generic controller nor started GPT. Generic `freeze_executor` could still create worktree aliases; this work repaired two selected historical batches. Future durable packaging needed shared integration.
3. Adapt family edit formats. Mosaic's original-frame references differ from Relay's complete derived trajectory package. Avoiding filename conflicts does not eliminate semantic adaptation.
4. Implement same-screen multi-table playback: sample each table using its own speed/edit clock, update all, then render once; hold completion state. At that point only individual videos existed, without claimed nine-/36-table combined replay.
5. Extend prolonged no-progress main-beam/spring oscillation review while retaining genuine release, drop and recovery evidence. Existing 960-interval review/timelines remained reusable; not all passive motion should be removed.
6. Integrate Factory detail, exact station sources, Robo Factory wall-lettering removal, near/far camera demos and cost comparisons. Retain assets, provenance and licenses. Context/compact settings belong to the Codex host, rather than claimed repository features.

## Data retention

`runs/`, `outputs/`, `vendor/` and `.venv/` were shared links outside Git commits.
Retain both original motion batches, completion cutoffs, user/native reports,
assistance labels, control extensions, request results and hashes. The historical
user acceptance of 9/9 was neither native original-scoring 9/9 nor a new autonomous
Oracle result from cleaned code.

Each consolidated video directory directly held 9 MP4s:
`outputs/oracle/relay-nine-videos-20x-20261027/` and
`outputs/robo-factory/relay-nine-videos-20x-20261027/`.
Edited motion/full frozen sources were in
`outputs/oracle/relay-edited-tracks-20261027/`. Original packages retained source
frame/time, edit time, cut boundaries, appearance events and hashes, without
requiring stillness reconstruction from video.

Runtime dependency archives remained in shared
`runs/engineering/relay-cleanup-20261027/`. They support review of the selected
Relay inputs, rather than providing a complete repository for every other
family's historical builds. New physical trials still require explicit user
authorization and independent directories, without reusing old IDs/control calls.

The recorded 164 Relay regressions and 40 related checks passed, with overlap,
alongside read-only checks of nine inputs. Full decoding/hashes passed for
18 videos, hashes for nine edited trajectories and checksums for 43,032 evidence
files. The 45 geometry/physics/registry files matched pre-cleanup bytes.
Removal was limited to 95 local pyc cache files, about 1.8MiB. This did not claim
all historical project tests passed; missing/external textures in some non-Relay
environments remained main-session work.

Results/removal list: `runs/engineering/relay-cleanup-20261027/cleanup-result.json`.
