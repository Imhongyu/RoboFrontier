# Multi-arm LLM communication: research evidence and testable hypotheses

Recorded research date: **2026-10-29**. This English translation preserves the
original paper references and project hypotheses. It does not reverify current
paper revisions, claim an implemented protocol, or establish an improvement in
RoboFrontier. The Controller name below replaces the historical coordinating
role's display name; archived role IDs remain unchanged.

## Relevant papers in the recorded review

1. [Chen et al., Scalable Multi-Robot Collaboration with Large Language Models:
   Centralized or Decentralized Systems? (ICRA 2024)](https://arxiv.org/html/2309.15943v2)
   compares a centralized planner, per-robot distributed agents and two hybrid
   architectures. In HMAS-2, a center proposes, affected robots provide feedback,
   and the center revises; only action participants join the current discussion.
   The authors report hybrid benefits in four 2D collaboration settings and
   some 3D simulation. Their history ablation finds a favorable success/token
   tradeoff for state-action history in that setting. **Limits:** iterative
   planning/communication and agreed plans differ from continuous contact-rich
   operations; collision-inclusive failure metrics do not directly map to this
   suite's terminal scoring. **Hypothesis:** direct questions to relevant Workers,
   obtain local feedback through the Controller, avoid whole-team confirmation
   for every action, and preserve unresolved commitments in concise summaries.
2. [Zhang et al., Building Cooperative Embodied Agents Modularly with Large
   Language Models (CoELA, ICLR 2024)](https://arxiv.org/html/2307.02485v2)
   studies decentralized control, raw perception, communication cost and long
   multi-goal tasks in C-WAH and TDW-MAT. Its memory, planning and communication
   modules treat sending a message as optional. **Limits:** environments and
   low-level actions differ from MuJoCo multi-arm contact; adding modules does
   not establish effectiveness here. **Hypothesis:** let agents choose messages
   from local need and retrieve relevant observations, actions and outstanding
   commitments without broadcasting the whole conversation.
3. [Li et al., Improving Multi-Agent Debate with Sparse Communication Topology
   (EMNLP Findings 2024)](https://aclanthology.org/2024.findings-emnlp.427/)
   reports sparse topologies matching or exceeding denser ones at lower compute
   cost in GPT/Mistral debate settings. **Limits:** debate, reasoning and
   multimodal alignment are not realtime physical cooperation. A sparse graph
   does not ensure coordination on shared objects. **Hypothesis:** compare
   directed, bounded peer messages with broadcast, while preserving paths to
   every genuinely affected participant.
4. [Khatana et al., Verifier-Mediated Multi-LLM Coordination for Multi-Robot Path
   Planning (2026 preprint)](https://arxiv.org/html/2610.12761v1)
   uses a geometric verifier to report predicted conflict participants, positions
   and times to relevant agents, with CARLA/Crazyflie experiments. **Limits:**
   navigation and a particular planner/verifier differ from visual manipulation;
   a prediction is not a continuous-physics safety proof. **Hypothesis:** explore
   voluntary candidate-motion checks with explicit coverage/uncertainty, without
   exposing private ground truth or judge results, or presenting existing
   advisory checks as collision guarantees.
5. [Pappu et al., Multi-Agent Teams Hold Experts Back
   (ICML 2026)](https://proceedings.mlr.press/v306/pappu26a.html)
   studies free-form teams on human-inspired and machine-learning benchmarks,
   reporting frequent underperformance against the best individual and diluted
   expert opinions in discussion. **Limits:** this is not multi-arm manipulation
   and does not prove Single must outperform here. **Hypothesis:** keep a fair
   Single control; more agents or communication do not guarantee better results.

## Testable design directions

- **Reliability first.** Validate startup, identity/authority, message delivery,
  termination and durable records for Single, Controller + Worker and
  Worker-Worker before interpreting stalls. Otherwise model limitations and
  infrastructure failures cannot be distinguished. Adaptive remains a separate
  dynamic-delegation configuration and comparator.
- **Minimal relevant shared information.** Send only public information relevant
  to the recipient's work. Suggested messages include scope, evidence source/time,
  the next actionable condition and release condition. Free text may express
  different purposes; mandatory fields must not deadlock tasks. This changes
  prompts and needs versioning plus a comparison against the existing condition.
- **Nonblocking negotiation.** While a shared resource is unavailable, an agent
  can perform nonconflicting local work. Coordinate among affected agents rather
  than requiring whole-team approval. Current skills already express similar
  rules; test actual compliance instead of assuming the capability is absent.
- **Summaries can lose important information.** Summarize only legally observed
  information. Preserve active constraints, action state, version/time,
  unresolved requests and uncertainty, together with original messages and
  provenance. Guard against stale summaries, overwritten conflicts and treating
  others' guesses as facts. Automatic generation and its extra token cost need
  explicit controlled comparisons.
- **Advice versus automatic policy.** The system must not secretly assign
  pick/place routes, prescribe strategy or import Oracle information. A shared
  board, scheduling assistant or automatically inferred conflict changes the
  experimental protocol if it changes visible information or role freedom.
  Do not pool its results with the unchanged protocol.

## Comparisons and metrics

Keep task, assets, initial state, public information, physics and scoring aligned.
Declare how startup/reading time is counted and freeze config/prompt versions
in manifests. Each topology has its own world. A declared Dial comparison may
share an instance without exposing its private answer.

First validate identity, receipt/deduplication, interleaving, uncertain actions,
turn-ending and termination offline; then perform a small bounded real run.
Measure terminal success/progress, wall time, tokens/cost, message count/length,
end-to-end delivery and wake latency, waiting/blocking, execution overlap, process
events and system failures. Repeat seeds and report missing/uncertain data.
Do not attribute all model tokens to communication merely because messages exist.

Topologies inherently differ in roles, history inheritance and message graphs.
Not every condition can be identical. State that the experiment compares complete
collaboration systems rather than claiming to change only one variable.
