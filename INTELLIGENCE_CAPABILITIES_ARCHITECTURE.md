# UNIVERSALIS Intelligence Capabilities Architecture

**Owner:** UNIVERSALIS / MotherThread  
**Posture:** Open, inspectable, independently operable, and portable.  
**Status:** First shared contract and semantic-test foundation implemented in this branch. External products remain candidates pending source, license, security, maintenance, and compatibility review.

## 1. Capability architecture

UNIVERSALIS Intelligence Capabilities are composable mechanisms for planning, self-model calibration, world-model interaction, adaptive inference-time compute, skill/harness improvement, and benchmark attestation. Capabilities have explicit inputs, budgets, outputs, evidence, and limitations. A benchmark score is not a complete description of an agent and is not an authorization grant.

## 2. Full open candidate inventory from the supplied document

### Reasoning, planning, and neuro-symbolic control

- **SymForge:** MCP tool-orchestration planner using HTN and backward chaining, producing a mathematically checked Plan DAG before tool execution.
- **SPIRAL (IBM / AAAI-2026 as stated in source):** tri-agent generation, grounding, and reflection architecture within an MCTS search loop.
- **Cognitive Kernel-Pro:** modular hierarchical agent framework with Python action space and specialist agents for web navigation, file handling, and tool invocation.

The proposed combination is a verifiable planning substrate, search-based self-correction, and open modular agent foundation. Candidate claims and results are not independently verified in this branch.

### Meta-cognition and self-model

- **open-agents-ai:** agent-as-organism architecture with environment/process health, global workspace/context assembly, episodic memory, cognitive map, action gating, temporal hierarchy, self-model, skill chunks, and safety/limits.
- **meta_cognitive_self_model_agents:** modular agent self-model framework with RL, hybrid, and dummy policies, self-model monitoring, and scientific metrics.
- **cuda-self-model:** Rust self-modeling, metacognition, capability calibration, limitation awareness, and growth tracking.
- **elume:** deterministic, replay-safe cognitive substrate with CognitiveCore, MetacognitiveParticle, and MentalAction primitives.

A self-model here means an operational snapshot of calibration, limitations, process health, and uncertainty. It does not establish subjective experience, consciousness, or personhood.

### World models as callable tools

- **wm-mcp:** handle-based MCP interaction with a video world model; operations are embed_video, predict, surprise, and compare.
- **Qwen-AgentWorld:** language-based world-model candidate for simulating agentic environments and next-state prediction across seven domains, with AgentWorldBench.

Raw media, model latents, and private representations remain within the world-model service. Interoperability exchanges opaque handle IDs and bounded metrics, not raw video or latent tensors. Responses expose task outputs and provenance, not private chain-of-thought.

### Inference-time compute scaling and adaptive control

- **Agentic Meta-Reasoning:** controller/worker pattern that maintains established task state, explores options, estimates their value under a remaining budget, and dispatches task-level work.
- **MOSAIC:** strategic, tactical, and operational reasoning scales with separate context scopes and a learned scale scheduler.
- **TrACE:** training-free adaptive compute allocation per agent timestep using inter-rollout action agreement.
- **Evolving Infra:** adaptive serving and KV-cache management for agent workloads.

### Skill acquisition and self-improvement

- **SkillOpt / SkillOpt-Sleep:** skill-document optimization with rollout/epoch discipline and held-out validation; offline harvest, mine, replay, and consolidate loop.
- **Harness² (Google Research / Apache-2.0 as stated in source):** task-level propose → probe → compose and meta-level improvement of the harness (prompts, guardrails, memory, skills, tools, scripts, subagents, plugins).
- **hermes-agent-camel:** experience-driven skill creation/refinement with a CaMeL-style safety boundary.
- **purpose-agent:** local-first self-improvement kernel without fine-tuning or required cloud infrastructure.

Shared self-improvement rule: optimize bounded skill/harness artifacts, not model weights. Candidate edits are proposals; acceptance requires strict improvement on the same held-out suite, with independent review and a versioned release record.

### Capability attestation and benchmarking

- **Janus Labs:** multi-axis coding-agent profile with Code Quality, Error Resilience, and optional Instruction Resilience axes.
- **Agent Effectiveness Index (AEI):** organisational-process learning benchmark with execution, transfer, and retention dimensions.
- **AgenticBench:** measurement protocol for what coding agents do on a developer's machine.
- **Exgentic:** cross-agent, cross-benchmark evaluation harness.
- **NTI Public Compliance Leaderboard / NTI-1:** source describes signed tool calls, fail-closed handoffs, Merkle audit trails, and ML-DSA-5 post-quantum attestation.

All benchmark scores, leaderboard results, tool counts, comparative results, and technical feature claims above are source-supplied research claims, not independently verified here. MOSAIC appears in more than one supplied capability context; verify exact repository, project identity, and version before merging those references into a single dependency.

## 3. Shared contracts implemented in this branch

The normative shared schema is schemas/intelligence-capabilities/intelligence-capability-contracts.v1.schema.json. It defines eight contract families:

1. **Capability profile:** multi-axis score, benchmark suite hash/version, task references, environment/harness identity, limitations, and attestation.
2. **Attestation envelope:** ML-DSA-5 / Ed25519 scheme metadata, statement digest, Merkle root, signer, independent verifier, timestamp, and offline bundle reference.
3. **Plan DAG:** node identities, dependencies, preconditions, postconditions, tool-scope reference, and verification reference.
4. **Operational self-model:** capability calibration, evidenced limitations, process-health signals, and uncertainty.
5. **Handle-based world-model request/response:** embed_video, predict, surprise, compare, opaque handles, and returned result handles/metrics.
6. **Compute budget:** unit, total limit, per-step allocations, reconciled remaining amount, and stopping criteria.
7. **Bounded self-improvement proposal:** target artifact and hashes, bounded edits, propose/probe/compose stage, held-out score comparison, review, and release reference.
8. **Sovereignty-boundary declaration:** ownership, deployment mode, data/model/traffic residency, egress, and audit requirement.

Synthetic fixtures are in examples/intelligence_capabilities/contracts.v1.json. The dependency-free validator is .github/scripts/intelligence_capability_contract.py.

## 4. UNIVERSALIS enforcement posture

- Core contract validation and evidence inspection must remain independently operable; cloud services and proprietary model APIs are optional adapters, not required for the contract layer.
- Capability profiles identify the benchmark version, suite hash, protocol, environment, task-level evidence, axes, and limitations.
- Attestation must be verified by an independent party; producers cannot verify their own scores.
- Plan DAG dependencies must be acyclic. Every node must have a verification reference and an explicit tool scope where needed.
- Self-model state is limited to operational calibration, limitations, process health, and uncertainty.
- World-model calls exchange opaque handles. Raw media and latent payloads stay local to the world-model service.
- Compute allocations reconcile exactly to the granted total and include stopping criteria.
- Skill/harness edits require strict improvement on a held-out suite and independent review; model-weight updates are outside this contract.
- Operators control their own storage, model endpoints, egress, compute budget, and acceptance thresholds.

## 5. Limits and next steps

The current validator checks selected semantic invariants and synthetic fixtures. It does not cryptographically verify ML-DSA-5/Ed25519 signatures or Merkle proofs, execute a world model, measure benchmark scores, run a planning engine, or deploy adaptive compute controls.

Next increments:
1. Pin and install a full JSON Schema 2020-12 validator.
2. Add conformance fixtures for Janus, AEI, AgenticBench, and Exgentic profile interchange.
3. Implement a Plan DAG parser/validator and a no-side-effect dry-run executor with explicit tool scopes.
4. Add a local opaque-handle mock for wm-mcp and privacy/egress tests.
5. Implement a fixed held-out harness/skill benchmark and proposal-only optimizer; require reviewer approval before release.
6. Verify NTI-1 / ML-DSA-5 against its canonical specification and independent test vectors before marking any signature verified.

## 6. Evidence status

| Item | Status |
|---|---|
| Owner-supplied UNIVERSALIS candidate inventory | Documented |
| Eight shared contract families | Implemented in this branch |
| Synthetic fixtures and eight negative semantic tests | Implemented in this branch |
| Dedicated CI workflow | Authored; run evidence pending |
| Third-party tools installed/integrated | None independently verified |
| Cryptographic verification and full JSON Schema validation | Pending |
| Real capability benchmark and self-improvement results | Not performed |
