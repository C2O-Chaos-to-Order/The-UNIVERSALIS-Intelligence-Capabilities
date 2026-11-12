# UNIVERSALIS Intelligence Capabilities Architecture

**Owner:** UNIVERSALIS / MotherThread  
**Posture:** Open, inspectable, independently operable, and portable.  
**Status:** Shared contract and semantic-test foundation implemented in this branch. Third-party tools remain candidates pending verification.

## 1. Capability architecture

UNIVERSALIS Intelligence Capabilities are composable mechanisms for planning, self-model calibration, world-model interaction, adaptive inference-time compute, skill/harness improvement, and benchmark attestation. Each capability has explicit inputs, budgets, outputs, evidence, and limitations. A benchmark score is not a complete description of an agent and is not an authorization grant.

## 2. Open candidate inventory from the supplied document

### Reasoning, planning, and neuro-symbolic control
- SymForge: MCP tool-orchestration planner using HTN and backward chaining, producing a checked Plan DAG before tool execution.
- SPIRAL (IBM / AAAI-2026 as stated in source): tri-agent generation, grounding, and reflection architecture within an MCTS search loop.
- Cognitive Kernel-Pro: modular hierarchical agent framework with Python action space and specialist agents for navigation, file handling, and tool invocation.

### Meta-cognition and self-model
- open-agents-ai: agent-as-organism architecture with environment/process health, context assembly, episodic memory, cognitive map, action gating, temporal hierarchy, self-model, skill chunks, and safety/limits.
- meta_cognitive_self_model_agents: modular agent self-model framework with RL, hybrid, and dummy policies, monitoring, and metrics.
- cuda-self-model: Rust self-modeling, metacognition, capability calibration, limitation awareness, and growth tracking.
- elume: deterministic, replay-safe cognitive substrate with CognitiveCore, MetacognitiveParticle, and MentalAction primitives.

A self-model means an operational snapshot of calibration, limitations, process health, and uncertainty. It does not establish subjective experience, consciousness, or personhood.

### World models as callable tools
- wm-mcp: handle-based MCP interaction with a video world model; operations embed_video, predict, surprise, and compare.
- Qwen-AgentWorld: language-based world-model candidate for simulating agentic environments and next-state prediction across seven domains, with AgentWorldBench.

Raw media, model latents, and private representations stay within the world-model service. Interoperability exchanges opaque handle IDs and bounded metrics, not raw video or latent tensors. Responses expose task outputs and provenance, not private chain-of-thought.

### Inference-time compute scaling and adaptive control
- Agentic Meta-Reasoning: controller/worker pattern that maintains established task state, explores options, estimates value under a remaining budget, and dispatches task-level work.
- MOSAIC: strategic, tactical, and operational reasoning scales with separate context scopes and a learned scale scheduler.
- TrACE: training-free adaptive compute allocation per agent timestep using inter-rollout action agreement.
- Evolving Infra: adaptive serving and KV-cache management for agent workloads.

### Skill acquisition and self-improvement
- SkillOpt / SkillOpt-Sleep: skill-document optimization with rollout/epoch discipline and held-out validation; offline harvest, mine, replay, and consolidate loop.
- Harness² (Google Research / Apache-2.0 as stated in source): task-level propose → probe → compose and meta-level improvement of the harness (prompts, guardrails, memory, skills, tools, scripts, subagents, plugins).
- hermes-agent-camel: experience-driven skill creation/refinement with a CaMeL-style safety boundary.
- purpose-agent: local-first self-improvement kernel without fine-tuning or required cloud infrastructure.

Shared rule: optimize bounded skill/harness artifacts, not model weights. Candidate edits are proposals; acceptance requires strict improvement on the same held-out suite, independent review, and versioned release.

### Capability attestation and benchmarking
- Janus Labs: multi-axis coding-agent profile with Code Quality, Error Resilience, and optional Instruction Resilience axes.
- Agent Effectiveness Index (AEI): organisational-process learning benchmark with execution, transfer, and retention dimensions.
- AgenticBench: measurement protocol for what coding agents do on a developer's machine.
- Exgentic: cross-agent, cross-benchmark evaluation harness.
- NTI Public Compliance Leaderboard / NTI-1: source describes signed tool calls, fail-closed handoffs, Merkle audit trails, and ML-DSA-5 post-quantum attestation.

Benchmark scores, leaderboard results, tool counts, comparative results, and technical claims above are source-supplied research claims, not independently verified here. MOSAIC occurs in more than one supplied tool context; verify project identity/version before treating those references as one dependency.

## 3. Shared contracts implemented in this branch

The normative schema is schemas/intelligence-capabilities/intelligence-capability-contracts.v1.schema.json. It defines eight contract families:
1. Multi-axis capability profile with benchmark suite hash/version, task references, environment identity, limitations, and attestation.
2. Attestation envelope with ML-DSA-5 / Ed25519 metadata, statement digest, Merkle root, signer, independent verifier, timestamp, and offline bundle reference.
3. Plan DAG with dependencies, preconditions, postconditions, tool-scope and verification references.
4. Operational self-model state with capability calibration, evidenced limitations, process-health signals, and uncertainty.
5. Handle-based world-model request/response: embed_video, predict, surprise, compare.
6. Compute budget with unit, total limit, per-step allocations, reconciled remaining amount, and stopping criteria.
7. Bounded self-improvement proposal with artifact hashes, bounded edits, propose/probe/compose stage, held-out score comparison, review, and release reference.
8. Sovereignty-boundary declaration.

Synthetic fixtures are in examples/intelligence_capabilities/contracts.v1.json. The dependency-free validator is .github/scripts/intelligence_capability_contract.py.

## 4. UNIVERSALIS enforcement posture

- Core contract validation and evidence inspection remain independently operable; cloud services are optional adapters.
- Capability profiles identify benchmark version, suite hash, protocol, environment, task evidence, axes, and limitations.
- Attestation requires an independent verifier; producers cannot verify their own scores.
- Plan DAG dependencies must be acyclic and every node requires a verification reference.
- Self-model data is limited to operational calibration, limitations, process health, and uncertainty.
- World-model calls exchange opaque handles; raw media and latent payloads stay local to the service.
- Compute allocations reconcile to the grant and include stopping criteria.
- Skill/harness edits require strict held-out improvement and independent review; model-weight updates are outside this contract.
- Operators control their own storage, model endpoints, egress, compute budget, and acceptance thresholds.

## 5. Limits and next steps

The validator checks selected semantic invariants and synthetic fixtures. It does not cryptographically verify ML-DSA-5/Ed25519 signatures or Merkle proofs, execute a world model, measure benchmark scores, run a planning engine, or deploy adaptive compute controls.

Next: install a pinned JSON Schema 2020-12 validator; add Janus/AEI/AgenticBench/Exgentic interchange fixtures; implement a Plan DAG dry-run executor; add an opaque-handle world-model mock; run fixed held-out skill/harness benchmarks; verify NTI-1/ML-DSA-5 against canonical specifications and independent test vectors.

## 6. Evidence status

| Item | Status |
|---|---|
| Owner-supplied UNIVERSALIS candidate inventory | Documented |
| Eight shared contract families | Implemented in this branch |
| Synthetic fixtures and ten negative semantic tests | Implemented in this branch |
| Dedicated CI workflow | Passed — see INTELLIGENCE_CAPABILITIES_VALIDATION.md |
| Third-party tools installed/integrated | None independently verified |
| Cryptographic verification and full JSON Schema validation | Pending |
| Real capability benchmark and self-improvement results | Not performed |


**Validation note:** The initial eight-case contract revision passed the recorded CI runs. The current branch strengthens C2O plan-node tool-scope and human-permit enforcement and now contains ten negative cases; a new GitHub Actions run for that exact revision is still pending/unavailable. See INTELLIGENCE_CAPABILITIES_VALIDATION.md for the distinction.
