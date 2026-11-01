#!/usr/bin/env bash
# Invoked by scripts.factory_server submit; no account or site-specific paths.
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:?Submit from the checkout root}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
python="${RF_FACTORY_PYTHON:-$PWD/.venv/bin/python}"
scratch="${SLURM_TMPDIR:-${TMPDIR:-/tmp}}/robofrontier-factory-${SLURM_JOB_ID:?}"
mkdir -p "$scratch"
exec "$python" -m scripts.factory_server run "$@" --index "${SLURM_ARRAY_TASK_ID:?}" --scratch "$scratch"
