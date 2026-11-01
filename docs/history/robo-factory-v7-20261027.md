# Historical Factory presentation and rendering

This archived record describes V7: a 55×50 m building with four zones and
36 tables. Configuration: `configs/backgrounds/robo_factory.json`; layout input:
`configs/suites/frontier-current-oracle.json`; scene:
`outputs/robo-factory/v7-workstations/scene.xml`. The offline presentation had
no physical degrees of freedom or actuators. V6 and earlier designs remain in
the [historical notes](robo-factory-before-integration-20261027.md).
Current delivery status is tracked separately in the development acceptance ledger.

## Sources, edits and independent loops

`configs/task_families/current.json` bound each table to its frozen scene,
recording and edit. Playback speeds were Transport 20x, Mosaic 30x, Relay 20x
and Dial 10x; output was 30fps from original 60Hz recordings. Each station
independently skipped its own unused intervals, then returned to its original
start and looped. Loop reset restored initial RGBA before accumulating the
cycle's appearance events. All stations updated before one Factory FK commit
and one render per frame. The latest 2026-10-27 requirement superseded the old
handoff's instruction to stop once all stations finished.

The new `robofrontier.station-edit.v2` tables were in
`outputs/robo-factory/source-edits-v3-20261027/`. Above the historical family
edits, they reviewed stillness, micro-jitter and repeated passive oscillation
with 2/8/32-second windows, protecting directed slow movement, continuous
rotation and source context near actions and result/violation/failure/recovery/
appearance events. New tables bound selection, source stream and semantic-log
hashes. Original streams, edits and videos were unchanged. Motion classification
used 10Hz review while source selection retained original 60Hz indices. This
neither measured contact force nor made presentation frame removal evidence
of physical success.

Stations used rigid translation and horizontal rotation. Arms and payloads were
not scaled; no action, IK or physics integration ran. The original Transport
Oracle was R13, with a tabletop-hole display scale of 0.5. GPT's R14 already had
half-sized holes and used scale 1. Display edits and source physics geometry
were recorded separately to avoid halving twice.

## Appearance and cameras

The four walls, roof, structural beams, windows/doors, zone text, original tables
and camera capabilities were retained; north-wall ROBO FACTORY lettering was
removed. Additions included under-table service connections, cable trays,
control boxes and power units; wall-side compressors, cabinets and pipes;
bins and bollards; and supply carts at unused zone edges. Equipment avoided
planned stations and aisles, without claiming all transport-pose swept volumes
were verified. Shared meshes, reused materials/textures and static batching
remained. Builds used assets within their output, leaving original asset
folders unchanged.

`camera-shots.json` opened with a 6-second overview and a 6-second small corner
orbit, then visited Transport→Mosaic→Relay→Dial, filming each scale in
L1→L2→L3 order. Camera clocks were independent of station source clocks. Fixed
cameras and custom edits were available. This was a filming foundation; a full
narration, subtitles and finished movie had not yet been made at that date.

## Historical build, view and export

Run from the repository root, always using new output directories:

```sh
.venv/bin/python -m scripts.factory build --output outputs/robo-factory/my-factory
.venv/bin/python -m scripts.factory view
.venv/bin/python -m scripts.factory video --duration 12 --output outputs/robo-factory/my-preview
```

`--scene` selected another scene, `--families` selected families and `--camera`
selected tour or original camera presets. The viewer supported roaming, pan,
zoom, top view and cutaway on all sides. Interactive refresh was capped at
15fps, sampling a 30fps timeline. Export used fixed 30fps, required duration,
wrote per-frame source mappings and verified complete decoding.

Interactive Filament previews still had large-scene shadow/aliasing and native
arena-fallback warnings. Production export used Cycles:

```sh
.venv/bin/python -m scripts.export_factory_blender --scene outputs/robo-factory/v7-workstations/scene.xml --output outputs/robo-factory/my-blender
.venv/bin/python -m scripts.factory poses --duration 12 --camera tour --output outputs/robo-factory/my-poses
/Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/render_factory_blender.py -- --asset outputs/robo-factory/my-blender --animation outputs/robo-factory/my-poses/animation.json --output outputs/robo-factory/my-cycles --samples 48
```

Cycles reused scene, meshes, materials and persistent render data, updating
source-bound poses, appearance and cameras per frame. State files and source
mappings were hash-verified, and original materials were restored after color
changes. Float visualization conversion had about 1 micrometer position error.
This was a visualization export, without establishing Isaac/USD dynamics equivalence.

## Recorded checks

- All 36 tables passed independent clocks, long jumps, reverse seeking, individual loop boundaries and RGBA reset checks.
- The 36-table, 4-second, 120-frame Filament preview encoded and fully decoded. A 15-frame Cycles animation was also actually rendered.
- The source table matched all 36 source selections checked in the preceding render. The v3 protection for slow progress within oscillation did not change this batch's actual frame selection. The new release preview was in `outputs/robo-factory/v7-release-preview/`.
- The building had 33042 visual geoms and 786 reused meshes, retaining the correct sources for all 36 tables.
- Five-camera 1280×720 benchmarks, alternating for three rounds, measured 9%–22% higher static-frame time and peak RSS of about 1756→1805MiB. This included both station source updates and appearance additions; the entire difference cannot be attributed to the background.
- Cycles material previews, animation and per-frame source mappings were in `outputs/robo-factory/v7-cycles*`; raw performance data was in `outputs/robo-factory/v7-performance/`. Offline export speed was not real-time 30fps.
