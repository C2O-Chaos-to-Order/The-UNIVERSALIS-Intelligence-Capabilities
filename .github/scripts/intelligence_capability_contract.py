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
    timestamp(p["created_at"],"plan.created_at"); nodes=p["nodes"]; ids=[n["node_id"] for n in nodes]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate plan node IDs")
    known=set(ids); degree={x:0 for x in ids}; children={x:[] for x in ids}
    for node in nodes:
        if not node.get("verification_ref"): raise ValueError("every plan node requires verification reference")
        for dep in node["depends_on"]:
            if dep not in known: raise ValueError("plan dependency references unknown node")
            if dep==node["node_id"]: raise ValueError("plan node cannot depend on itself")
            degree[node["node_id"]]+=1; children[dep].append(node["node_id"])
    queue=[n for n,d in degree.items() if d==0]; visited=0
    while queue:
        n=queue.pop(); visited+=1
        for child in children[n]:
            degree[child]-=1
            if degree[child]==0: queue.append(child)
    if visited!=len(nodes): raise ValueError("plan dependencies contain a cycle")
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
    walk_handles(req); walk_handles(res)
def validate_budget(b):
    timestamp(b["issued_at"],"compute_budget.issued_at"); total=b["total_budget"]["limit"]; allocated=sum(x["amount"] for x in b["allocations"])
    if allocated+b["remaining"]>total+1e-9: raise ValueError("compute allocations exceed granted budget")
    if not math.isclose(allocated+b["remaining"],total,rel_tol=1e-9,abs_tol=1e-9): raise ValueError("allocations plus remaining must reconcile to grant")
def validate_improvement(p):
    if p["baseline_sha256"]==p["candidate_sha256"]: raise ValueError("candidate must change artifact hash")
    if p["model_weights_changed"] is not False: raise ValueError("contract does not authorize model-weight changes")
    g=p["held_out_gate"]
    if p["loop_stage"] in {"probe","compose"}:
        improved=g["candidate_score"]>g["baseline_score"] if g["objective"]=="maximize" else g["candidate_score"]<g["baseline_score"]
        if g["strict_improvement"]!=improved or g["passed"]!=improved: raise ValueError("held-out gate passes only on strict improvement")
    if p["review"]["status"]=="approved" and (not g["passed"] or not p["review"].get("reviewer_ref")): raise ValueError("approved proposal requires passed held-out gate and reviewer")
def validate_boundary(b,profile):
    if profile=="c2o":
        if b["owner"]!="c2o" or b["deployment_mode"] not in {"private_sovereign","air_gapped"}: raise ValueError("C2O requires private sovereign or air-gapped boundary")
        if b["egress_default"]!="deny" or not b["audit_required"] or not b.get("policy_ref"): raise ValueError("C2O requires deny-by-default egress, audit, and private policy reference")
        if not (b["data_residency"]==b["model_weights_residency"]==b["inference_traffic_residency"]): raise ValueError("C2O data, weights, and traffic must share sovereign boundary")
    else:
        if b["owner"]!="universalis": raise ValueError("UNIVERSALIS profile requires independently owned boundary")
        if b.get("policy_ref"): raise ValueError("UNIVERSALIS fixture cannot contain C2O-private policy reference")
def validate_all(f,profile):
    validate_profile(f["capability_profile"]); validate_plan(f["plan_dag"]); validate_self_model(f["self_model_state"])
    validate_world(f["world_model_request"],f["world_model_response"]); validate_budget(f["compute_budget"])
    validate_improvement(f["self_improvement_proposal"]); validate_boundary(f["sovereignty_boundary"],profile)
def load(root): return json.loads((root/FIXTURE).read_text(encoding="utf-8"))
def self_test(root):
    f=load(root); validate_all(f,"c2o"); validate_all(f,"universalis"); tests=[]
    bad=copy.deepcopy(f["plan_dag"]); bad["nodes"][0]["depends_on"]=["execute"]; tests.append((lambda:validate_plan(bad),"plan DAG cycle"))
    bad=copy.deepcopy(f["compute_budget"]); bad["allocations"][0]["amount"]=9000; tests.append((lambda:validate_budget(bad),"compute budget overspend"))
    bad=copy.deepcopy(f["world_model_request"]); bad["raw_video"]="embedded"; tests.append((lambda:validate_world(bad,f["world_model_response"]),"raw media in handle request"))
    bad=copy.deepcopy(f["self_improvement_proposal"]); bad["held_out_gate"]["candidate_score"]=bad["held_out_gate"]["baseline_score"]; tests.append((lambda:validate_improvement(bad),"no strict held-out improvement"))
    bad=copy.deepcopy(f["self_improvement_proposal"]); bad["model_weights_changed"]=True; tests.append((lambda:validate_improvement(bad),"model weight change"))
    bad=copy.deepcopy(f["capability_profile"]); bad["axes"][0]["score"]=120; tests.append((lambda:validate_profile(bad),"capability score outside scale"))
    bad=copy.deepcopy(f["capability_profile"]); a=bad["attestation"]; a["verification_status"]="verified"; a["verified_by"]=a["signer_ref"]; a["verified_at"]="2026-11-12T10:22:00Z"; tests.append((lambda:validate_profile(bad),"self-verified attestation"))
    bad=copy.deepcopy(f["sovereignty_boundary"]); bad["egress_default"]="allow"; tests.append((lambda:validate_boundary(bad,"c2o"),"C2O egress default allow"))
    for op,label in tests:
        try: op()
        except (ValueError,KeyError,TypeError): continue
        raise AssertionError("negative test unexpectedly passed: "+label)
    print("Intelligence capability contract self-test: PASS (7 contract families, 8 negative cases)")
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--profile",choices=("c2o","universalis"),default="universalis"); p.add_argument("--self-test",action="store_true"); p.add_argument("--check",action="store_true"); p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); a=p.parse_args(); root=a.root.resolve()
    if a.self_test: self_test(root)
    if a.check:
        try: validate_all(load(root),a.profile); print(f"Intelligence capability contracts: PASS (profile={a.profile}, seven families)")
        except (OSError,UnicodeError,json.JSONDecodeError,ValueError,KeyError,TypeError) as exc: print("Intelligence capability validation: FAIL: "+str(exc)); return 1
    if not a.self_test and not a.check: p.error("choose --self-test and/or --check")
    return 0
if __name__=="__main__": sys.exit(main())
