"""Adversarial acceptance run for the judging harness (stage-1 check #3).

Runs every sample in adversarial/expected.yaml through judge.judge() and
compares the bucket (and T3 tier where specified) against the manifest.
Writes validation_report.md. Exits nonzero unless 40/40 match.
"""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from judge import judge  # noqa: E402

HERE = Path(__file__).resolve().parent
ADV = HERE / "adversarial"


def run_group(entries, folder):
    rows = []
    for e in entries:
        path = ADV / folder / e["file"]
        if e.get("completion_only"):
            v = judge(e["task"], code_path=None, completion_path=path)
        else:
            v = judge(e["task"], code_path=path)
        ok = v["bucket"] == e["expect"]
        if ok and "tier" in e:
            ok = v["tier"] == e["tier"]
        rows.append({"file": e["file"], "task": e["task"],
                     "expected": e["expect"] + (f"/{e['tier']}" if "tier" in e else ""),
                     "got": (v["bucket"] or "?") + (f"/{v['tier']}" if v["tier"] else ""),
                     "ok": ok,
                     "detail": "" if ok else str(v["details"])[:160]})
    return rows


def main():
    manifest = yaml.safe_load((ADV / "expected.yaml").read_text(encoding="utf-8"))
    rows = run_group(manifest["correct"], "correct") + \
        run_group(manifest["planted"], "planted")

    n_ok = sum(r["ok"] for r in rows)
    lines = ["# Harness adversarial validation report", "",
             f"Result: **{n_ok}/{len(rows)}**", "",
             "| sample | task | expected | got | ok |",
             "|---|---|---|---|---|"]
    for r in rows:
        mark = "PASS" if r["ok"] else f"FAIL ({r['detail']})"
        lines.append(f"| {r['file']} | {r['task']} | {r['expected']} | {r['got']} | {mark} |")
    report = "\n".join(lines) + "\n"
    (HERE / "validation_report.md").write_text(report, encoding="utf-8")

    for r in rows:
        status = "PASS" if r["ok"] else "FAIL"
        print(f"[{status}] {r['file']:<38} expected={r['expected']:<24} got={r['got']}")
        if not r["ok"]:
            print(f"        {r['detail']}")
    print(f"\nRESULT: {n_ok}/{len(rows)}")
    sys.exit(0 if n_ok == len(rows) else 1)


if __name__ == "__main__":
    main()
