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
`runs/engineering/main-integration-oracle-final-20261102/`. The optional local
delivery contains `legacy-test-fixtures-v2.tar.gz` and
`legacy-test-fixtures-v2.json`. It contains original ignored test inputs, not
new task qualification or native sessions. Its 43,678 files are pinned by
individual SHA-256 checksums. The archive checksum is
`4ba71cce3f56ee72e8820f11ef885e4a773744e24156c91b0a9dc7b68e6f5f00`.
The manifest checksum, supplied independently of its contents, is
`31dca637c84c17a90fa6547192ac41292c4ff2814f4158be9657824314acc7cf`.

Given a copy of this separately supplied bundle, install it into a checkout:

```sh
python3 scripts/install_historical_fixtures.py \
  --archive /path/to/legacy-test-fixtures-v2.tar.gz \
  --manifest /path/to/legacy-test-fixtures-v2.json \
  --manifest-sha256 31dca637c84c17a90fa6547192ac41292c4ff2814f4158be9657824314acc7cf \
  --report runs/engineering/historical-fixture-install.json
```

This standard-library installer verifies the archive and every member before
installing any fixture, rejects tracked source destinations, links outside the
bundle and paths outside the historical fixture roots, and preserves existing
files. An existing different file is an error; an identical file is reused.
Interrupted installation can be retried. Shared content links only newly staged
copies, never the supplied original recordings or an existing fixture. Extraction
reads the archive sequentially, including hardlinks, to avoid repeatedly
decompressing the large bundle.

This is an explicit optional development bundle, not an automatic download in
the ordinary policy bootstrap. Public distribution of this separate bundle
remains a delivery gate. Do not claim that the policy download alone reproduces
full historical discovery in a fresh clone.

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
