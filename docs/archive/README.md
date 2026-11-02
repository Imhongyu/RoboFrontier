# Archive

Records kept for provenance. Nothing here describes how to run the current
system; start from the [README](../../README.md) and the guides in
[`docs/`](..).

| Path | Contents |
| --- | --- |
| [`history/`](history/) | Engineering logs and handoffs, as written at the time |
| [`plans/`](plans/) | Superseded plans, including builder snapshots that are not imported |
| [`unified-main.md`](unified-main.md) | The full acceptance log of the unified main branch |
| Dated reports | Validations, audits, model compatibility and pricing observations, each named with its date |

Records here name the commands and scripts that were current when they were
written. Scripts without a remaining caller were removed on 2026-11-03; read
any of them from the last commit that had it, for example:

```sh
git show 74a6e9c:scripts/verify_pipeline.py
```
