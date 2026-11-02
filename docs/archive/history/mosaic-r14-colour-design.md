# History: Mosaic R14 supply-color design

This preserves the color design and checks. See the [task specification](../../tasks/mosaic.md)
for current rules and the [merge handoff](../plans/suite-v2/mosaic-merge-handoff.md)
for current commands and shared work. Implementation statements below describe
the design stage, rather than replacing the current integration ledger.

R14 was intended for subsequent GPT tasks; historical Oracle videos and later
Factory Oracle replay retained R13. Only initial block colors and corresponding
RGB changed. Across nine tasks, block positions/sizes, robot bases, initial
joints, table, target, pockets/printed lines, cameras and physics were unchanged.
Color totals still exactly matched the target. L1/L2/L3 at each scale shared
supply colors.

The latest user request was nearby supply matching nearby target colors at
about 60%–80%, rather than a hard 80% threshold. The design used 70%, rounding
block counts upward. Each arm had sampled same-arm pickup/placement geometry
for distinct same-color cells for 70.0%–72.7% of its nearest supplies.
Across nine cases: 1119/1566 pairs, 71.46%.

| Scale, each applying to L1/L2/L3 | Verified local pairs / nearest supplies per arm |
| --- | --- |
| 4 arms | A13/18, B13/18, C13/18, D13/18 |
| 6 arms | A14/20, B23/32, C21/29, D15/21, E23/32, F20/28 |
| 8 arms | A23/32, B21/29, C30/42, D29/41, E24/33, F21/30, G28/40, H29/41 |

Nearest supply was assigned by world-XY distance to the base, breaking ties by
robot ID. This neither used historical source labels nor created ownership.
A local pair required the same robot to have sampled grasp/lift evidence for
the corresponding original R13 supply and sampled approach/open/withdrawal
evidence for the target. Distinct supplies matched distinct target cells;
one cell was not counted as available for multiple blocks.

Assigning targets strictly to their nearest bases gave some end arms at the
8-arm scale only 24 cells but 41 nearby blocks. Candidates therefore included
same-side neighbors with at most 240mm extra distance relative to the closest
base and at most 860mm robot-to-cell-center XY distance. These distances only
screened candidates; **they did not replace actual geometry evidence**.
Every selected extra cell ran the existing Coverage sampler. L2/L3 reused
evidence only when complete compiled physics/initial-state identities matched.
Engineering scratch neither advanced dynamics nor altered the live scene.

Allocation used minimum-cost one-to-one matching, preferring the nearest target
region and adjacent-arm regions for cross-zone work. Specific supply locations
then used transport distance and a small preference for original colors.
This was not a global time-optimal plan or proof of collision-free concurrency.
Full loaded paths connecting pickup and placement, grasp/withdrawal after dense
completion, actual stable grasp/placement and parallel efficiency still required
observation in GPT runs.

The remaining roughly three tenths left room for cross-zone collaboration;
**it did not prescribe a handoff count**. Same-color blocks may be reassigned,
and GPT may grasp directly across zones, using fewer handoffs. Engineering
pairs, joint witnesses and ratios were excluded from GPT public inputs.
Policies choose their own assignments, sequence and paths.

## Version entries

- `configs/task_families/mosaic/selection.json` distinguishes purposes.
- `configs/task_families/mosaic/r14.json` binds the revised nine-case assets and private design evidence for later GPT trials.
- `configs/suites/frontier-mosaic-r14.json` lists all nine environment directories.
- `prompts/tasks/mosaic-r14.md` supplies revised public guidance, retaining the geometry/operation-generic mosaic-r13 skill.
- `configs/task_families/mosaic/r13.json` retains original Oracle and Factory replay bindings. Old actions must not be applied to R14 colors and presented as revised Oracle success.

At this historical stage, selection was a family declaration not automatically
read by the shared runner. Shared gating, loading and sealing were integration
work listed in the handoff. Falling back to generic R10 was unacceptable, as was
setting R14 oracle_verified=true merely because geometry matched. No revised
Oracle or GPT trial was started.

## Historical generation and checks

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m scripts.build_mosaic_local_colors \
  --arms 4 --engineering runs/engineering/mosaic-local-colours-r14-20261027
# Use --arms 6 and --arms 8 for the other scales.
python -m scripts.build_mosaic_local_colors \
  --engineering runs/engineering/mosaic-local-colours-r14-20261027 \
  --output outputs/policy-packages/mosaic-r14-local-colours-20261027
python -m scripts.check_mosaic_local_colors \
  --engineering runs/engineering/mosaic-local-colours-r14-20261027 \
  --package outputs/policy-packages/mosaic-r14-local-colours-20261027
```

Builds refused to overwrite existing R14 directories or output packages.
Review read existing inputs without generating actions. Checks covered complete
XML equality after removing supply RGBA, compiled physics/initial-state equality,
color-count conservation, source evidence for each local pair, exclusion of
private pairs from public tasks, nine color diagrams and 18 initial-state images.
SHA values of 496 historical R13 assets, task-package files, videos and timelines
remained unchanged. The 29 related tests passed.

## Review artifacts

Main directory: `outputs/policy-packages/mosaic-r14-local-colours-20261027/`.
Its explanatory Markdown file distinguishes the two versions.
`previews/index.html` contains all nine galleries.
`previews/all-nine-colour-layouts.jpg` is the combined view; center cells are a
target illustration, not already-completed initialization. Each case's `top.png`
and `global.png` are actual MuJoCo initial-state images.
`previews/before-after-colours.jpg` compares original/revised supplies at three scales.
