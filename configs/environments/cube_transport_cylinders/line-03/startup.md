# Legacy line-03 startup guide (rules v4)

Open initial_top_image from startup.json in this directory and identify the labelled bases.
This guide and preview describe initialization. After execution, use fresh RGB and robot observations.

Robot IDs match the uppercase base labels. World +X is east, +Y north and +Z up; top views show north above and east right.
Adjacent stations: A—B, B—C.

| Station / robot_id | Mounting side | Initial stock (three items each) |
| --- | --- | --- |
| A | linear layout | red cube (a) |
| B | linear layout | blue cube (b) |
| C | linear layout | green cube (c) |

Read the assigned seed task for the three slot color/shape requirements. Matching items are interchangeable; slot numbers do not prescribe action order.
Use adjacent-station handovers. The policy chooses routes, allocation, action order and parallel execution.

There are 9 cameras: global and global_side are opposing global oblique views, top is overhead, and each station also has <ID>_front and <ID>_side.
Local views face the assigned station and may include neighbors. Choose views as needed; startup.json records fixed camera geometry.
Label runtime images with camera name and simulation time. Static previews do not replace runtime observations.

This is an offline asset package, not a bound runtime. This guide provides no action entry point.
