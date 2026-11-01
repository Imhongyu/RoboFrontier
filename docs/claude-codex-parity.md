# Native Codex and Claude Code: component map

The two engines execute the same public robot tasks and share runtime authority,
START timing, terminal-outcome scoring, process records and evidence formats.
Their native session/tool interfaces are different. Use
[harness alignment](harness-alignment.md) for current IDs, recovery and reporting,
[architecture](architecture.md) for shared contracts, and the
[acceptance ledger](development/unified-main.md) for actual integration evidence.

New Single/Adaptive runs use direct Controller START; all initial standing-team
Codex roles use direct team START. `ready` is a capability query in those runs.
Historical `ready_barrier_v1` inputs retain their old READY/idle barrier.
Claude currently exposes Single/Adaptive engineering drafts only. Permanent
Workers and formal scored Claude execution are not yet available. Earlier
migration records below describe their original stages, not current defaults.

## Component map

| Component | Native Codex | Native Claude Code | Qualification boundary |
| --- | --- | --- | --- |
| Provider/model catalog | `configs/models.json`; launch configuration writes `codex.json` | `configs/claude-models.json`; `scripts/claude_benchmark.py` | Profiles alone do not establish provider compatibility. |
| Task selection/freeze | `benchmark.select_cases`, shared preparation | Same selection/preparation; `engine: claude` in new harness/manifest | Shared tasks, separate engine qualification. |
| One policy turn | app-server `turn/start` | `claude -p`, `robofrontier/claude/runner.py` | Native turn lifecycle is not task success. |
| Robot tools | app-server dynamic `robot` tool | Role-bound MCP in `robot_mcp.py` | Actual provider image handling requires its own evidence. |
| Per-task host | `scripts/codex_policy_host.js` | `policy_host.py`, `adaptive_policy_host.py` | Claude Single/Adaptive engineering only. |
| Scheduling | `scripts/meta_dispatcher.js` | `dispatch.py`, `adaptive_dispatch.py` | Both use shared deterministic runtime rules; Claude engineering does not run through a fabricated Codex tool object. |
| Session observation source | `codex.wait_threads`, `codex.app-server` | `claude.host` | `SESSION_SOURCES` is restricted by selected engine. |
| Fork history | Native ordinal/prefix hashes in the task's Codex home | Native transcript UUID sequence/content in `provenance.py` | Prefix equality alone does not establish trusted creation or role authority. |
| Source freeze | Benchmark launch and native host/RPC scripts | Claude launcher/catalog and imported shared Python modules | Current freeze checks do not retroactively protect old drafts. |
| Supervision | Preflight/run/status/stop | Precheck and engineering run/status/stop | A matching receipt does not authorize a scored Claude task. |
| Local doctor | Unified CLI selects native engine | Native Claude doctor also checks local credentials/assets/tools | Presence is not successful authentication; no model is called. |
| Evidence/reporting | Native sessions plus host/motion/tool records | Native transcripts/tool-results plus host/motion/tool records | Shared metrics preserve engine-specific units and missing fields. |

## Real qualification still required

1. Obtain profile/account/current-CLI evidence for text, image/tool round trip,
   continuation and fork. Adaptive additionally needs a parent blocked in a tool
   call. Check intended batch use, model mapping, visual/tool support, concurrency
   and actual billing. Receipt consistency does not prove provider model identity.
2. With explicit spending authorization, verify a real task's observations,
   actions, delegation, handback, continuation, finish, terminal world state and
   evaluation. Synthetic displacement and process sealing do not establish task
   completion or model ability.
3. Compare frozen task selection, authority, observations, timing and evaluation.
   Record native differences such as a tool-free Claude fork-creation turn rather
   than declaring them identical conditions.
4. Verify startup, stopping, unknown actions, process exceptions and supervisor
   loss under concurrency, retaining their evidence. SIGTERM smoke does not cover
   SIGKILL, power loss or every physical action boundary.
5. Open scored preparation/qualification/batching only after these conditions are
   supported by evidence. `formal_execution_available` remains false for Claude.

Credentials stay outside Git. Real calls and engineering trials need explicit
operator authorization. Current Mosaic is R14; do not import a Mosaic R15 draft
because another source branch has a newer-looking name.

## Verified native CLI observations, 2026-10-28

The following local observations used Claude CLI 2.1.312. They are reproducibility
facts for that version, not claims about every future CLI release.

1. `--resume P --fork-session` produced a child transcript containing the parent
   message prefix in the same order with the same UUID/content. `sessionId` and
   `promptId` differed; there was no explicit `forkedFrom` field. This is history
   matching, not independent identity or authority proof.
2. Adding `--session-id C` returned the specified child UUID, permitting the host
   to persist the intended child identity before launch.
3. Fork creation requires a CLI turn. Codex can `thread/fork` before binding,
   activation and a first prompt; Claude cannot verify a nonexistent child
   transcript before its creation turn. The implemented engineering path uses a
   tool-free creation turn, verifies it, then activates role-bound robot access.
   This setup work and its cost remain visible.
4. Child history can reference images in the parent's `tool-results/` directory.
   Preserve that directory during execution and include required references in
   collection; deleting it can break inherited visual history.
5. `MCP_TOOL_TIMEOUT` is in milliseconds. A two-second limit rejected a six-second
   sleep; a twenty-second limit allowed a four-second call. `wait_events` can wait
   600 seconds, so the host sets 660,000 ms for transport allowance. The native
   CLI's default timeout was not measured by those tests.
6. With `--bare`, `--tools ''` and `--strict-mcp-config`, the loopback service
   observed only the requested model and the configured robot tool. That finite
   observation does not prove all possible network behavior or provider identity.
7. Without explicit stdin redirection, `claude -p` waited three seconds and
   warned. `run_turn` now passes `stdin=DEVNULL`.

## Trusted internal adaptive fork

General Claude `delegate-bind` remains closed. Transcript-prefix equality by
itself cannot show that a trusted host created a child at the intended time or
bound the correct MCP authority. The internal engineering path checks the
claimed delegation and the parent's outstanding native tool call, persists one
child UUID before invocation, creates a tool-free native fork and verifies that
the parent history is unchanged and the child prefix/session/cost records match.
Unknown setup keeps its uncertain record and never automatically reforks.

`fork_setup.py` supplies that creation boundary. `adaptive_setup.py` connects
claiming, creation, provenance, scope binding, activation and the first child
assignment. Only after verification does
`ClaudeSessionHost.adopt_verified_fork` create the role's MCP configuration and
resume its native child ID. Frozen input/profile matching and a one-time adoption
marker prevent ordinary repeated adoption. Host-side evidence does not protect
against another process with the same OS account tampering with files.

The native blocked-parent loopback test created a no-tool child while the parent
waited on MCP; the child tool list was empty and the parent remained active.
This proved a finite native CLI boundary, not production security, full task
qualification or arbitrary provider compatibility.

`adaptive_dispatch.py` routes deterministic wakes to the bound parent/child
sessions. A missing role, unknown state/send, leftover creation claim or failed
setup pauses instead of guessing. Setup runs in a separate thread; stop cancels
it and prevents new role starts. Accepted requests settle before eligible
capacity recovery; uncertain actions and uncertain fork creation remain blocked.
See [recovery rules](harness-alignment.md#capacity-and-rate-limit-recovery).

## Cost accounting and engine differences

The run-local budget ledger can be shared by Controller, delegates and fork
setup. New default engineering runs have no optional dollar ceiling; reported
costs are still collected. With an explicit allowance, the host reserves before
launch and blocks on unknown/overspent cost or unresolved reservations. Without
an allowance, missing cost is recorded rather than treated as zero, and does not
alone block an otherwise confirmed completed turn. Unknown execution remains a
separate problem regardless of budget. CLI estimates are not provider billing
limits or subscription-credit measurements.

Normal policy turns have no separate default timeout, while bounded startup,
RPC and tool-free fork setup still have limits. Engine-native prompts,
compaction, context inheritance and creation work can differ. Shared elapsed,
usage and tool metrics report these differences; they do not erase them.

## Historical migration checks

The original stage introduced optional `engine`, preserving absent fields in
already frozen Codex inputs. Runtime session observations became engine-specific.
`runtime_cli.native_fork_provenance` dispatches by engine; Claude reads native
transcripts below the run-local `private/claude-config/projects/`. The shared
Node dispatcher has an adapter seam, but Claude's actual engineering hosts use
their Python dispatchers, not a Codex-shaped emulation.

An early shared-source check at `188fff6` passed 55 run-setup/runtime/report/
delegation/execution-contract/action tests; report imports required
`PYTHONPATH=scripts`. Another early baseline passed scheduling, delegation,
callbacks, benchmark, pipeline, centralized, batching, setup, runtime,
synchronization, handoff and Claude groups. Two execution/action cases lacked
historical scene assets. These dated results neither establish every current
asset nor replace the integration regression ledger.

Early role hosts bound an existing centralized world, loaded public materials
and waited on READY/idle. The first adaptive drafts and synthetic runtime tests
later connected delegation, setup, scheduling and stopping. Subsequent real
MuJoCo/CLI loopback tests exercised those paths. Current direct START supersedes
the old barrier only for new inputs; old recordings keep their original protocol.
See the [Claude handoff](claude-handoff.md) for preserved historical provider
prechecks, costs, physical smoke scope and remaining lifecycle gates.
