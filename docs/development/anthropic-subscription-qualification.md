# Claude subscription qualification: official documentation findings

Checked 2026-11-02 against Anthropic's live documentation. This research makes no
model calls, changes no credentials, and does not run cluster acceptance. The
user stopped natural-expiry observation and retained the US$2 aggregate budget.
Existing Slurm and authentication functionality remains available.

## What the provider documents

Saved claude.ai login has a renewal path. The error reference distinguishes a
server's expired/revoked-token rejection from a locally rejected request after
refresh credentials fail. The latter produces `authentication_failed` in print
mode and needs another native sign-in. A competing process can also hold the
shared refresh lock; that separate condition uses `server_error`. These are
provider-defined failure cases, not evidence that this account encountered them.
[Error reference: OAuth expiry, login expiry and refresh contention](https://code.claude.com/docs/en/errors#oauth-token-revoked-or-expired).

The authentication page distinguishes a login nearing its final expiry from a
renewable credential: it recommends renewing an expiring login through `/login`.
It also documents a different automation option: `claude setup-token` creates a
subscription token valid for one year. The native authorization flow displays
that token rather than saving it; scripts supply it through
`CLAUDE_CODE_OAUTH_TOKEN`. Configured local MCP servers work with this option;
Remote Control and claude.ai connectors do not. This research did not generate
or read such a token.
[Renew an expiring login](https://code.claude.com/docs/en/authentication#renew-an-expiring-login),
[Generate a long-lived token](https://code.claude.com/docs/en/authentication#generate-a-long-lived-token).

The current CLI reference describes `claude auth status` as a status report with
credential-source and configuration-directory information. It lists native
login, logout and token generation, but no force-refresh or forced-expiry
command was found in that reference. A successful status report therefore does
not establish that a refresh happened. The same reference supports explicit MCP
configuration and exclusive selection through `--strict-mcp-config`.
[CLI commands](https://code.claude.com/docs/en/cli-reference#cli-commands),
[CLI flags](https://code.claude.com/docs/en/cli-reference#cli-flags).

Print mode supports unattended requests, structured output and session
continuation. It can load MCP tools; its startup event provides server status and
configuration errors that a harness can check. Bare mode excludes subscription
credentials, so switching a subscription probe to bare mode changes its
authentication assumptions.
[Programmatic execution](https://code.claude.com/docs/en/headless),
[Startup MCP checks](https://code.claude.com/docs/en/headless#fail-ci-when-a-plugin-or-mcp-server-doesnt-load).

Native cost output is an estimate. The official CLI description excludes
inherited conversation totals from a resumed invocation's spending ceiling and
warns that spending can exceed the ceiling. Subscription session figures are
not invoices; the project should continue conservative accounting rather than
infer free usage.
[Budget flag](https://code.claude.com/docs/en/cli-reference#cli-flags),
[Cost tracking](https://code.claude.com/docs/en/costs#using-the-usage-command).

## What this repository actually demonstrated

At commit `900816d5e15e650f502818f09841b7c8d2b86739`, a genuine native Haiku
subscription completed a declared engineering fixture: observation, snapshot and
fork, one 5 mm physical move, delegation return, parent continuation and normal
finish. Every native process exited successfully and reservations settled. The
independent Transport result remained false: the fixture explicitly replaced
placement solving with a protocol exercise. Its native list-price upper bound
was US$0.03195554.
[Published source and review](https://github.com/changxuanfan/RoboFrontier/pull/4),
[Source-pinned delivery receipt](https://github.com/changxuanfan/RoboFrontier/releases/download/development-fixtures-20261102/final-native-subscription-qualification-900816d.json).

The observer was then stopped at the user's instruction while idle, rather than
left waiting for expiry. Its six completed native probes all exited normally
with known cost, totaling US$0.0022995600000000003. No refresh event was observed.
After releasing only its unused allowance, the local conservative reconciliation
is US$1.9378691900000000053 reserved out of US$2, leaving approximately US$0.06213.
All older uncertain allowances remain reserved. This updates the earlier
published delivery snapshot; these amounts remain list-price estimates.

The installed native CLI help independently lists only login, logout and status
under authentication, and only JSON/text output options for status. These local
help observations agree with the examined reference; no authentication action
was performed by this research.

The project still returns an engineering-only Claude qualification and writes
unscored engineering results. This restriction belongs to RoboFrontier; provider
authentication documentation cannot certify task success or clear it.
[CLI admission](../../robofrontier/cli.py),
[Engineering launcher](../../robofrontier/claude/engineering_run.py),
[Local authentication contract](../engines/claude-code.md#authentication).

## Next steps without a passive expiry wait

1. Keep the saved-login profile available, record automatic renewal as documented
   provider behavior, and retain actual expired-token renewal as unobserved.
   Exercise project handling of the documented authentication and contention
   failures with deterministic offline fixtures; label that as harness testing.
2. The user selected the documented long-lived-token flow as the default for
   Claude scripts. Keep it in the separate `haiku_subscription_token` profile.
   Qualify its model,
   image, tool, fork, budget and lifecycle behavior separately. Passing it would
   establish that profile's operation, not prove saved-login renewal.
3. Keep ordinary task qualification separate: use the original public benchmark
   inputs and independent evaluator for any task claim. The passing short
   protocol fixture already establishes its stated interface scope; it does not
   need to be misrepresented as a solved Transport task.
4. Preserve cluster support while excluding cluster execution from this round.
   Do not transfer the account store or reconfigure cluster networking. No
   further paid task trial is part of this research; the small remaining
   aggregate allowance is not a plan for completing ordinary Transport
   qualification. Documentation research consumes no model budget.

No documented deterministic, zero-model force-refresh method was found in the
examined Claude Code pages. Native reauthentication is an available renewal
procedure, but it is not an experiment proving automatic refresh after expiry.
Neither a long-lived token nor a provider statement should silently convert the
existing empirical refresh gate into a passing receipt.
