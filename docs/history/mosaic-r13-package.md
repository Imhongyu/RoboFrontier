# History: Mosaic R13 review package

This preserves the R13 package's original preparation notes. See the
[task specification](../tasks/mosaic.md) for current rules and the
[merge handoff](../plans/suite-v2/mosaic-merge-handoff.md) for commands/shared work.
Commands below describe the historical workflow. Recheck a delivered package
with `python -m scripts.mosaic check --purpose oracle`. Historical scorer and
playback requirements below do not override later terminal-outcome and looping
requirements documented in the current guides.

At that stage, nine complete Mosaic Oracle runs had passed, totaling 1566 cells.
Original scenes, execution records and success evidence were unchanged. The
package organized public static specifications, completion rules and operating
guidance for the integrated GPT preparation chain. **It was a review package,
not a GPT run with execution gates already unlocked.**

## Sole family entry at that stage

`configs/task_families/mosaic/r13.json` explicitly bound the nine cases in
`configs/suites/frontier-mosaic-r13.json`. Generic `v2.cases()` and the old
minimum-policy-batch script could select R10 and were not substitutes.

| Arms | Grid | Goal cells per level | Frozen environment outer tabletop dimensions, m |
| --- | --- | ---: | --- |
| 4 | 6×12 | 72 | 2.465×2.66175 |
| 6 | 9×18 | 162 | 3.0725×3.41125 |
| 8 | 12×24 | 288 | 3.68×3.3435 |

All tables were 0.8m high. Each generated public task.json supplied its own bases,
orientations, actual workspaces and static camera parameters. The outer table
outline must be interpreted with L1 pocket geometry, rather than as an unbroken
support surface. Coordinates from another experiment need not be memorized.

## Pattern, supplies and levels

Block sides were 60mm, pitch 81mm. Colors were cream, navy, coral and sage.
The pattern and generated reference were already world-north-up: first row +Y,
first column −X. Earlier descriptions of rotating the full image 90 degrees
or mirroring 9×18 described reference preparation. GPT should use the provided
finished reference without repeating that transformation. Background-color cells
also counted as targets.

Supply labels and initial color counts created no exclusive ownership. Goals
matched colors, without requiring blocks from a fixed source. Assignment,
sequence, handoffs and temporary storage could depend on reachability, grasp
access, interference and handling counts. There were no fixed robot pairs,
mandatory routes or color order.

- L1: physical square pockets, 80mm clear opening and 20mm deep. The full rotated block footprint had to fit and seat on the bottom.
- L2: 3mm red printed lines, without a physical grid locking blocks in place.
- L3: no visible grid; the target and declared assembly frame still applied.

## Completion under the historical scorer

Machine-readable values came from registry completion. Tests directly called
the existing private scorer at these boundaries. That package change did not
modify the original scorer.

| Condition | Criterion |
| --- | --- |
| Coverage | A distinct correctly colored block per cell; all cells simultaneously qualified at the end |
| Release | No block/robot-geometry contact at distance ≤0.2mm; sending open alone was insufficient |
| Stability | Linear speed strictly <0.01m/s and angular speed strictly <0.1rad/s for 1 continuous simulation second |
| Orientation | Block/station axis error ≤8 degrees, allowing the block's own 90-degree symmetry |
| L2/L3 position | Center XY Euclidean error ≤5mm and center Z error ≤3mm |
| L1 position | Full rotated footprint inside the clear pocket with 0.3mm margin; bottom-height error ≤0.8mm and seating contact ≤0.2mm |
| Process | All final cells qualified and no process violations; valid recovery could continue in the same world without deleting failure history |

L1 did not require a center within 5mm. Center estimates, grasp offsets, opening
clearance and safe withdrawal were separate judgments. Later contact could
invalidate finished cells, requiring observation. Acceptance tolerances differed
from command terminal thresholds; READY/tool feedback remained the source of
actual execution capability.

## Public materials and engineering evidence

The generated `public/` contained only nine task.json files, nine targets,
the Mosaic task prompt and a standalone Mosaic skill. Public tasks supplied
static table/block/camera/robot specifications, completion rules, supply totals
and the already-public target matrix. They excluded live object truth, Oracle
goal/object assignment, action sequences, repair recipes and execution snapshots.

`engineering/` retained versions, per-case Oracle/audit/stream/asset hashes and
actual assistance/failure flags for review, rather than policy initial experience.
All 9 frozen harnesses matched servo2 and used pd1000-v1. Scorer sources matched
the selected executions. Source, asset, control or evidence changes invalidated
checks; setting an old task's oracle_verified to true could not repair this.

Shared role prompts, generic robot-collaboration skill, READY/action interfaces
and execution gates were unchanged. The future shared loader had to select public
materials, freeze them into a new run and record hashes. Files could not be
silently added to a sealed old run or misrepresented as an old bounded probe.

## Historical build and check

```sh
python -m scripts.build_mosaic_policy_package \
  --output outputs/policy-packages/mosaic-r13-20261027 \
  --verify-recorded-chunks

python -m scripts.build_mosaic_policy_package \
  --output outputs/policy-packages/mosaic-r13-20261027 --check
```

New output directories had to be absent to protect reviewed inputs. Build/check
created no run, called no model, advanced no physics and changed no source.
Default checks accepted the bound full action audit and verified assets; the
explicit flag additionally checked all original action-chunk checksums. Extra,
missing or changed public files, wrong image orientation/color, private fields
or symlinks even after resealing caused rejection.

## Historical integration work and Factory playback boundary

This work delivered Mosaic-specific materials/checkers only. Shared readiness
registration, public projection extensions, task prompt/skill loading and run
sealing still required common integration; policy_launch_ready=false until then.
GPT model, topology, observations and cost/execution protocol would be frozen
separately. Old pilot/probe deadlines were not inherited.

Mosaic presentation preferred 30x / 30fps from original 60Hz motion. That
preference did not change physical control or select other families' speeds.
Delivered stillness-removal timelines could be reused across backgrounds;
independent station clocks and prolonged obvious task-irrelevant oscillation
classification were separate work, not established by this package.

The then-planned multi-station behavior was independent unused-interval skipping
with one Factory render; earlier finishers held the final assembly, could remain
still and did not loop. Later requirements superseded that endpoint policy.
Continued grasp/support could be useful; pose/force settings were not full
measured contact forces. The recorded public/private boundary also applied to
future unused-interval analysis.

## Private Mosaic motion-review artifacts

```sh
python -m scripts.audit_mosaic_motion_intervals \
  --output runs/engineering/mosaic-motion-review-20261027 --workers 3
```

Parameters were in `configs/task_families/mosaic/motion-review-r13.json`.
Review first protected actual actions, recorded force-holding, progress/pickup/
release and completion events, then inspected remaining long idle windows.
Micro-jitter could become an idle proposal. Obvious repeated object/gripper/joint
oscillation could require review; slow net displacement and non-repeated object
motion stayed. Unknown/failed opening was not assumed to end holding.

Nine-case analysis produced 135 proposed_idle_cut and 5 keep_slow_net_motion
intervals. Three 4-arm cases had no long idle candidates. Actual candidates
contained no review_repeated_*; synthetic oscillation cases checked that branch.
No existing edit/video changed and no zero measured mechanical force was claimed.
Exact source intervals, action/progress protection, hashes and labels stayed in
separate engineering reports, excluded from public tasks.

See the [merge handoff](../plans/suite-v2/mosaic-merge-handoff.md) for shared
integration interfaces and acceptance.
