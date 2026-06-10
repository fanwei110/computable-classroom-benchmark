"""Schema validation for tasks/*.yaml (stage-1 acceptance check #1).

Checks: 18 files, unique ids, required fields present, scoring entries cover
required keys (figure_path exempt - checked by existence, vis adequacy is
human-rated), T3 tasks carry a defensible-convention enumeration including
exactly one strict label, valid tolerances, knowledge-point/task-type grid
complete (6 KPs x T1/T2/T3).
"""

import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REQUIRED_FIELDS = ["id", "knowledge_point", "pillar", "task_type", "title",
                   "description", "inputs", "data_file", "figure_required",
                   "required_keys", "scoring", "conventions_binding"]
VALID_PILLARS = {"portfolio_theory", "asset_pricing", "fixed_income", "derivatives_risk"}


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def main():
    files = sorted(HERE.glob("KP*_T*.yaml"))
    if len(files) != 18:
        fail(f"expected 18 task files, found {len(files)}")

    ids, grid = set(), set()
    for f in files:
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        for field in REQUIRED_FIELDS:
            if field not in spec:
                fail(f"{f.name}: missing field '{field}'")
        if spec["id"] != f.stem:
            fail(f"{f.name}: id mismatch")
        if spec["id"] in ids:
            fail(f"duplicate id {spec['id']}")
        ids.add(spec["id"])
        kp, tt = spec["id"].split("_")
        grid.add((kp, tt))
        if spec["task_type"] != tt:
            fail(f"{f.name}: task_type field disagrees with id")
        if spec["pillar"] not in VALID_PILLARS:
            fail(f"{f.name}: unknown pillar {spec['pillar']}")

        scored = {k["key"] for k in spec["scoring"]["keys"]}
        for key in spec["required_keys"]:
            if key == "figure_path":
                if not spec["figure_required"]:
                    fail(f"{f.name}: figure_path required but figure_required false")
                continue
            if key not in scored:
                fail(f"{f.name}: required key '{key}' has no scoring entry")
        for k in spec["scoring"]["keys"]:
            if k["method"] not in {"tolerance", "portfolio_objective"}:
                fail(f"{f.name}: bad scoring method {k['method']}")
            if not (0 < k["tau_rel"] <= 1e-2):
                fail(f"{f.name}: tau_rel out of range for {k['key']}")
            if spec["scoring"]["optimization"] and k["tau_rel"] < 1e-3 - 1e-12:
                fail(f"{f.name}: optimization task should use tau_rel=1e-3")

        if tt == "T3":
            if "canonical_question" not in spec:
                fail(f"{f.name}: T3 missing canonical_question")
            t3 = spec.get("t3_defensible_conventions")
            if not t3 or len(t3) < 2:
                fail(f"{f.name}: T3 needs >=2 enumerated conventions")
            stricts = [c for c in t3 if c["label"].startswith("strict")]
            if len(stricts) != 1:
                fail(f"{f.name}: T3 needs exactly one strict label")
        if spec["data_file"]:
            if not (HERE.parent / spec["data_file"]).exists():
                print(f"  note: {f.name} references {spec['data_file']} "
                      f"(must exist before build_answers)")

    expected_grid = {(f"KP{i}", f"T{j}") for i in range(1, 7) for j in range(1, 4)}
    if grid != expected_grid:
        fail(f"grid incomplete: missing {expected_grid - grid}")

    print(f"OK: 18/18 task specs pass schema validation "
          f"({len([1 for f in files if 'T3' in f.name])} T3 tasks with conditional sets)")


if __name__ == "__main__":
    main()
