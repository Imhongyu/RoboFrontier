> Historical archive. Current specification/status: [Transport task](../../tasks/transport.md).
> Merge procedure: [handoff](../plans/suite-v2/transport-merge-handoff.md).
> This record preserves the original process/evidence.

See the [Transport task](../../tasks/transport.md) and
[merge handoff](../plans/suite-v2/transport-merge-handoff.md) for current versions
and completion status. This records the period before and during initial Oracle work.

# Dedicated Transport worktree and complete Oracle plan

Branch: `task/transport-oracle`, from `main` at `d3e5916`. At this historical
stage it was unmerged and did not take over Dial, Relay or Mosaic sessions.

Source and Transport R13 / test R10 scene assets were in this worktree. Model
assets used independent COW copies; vendor was also independently copied, so
changes could not write back to the original directory. `.venv` was a shared
read-only dependency entry. Added `greenlet==3.2.4` lived separately in this
worktree's `.oracle-deps/`, without modifying other tasks' shared environment.

Runtime data used shared durable storage, with unique directories per batch,
scene and attempt. Records bound worktree, commit, frozen executor, dependency
binary hashes, control/acceptance fingerprints, full scenes and 60 Hz state
streams. Offline Factory rendering retained its original format; command lists
were not substituted for complete motion records.

## Execution boundaries

`transport_runtime.py` reused synchronous action recipes, cooperatively switching
only at execute/wait boundaries. greenlet switching was explicit/cooperative;
see the [official greenlet concepts](https://greenlet.readthedocs.io/en/stable/greenlet.html).
All planning/physics ran on one OS thread; only the scheduling owner could step.
Planning computation never coincided with another thread mutating the world.
Physical motion advanced interleaved; model/CPU planning parallelism was not claimed.

Every transport job had an explicit robot resource set. After completed handoff
and sender release/withdrawal/parking, sender resources could return early while
independent jobs continued. Failed robots still holding objects or with uncertain
results remained reserved, rather than being reassigned automatically.

New actions underwent bounded full-scene nominal joint-sweep screening against
in-flight actions. Conflicts waited for existing actions instead of interrupting
them. Sampled predictions were not continuous-collision/contact-dynamics
certificates; actual monitoring and original acceptance remained authoritative.

`transport_full_oracle.py` used a private candidate reachability graph and
minimum-cost matching of objects/targets with matching identities. It did not
write that graph into scenes, which had no fixed transfer boxes. It preferred
fewer necessary handoffs and allowed any candidate-capable arm to pick/place.
Actual handoffs, receiver grasps, insertion and withdrawal still required execution.

This executor was engineering Oracle only. It neither injected private
coordinates/grasps/routes into GPT Prompt/Skill nor replaced autonomous planning.

## Order and stopping conditions

1. First: the complete original 12-item R13 four-arm L1 order, without treating local-unit passes as a whole-task result.
2. Only after that passed, expand four/eight/twelve arms across L1/L2/L3, with at most two independent physics instances and frozen environment parameters.
3. Require original-goal success, no violations and no unresolved actions, then recheck after terminal settling. Seal videos and state chunks separately.
4. Preserve the same failed world's actual state/cause. Never replay uncertain actions, clear prohibited contact, roll back, combine scores across worlds or silently tune physics for a pass.
5. After Oracle stabilized, freeze integration before formal GPT Adaptive comparison. At this stage no GPT had started and nine complete Oracle passes were not claimed.

Entry: `scripts/run_transport_full_oracle.py`. Execution required clean Git and
a frozen source copy. Reference-code changes required a new commit/attempt.

Recorded tests: 59 Transport regressions passed, including existing minimum-unit
planning, same-thread physics ownership, fast-arm progress, conflict deferral,
resource boundaries and uncertainty retention. Every R13 scene matched its
previous frozen bytes.

## In-world recovery from ordinary failures

Ordinary grasp/handoff/placement failures ended only that job context; unrelated
jobs continued. Known failed holders retained resources rather than pretending
to have released. After predicted conflict, a new action waited for the relevant
in-flight action to finish before rescreening, without repeating the same check
every physics step.

`transport_recovery.py` published `recovery/frontier.json`. If remaining work
blocked, the physical process retained the world, continuing gravity, contact
and grasp control near real time while engineering chose recovery. Waiting counted
toward execution. Ending a reply/reopening a world did not count as same-world recovery.

Research could atomically submit `recovery/inbox/<UNIQUE_ID>.json` containing
`id`, failed `job`, `scene_sha256`, optional `robots`, up to 64 ordinary robot
`steps`, `reason` and `author`. Each step contained existing move/gripper
parameters or a wait of at most 30 s. Inputs could not supply qpos, physics,
score edits or arbitrary Python. Hashes, timestamps and acceptance/rejection
were retained. Old failures stayed; uncertain actions could not be taken over
or replayed.

Empty steps requested replanning from the actual scene; ordinary steps also
returned to scene-based goal continuation afterward. Recovery could acquire its
known-idle resources while independent jobs continued. Partial handoffs and
multiple holders required explicit release/withdrawal plans before regrasping.

Research-supplied recovery inputs set `engineering_assisted=true` and
`llm_used=true`, separately from pure frozen-program results. Original complete
task acceptance still determined success; collisions stayed recorded and scores
were not stitched together or old failures rewritten. Executor-code changes
sealed the old attempt; a new commit/new initial state was an explicit new attempt.
