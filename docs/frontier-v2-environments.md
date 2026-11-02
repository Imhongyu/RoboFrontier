# Frontier V2 task entry

Four families each have three scales and three levels, giving 36 cases.
`configs/task_families/current.json` distinguishes `gpt` and `oracle` purposes.

| Family | GPT input | Oracle presentation | Speed | Specification/evidence |
| --- | --- | --- | --- | --- |
| Transport | R14 physical half-holes | Original R13 frozen recordings; half-hole presentation | 20x | [Task guide](tasks/transport.md) |
| Mosaic | R14 nearby mixed colors | Original R13 color recordings | 30x | [Task guide](tasks/mosaic.md) |
| Relay | Final 50 mm GOAL, low release, stacking allowed | Each recording's own frozen source | 20x | [Task guide](relay.md) |
| Dial | R11 BEST5 | Original R11 recordings | 10x | [Task guide](tasks/dial-best5.md) |

Transport/Mosaic R14 are new inputs; R13 full Oracle results do not qualify R14
physics. Relay terminal-GOAL results and historical native acceptance are
reported separately. Assisted and pure-program evidence retain their labels.

New runs freeze public material and use a source-bound evaluation/recording
protocol; original task preview labels are not rewritten. See
[policy preparation](gpt-policy.md). Factory uses source-level edits, independent
station loops and 30 fps, superseding the old play-once/stop instruction. See
[Factory](robo-factory.md).

Historical catalogs, generators and packages explain old experiments; they do
not directly select the current release. The [earlier environment guide](archive/history/frontier-v2-environments-before-cleanup-20261027.md)
preserves revision history.
