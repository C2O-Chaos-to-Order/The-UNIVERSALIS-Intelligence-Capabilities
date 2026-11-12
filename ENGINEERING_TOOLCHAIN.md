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
