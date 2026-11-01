# Transport R12: increase adjacent target spacing by 20 mm

Historical archive. Use the [current Transport guide](../tasks/transport.md) for
current specifications/status and the [handoff](../plans/suite-v2/transport-merge-handoff.md)
for the historical integration. This note preserves that revision's evidence.

Only board-target spacing changed, followed by static rendering of nine
Transport scenes. No Oracle was run.

- Marker side/diameter remained 84 mm.
- Adjacent centers changed from 100 to 120 mm, increasing clear edge spacing
  from 16 to 36 mm.
- Physical L2/L3 sockets, numbering and target coordinates moved with the
  markers; hole dimensions and depth were unchanged.
- The board remained 143×416 mm, with 46 mm between end markers and board ends.
- Board mounting, robots, supply, orders, springs, materials and acceptance
  remained from [R11](transport-r11.md). Compilation recomputed mass/inertia.
- R11 scenes/previews were retained. At this date the active catalog selected
  R12 Transport and 27 unchanged R10 cases:
  `configs/suites/frontier-transport-r12.json`.

Historical preview: `docs/generated/frontier-v2/transport-r12/index.html`.
Only model compilation, static contact/support checks and rendering were done;
there were no arm commands or physical integration.
