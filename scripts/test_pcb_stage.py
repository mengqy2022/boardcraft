"""Behavioral checks for missing coverage and stale evidence; no EDA needed."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from check_pcb_stage import FINAL_CHECKS, LAYOUT_CHECKS, digest, validate


class StageReviewTests(unittest.TestCase):
    def test_incomplete_or_stale_review_is_blocked(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            pcb = root / "current.epcb"
            pcb.write_text("test-only PCB snapshot", encoding="utf-8")
            inv = root / "inventory.json"
            inv.write_text(json.dumps({"components": ["U1", "C1"], "power_pins": ["U1.4"]}), encoding="utf-8")
            evidence = root / "review.txt"
            evidence.write_text("synthetic review fixture, not a real board approval", encoding="utf-8")
            passed = {"status": "pass", "evidence": ["review"], "rationale": "Synthetic test record"}
            report = {
                "schema_version": 1, "project": "test", "revision": "test", "stage": "final",
                "artifacts": {k: {"path": p.name, "sha256": digest(p)} for k, p in {"pcb": pcb, "inventory": inv, "review": evidence}.items()},
                "checks": {k: copy.deepcopy(passed) for k in FINAL_CHECKS},
                "layer_decision": {
                    "baseline_layer_count": 2, "selected_layer_count": 2,
                    "baseline_basis": "Original board is two layers",
                    "candidates": [{"layer_count": 2, "status": "feasible", "blocking_constraints": [], "evidence": ["review"]}],
                    "selection_rationale": "Two layers meet the design constraints",
                    "cost_tradeoff": "No additional layer cost",
                },
                "components": {k: copy.deepcopy(passed) for k in ["U1", "C1"]},
                "power_pins": {"U1.4": copy.deepcopy(passed)},
            }
            target = root / "stage.json"

            def check(value, allowed=False):
                target.write_text(json.dumps(value), encoding="utf-8")
                self.assertEqual(not validate(target, pcb), allowed)

            check(report, True)
            # Core gates cannot be omitted or waived; engineering categories need
            # current evidence even when genuinely inapplicable to a simple board.
            for key in ("RULE_GATE", "DRC", "PCB-P11", "PI", "SI", "EMC", "THERMAL", "FAB"):
                with self.subTest(missing_check=key):
                    missing = copy.deepcopy(report)
                    del missing["checks"][key]
                    check(missing)
            for key in ("RULE_GATE", "DRC"):
                with self.subTest(waived_core_gate=key):
                    waived = copy.deepcopy(report)
                    waived["checks"][key]["status"] = "not_applicable"
                    check(waived)
            no_si_required = copy.deepcopy(report)
            no_si_required["checks"]["SI"] = {
                "status": "not_applicable", "evidence": ["review"],
                "rationale": "Synthetic passive-board fixture: interface review found no timing-sensitive nets.",
            }
            check(no_si_required, True)
            no_si_required["checks"]["SI"]["evidence"] = []
            check(no_si_required)
            missing_layer_decision = copy.deepcopy(report)
            del missing_layer_decision["layer_decision"]
            check(missing_layer_decision)
            unjustified_extra_layers = copy.deepcopy(report)
            unjustified_extra_layers["layer_decision"]["selected_layer_count"] = 4
            unjustified_extra_layers["layer_decision"]["candidates"].append({
                "layer_count": 4, "status": "feasible", "blocking_constraints": [], "evidence": ["review"],
            })
            check(unjustified_extra_layers)
            justified_extra_layers = copy.deepcopy(unjustified_extra_layers)
            justified_extra_layers["layer_decision"]["candidates"][0]["status"] = "infeasible"
            justified_extra_layers["layer_decision"]["candidates"][0]["blocking_constraints"] = ["Critical net cannot escape without breaking mechanical clearance"]
            justified_extra_layers["layer_decision"]["selection_rationale"] = "Four layers avoid the documented escape conflict"
            check(justified_extra_layers, True)
            self.assertTrue(validate(target, pcb, "layout"))
            layout = copy.deepcopy(report)
            layout["stage"] = "layout"
            layout["checks"] = {k: layout["checks"][k] for k in LAYOUT_CHECKS}
            check(layout, True)
            for key in ("RULE_GATE", "PCB-P09", "PCB-P11"):
                with self.subTest(missing_layout_gate=key):
                    incomplete_layout = copy.deepcopy(layout)
                    del incomplete_layout["checks"][key]
                    check(incomplete_layout)
            layout_without_partition_review = copy.deepcopy(layout)
            del layout_without_partition_review["checks"]["PCB-P10"]
            check(layout_without_partition_review)
            self.assertTrue(validate(target, pcb, "final"))
            missing_pin = copy.deepcopy(report)
            missing_pin["power_pins"].clear()
            check(missing_pin)
            missing_component = copy.deepcopy(report)
            del missing_component["components"]["C1"]
            check(missing_component)
            failed = copy.deepcopy(report)
            failed["checks"]["PCB-V04"]["status"] = "fail"
            check(failed)
            missing_partition_review = copy.deepcopy(report)
            del missing_partition_review["checks"]["PCB-P10"]
            check(missing_partition_review)
            unchecked = copy.deepcopy(report)
            del unchecked["checks"]["PCB-L01/L17/L20"]
            check(unchecked)
            undocumented_na = copy.deepcopy(report)
            undocumented_na["power_pins"]["U1.4"] = {"status": "not_applicable", "evidence": [], "rationale": ""}
            check(undocumented_na)
            no_review = copy.deepcopy(report)
            no_review["checks"]["PCB-V04"]["evidence"] = ["pcb"]
            check(no_review)
            missing_file = copy.deepcopy(report)
            missing_file["artifacts"]["review"]["path"] = "missing.txt"
            check(missing_file)
            other_pcb = root / "other.epcb"
            other_pcb.write_bytes(pcb.read_bytes())
            wrong_source = copy.deepcopy(report)
            wrong_source["artifacts"]["pcb"]["path"] = other_pcb.name
            check(wrong_source)
            pcb.write_text("changed PCB", encoding="utf-8")
            check(report)
            pcb.write_text("test-only PCB snapshot", encoding="utf-8")
            evidence.write_text("changed evidence", encoding="utf-8")
            check(report)
            target.write_text("[]", encoding="utf-8")
            self.assertTrue(validate(target, pcb))


if __name__ == "__main__":
    unittest.main()
