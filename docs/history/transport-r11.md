# Transport R11: environment and task snapshot

Historical archive. Current specifications/status are in the
[Transport guide](../tasks/transport.md); historical integration is in the
[handoff](../plans/suite-v2/transport-merge-handoff.md).

This revision covered only 4 / 8 / 12 arms × L1/L2/L3, 9 Transport environments.
It created/woke no delegates and started no Oracle, GPT, grasp, handover or
insertion-unit experiments.

## Inputs and versions

- New catalog: `configs/suites/frontier-transport-r11.json`.
- At that date `configs/suites/frontier-v2.json` selected nine Transport R11 and
  27 unchanged R10 scenes out of 36 cases.
- Frozen R10 catalogs, scenes, reports and recordings remained. The earlier
  18/36 full-success result belonged to those R10 inputs, not R11.
- New scenes retained complete models/assets, joint/geometry maps and source
  hashes for matching future recording/Factory reconstruction. Factory layouts,
  old motion migration and Isaac verification were not changed/performed.

## Changes

1. Remove large intermediate staging boxes and fixed staging-point data. Direct
   airborne handover, waiting and safe temporary table placement were permitted
   without prescribed boxes, routes or robot pairings. Final boards remained.
2. Each final target displayed its ordered color/shape: square for cubes, circle
   for cylinders. Markers were 84 mm across, 1.4 times a 60 mm object. A dark
   0.8 mm outline made white markers readable. Painted geometry left physical
   socket openings empty, without noncolliding covers.
3. Boards grew from 110×320 mm to 143×416 mm, 30% along each axis. Thickness
   remained 3 mm at L1 and 32 mm at L2/L3.
4. Keeping centers would overlap adjacent rectangular board corners in the
   four-arm scene. Every scale moved boards/supports 50 mm toward their arm.
   Board-local centers remained 0 and ±100 mm; local tabs/sockets were unchanged.
   Robot mounting, initial stock and orders were unchanged.
5. Order-color markers did not widen acceptance tolerances. The old reference
   depended on fixed staging points and had not been adapted/qualified. Oracle
   routing/parallel algorithms, shared skills, controllers and harness were unchanged.

## Physics changes

Boards retained material density 650 kg/m³. MuJoCo recomputed mass/inertia;
paint was massless and noncolliding. Per-board L2/L3 mass changed approximately
0.7253155→1.2305059 kg; L1 changed 0.06864→0.1160016 kg.
Each scene's `board-physics.json` retained old/new principal inertia, COM and
static estimates.

L3 springs retained Kz=1400 N/m, Cz=45 Ns/m, angular stiffness 0.60 Nm/rad and
angular damping 0.075 Nms/rad, with unchanged travel/limits. Simple F/k estimates
gave approximately 8.62 mm empty-board sag and 12.41 mm carrying three tabbed
cubes, below 18 mm travel. These static estimates did not qualify tilt, contact,
oscillation or actual insertion.

## Checks and previews at that date

- Static compilation, order counts, identity conservation and public task output.
- Compared with R10: unchanged robot/object initial state, object mass, joint
  layout, springs and actuators; unchanged local sockets/final acceptance logic.
- Nonoverlapping board projections inside tabletop support; initial robot/device
  penetration checks.
- Noncolliding paint leaving real socket openings exposed; marker shapes match orders.
- Self-contained assets and pose-export contract retained.

Historical preview: `docs/generated/frontier-v2/transport-r11/index.html`, with
nine top/front/rear sets and board/socket close-ups. These were static checks,
without physics integration or arm commands. Minimum-operation verification and
full parallel planning required separate authorization/work.
