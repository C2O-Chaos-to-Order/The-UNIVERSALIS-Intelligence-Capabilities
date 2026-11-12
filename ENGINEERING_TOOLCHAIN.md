# Engineering Toolchain and Initial Build Plan

**Repository:** `C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Capabilities`  
**Responsibility:** Intelligence Capabilities  
**Status:** Initial executable foundation in this branch; domain candidates remain proposed pending verification.  
**Boundary:** Open UNIVERSALIS / independently operable. No C2O-private credentials, policies, authority state, or restricted operational data.

## Universal engineering foundation

- Least-privilege GitHub Actions CI, automated tests, and JSON contract/config validation.
- CodeQL/static analysis, secret scanning, dependency review, Dependabot, actionlint, and SBOM generation after settings, ownership, and outputs are verified.
- CycloneDX/SPDX, OSV-Scanner, Trivy/Grype, Gitleaks, SLSA provenance, in-toto attestations, cosign signing, and immutable releases as staged assurance capabilities.
- Pin toolchain versions and action references; preserve specifications, fixtures, execution logs, provenance, limitations, and version history.

**Foundation candidates:** Secure SDLC Evidence Collector; repo-assurance; Chainguard Actions; cnspec SBOM Cataloger; CodeQL; actionlint; OSV-Scanner; Trivy/Grype; Gitleaks; SLSA/in-toto; cosign. These are research candidates, not assumed integrations.

## Domain-specific candidate tools

@continua-ai/wheelie-capability-core for typed capability SDK/testkit; dummy-a2a for A2A 1.0 client/extension testing; Agent Conformance Testing for shared YAML behavior specs; agentic-dataset-conformance for claims-as-tests; @absolutejs/agent-conformance for adversarial MCP/A2A/Arazzo/WebMCP checks; @openwop/openwop-conformance for workflow-protocol contracts.

Verify each candidate's source, license, maintainer, release activity, security, compatibility, data flow, and claims before adoption. A capability advertised by a tool is not evidence that this repository has implemented it.

## Initial executable implementation

- `.github/workflows/repository-quality.yml` runs on pushes and pull requests with read-only repository permissions.
- `.github/scripts/repository_quality_baseline.py` provides a dependency-free self-test and validates JSON in schema/manifest/contract/capability/skill directories plus `package.json` and `tsconfig.json`.
- This is a deliberately narrow first check, not a substitute for domain conformance, CodeQL, secret scanning, SBOMs, or privacy review.

## Next increments

1. Audit existing source, schemas, fixtures, workflows, permissions, and dependencies.
2. Add repository-native contracts and positive/negative test fixtures.
3. Integrate the domain harness after source/license/security review.
4. Publish test, dependency, SBOM, and provenance evidence.
5. Record failures and unresolved items honestly; no unexecuted check receives pass credit.

## Evidence status

| Item | Status |
|---|---|
| Tool candidates recorded | Documented |
| Baseline validator and CI authored | Implemented in this branch |
| GitHub Actions execution | Pending |
| Domain candidate verification | Pending |
| Specialized integration | Not yet implemented |

## Cross-repository architecture register — 2026-11-12

The following are the canonical working records for the latest owner-supplied toolchain proposals. This repository records the references and boundary rules; implementation belongs in the domain-owning repositories.

### Human Knowledge
- [C2O Human Knowledge architecture](https://github.com/C2O-Chaos-to-Order/The-C2O-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_ARCHITECTURE.md), [shared MCP interface contracts](https://github.com/C2O-Chaos-to-Order/The-C2O-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/MCP_INTERFACE_CONTRACTS.md), and [validation evidence](https://github.com/C2O-Chaos-to-Order/The-C2O-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_VALIDATION.md).
- [UNIVERSALIS Human Knowledge architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_ARCHITECTURE.md), [shared MCP interface contracts](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/MCP_INTERFACE_CONTRACTS.md), and [validation evidence](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_VALIDATION.md).

### OS provisioning and virtualization
- [C2O private provisioning architecture](https://github.com/C2O-Chaos-to-Order/The-C2O-Ecosystem/blob/implementation/repository-foundation-2026-11-12/OS_PROVISIONING_ARCHITECTURE.md).
- [UNIVERSALIS open provisioning architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Ecosystem/blob/implementation/repository-foundation-2026-11-12/OS_PROVISIONING_ARCHITECTURE.md).

### UNIVERSALIN Grid, Guardian, and Golden Compass
- [C2O boundary and verifier architecture](https://github.com/C2O-Chaos-to-Order/The-C2O-Ecosystem/blob/implementation/repository-foundation-2026-11-12/UNIVERSALIN_GUARDIAN_GOLDEN_COMPASS.md).
- [UNIVERSALIS Grid / Guardian / Compass architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Ecosystem/blob/implementation/repository-foundation-2026-11-12/UNIVERSALIN_GUARDIAN_GOLDEN_COMPASS.md).

### Boundary and evidence status
C2O-private credentials, policies, identity state, authority tokens, private source text, and operational evidence remain inside authorized C2O environments. UNIVERSALIS remains public, local-first, inspectable, and independently operable. Only versioned, explicitly approved interface schemas and evidence packages may cross the boundary; an interface does not grant authority.

All named external tools remain owner-supplied candidates or reference patterns pending canonical-source, license, maintainer, release, security, compatibility, and claim verification. No candidate is represented as installed or adopted merely because it appears in these records.

## Powers energy architecture register — 2026-11-12

Powers treat energy efficiency as a measurable, enforceable, auditable capacity—not only a permission or evaluation. In the current UNIVERSALIS repository set, the canonical implementation is maintained in the Intelligence Powers repository.

- **Canonical open architecture:** [UNIVERSALIS Powers energy architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Powers/blob/implementation/repository-foundation-2026-11-12/POWERS_ENERGY_ARCHITECTURE.md).
- **Shared v1 contract:** [Powers energy schema](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Powers/blob/implementation/repository-foundation-2026-11-12/schemas/powers/powers-energy-contracts.v1.schema.json).
- **Executed checks and limitations:** [Powers validation record](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Powers/blob/implementation/repository-foundation-2026-11-12/POWERS_ENERGY_VALIDATION.md).

The open implementation is local-first and independently operable. Measurement, forecasting, receipts, and synergy calculation do not require a central database or truth authority. It keeps actual workload telemetry and local policy in the operator's chosen environment. The shared contract excludes private credentials and policy values. PDU/RAPL/Kepler/GPU layers require overlap reconciliation; synergy comparisons require matched workload cohorts and SLO profiles. External tools and their advertised savings remain candidates until independently verified.

## Four-document source coverage — 2026-11-12

The complete owner-supplied tool inventory and status matrix for Human Knowledge, Powers, Human Capabilities, and Mapping/Matrix/Organization/Ecosystem Mapping is maintained in the UNIVERSALIS research register: https://github.com/C2O-Chaos-to-Order/Research-for-the-UNIVERSALIS-Ecosystem/blob/implementation/repository-foundation-2026-11-12/FOUR_DOCUMENT_TOOLCHAIN_COVERAGE.md.

Treat every third-party name in that register as a proposed candidate/reference pattern until canonical source, license, maintenance, security, compatibility, and behavior are reviewed. The register distinguishes documented tools, basic contracts, passing CI, and actual integrations. This repository owns only the parts assigned to its domain. No C2O-private repository links or policy values are part of this public register.

## Intelligence Capabilities implementation

See INTELLIGENCE_CAPABILITIES_ARCHITECTURE.md for the complete owner-supplied tool inventory and the boundary-specific build posture. Shared contract definitions are in schemas/intelligence-capabilities/intelligence-capability-contracts.v1.schema.json; profile-specific synthetic fixtures and semantic checks are in examples/intelligence_capabilities/contracts.v1.json and .github/scripts/intelligence_capability_contract.py. Third-party products remain candidates pending verification.

Intelligence Capabilities contract CI passed. The exact run IDs, negative cases, and outstanding cryptographic, benchmark, and product-integration work are recorded in INTELLIGENCE_CAPABILITIES_VALIDATION.md.

## Master toolchain coverage register — 2026-11-12

The current public inventory for the original four toolchain documents plus the Intelligence Capabilities source is maintained in the UNIVERSALIS research register: https://github.com/C2O-Chaos-to-Order/Research-for-the-UNIVERSALIS-Ecosystem/blob/implementation/repository-foundation-2026-11-12/TOOLCHAIN_COVERAGE_REGISTER.md. It distinguishes documentation, basic contracts, passing CI, and actual integrations. This public register contains no links to C2O-private owner repositories or policy values.
