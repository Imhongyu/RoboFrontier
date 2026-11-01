# Unified main integration

This document tracks implementation gates. It is not a statement that all gates
have passed. Work is isolated on `integration/unified-main`; existing worktrees
and `main` remain intact until the integration is reviewed.

## Product

**RoboFrontier: Benchmarking How LLM Agents Organize, Communicate, and Collaborate
in a Multi-Robot World**

Confirmed first author: **Changxuan Fan**, **Hong Kong University of Science and
Technology**. The full author list, author order beyond first author, copyright
holder, publication status, DOI, and paper URL are not finalized. Do not infer
these fields from Git history or the repository owner.

## Sources and provenance

| Source | Pinned source commit | Integration intent |
| --- | --- | --- |
| Main | `c8b41371fbc49aa014b2d36332c43529b3c6d4f4` | Existing shared benchmark |
| Codex | `b518bc164eb1cdcd5766435a6e49345a7f880557` | Native Codex policy engine and protocol fixes |
| Factory server | `d1e1b3d7e274fb001c1576f9876239601fc72647` | Portable assets, frozen-source replay and Slurm rendering; already contains the pinned Codex source |
| Luna | `907f4807eb43644e9db4621c5305fa3300017830` | CPU rendering, Docker, providers and command-line operation |
| Multi-topology | `c1d05e3426468322fc5e89141e0cb5f49e87a925` | Four topology modes and communication measurement |
| Claude | `3b3fd08e8220d486b004c9dc2d764f5ba0d27d8b` | Native Claude Code sessions, MCP and recovery |
| Oracle | `a0249a6977e8137442a3d1f323be903a64c3f8c9` | Curate validated R14 fixes; do not import R15 experiments as defaults |

## Acceptance gates

- [x] Preserve refs and uncommitted source work outside the integration worktree.
- [x] Fast-forward Codex and Factory server without duplicating their shared history.
- [ ] Integrate Luna, multi-topology and Claude with targeted regression checks.
- [ ] Provide one validated TOML configuration and CLI; resolve defaults once and freeze the effective configuration per run.
- [ ] Launch hosts through one scheduler with a default 0.3-second interval.
- [ ] Isolate task runtime state, verify Codex initialization/authentication, and stage Slurm SQLite state on node-local storage.
- [ ] Preserve shared START, scoring, safe call-ID and stop semantics across native engines.
- [ ] Keep R14 as the Mosaic default; validate recommended physical candidates before publishing changed assets.
- [ ] Verify automatic pinned policy-asset installation from a fresh checkout.
- [ ] Verify old and compressed motion, image references, evidence restore and frozen-source Factory replay.
- [ ] Integrate qualified Oracle functionality without exposing private solutions to policies.
- [ ] Publish English-only current content, task atlas, editable full video project, detailed README and documentation.
- [ ] Exercise CPU, native macOS, NVIDIA/EGL and Slurm paths where hardware is available; record unavailable checks explicitly.
- [ ] Run offline suites and clean-checkout checks; record any remaining paid/hardware qualification separately.
- [ ] Review the integrated branch before publishing or merging it into main.

## Invariants

Task limits are measured from persisted START, normally 86,400 seconds. An
engineering stop is separate and must not silently replace the public task limit.
`ready` queries capability; it does not unlock START. Completion is evaluated by
an independent scorer; process events are reported separately. Dial completion
remains latched on unlock. Adaptive delegation remains optional and dynamic.

New requests receive host-generated IDs. Uncertain physical requests must not be
replayed under new IDs. Collection and archival run only after all writers stop;
source evidence is retained by default. Factory playback uses each recording's
frozen scene and assets, including legacy recordings. A successful restore or
render does not imply that the recorded task succeeded.

## Merge decisions

Luna's offscreen capture and capture timing are retained. Factory server's
array-based diagnostic Factory replay is retained, because it avoids requiring
production Cycles video rendering for pixel/FK comparisons. Luna's additional
call-ID query/uncertain-result tests are retained alongside Codex error tests.
