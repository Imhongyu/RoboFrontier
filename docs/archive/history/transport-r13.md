# Transport R13: shorten the board by 20 mm

Historical archive. See the [current Transport guide](../../tasks/transport.md) for
current specifications/status and the [handoff](../plans/suite-v2/transport-merge-handoff.md)
for historical integration. This note preserves that revision's evidence.

Boards in nine Transport environments changed from 143×416 mm to 143×396 mm,
removing 10 mm at each end. Mount centers, target/socket centers, numbering,
84 mm markers and 36 mm marker gaps remained from R12. The remaining marker-to-end
clearance was 36 mm. Thickness, materials, springs, robots and supply were
unchanged; compilation recomputed board mass/inertia.

R12 and earlier environments were retained. The catalog at this date was
`configs/suites/frontier-transport-r13.json`; preview:
`docs/generated/frontier-v2/transport-r13/index.html`.
The dimensional change received static checks and rerendering, without an
Oracle run or arm commands.

Subsequent user-authorized [minimum-operation checks and parallel planning](transport-r13-units.md)
are recorded separately. They did not constitute full-task execution.
