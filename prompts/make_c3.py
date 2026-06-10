"""Assemble the final C1 and C3 prompts from the frozen external phrasings.

C1 = instructor phrasing + output contract.
C3 = instructor phrasing + convention header + output contract.

Input: prompts/C1/teacher_A.md and teacher_B.md (the filled collection
templates, frozen verbatim). Each task contributes 2 phrasings per teacher;
the preregistered design uses 2 frozen variants per task (one per teacher,
V1; V2 is the recorded backup), each run 5 repetitions in C1 and C3.

Output: prompts/C1_final/<task>_<teacher><variant>.md and
        prompts/C3_final/<task>_<teacher><variant>.md

Run AFTER the external phrasings arrive; stage 2 must not start before the
assembled set is committed and frozen (preregistration scenario-4 rule).
"""

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TASKS = HERE.parent / "tasks"
HEADER = (HERE / "convention_header.txt").read_text(encoding="utf-8").strip()


def output_contract(spec):
    keys = ", ".join(f"'{k}'" for k in spec["required_keys"])
    line = (f"Output contract: store all required outputs in a dictionary named "
            f"`result` under exactly these keys: {keys}.")
    if spec["figure_required"]:
        line += (" Save the figure to a file and store its path under "
                 "result['figure_path'].")
    return line


def parse_filled_template(path):
    """Extract {task_id: [v1, v2]} from a filled collection template."""
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    blocks = re.split(r"^### (KP\d_T\d)", text, flags=re.M)[1:]
    for task_id, body in zip(blocks[0::2], blocks[1::2]):
        v1 = re.search(r"^V1:\s*(.+?)(?=^V2:)", body, re.M | re.S)
        v2 = re.search(r"^V2:\s*(.+?)(?=^###|\Z)", body, re.M | re.S)
        variants = [m.group(1).strip() for m in (v1, v2) if m and m.group(1).strip()]
        if len(variants) != 2:
            raise ValueError(f"{path}: task {task_id} needs exactly 2 phrasings, "
                             f"found {len(variants)}")
        out[task_id] = variants
    if len(out) != 18:
        raise ValueError(f"{path}: expected 18 tasks, found {len(out)}")
    return out


def main():
    teacher_files = {"A": HERE / "C1" / "teacher_A.md",
                     "B": HERE / "C1" / "teacher_B.md"}
    missing = [str(p) for p in teacher_files.values() if not p.exists()]
    if missing:
        print("External phrasings not yet collected; missing:")
        for m in missing:
            print("  " + m)
        print("Stage 2 must not start before these are frozen (scenario 4).")
        sys.exit(2)

    for cond in ("C1_final", "C3_final"):
        (HERE / cond).mkdir(exist_ok=True)

    n = 0
    for teacher, path in teacher_files.items():
        phrasings = parse_filled_template(path)
        for task_id, variants in phrasings.items():
            spec = yaml.safe_load((TASKS / f"{task_id}.yaml").read_text(encoding="utf-8"))
            contract = output_contract(spec)
            for vi, phrase in enumerate(variants, 1):
                stem = f"{task_id}_{teacher}{vi}.md"
                (HERE / "C1_final" / stem).write_text(
                    f"{phrase}\n\n{contract}\n", encoding="utf-8")
                (HERE / "C3_final" / stem).write_text(
                    f"{phrase}\n\n{HEADER}\n\n{contract}\n", encoding="utf-8")
                n += 2
    print(f"assembled {n} prompts into C1_final/ and C3_final/")


if __name__ == "__main__":
    main()
