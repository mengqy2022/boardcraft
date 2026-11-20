"""Check PCB review coverage and evidence freshness; does not run EDA or measure geometry."""
import argparse
import hashlib
import json
import re
from pathlib import Path

LAYOUT_CHECKS = {
    "INVENTORY", "RULE_GATE", "PCB-P01", "PCB-P09", "PCB-P10", "PCB-P11", "PCB-P12",
    "PCB-V04", "PCB-L01/L17/L20", "PCB-L18", "PCB-R18",
}
FINAL_CHECKS = LAYOUT_CHECKS | {
    "NETLIST", "CONNECTIVITY", "DRC", "PCB-G06/G08", "PCB-R07", "PCB-R11/R12",
    "PCB-R14/R17", "PCB-L21", "PCB-V02", "PCB-V06", "PI", "SI", "EMC", "THERMAL", "FAB",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(report_path, current_pcb, expected_stage=None):
    report_path, current_pcb = Path(report_path).resolve(), Path(current_pcb).resolve()
    errors = []
    try:
        report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return [f"Cannot read review: {exc}"]
    if not isinstance(report, dict):
        return ["Review must be a JSON object"]
    if report.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for field in ("project", "revision"):
        if not isinstance(report.get(field), str) or not report[field].strip():
            errors.append(f"Missing {field}")
    stage = report.get("stage")
    if stage not in ("layout", "final"):
        errors.append("stage must be layout or final")
    if expected_stage is not None and stage != expected_stage:
        errors.append(f"Expected {expected_stage} review; got {stage}")
    artifacts = report.get("artifacts", {})
    if not isinstance(artifacts, dict):
        return errors + ["artifacts must be an object"]
    paths = {}
    for key, value in artifacts.items():
        if not isinstance(value, dict) or not isinstance(value.get("path"), str) or not value["path"].strip():
            errors.append(f"{key}: missing artifact path")
            continue
        path = (report_path.parent / value["path"]).resolve()
        try:
            actual = digest(path)
        except OSError as exc:
            errors.append(f"{key}: cannot read artifact ({exc})")
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", str(value.get("sha256", ""))) or actual != value["sha256"]:
            errors.append(f"{key}: missing or stale SHA-256")
            continue
        paths[key] = path
    for key in ("pcb", "inventory"):
        if key not in paths:
            errors.append(f"Missing verified artifact: {key}")
    if paths.get("pcb") != current_pcb:
        errors.append("pcb artifact must be the current source passed with --pcb")
    inventory = {}
    if "inventory" in paths:
        try:
            inventory = json.loads(paths["inventory"].read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as exc:
            errors.append(f"Cannot read inventory: {exc}")
    if not isinstance(inventory, dict):
        return errors + ["inventory must be an object"]

    def reviewed(label, value, allow_na=True):
        if not isinstance(value, dict):
            errors.append(f"{label}: missing review")
            return
        status = value.get("status")
        if not isinstance(status, str) or status not in ({"pass", "not_applicable"} if allow_na else {"pass"}):
            errors.append(f"{label}: not passed")
        refs = value.get("evidence")
        if not isinstance(refs, list) or not refs or any(not isinstance(k, str) or k not in paths or k in {"pcb", "inventory"} for k in refs):
            errors.append(f"{label}: requires verified review evidence beyond source/inventory")
        if not isinstance(value.get("rationale"), str) or not value["rationale"].strip():
            errors.append(f"{label}: missing result or not-applicable rationale")

    checks = report.get("checks", {})
    if not isinstance(checks, dict):
        checks = {}
        errors.append("checks must be an object")
    required = FINAL_CHECKS if stage == "final" else LAYOUT_CHECKS
    for key in sorted(required):
        reviewed(key, checks.get(key), allow_na=key not in {"INVENTORY", "RULE_GATE", "PCB-P01", "PCB-P12", "PCB-V04", "NETLIST", "CONNECTIVITY", "DRC", "PCB-R07", "PCB-V02", "FAB"})
    decision = report.get("layer_decision")
    if not isinstance(decision, dict):
        errors.append("layer_decision: missing structured layer-count review")
    else:
        baseline = decision.get("baseline_layer_count")
        selected = decision.get("selected_layer_count")
        if not isinstance(baseline, int) or baseline < 2:
            errors.append("layer_decision.baseline_layer_count: must be an integer >= 2")
        if not isinstance(selected, int) or selected < 2:
            errors.append("layer_decision.selected_layer_count: must be an integer >= 2")
        for field in ("baseline_basis", "selection_rationale", "cost_tradeoff"):
            if not isinstance(decision.get(field), str) or not decision[field].strip():
                errors.append(f"layer_decision.{field}: required")
        candidates = decision.get("candidates")
        if not isinstance(candidates, list):
            candidates = []
            errors.append("layer_decision.candidates: must be a list")
        by_count = {}
        for candidate in candidates:
            if not isinstance(candidate, dict):
                errors.append("layer_decision.candidates: entries must be objects")
                continue
            count = candidate.get("layer_count")
            if not isinstance(count, int) or count < 2 or count in by_count:
                errors.append("layer_decision.candidates: layer_count must be unique and >= 2")
                continue
            by_count[count] = candidate
            if candidate.get("status") not in {"feasible", "infeasible"}:
                errors.append(f"layer_decision.candidates[{count}]: status must be feasible or infeasible")
            refs = candidate.get("evidence")
            if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in paths or ref in {"pcb", "inventory"} for ref in refs):
                errors.append(f"layer_decision.candidates[{count}]: requires verified evidence")
            blockers = candidate.get("blocking_constraints")
            if candidate.get("status") == "infeasible" and (not isinstance(blockers, list) or not blockers or any(not isinstance(item, str) or not item.strip() for item in blockers)):
                errors.append(f"layer_decision.candidates[{count}]: infeasible result needs concrete blocking_constraints")
        if isinstance(baseline, int) and baseline >= 2:
            if baseline not in by_count:
                errors.append("layer_decision.candidates: baseline layer count must be evaluated")
            elif isinstance(selected, int) and selected > baseline and by_count[baseline].get("status") != "infeasible":
                errors.append("layer_decision: adding layers requires the baseline candidate to be infeasible")
        if isinstance(selected, int) and selected >= 2:
            if selected not in by_count or by_count[selected].get("status") != "feasible":
                errors.append("layer_decision: selected layer count must have a feasible candidate review")
    for key in ("components", "power_pins"):
        values = inventory.get(key)
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            errors.append(f"inventory.{key}: requires list of unique references")
            continue
        if len(values) != len(set(values)):
            errors.append(f"inventory.{key}: duplicate references")
        records = report.get(key, {})
        if not isinstance(records, dict):
            errors.append(f"{key}: requires per-object review records")
            continue
        if set(records) != set(values):
            errors.append(f"{key}: coverage differs; missing={sorted(set(values)-set(records))}, extra={sorted(set(records)-set(values))}")
        for ref in values:
            reviewed(f"{key}.{ref}", records.get(ref))
    if not inventory.get("components"):
        errors.append("inventory.components must not be empty")
    if inventory.get("power_pins") == []:
        reason = inventory.get("no_power_pins_reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("Empty power_pins inventory needs no_power_pins_reason and INVENTORY review evidence")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("--pcb", required=True, type=Path, help="Freshly exported current PCB source")
    parser.add_argument("--stage", required=True, choices=("layout", "final"), help="Require the intended workflow stage")
    args = parser.parse_args()
    errors = validate(args.review, args.pcb, args.stage)
    if errors:
        print("PCB stage review BLOCKED:\n- " + "\n- ".join(errors))
        raise SystemExit(1)
    print("PCB stage review evidence OK: coverage and file hashes match. Review accuracy, live EDA, geometry and hardware performance still require their own checks.")


if __name__ == "__main__":
    main()
