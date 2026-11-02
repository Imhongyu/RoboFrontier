# Native subscription authentication

The API defaults are unchanged. `luna_subscription` selects GPT-6 Luna through
native Codex ChatGPT authentication. `haiku_subscription` selects Haiku 5.5
through native Claude Code login. These are separate profiles from their API
counterparts; their compatibility receipts are not interchangeable.

## Codex

Use the native CLI to sign in and inspect its status:

```sh
codex login
codex login status
```

Select an explicitly shared local home in an ignored site configuration:

```toml
[policy]
engine = "codex"
profile = "luna_subscription"

[runtime]
codex_home_scope = "shared"
codex_home = "~/.codex"
```

Credentials remain in Codex's native store. Preparation writes command-line
overrides that disable MCP servers found in native and project configuration
layers. Before inference, the native subscription host and preflight verify
that the effective configuration has no enabled inherited MCP server. The
benchmark supplies its assigned dynamic tools. A later configuration change
that introduces another server fails this admission check. User configuration
files are not rewritten. Names that cannot be safely expressed through the CLI
override syntax require a separate native home.

The native account refresh probe uses `account/read` with `refreshToken: true`,
then verifies authenticated access and persistence in a new app-server process.
That probe makes no model turn. A passing probe is separate from image/tool,
compaction, fork, concurrency and task qualification.

## Claude Code

Choose the native configuration directory explicitly before preparation:

```sh
export ROBOFRONTIER_CLAUDE_HOME="$HOME/.claude"
claude auth login --claudeai
claude auth status --json
robofrontier prepare --engine claude --profile haiku_subscription \
  --topology adaptive --render native --cases transport-a04-d1 \
  --output runs/engineering/haiku-subscription-example
```

`haiku_subscription` uses the default native login namespace. It requires the
selected directory to equal HOME/.claude and leaves CLAUDE_CONFIG_DIR unset.
Claude Code 2.1.312 selects a distinct credential namespace when that variable is
explicitly set, even to the same path. For an account authenticated with an
explicit CLAUDE_CONFIG_DIR, choose `haiku_subscription_directory` and the same
directory used during its native login. The selection is part of the profile
fingerprint; receipts cannot be reused between these namespaces.

The selected absolute directory is frozen in the private launch profile. Keep
the authentication home outside the evidence batch. Preparation, batch admission
and collection reject an authentication home inside that batch. Each role still
uses a host-generated explicit native session ID and its bound robot MCP.
Settings sources and unrelated MCP servers are disabled by command-line options.
Provider API keys and token environment variables are not inherited in this mode.
The unmodified native CLI owns authentication and credential persistence.

Evidence collection copies only the bound native transcripts and their session
sidecars. It excludes the credential/configuration store and unrelated sessions.
A collection marker lets restored provenance use the collected histories on a
machine without the original account. Launching another native turn still
requires the explicitly selected live authentication home.

`opus_subscription` retains its older explicit `CLAUDE_CODE_OAUTH_TOKEN` mode for
existing configurations. Native managed login does not require exporting that
token. Fresh login and a successful cached-login call do not by themselves verify
automatic refresh after token expiry.

## Qualification and limits

Preflight remains explicit and may consume subscription quota:

```sh
robofrontier preflight --engine claude --profile haiku_subscription \
  --max-budget-usd 0.10 --confirm-spend
```

CLI USD reports are estimates; subscription list-price equivalents are not
provider invoices. Keep API spending, subscription quota and unknown outcomes
separate. Claude task execution still requires `--engineering`; these profiles
do not open formal scored eligibility. Local shared-home checks do not qualify
Docker, Slurm, 36 simultaneous subscription tasks or every refresh boundary.
The Slurm entry continues to accept API credentials only. See the
[acceptance ledger](development/unified-main.md) for actual source-pinned results.

Official references: [Codex authentication](https://learn.chatgpt.com/docs/auth),
[Codex account refresh](https://learn.chatgpt.com/docs/app-server), and
[Claude Code authentication](https://code.claude.com/docs/en/authentication).
