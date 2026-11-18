#!/usr/bin/env python3
"""Semantic checks for portable Intelligence Capabilities contracts."""
from __future__ import annotations
import argparse, copy, json, math, sys
from datetime import datetime
from pathlib import Path
FIXTURE = Path("examples/intelligence_capabilities/contracts.v1.json")
FORBIDDEN_WORLD_MODEL_FIELDS = {"raw_video","video_bytes","raw_media","pixels","frame_bytes","latent_tensor","latents","embedding_values","raw_frames"}
def timestamp(value,label):
    if not isinstance(value,str): raise ValueError(f"{label} must be an ISO-8601 timestamp")
    try: parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError as exc: raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None: raise ValueError(f"{label} must include an explicit timezone")
    return parsed
def validate_attestation(a):
    for field in ("statement_sha256","merkle_root"):
        if len(a.get(field,""))!=64: raise ValueError(f"{field} must be a SHA-256 digest")
    timestamp(a["issued_at"],"attestation.issued_at")
    if not a.get("signature") or not a.get("offline_bundle_ref"): raise ValueError("attestation requires signature material and offline bundle reference")
    if a["verification_status"]=="verified":
        if not a.get("verified_by") or a["verified_by"]==a["signer_ref"]: raise ValueError("attestation requires an independent verifier")
        if not a.get("verified_at"): raise ValueError("verified attestation requires a verification timestamp")
        if a["scheme"]=="none": raise ValueError("unsigned attestation cannot be verified")
        if any(not x["passed"] for x in a.get("fail_closed_handoff_tests",[])): raise ValueError("failed handoff test blocks verified attestation")
    elif a.get("verified_by") or a.get("verified_at"): raise ValueError("non-verified attestation cannot carry a completed verifier identity")
    if a.get("verified_at"): timestamp(a["verified_at"],"attestation.verified_at")
    # Structural checks only: no cryptographic ML-DSA-5/Ed25519 signature or Merkle proof verification.
def validate_profile(p):
    start=timestamp(p["benchmark"]["started_at"],"benchmark.started_at"); end=timestamp(p["benchmark"]["completed_at"],"benchmark.completed_at"); issued=timestamp(p["attestation"]["issued_at"],"attestation.issued_at")
    if end<start or issued<end: raise ValueError("benchmark and attestation timestamps are out of order")
    if not p["benchmark"]["reproducible"] or not p["benchmark"]["held_out"]: raise ValueError("portable profile requires reproducible held-out evaluation")
    ids=[a["axis_id"] for a in p["axes"]]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate capability axes")
    for axis in p["axes"]:
        if axis["scale_max"]<=axis["scale_min"] or not axis["scale_min"]<=axis["score"]<=axis["scale_max"]: raise ValueError("capability score falls outside declared scale")
    if p["overall"]["aggregation_method"]=="arithmetic_mean":
        expected=sum(a["score"] for a in p["axes"])/len(p["axes"])
        if not math.isclose(expected,p["overall"]["score"],rel_tol=1e-9,abs_tol=1e-9): raise ValueError("overall score does not match arithmetic mean")
    validate_attestation(p["attestation"])
def validate_plan(p):
    timestamp(p["created_at"], "plan.created_at")
    nodes = p["nodes"]
    ids = [node["node_id"] for node in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate plan node IDs")

    known = set(ids)
    degree = {node_id: 0 for node_id in ids}
    children = {node_id: [] for node_id in ids}
    for node in nodes:
        if not node.get("verification_ref"):
            raise ValueError("every plan node requires a verification reference")
        scope_ref = node.get("tool_scope_ref")
        if not isinstance(scope_ref, str) or not scope_ref.strip():
            raise ValueError("every UNIVERSALIS Plan DAG node requires an explicit tool-scope reference")
        for dependency in node["depends_on"]:
            if dependency not in known:
                raise ValueError("plan dependency references an unknown node")
            if dependency == node["node_id"]:
                raise ValueError("plan node cannot depend on itself")
            degree[node["node_id"]] += 1
            children[dependency].append(node["node_id"])

    queue = [node_id for node_id, value in degree.items() if value == 0]
    visited = 0
    while queue:
        node_id = queue.pop()
        visited += 1
        for child in children[node_id]:
            degree[child] -= 1
            if degree[child] == 0:
                queue.append(child)
    if visited != len(nodes):
        raise ValueError("plan dependencies contain a cycle")

def validate_self_model(s):
    timestamp(s["observed_at"],"self_model.observed_at")
    if not s["limitations"]: raise ValueError("self-model must disclose evidence-backed limitations")
    if not 0<=s["uncertainty"]<=1: raise ValueError("self-model uncertainty out of range")
    for c in s["capability_calibrations"]:
        if not 0<=c["estimated_level"]<=1: raise ValueError("capability calibration out of range")
        timestamp(c["last_assessed_at"],"self_model.last_assessed_at")
    for x in s["process_health"]["signals"]: timestamp(x["observed_at"],"self_model.signal.observed_at")

def walk_handles(value):
    if isinstance(value,dict):
        if FORBIDDEN_WORLD_MODEL_FIELDS.intersection(k.lower() for k in value): raise ValueError("world-model exchange must use opaque handles, not raw media/latent payloads")
        for v in value.values(): walk_handles(v)
    elif isinstance(value,list):
        for v in value: walk_handles(v)

def validate_world(req,res):
    if req["request_id"]!=res["request_id"]: raise ValueError("world-model request/response IDs do not match")
    if not req["privacy"]["raw_media_stays_local"] or not req["privacy"]["latents_stay_local"]: raise ValueError("raw media and latents must stay local to world-model service")
    if not req["handles"]: raise ValueError("world-model request requires opaque handles")
    handles=[h["handle_id"] for h in req["handles"]]
    if len(handles)!=len(set(handles)): raise ValueError("world-model request contains duplicate handles")
    walk_handles(req); walk_handles(res)

def validate_budget(b):
    timestamp(b["issued_at"],"compute_budget.issued_at")
    total=b["total_budget"]["limit"]; allocations=b["allocations"]; allocated=sum(x["amount"] for x in allocations)
    if any(x["amount"]<0 for x in allocations) or b["remaining"]<0: raise ValueError("compute budget amounts cannot be negative")
    steps=[x["step_id"] for x in allocations]
    if len(steps)!=len(set(steps)): raise ValueError("compute budget has duplicate step allocations")
    if allocated+b["remaining"]>total+1e-9: raise ValueError("compute allocations exceed granted budget")
    if not math.isclose(allocated+b["remaining"],total,rel_tol=1e-9,abs_tol=1e-9): raise ValueError("allocations plus remaining must reconcile to grant")

def validate_improvement(p):
    if p["baseline_sha256"] == p["candidate_sha256"]:
        raise ValueError("candidate must change artifact hash")
    if p["model_weights_changed"] is not False:
        raise ValueError("contract does not authorize model-weight changes")
    gate = p["held_out_gate"]
    if p["loop_stage"] in {"probe", "compose"}:
        improved = (
            gate["candidate_score"] > gate["baseline_score"]
            if gate["objective"] == "maximize"
            else gate["candidate_score"] < gate["baseline_score"]
        )
        if gate["strict_improvement"] != improved or gate["passed"] != improved:
            raise ValueError("held-out gate passes only on strict improvement")
    if p["review"]["status"] == "approved":
        if not gate["passed"] or not p["review"].get("reviewer_ref"):
            raise ValueError("approved proposal requires a passed held-out gate and reviewer")


def validate_boundary(boundary):
    if boundary["owner"] != "universalis":
        raise ValueError("UNIVERSALIS requires an independently owned public boundary")
    if boundary["deployment_mode"] != "local_first":
        raise ValueError("UNIVERSALIS requires a local-first deployment boundary")
    if boundary["egress_default"] != "deny" or boundary["audit_required"] is not True:
        raise ValueError("UNIVERSALIS requires deny-by-default egress and an audit trail")
    if boundary.get("policy_ref"):
        raise ValueError("public UNIVERSALIS fixtures cannot contain private policy references")
    if not (
        boundary["data_residency"]
        == boundary["model_weights_residency"]
        == boundary["inference_traffic_residency"]
    ):
        raise ValueError("UNIVERSALIS data, model weights, and inference traffic must share the declared local-first boundary")

def validate_all(f):
    validate_profile(f["capability_profile"])
    validate_plan(f["plan_dag"])
    validate_self_model(f["self_model_state"])
    validate_world(f["world_model_request"], f["world_model_response"])
    validate_budget(f["compute_budget"])
    validate_improvement(f["self_improvement_proposal"])
    validate_boundary(f["sovereignty_boundary"])
def load(root): return json.loads((root/FIXTURE).read_text(encoding="utf-8"))
def self_test(root):
    fixture = load(root)
    validate_all(fixture)
    tests = []

    bad = copy.deepcopy(fixture["plan_dag"])
    bad["nodes"][0]["depends_on"] = ["execute"]
    tests.append((lambda: validate_plan(bad), "plan DAG cycle"))

    bad = copy.deepcopy(fixture["compute_budget"])
    bad["allocations"][0]["amount"] = 9000
    tests.append((lambda: validate_budget(bad), "compute budget overspend"))

    bad = copy.deepcopy(fixture["world_model_request"])
    bad["raw_video"] = "embedded"
    tests.append((lambda: validate_world(bad, fixture["world_model_response"]), "raw media in handle request"))

    bad = copy.deepcopy(fixture["self_improvement_proposal"])
    bad["held_out_gate"]["candidate_score"] = bad["held_out_gate"]["baseline_score"]
    tests.append((lambda: validate_improvement(bad), "no strict held-out improvement"))

    bad = copy.deepcopy(fixture["self_improvement_proposal"])
    bad["model_weights_changed"] = True
    tests.append((lambda: validate_improvement(bad), "model weight change"))

    bad = copy.deepcopy(fixture["capability_profile"])
    bad["axes"][0]["score"] = 120
    tests.append((lambda: validate_profile(bad), "capability score outside scale"))

    bad = copy.deepcopy(fixture["capability_profile"])
    attestation = bad["attestation"]
    attestation["verification_status"] = "verified"
    attestation["verified_by"] = attestation["signer_ref"]
    attestation["verified_at"] = "2026-11-12T10:22:00Z"
    tests.append((lambda: validate_profile(bad), "self-verified attestation"))

    bad = copy.deepcopy(fixture["sovereignty_boundary"])
    bad["egress_default"] = "allow"
    tests.append((lambda: validate_boundary(bad), "UNIVERSALIS egress default allow"))

    bad = copy.deepcopy(fixture["plan_dag"])
    bad["nodes"][0]["tool_scope_ref"] = None
    tests.append((lambda: validate_plan(bad), "Plan DAG missing tool scope"))

    bad = copy.deepcopy(fixture["sovereignty_boundary"])
    bad["policy_ref"] = "private-policy:synthetic"
    tests.append((lambda: validate_boundary(bad), "private policy reference in public boundary"))

    for operation, label in tests:
        try:
            operation()
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("negative test unexpectedly passed: " + label)

    print("Intelligence capability contract self-test: PASS (7 contract families, 10 UNIVERSALIS negative cases)")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()

    if args.self_test:
        self_test(root)
    if args.check:
        try:
            validate_all(load(root))
            print("Intelligence capability contracts: PASS (UNIVERSALIS profile, seven families)")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
            print("Intelligence capability validation: FAIL: " + str(exc))
            return 1
    if not args.self_test and not args.check:
        parser.error("choose --self-test and/or --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
