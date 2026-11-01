# Engineering command index

Use the unified `robofrontier` command for new experiments. Start with the root
[README](../README.md), [configuration guide](../docs/unified-cli.md), and
[component map](../docs/claude-codex-parity.md). The unified CLI selects a native
Codex or Claude runner; it does not turn one engine into the other.

For a lower-level module, run `.venv/bin/python -m scripts.MODULE` from the
repository root. Keep existing module names when reproducing historical evidence.

| Entry | Purpose and scope |
| --- | --- |
| `robofrontier config/plan/bootstrap/prepare` | Resolve public TOML settings, select current released tasks, restore pinned assets, and freeze new inputs without calling a model |
| `robofrontier doctor/preflight/run/status/stop` | Check local prerequisites; explicitly authorize provider checks; execute and monitor the selected native engine; request an orderly stop |
| `robofrontier collect/archive/extract` | Collect stopped native sessions and task evidence, create a verified deduplicated ZIP, and verify/extract it |
| `robofrontier container` | Build committed source and execute with persistent local Docker volumes |
| `robofrontier slurm-submit` | Freeze a submission and optionally queue node-local execution with verified stage-out |
| `robofrontier factory/oracle` | Replay frozen motion in Factory, or explicitly run privileged reference execution; neither is a policy benchmark launch |
| `benchmark models/plan/preflight/prepare/run/status/stop` | Native Codex interface retained for compatibility, with model selection, task filters, provider checks, concurrency, and START-based task limits |
| `claude_benchmark` | Native Claude draft, provider-check, and explicitly unqualified engineering interface; see the [Claude guide](../docs/claude-handoff.md) |
| `benchmark_handoff doctor/init-env/assets/restore` | Inspect handoff prerequisites, create a private local environment file, and export/restore assets with SHA verification |
| `check_codex_cli` | Exercise the real Codex CLI's tools, images, and forks against a local Responses stub, without external model calls |
| `curate_repository` | Plan and verify data cleanup while protecting frozen source recordings |
| `tasks list/check/prepare/prepare-batch` | Audit current release selection and inputs, or use the retained lower-level preparation interface |
| `factory build/video/poses` | Low-level scene construction, public pose export, and Cycles video; requires an explicitly matching source |
| `factory_server setup/doctor/prepare/submit/run/status/import-motion/project/edit-video` | Restore independent R14 Factory data, prepare Linux render arrays, import motion, edit source-bound camera/subtitle projects and verify movies; see the [server guide](../docs/factory-server.md) and [editorial guide](../docs/factory-editorial.md) |
| `restore_scene_assets` | Restore ignored historical scene assets by their original SHA; refuse to overwrite drifted files |
| `check_harness` | Run the offline Python, JavaScript, documentation, and protocol regression inventory; historical fixtures may require separate assets |
| `check_oracle_preservation` | Check the preservation manifest and frozen Oracle source bindings |
| `export_factory_blender`, `render_factory_blender` | Export and render Cycles scenes, reuse fixed-camera frames, and compare sampled source poses |
| `check_factory_blender_instances` | Check actual Blender instance geometry, motion, and independent color changes |
| `build_task_atlas` | Build, verify, or package the public 36-task visual atlas without policy inference |

`create_pipeline_run` remains a Legacy interface for historical tasks and
explicit configurations. `meta_dispatcher.js` executes frozen Meta operations;
it is not an autonomous task-solving agent.

Family builders, audits, and Oracle scripts keep their historical names for
provenance, tests, and reproducibility. A name containing `oracle`, `commission`,
or `probe` does not make that script a scored policy entry or select the current
released task version.

`archive_worktree_dependencies` preserves migration receipts.
`prepare_factory_edits` creates new source edit versions without modifying the
original recording or previous edits. Do not modify frozen inputs or delete
source evidence merely to make a preparation or archive check pass.
