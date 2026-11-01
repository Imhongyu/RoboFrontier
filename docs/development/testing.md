# Development checks and optional historical fixtures

Install the locked Python environment and Node.js before running these checks.
The selected native CLIs are needed only by tests that explicitly exercise them.
See the [acceptance ledger](unified-main.md) for exact results and limitations.

## Protocol checks

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m scripts.check_harness \
  --protocol-only --report runs/engineering/protocol.json
```

This group prohibits MuJoCo model creation and physical stepping. It tests
synthetic task/runtime contracts, source-compatibility guards, private scoring,
frozen inputs, recovery boundaries, JavaScript and portable documentation links.
It starts no native policy session and calls no model/provider. Its passing
result does not qualify actual robot dynamics, native provider behavior or
multi-agent task solving.

## Full local discovery

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m scripts.check_harness \
  --report runs/engineering/full.json
```

Full discovery additionally exercises real robot/contact physics and media
codecs. When installed, native CLIs may communicate with isolated synthetic
loopback model endpoints. These are test sessions, not paid provider inference
or measured model-solving runs. Existing explicit physical/provider qualification
switches remain separate; inspect skipped tests rather than counting them as
executed qualifications.

The ordinary policy bootstrap restores the current 36-case policy inputs. Full
historical discovery also reads older scene assets/previews, the original
source-preservation receipt, selected closed Oracle reports/streams and their
frozen harness/evaluator source. They are ignored data, not Git source. Missing
fixtures are errors; do not regenerate approximate images, rewrite old reports,
change hashes or relabel a historical success as current physics qualification.

The local 2026-11-02 passing discovery used independently copied historical
fixtures from the preserved primary checkout. Scene XML identities and pinned
asset/report/source hashes were verified, and original files were retained.
The restoration receipts are under
`runs/engineering/main-integration-oracle-final-20261102/`. A portable installer
for this additional development fixture set is still a delivery gate. Do not
claim that the ordinary policy download alone reproduces full historical
discovery in a fresh clone.

## Filesystems and platform scope

Keep test databases, native homes, temporary executables and fixture outputs on
the same local operating-system filesystem. In Linux containers, use writable
local temporary directories for legacy fixture generation and Python bytecode;
read-only source alone is not a writable test environment. Do not open active
SQLite databases across a Docker/host boundary.

An existing dependency image with current source mounted or copied into it is
distinct from a newly built image containing that source. Linux CPU/Mesa checks
do not qualify NVIDIA/EGL, OPTIX, x86_64, real Slurm allocations, subscription
refresh or 36-task resource capacity. Keep those boundaries in every receipt.
