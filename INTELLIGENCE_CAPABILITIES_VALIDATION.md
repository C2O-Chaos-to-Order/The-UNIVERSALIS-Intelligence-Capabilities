# Intelligence Capabilities Contract Validation Record

**Original CI record:** 2026-11-12  
**Public-only contract revision updated:** 2026-11-18  
**Profile:** UNIVERSALIS  
**Branch:** implementation/repository-foundation-2026-11-12

## Executed checks

| Check | Result | GitHub Actions run |
|---|---|---|
| Intelligence Capabilities Contract | Passed | [Run 43241755277](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Capabilities/actions/runs/43241755277) |
| Repository quality baseline | Passed | [Run 43241754989](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Capabilities/actions/runs/43241754989) |

The listed runs are historical evidence for the initial mixed-profile validator revision only. They completed Python runtime setup, seven shared contract-family checks, eight negative cases, the then-current UNIVERSALIS local-first fixture, and the repository-quality baseline. They do not validate the public-only schema, validator, fixture, or workflow changes recorded on 2026-11-18.

## Contract families exercised

1. Multi-axis capability profile and benchmark evidence.
2. Attestation envelope with ML-DSA-5 / Ed25519 metadata and independent-verifier fields.
3. Plan DAG dependency and acyclicity checks.
4. Operational self-model calibration, limitations, process-health signals, and uncertainty.
5. Handle-based world-model request/response with raw-media/latent locality.
6. Compute-budget reconciliation and stopping criteria.
7. Bounded skill/harness improvement with strict held-out score gate and reviewer.
8. Sovereignty-boundary declaration.

## Negative tests in the initial CI-tested revision (8 cases)

1. Plan DAG cycle.
2. Compute-budget overspend.
3. Raw media embedded in a handle-based world-model request.
4. No strict held-out improvement.
5. Attempted model-weight modification.
6. Capability score outside declared axis scale.
7. Self-verification of an attestation.
8. UNIVERSALIS public boundary configured with egress default allow.

## What this establishes

- The earlier dependency-free semantic validator ran in GitHub Actions on the 2026-11-12 revision.
- The historical synthetic fixture passed the then-current UNIVERSALIS profile.
- Eight intended negative cases were rejected in those historical runs.
- The repository-quality baseline validated JSON syntax on that earlier revision.
- None of these results establishes that the 2026-11-18 public-only revision passes.

## Current public-only validator revision — 10 cases; CI PASSED 2026-11-18

The public contract is now UNIVERSALIS-only. The validator no longer contains the separate private-profile branch or private-permit rule. The public schema namespace is `urn:universalis:intelligence-capabilities:v1`; the only permitted boundary owner is `universalis`; deployment is `local_first`; every Plan DAG node requires a non-empty tool-scope reference; and public fixtures cannot carry a private policy reference. The workflow invokes the public-only check without a profile switch.

The validator includes ten negative cases:

1. Plan DAG cycle.
2. Compute-budget overspend.
3. Raw media embedded in a handle-based world-model request.
4. No strict held-out improvement.
5. Attempted model-weight modification.
6. Capability score outside the declared axis scale.
7. Self-verification of an attestation.
8. UNIVERSALIS public boundary configured with egress default allow.
9. Plan DAG node missing an explicit tool-scope reference.
10. Private policy reference present in a public boundary.

These changes were committed on 2026-11-18. The earlier run IDs above remain historical and do not validate this revision. The corrected public-only revision was executed successfully by GitHub Actions run [44379146071](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Capabilities/actions/runs/44379146071) on commit `2aacabe5961a90515a225d9e361e96d775252453` (push event, 2026-11-18). The run passed the positive/negative self-test, UNIVERSALIS profile validation, and repository-quality baseline step. This is synthetic contract validation, not integration or production assurance.

## Limits and unresolved work

- CI does not execute a full JSON Schema 2020-12 validator; the Python checker implements selected semantic invariants.
- ML-DSA-5 / Ed25519 signature bytes and Merkle proofs are not cryptographically verified. The fixture contains an explicitly synthetic placeholder signature and status unverified.
- NTI-1, AST analysis, signed tool-call enforcement, fail-closed handoff enforcement, and offline verifier are not integrated.
- No SymForge/SPIRAL planner, self-model runtime, world-model service, adaptive compute controller, SkillOpt/Harness² optimizer, benchmark runner, or sovereign platform has been installed or exercised.
- No real benchmark profile, real model/harness comparison, self-improvement gain, or sovereign runtime validation is claimed.
- Candidate performance figures and product feature claims remain supplied research claims pending canonical source, license, maintenance, security, compatibility, and independent reproduction.

## Next verification increment

Add a pinned standards-compliant JSON Schema 2020-12 validator and canonical test vectors for ML-DSA-5 / Merkle verification. Then implement one read-only Plan DAG dry-run and one mock world-model handle exchange before enabling real tool execution or self-improvement.
