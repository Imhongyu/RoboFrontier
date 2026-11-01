# Historical post-compaction handoff — 2026-10-27

This preserves the original Relay handoff and successive checkpoints. It superseded
outdated progress, 5/25mm standards and authorization/hot-loading statements in
`relay-continuation.md` at the time. All process IDs, active-frontier instructions
and “latest” labels below refer to that historical session, not current processes.
Read [unified main](../development/unified-main.md) for present integration work.

The user had requested detailed compaction and “do not stop the program.” The
original instruction was to continue the same worlds until 9 tasks completed,
without stopping, restarting or creating duplicate simulations. Compaction did
not cancel that work. The completion updates below supersede earlier frontiers;
none authorizes resuming old requests today.

## Latest on 2026-10-27: portable edits and all 18 simple/Factory 20x videos complete

The user requested trajectory-bound idle removal shared across backgrounds and
20x speed. This was complete; no control/media process needed resuming. No Oracle
rerun or commands to original worlds. Historical physics acceptance remained
9/9 and 27/27; native scores, raw trajectories and old MP4 files were unchanged.

Overview: `outputs/oracle/relay-20x-20261027/report.md`; summary.json complete=true,
completed_tasks=9/completed_videos=18. New videos: 30fps, effective simulation time
at 20x, one evidence-pose frame at each endpoint. Old nominal 4x/16fps versions
remain; lower sections mentioning 4x describe history.

Delivery directories, each containing 9 MP4 files named by arms/Level:

- `outputs/oracle/relay-nine-videos-20x-20261027/`: simple backgrounds.
- `outputs/robo-factory/relay-nine-videos-20x-20261027/`: Factory backgrounds.

Matching durations in both backgrounds: 8-arm L1/L2/L3 17.667/24.467/23.033s;
12-arm 50.300/45.733/58.033s; 16-arm 87.500/79.500/88.867s. All 18 completely
decoded and passed 30fps/frame-count/SHA256 delivery-copy checks. All three
qa-08/12/16-paired-first-last.jpg images were viewed, along with an 8L1 middle
frame and 12L3/16L2 Factory final frames.

Reusable package: `outputs/oracle/relay-edited-tracks-20261027/`. Each case includes
exact frozen source model/assets; edit.json with intervals/thresholds and the
previous 960-window image-review sources; track.npz containing original 60Hz qpos
inside retained intervals, 570746 rows total. Every row retains source frame/time,
edited time/duration/segment. It also includes exact endpoint evidence states,
appearance events, initial RGBA and source-chunk hashes. Physics: 2ms=500Hz;
recording: 60Hz; selection: reviewed 20Hz mask with 0.25/2-second windows. No new
background pixel classification, cut interpolation or physics integration. All
nine track-validation.json checks passed.

Factory: `outputs/robo-factory/relay-recorded-20261027/scene.xml`, 9 visual
stations built from exact frozen recordings, rejecting older sources sharing IDs.
FactoryPlayback.apply_arrays vectorizes FK/common translation/vertical yaw, without
scaling or relative-layout changes. Materials/background may differ. All visible
geometries' source/destination positions/rotations were checked in every output
frame; maximum positional difference 5.03e-15m. Backgrounds share each frame-map.csv.
This displays original records, not new successful Factory physics.

Implementation: robofrontier/motion_edit.py, scripts/export_relay_edited.py,
FactoryPlayback.apply_arrays; format/commands in docs/relay-recorded-video.md.
19 edit/motion/rigid-transform tests passed. Another 7 old aggregate checks could
not reach assertions because existing non-Relay generated scenes had missing or
external identity textures. Those scenes/checks were not weakened; see new
test-results.json. Do not call that full-repository acceptance.

Only offline extraction/render helpers were started; all completed without STOP
or restart of original simulations. Read-only ps no longer found old 52509/52510;
do not claim they were still live from older sections, restart them or replay IDs.
Original 9/9 completion evidence remains.

## All nine idle-removed videos, including three L1 cases (historical 4x)

When asked whether all 9 were edited, the initial answer correctly covered
only 6 L2/L3; then three L1 were added. The same
`outputs/oracle/relay-active-only-20261027/report.md` became the nine-video overview.
8-arm L1 1:33 (1482 frames/16fps), 12-arm L1 4:26 (4256), 16-arm L1 7:49 (7501).
Six L2/L3 durations remained 2:11/2:06/4:08/5:42/7:20/8:06. Old versions retained.

L1 uses real native-success unchanged_l1 sources at
`runs/oracle/relay-nine-ab1abec-20261026-032833/relay-aXX-d1/attempt-001`, without
physics reruns. Old L1 schema lacks beam_bodies/user-goal-report; offline fallback
supports beam_body and native report.passed=true, retaining exact final close
event. All nine decoded with matching frame counts; all endpoint images viewed;
960 longer candidate cuts reviewed. L1 montage: qa-l1-first-last.jpg; summary.json
complete=true/completed_videos=9. Helpers completed. At this checkpoint original
52509/52510 were reported live; raw trajectories/old MP4/scenes unchanged. The
latest section above supersedes that historical process observation. The original
reply to later 9-video questions could point directly to this overview.

## Additional video requirements completed: prefer idle-removed versions

The user required all arm joints/fingers/main-body poses, 0.25s/2s cumulative
windows to reject numeric jitter and detect slow motion, whole-table idle removal,
removal of isolated weight sway without useful arm motion, preservation when arms
move, and image review.

The original did not fully meet this. All six L2/L3 were re-edited without touching
original simulations/trajectories. Report:
`/Users/fanchangxuan/Repos/roomscript2/outputs/oracle/relay-active-only-20261027/report.md`.
Each `relay-aXX-dY/global.mp4`: 8L2 2:11, 8L3 2:06, 12L2 4:08, 12L3 5:42,
16L2 7:20 (7037 frames/16fps), 16L3 8:06 (7768 frames/16fps). Originals retained;
old report links new versions.

`robofrontier/relay_video_motion.py` + `scripts/render_relay_active_only.py` passed
13 rule tests: one active arm, slow motion, numeric jitter, isolated/concurrent
weight motion, main-body slip, large independent weight fall, quaternion sign,
and weight occlusion not inventing arm motion. Extract 20Hz from original 60Hz,
compare 0.25/2s net changes/direction, OR every arm/finger's joints across the table;
retain main timber/L3 passive motion and large possible falling-weight changes.
An action command alone no longer protects its entire interval. One endpoint
frame each, without a stationary tail.

771 suspicious candidate cuts >=0.4s received RGB+geom-ID review, excluding weight
occlusion and checking visible geometry centers/outlines for useful arm/body
motion. 0 required restoration. Short numerical gaps used trajectories. See
frame-map.csv, manifest, state-summary, visual-audit and audit JPG. Six videos
fully decoded with matching counts; endpoint QA and qa-first-last.jpg viewed;
old MP4 files untouched.

Helpers completed. Physics remained 9/9, 27/27; 52509/52510 were reported live at
this checkpoint, without STOP/new worlds/restart/rollback. Offline edits needed
no old control request resumed.

## Final delivery complete: physics, verification and both videos

**9/9, 27/27; no control or media work remained.** Original 52509/52510 were kept
running at user request at this checkpoint, without STOP. Do not execute old IDs
or rerun user-accepted tasks because old native scoring says 3/9.

Report:
`/Users/fanchangxuan/Repos/roomscript2/outputs/oracle/relay-user-completed-20261027/completion-report.md`.
New complete videos span original time 0 to near acceptance, actions 4x/waits compressed:

- `relay-a16-d2-full/global.mp4`: 15255 frames/15fps, 16:57; full decode/endpoints viewed.
- `relay-a16-d3-full/global.mp4`: 47618 frames/15fps, about 52:55; full decode/endpoints viewed.

Same output root contains manifests, video-inspection.json and display sidecars.
These are neither new simulations nor closed episodes. Originals continued;
cutoffs use real records, with landing/separation/inside checked independently.
The earlier four complete 8/12-arm L2/L3 videos remain in 20261026 output and are
linked from the final report.

Media PID32831/32832 and encoders completed; sessions22221/84382 no longer needed
polling. After frame22844 in L3, export shadows/reflections were disabled for
speed, affecting drawing only. Idle optimization removes joint/finger jitter
outside execution intervals; all executed intervals/payload free-body/passive
thresholds remain. Effective frame/source times are in final manifests; earlier
footage retains more waits. No errors or real object motion were deleted.

Root acceptance: `USER-GOAL-ALL-NINE-COMPLETE.json`, `user-goal-batch-status.json`
(9/9); strict native batch-status.json unchanged. Recent checks: 36 passes;
source/control fixes committed. Follow later user instructions without duplicate worlds.

## Completed: 9/9 tasks, 27/27 timbers; supersedes all earlier unfinished frontiers

**All physics tasks complete; no further Oracle control/reruns.** At this point
PID52509/52510 remained alive at user request; no STOP. Final L3 P1: J/P(v155),
I short retreat(v156), Goal advance(v158), descent v159-1..10, real full 80mm opening
v159-11 at about13mm clearance, observation v160. All4/4 separated/landed inside;
first L3 acceptance had 0 boundary excess for all four. L2 also4/4. Independent
user-goal-batch-status.json reports9/9; USER-GOAL-ALL-NINE-COMPLETE.json saved;
strict native score/history remain3/9.

Final P grasp was solved by O24cm temporary receiving, actual empty P exit,
I/O leveling, and a P58cm Top branch screened through complete onward transport.
v149 free-wrist P exit, v150 leveling, v151 new P Top handoff, v152/v153 O home,
v154 final-window entry, v155 J/P handoff all executed. Earlier v124 Side P and
optional full-timber roll exhausted wrist limits; preserve history, no checkpoint rollback.

Last contact escape **revision5** acknowledged in same52510; frozen
`open-contact-withdraw-v5.py` SHA256
`6d761f2e3ca1755bd4b5160e124da020d5ee6cbdc76f74aecd7a5f67872137bb`.
Only with actual bilateral-force support by two other arms may a6cm empty exit
rotate up to0.20rad; Goal support without two receiving arms retains0.04rad.
81+ original-geometry samples, no deeper/new penetration, robot/world collision
and actual-separation postchecks remain. Physics/monitor unchanged;6 tests pass.
Final `final-goal-recovery-v2.py` installer SHA256
`491e2b39120c79b7bb44d1f96967f7079a5ded87530bbb7313cfcbba499569e3`
installs only tested Goal50, real support/low80mm opening and withdrawal in the
same instance/world. Experimental world-topdown/Top-only semantics were never
installed; source restored original semantics and did not depend on them.

At this earlier sub-checkpoint, **only media export/delivery remained**:

- `scripts/verify_relay_completion_prefix.py` verified L2 565086 frames,
  L3 1517398 from time0: every checksum/shape/time/finite plus actual final
  inside50/released/grounded/qualified handover, without a new episode.
- No close/STOP for video. Renderer --completion-sim-s uses real cutoff frames,
  no invented trial-end: L2 9418.100001001016, L3 25289.960004234537. Full original
  motion remained retained as recording continued.
- `/Users/fanchangxuan/Repos/roomscript2/outputs/oracle/relay-user-completed-20261027/`
  contained ongoing exports `relay-a16-d2-full/global.mp4`, `relay-a16-d3-full/global.mp4`.
  Sessions **22221/84382**, media PIDs32831/32832, encoders32835/32836. VideoToolbox
  hardware encoding smoke passed; ffmpeg threads/filters1, total CPU per case<200%.
- Media-only idle optimization removed outside-command arm/finger micro-jitter;
  command intervals and payload thresholds unchanged. Original physics untouched.
  export-idle-motion-policy.json records effective frame/time, later merged into
  manifest. No failure/real object motion removed; early footage has extra waits.
- Original next steps: view endpoint PNG, ffprobe duration, manifest decode_passed,
  deliver both full videos and update completion-report.md's two exporting rows.
- Then-uncommitted changes: contact escape revision5/6 tests, cutoff/hardware
  options, verify-prefix and this checkpoint. Never mark9/9 incomplete or replay IDs.

## Historical L3 bottleneck resolved: latest actions at that checkpoint

Then26/27,8/9;16L2 complete,52509 still alive/no STOP. Last16L3 P1:
`r16-p1-N-local-lattice-v117-1` completed empty-N local reorientation;
`r16-p1-IO-past-lattice-N-v118` advanced250mm through N obstruction.
Read-only planner: `runs/engineering/relay-descent-20261026/finite_local_empty_lattice.py`.
Four N joints,625/750 candidates,186 clear states,135 with full onward carry,
185 visibility edges,1 expanded state,3.229s for 1 ordinary empty-hand segment.
Not another million-sample global IK expansion. Home/single-joint attempts had
failed; do not repeat those searches.

Actual I/O P1 Root≈[1.5022,.7573,1.2570], yaw1.87037, still tilted/rolled.
Finite helper at the time: `IO-level-after-N-v119` → `IO-open-P-window-v120`
([1.5,.65,1.2] and finite alternatives) → `IO-to-IP-final-Top-v121`. Inspect original
pending/results instead of replaying. Then I/P→J/P→Goal and independent50mm checks
of all4/original records.

The user had not yet received the complete16L2 success video. Preserve full
actions/errors/corrections, allowing idle compression. Both cases were then live;
renderer --user-goal-complete required closed streams/exact final event, so no
false sealed/full-video claim. Original instruction allowed closing after9/9
acceptance; later updates record the user's keep-running requirement.

## Historical26/27,8/9; supersedes earlier frontiers

16L2 real4/4, user-goal-report.json passed=true, USER-GOAL-COMPLETE.json saved.
No STOP to16L2;52509 reported running while L3 continued.16L2 P1 I/P→J/P(v78),
Goal(v79), descent(v80) encountered old Goal5mm rule. user50 policy v81 allowed
P1 weight contact with P3. P release failed but force was off; full80mm v85 and
P+30mm retreat v86 completed actual separation, all Goal50. Native/drop history unchanged.

Authorized hot-loaded changes in the same original processes, recorded under
controller-extensions:

- relay_user_goal_policy.py: Goal50 contact list, real stacked support and
  lowest-component30mm release. Operational policy only, no native scoring/history/geometry changes.
- 16L2 goal-stack-open-v1-loaded.json:
  49448a4f94d66c3c6788d902d5a54e1dc2dd7a7e4e6419f5f7e6e8e452b5d425.
  Typed open permits supported user50 stacks/full80mm, not another cargo's hand;
  retain held labels while contact remains. Same world/guards;16 live_recovery tests.
- relay_contact_escape.py revision3: same short distance/81 samples/nondeepening;
  approved user50 Goal support list includes edge-completed P3. Frozen16L2
  open-contact-withdraw-v3.py; installer user-goal-withdraw-native-v1.py SHA256
  `3c34d1bec3a46a6ca3b021b3a56663b1af0474d707187d192295996edb84557b`.
- relay_observation_state.py: read-only native double joints/cached free-body poses,
  weight/hinges included, replacing potentially2simsec-old float32 video chunks.
  No live qpos writes. Both cases loaded. native-kinematic-state.required waits
  for diagnostic publication; no fallback to old chunks during partially written
  ordinary/native JSON.3 tests plus actual full-geometry FK reconstruction error0;
  Goal policy4/contact3 tests.

Only16L3 P1 remained, I/O Top, tilted/rolled:

- v87 tilt≈17deg, v88-1/2 advance, v93/v94 spatial turn, v95 I/O handoff,
  v96 H home completed.
- v99 long-axis roll-0.2, v100 advance80mm advance, v102Root x≈1.50, v103y-50mm,
  v104roll-0.15 completed. v105 rejected by guard without action.
- Key: empty N need not home or move only its wrist; lower forearm under weight.
  Old v54 raised N q[2] by.4, obstructing O_link2 with N_link5. Actual v108
  lowered q[2] by.15 to≈-1.74, with4mm endpoint/10mrad sweep checks. Ordinary
  recorded action, no rollback; N stayed force-free/open/separated.
- finite_spatial_local_progress.py under runs/engineering/relay-descent-20261026
  was the ended v92 helper, not to rerun. Then finite prefix:
  `r16-p1-IO-past-N-v110-1..3`, if needed `r16-p1-N-under-cargo-v109-1..3`.
  Inspect immutable feedback, not resubmit. Aim Root y≈.8, level, I/O→I/P→J/P→Goal.
- Other L3 P2/P3/P4 in Goal need final recheck. Most v69..107 planning was not
  submitted; numbering does not imply execution. World
  be2204c7cc834e2792271a959a435d9e/PID52510 remained.

## Historical later frontier:25/27,7/9

16L2 P2 completed, Top J/P release, 0 excess/drops0. 16L2 at3/4, P1 remaining;16L3 at3/4, P1
remaining; original worlds unchanged.

- L2 P1: D/M advance, D/M→E/M(v63), E/M→F/M(v65), F/M→F/N(v66), F/N→G/N(v68).
  Negative-side offsets alternate32/54cm for palm clearance. v69 advance completed,
  v70G/O selected/executing; v71advance/v72H/O Top needed feedback. Never replay.
- L3 P1: 3 N folds(v65-1..3), H/O advance v66 completed. Actual H/O Top,
  Root≈[1.269,1.181,1.190], N still in crowded shoulder/elbow area. Failed read-only
  home/fold/IK/carry searches were not physical requests/drops/process exits.
- L3 spatial target_quaternion_wxyz branch hot-loaded into same52510
  RelayLiveRecovery.process; no wait-loop/instance/state/history replacement.
  14 tests; spatial-carry-v1.py SHA256
  `93d3e04dab818bb67a7214b360354cd1a06ef93e70a6a0c012b9e6b76b88fbc5`.
  installed=true, same world, LLDB detached; loader
  runs/engineering/relay-descent-20261026/relay_spatial_hotload_loader.py.
- Actual L3 v87 tilted17deg around H negative grasp, raising positive end; full
  timber/robot/hardware sweep passed. Helper v88-1..8≤5cm each, reconstructing
  free-weight pose after feedback rather than rigidly predicting distant motion.
  This was the frontier then; ordinary action/drop/collision guards retained.
- Ordinary recorded retreat allowed; live rollback forbidden. v84/v85 full
  retreats failed planning only. Most v69..86 L3 IDs were not submitted.

## Historical compaction increment (2026-10-27):24/27,7/9

Original worlds unchanged:

- 16L2 P3 r16-p3-P-current-normal-escape-v44 actually separated; independent50mm
  pass, about1.56mm excess, no force/robot contact, native completed=true,drops0.
  r16-p3-P-separated-home-v45 completed; P reusable.16L2 now2/4.
- 16L2 P2 G/O→H/O(v41), valid Side H intermediate. Carries to[1.55,.8,1.2],
  r16-p2-HO-to-IO-palm-clear-Top-v51 completed I/O Top. Helper then v52I/P,
  v53advance,v54J/P; inspect feedback. P1 D/M Top offsets≈-.431/+.320m.
- 16L3 P1: open old N Side could remain contact-free; immediate home was redundant.
  robofrontier/suite/relay_donor_staging.py predicts full21-point75mm opening,
  requires1mm all-scene clearance, and keeps donor geometry in later carry.
  Same52510 loaded parked-donor-v1.py SHA256
  `2fa937b9cbc878075ded78ae0ac6c30cc2b9584e07dad7ae3d95696a83e13126`.
  Ack/queue/detach confirmed; source/meta in original16L3 recovery/controller-extensions.
  Loader runs/engineering/relay-descent-20261026/relay_parked_hotload_loader.py.
  Saved scene75mm positive/45mm insufficient-open negative passed, private qpos
  unchanged;21 existing recovery tests passed.
- r16-p1-HN-to-HO-safe-parked-N-v47 completed; r16-p1-HO-separate-parked-N-v50
  moved120mm along measured N tool Z and separated. Home(v51) planning failed;
  q[2]+.4 v54 executed. N_hand/O_link5..7 still blocked onward carry. Then helper
  checked N-compound-future-fold-v58-1.. and HO-Ncompound-forward-v59 for finite
  empty-hand clearance through full onward carry. v56/v57 not submitted.
  No mandatory N home, only a real force-free route clear of later transport.
- L2 and L3 original cases ran concurrently, each≤1 physics+1 helper core;
  no new/stopped original processes.

## Original one-minute recovery procedure

1. Workdir `/Users/fanchangxuan/.codex/worktrees/relay-continuation/roomscript2`,
   branch codex/relay-continuation; this handoff before older continuation.
2. `/tmp/relay-r16-active-root.txt` identified the only active original root.
3. Confirm52509/52510 and world IDs; supervisor52485.
4. Read attempt-001/recovery/observation.json and recent results/*.json; ensure
   requests/accepted has no unresolved action. Never replay an existing ID.
5. Snapshot runs/engineering/relay-descent-20261026/owner-frontier-current.json
   can be stale; newest immutable original feedback wins.
6. At this old checkpoint7/9,23/27; 4 remaining:16L2P1/P2/P3 and16L3P1.
   Continue actual scheduling, not merely an offer. Completion above supersedes it.

Original session JSONL, read selectively by role/keyword rather than dumping:
`/Users/fanchangxuan/.codex/sessions/2026/10/26/rollout-2026-10-26T00-40-13-01a173ef-208f-74d0-ae4c-faf10e1135f1.jsonl`.

## Original user requirements

- Oracle nine only:8/12/16 arms×L1/L2/L3; no GPT policy.
- No global deadline or sealing incomplete tasks due to slowness.
- Continue original worlds; no prefix reruns, rollback, live qpos writes or welding.
- Real release inside white Goal, uniform50mm boundary tolerance. No speed/dwell
  gate or mandatory prior timber/weight contact. Contact/collision/stable stacks allowed.
- Real qualified airborne handoffs and all actual action/failure history; no
  fabricated strict native pass.
- At most2 cores/case:1 physics+at most1 helper, reserve_helper_core flock slot.
  Do not hold the slot while waiting for a child to acquire it; use same-process runpy.
- Improve speed; promptly collect feedback and execute bounded known prefixes,
  return for decisions at new obstacles; different cases can proceed in parallel.
- No subagents without explicit user/applicable-instruction request; proactive delegation prohibited.

## Original worlds/processes

Shared runs root: `runs/oracle/relay-r16-38b5423-20261026-171651`.

| World | PID | world_id |
| --- | --- | --- |
| relay-a16-d2 | 52509 | 9ecf541b82b9407988a5aeb2a58db55f |
| relay-a16-d3 | 52510 | be2204c7cc834e2792271a959a435d9e |

Other accepted cases were closed/preserved. Duplicate R17 supervisor74995/children
75025–75030,8L2PID66700,old55214/99193 were SIGSTOP, not effective progress; do
not resume duplicates. L1 evidence/geometry retained.

## Completion/video status at the older frontier

- Three L1 complete:8L1 2/2,12L1 3/3,16L1 4/4.
- Original8L2/8L3 each2/2,12L2/12L3 each3/3, closed under final user rules.
- Last12L2 P1≈35.9mm excess is inside allowed50mm; no further correction.
- Complete12L2 recording472,741 frames;12L3 1,094,707, every chunk checked for
  checksum/decode/time. Exact final event separately checked; it may follow the
  last60Hz sample by≤one interval, without fabricated stream state.
- USER-GOAL-COMPLETE.json,user-goal-report.json,RECORDING-VERIFIED-USER-GOAL.json
  are independent acceptance/integrity evidence.
- Strict native task/stream may remain failed from old rules/STOP/guard history;
  never rewrite as success.
- Videos under
  `/Users/fanchangxuan/Repos/roomscript2/outputs/oracle/relay-user-completed-20261026/`:
  relay-a08-d2-full/global.mp4,relay-a08-d3-full/global.mp4,
  relay-a12-d2-full/global.mp4,relay-a12-d3-full/global.mp4.
  8L2 6m13s,8L3 6m36s,12L2≈7m01s,12L3≈17m31s.4x actions/low-motion waits
  compressed, all actions/failures/corrections retained.12L3 endpoints viewed;
  12L2 decoded, endpoints could be reviewed. No new physics; renderer reads50mm
  from report and appends exact final event.

## Original16L2,1/4 complete

- P4 complete;≈3mm strict error allowed, no correction.
- P3 inside Goal, no force,80mm open but resting on P fingers/occasional palm;
  not complete. Open alone is insufficient; P was the key blocked resource.
- P1 D/M,Root≈[-.696,1.516,1.294], r16-p1-DL-next-positive-Mfreed-v1 complete;
  M released P2 then actually received P1.
- P2 G/O Top,Root≈[1.102,1.300,1.196], r16-p2-GO-open-H-Top-window-v29 complete.
  H54 may now be reachable; earlier failure at Root[.9,1.4] was position-specific.
  Do not assign P to P2 before P3 separates.

## Original16L3,3/4 complete

- P2/P3/P4 released/inside, rechecked3/4. Approximate poses P2[1.610,-.434,.871],
  P3[1.750,-.546,.836],P4[1.727,-.635,.842]; contact/stacks allowed.
- P1 H/N: H Top Dot≈-.999,N Side Dot≈+.095. Old prose called H32mm, but its
  actual offset notation was `.32m`; N `.58m`. Preserve this discrepancy.
- r16-p1-HN-receiver-height-room-v38 completed vertical descent to
  [1.203,1.302,1.158], actual orientation retained, lowest component above table;
  lowest≈.961→.886, no artificial Root1.2/1.3 requirement.
- Stale P2 held label excluded H from choose_team. Ordinary typed move_empty
  feedback at current joints r16-p2-H-empty-stage-feedback-v56 cleared it with
  actual empty/no-force/contact-free/table-supported state, not cache tampering.
  r16-p1-GN-to-HN-Hfreed-v35 then actually handed over.
- O Top receiving remained. Do not require_topdown=True while retaining old Side
  N in negative-side handoff. H already Top; when retaining H/receiving O, both Top is valid.
- r16-p1-HN-to-HO-lowered-Top-v39 finite offsets [.32,.54],[.32,.44],[.32,.32],
  [.32,.24] found no candidate; no physical v39 submitted. Recheck results.
- Check O endpoint/100/150mm preapproach and N forearm/O link2 instead of broader
  repeated search. Root descent partly solved approach-height problems.
- Old advance to[1.6,1.15,1.2] with yaw2.2 failed N IK immediately; pure descent
  to1.16 with actual orientation passed. Local pose/branch limit, not global deadlock.
- Once H/O both Top, continue validated I/O,I/P,J/P; finite XY/yaw waypoints avoid
  timber sweep through bases, without blindly moving by station index.

## Authorized hot-loading already completed in original process

The user was told attachment briefly pauses simulation/time, then continues the
same process, and replied that continuation without restarting was acceptable.
This authorized the original control-only hot load; no repeated approval needed.

- Original16L2PID52509 loaded **v1**, without restarting/restoring state.
- Frozen original16L2 recovery/controller-extensions/open-contact-withdraw-v1.py SHA256
  `11c63d5f1d3e5f3e011e3a8491013740d2cb1f1f066cc3ea72719f813a57cd80`.
- open-contact-withdraw-v1-loaded.json confirmed installed=true,samePID/world.
- LLDB attach→Py_AddPendingCall→safe Python callback→detach. No debugger action
  command or live qpos/physics/monitor writes; debugger detached/process resumed.
- Loader runs/engineering/relay-descent-20261026/relay_hotload_loader.py; inspect
  ack/queue before any enqueue. Buffer≈2KB, with no physical-state meaning.
- Handles short exits only when open/force-free/ground-supported/still contacting.
  Private FK does not weld by stale held label; retains80mm opening, nondeepening
  existing contact, no new penetration or robot/table collision. Actual t.execute
  retains speeds/joints/recording guards.
- Ordinary noncontact move_empty unchanged. Remaining actual contact preserves
  failed feedback/held label; only genuine separation clears cache normally.
- robofrontier/suite/relay_contact_escape.py:3 unit+4 empty+14 live-recovery tests,
  actual saved-scene81-point checks/mock actuator scheduling.
- Experimental **v2** large rotations failed complete collision checks, never
  loaded/executed. Archived open-contact-withdraw-v2-uninstalled.py/.json;
  tracked source restored loaded-v1 SHA. Do not claim v2 active.

## Actual P3 withdrawals: never repeat

Original16L2 P3/P remained force-free/open/contacting:

1. r16-p3-P-open-contact-withdraw-v16:≈-20mmX/-5mmZ, actual motion/object followed,
   separation postcheck failed; same world/history, no collision violations.
2. r16-p3-P-progressive-open-exit-v17-1..4:4 real segments, all “moved but cargo
   contact remains”; script stopped when no new path existed.
3. r16-p3-P-lower-open-exit-v19-1:≈-10mmY/-25mmZ, real motion/contact remained.
   Segment2 had no verified path and was not submitted. Never replay IDs.
4. Then P3 Root≈[1.694,-.486,.992]; newest observation authoritative. P_tool moved,
   so old80mm straight-exit conclusions were stale.

Failure means actual motion with remaining contact, not simulation termination
or teleportation. Friction may make timber follow despite fixed-object FK.
Design exits from actual contact/wrist pose (Top opening or table taking load),
not another repeated grasp RRT. Old grasp plans reduced80mm to65mm and introduced
fixed-timber initial penetration, explaining many futile searches.

## Interfaces/evidence/recovery at that checkpoint

- .venv/bin/python; environment
  `PYTHONPATH=.:runs/engineering/relay-descent-20261026 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`.
- No pytest in that venv; use `python -m unittest discover -s tests -p 'test_relay_*.py'`
  without accidental dependency install/rebuild.
- owner_client.send(run,request) is the sole typed route, unique IDs/no replay.
  Exceptions can follow real motion; inspect result/new observation first.
- diagnostic_world(run) is read-only FK, using latest complete chunk for weights/
  hinges as needed, not new physics. Zero qvel/default force cannot establish
  actual stability/holding; use original observation.
- scripts/check_relay_user_goal.py independently checks50mm, real release/ground/
  qualified transfer, no speed/dwell; strict reports/counters retained. Recheck
  placed objects after later contact.
- user_goal_lower_open.py: real small Goal descents/support/normal release/open;
  worked for16L2P1/16L3P2. Failed release may already open and complete; verify separately.
- original_recovery_lift.py: original custody/actual bilateral holding only,
  real24mm lift; preserve drops/flags, no foreign pickup while grounded.
- finite_top_route.py/finite_owner_sequence.py run bounded prefixes, returning
  failures for model decisions.16l3-p1-top-roadmap.json v14 executed,v15 not sent;
  later H/N frontier supersedes it. No replay from old roadmap start.
- Read tails/specific IDs of large JSONL; never dump manifests/image base64.

## Final user geometry

L1 unchanged;8/12-arm L2/L3 span1.15m,16-arm1.20m,16-arm radial rows1.40m.
L2 arc63°;L3 bend31.5°/internal148.5°, perpendicular-to-initial-plane bending
(horizontal axis),nominal±25°,stiffness18/damping.55. Direct underside rings100mm
from end, no posts; same double rings+170mm timber+600g weight. Goal0.80×1.36m,
timber section45mm. All R16 worlds already used this geometry; no rebuild.

## Original communication requirements

The user objected to repeated computation/waiting. Own diagnosis/control-state
problems rather than blaming inherent difficulty. Prefer direct actions and
verifiable feedback with meaningful updates within about60 seconds. Do not repeat
permission requests for already authorized hot loads. During original compaction,
both physics processes continued; recovery required this file/new original
feedback, no STOP/SIGTERM or false complete/paused status for unfinished work.
These historical instructions do not reopen the completed worlds today.
