#!/usr/bin/env bash
# Legacy entry: it formerly created active SQLite files on shared storage.
set -euo pipefail
cat >&2 <<'HELP'
This legacy sbatch entry is retired. Use the frozen node-local submission flow
from the Linux login node after configuring robofrontier.toml and completing
an explicitly authorized provider preflight:

  robofrontier --config site.toml slurm-submit --output runs/submissions/BATCH --queue

For CPU rendering, site.toml must select render.device = "cpu" and slurm.gpus = 0.
See docs/slurm.md for storage, status, stop, recovery, and collection details.
No model call or simulation was started by this script.
HELP
exit 2
