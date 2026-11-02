#!/usr/bin/env bash
# Legacy entry: active SQLite and temporary state must not use the shared checkout.
set -euo pipefail
cat >&2 <<'HELP'
This legacy sbatch entry is retired. Use the frozen node-local submission flow
from the Linux login node. Copy configs/examples/luna-l3-cpu.toml to an untracked
site TOML, review the cluster resource settings, and inspect the four-task plan:

  robofrontier --config l3-cpu-site.toml plan

Perform an explicitly authorized provider preflight separately, then submit:

  robofrontier --config l3-cpu-site.toml slurm-submit --output runs/submissions/L3_BATCH --queue

The example selects maximum-arm Level 3 tasks, parallel 4, Luna high/adaptive,
CPU rendering, and a 3600-second task limit from each persisted START.
See docs/engines/codex.md and docs/slurm.md for storage, stop and collection details.
No model call or simulation was started by this script.
HELP
exit 2
