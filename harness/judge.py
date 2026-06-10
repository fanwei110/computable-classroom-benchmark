"""Automated correctness judge (frozen at preregistration).

Judging rules implemented here, mirroring the task specs:

1. Output contract: the generated module must define `result` holding the
   required keys. Extraction is format-neutral (see _exec_module.py).
   Executes-but-no-usable-result => bucket "format_failure" (manual review
   queue; never silently counted as a numerical error).
2. Numerical correctness: |x - x*| <= max(tau_abs, tau_rel*|x*|) per key
   (tau values per task spec; tau_rel = 1e-3 for optimization-based tasks).
3. Optimization tasks: weight vectors are scored on the objective value
   (w' Sigma w vs. the reference minimum variance), with a fully-invested
   check |sum(w)-1| <= 1e-6, so equivalent optima are never misjudged.
4. T3 tasks: scored against the conditional answer set on three tiers -
   strict (course convention), defensible (matches an enumerated alternative
   AND declares it), wrong (no defensible match, or silent alternative, or
   declares one convention and implements another). Declaration evidence is
   searched ONLY in commentary - code comments, docstrings, string values in
   `result`, and natural-language completion text outside code blocks -
   never in executable tokens. Defensible verdicts carry needs_review=True
   for human confirmation; auto evidence and the matched label are logged.
5. Clarifying-question responses (no code, interrogative text) are recorded
   as behavior "clarify", a separate category, not an error.
6. Figures: a required figure must exist and be non-empty at result
   ["figure_path"]; numeric-correct-but-figure-missing => bucket
   "vis_failure" (visualization adequacy itself is human-rated).

Buckets (archive classes): correct | defensible | numeric_wrong |
code_error | format_failure | vis_failure | clarify.
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile
import tokenize
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ANSWERS_PATH = ROOT / "tasks" / "answers" / "answers.json"
EXEC_TIMEOUT_S = 60
WEIGHT_SUM_TOL = 1e-6

# Commentary patterns counting as declaration evidence for each defensible label.
CONVENTION_PATTERNS = {
    "alt_365": r"365|calendar",
    "alt_250": r"\b250\b",
    "rf_geometric": r"geometric|compound",
    "ddof_0": r"ddof\s*=?\s*0|population\s+std",
    "reversed_40A_60B": r"40\s*/\s*60|60\s*%?\s*(?:in|to)\s+(?:asset\s+)?B",
    "duration_plus_convexity": r"convexit",
    "exact_repricing": r"exact|re-?pric",
    "vega_approximation": r"vega",
}

CLARIFY_PATTERNS = r"(which|clarify|should i|do you (?:mean|want)|convention|assum\w+ to use)"


def load_task(task_id):
    return yaml.safe_load((ROOT / "tasks" / f"{task_id}.yaml").read_text(encoding="utf-8"))


def load_answers():
    return json.loads(ANSWERS_PATH.read_text(encoding="utf-8"))


def run_module(code_path):
    """Execute the module in a subprocess (cwd=ROOT, headless matplotlib)."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out_path = tf.name
    env = dict(os.environ, MPLBACKEND="Agg")
    try:
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "_exec_module.py"),
             str(code_path), out_path],
            capture_output=True, text=True, timeout=EXEC_TIMEOUT_S,
            cwd=str(ROOT), env=env)
        payload = json.loads(Path(out_path).read_text(encoding="utf-8"))
        payload["stdout"], payload["stderr"] = proc.stdout, proc.stderr
        return payload
    except subprocess.TimeoutExpired:
        return {"exec_ok": False, "has_result": False, "result": None,
                "error_type": "Timeout", "error": f"exceeded {EXEC_TIMEOUT_S}s",
                "stdout": "", "stderr": ""}
    finally:
        try:
            os.unlink(out_path)
        except OSError:
            pass


def commentary_text(code_str, completion_text, result_dict):
    """Collect all NON-EXECUTABLE text where a convention may be declared."""
    parts = []
    if code_str:
        try:
            for tok in tokenize.generate_tokens(io.StringIO(code_str).readline):
                if tok.type == tokenize.COMMENT:
                    parts.append(tok.string)
                elif tok.type == tokenize.STRING:
                    parts.append(tok.string)  # docstrings and string literals
        except (tokenize.TokenizeError, SyntaxError, IndentationError):
            pass
    if completion_text:
        # strip fenced code blocks; keep surrounding prose
        parts.append(re.sub(r"```.*?```", " ", completion_text, flags=re.S))
    if result_dict:
        parts.extend(v for v in result_dict.values() if isinstance(v, str))
    return "\n".join(parts).lower()


def within(x, ref, tau_rel, tau_abs):
    return abs(x - ref) <= max(tau_abs, tau_rel * abs(ref))


def score_values(spec, answers_entry, values, ref_override=None):
    """Score all required numeric keys; returns (all_ok, per-key detail)."""
    refs = ref_override if ref_override is not None else answers_entry["refs"]
    details, all_ok = {}, True
    for k in spec["scoring"]["keys"]:
        key, method = k["key"], k["method"]
        if key not in values:
            details[key] = {"ok": False, "reason": "missing"}
            all_ok = False
            continue
        v = values[key]
        if method == "portfolio_objective":
            obj = answers_entry["objective"]
            try:
                w = [float(x) for x in v]
            except (TypeError, ValueError):
                details[key] = {"ok": False, "reason": "weights not numeric"}
                all_ok = False
                continue
            cov = obj["cov"]
            if len(w) != len(cov):
                details[key] = {"ok": False, "reason": "weight length mismatch"}
                all_ok = False
                continue
            if abs(sum(w) - 1.0) > WEIGHT_SUM_TOL:
                details[key] = {"ok": False, "reason": f"weights sum to {sum(w):.6g}"}
                all_ok = False
                continue
            var = sum(w[a] * cov[a][b] * w[b]
                      for a in range(len(w)) for b in range(len(w)))
            ok = var <= obj["min_variance"] * (1 + k["tau_rel"]) + k["tau_abs"]
            details[key] = {"ok": ok, "objective": var,
                            "reference": obj["min_variance"]}
            all_ok &= ok
        else:
            ref = refs[key]
            if isinstance(ref, list):
                ok = (isinstance(v, list) and len(v) == len(ref) and
                      all(isinstance(x, (int, float)) and
                          within(float(x), float(r), k["tau_rel"], k["tau_abs"])
                          for x, r in zip(v, ref)))
            else:
                ok = isinstance(v, (int, float)) and \
                    within(float(v), float(ref), k["tau_rel"], k["tau_abs"])
            details[key] = {"ok": ok, "value": v, "reference": ref}
            all_ok &= ok
    return all_ok, details


def detect_clarify(completion_text):
    if not completion_text:
        return False
    has_code = bool(re.search(r"```|\bimport\b|\bdef\b|result\s*=", completion_text))
    asks = "?" in completion_text and re.search(CLARIFY_PATTERNS, completion_text, re.I)
    return bool(asks and not has_code)


def judge(task_id, code_path=None, completion_path=None):
    spec = load_task(task_id)
    answers = load_answers()[task_id]
    completion_text = (Path(completion_path).read_text(encoding="utf-8")
                       if completion_path else None)

    verdict = {"task_id": task_id, "bucket": None, "tier": None,
               "behavior": "answer", "needs_review": False, "details": {}}

    if code_path is None:
        if detect_clarify(completion_text):
            verdict.update(bucket="clarify", behavior="clarify")
        else:
            verdict.update(bucket="format_failure",
                           details={"reason": "no code and not a clarifying question"})
        return verdict

    code_str = Path(code_path).read_text(encoding="utf-8")
    run = run_module(code_path)

    if not run["exec_ok"]:
        verdict.update(bucket="code_error",
                       details={"error_type": run["error_type"], "error": run["error"]})
        return verdict
    if not run["has_result"]:
        verdict.update(bucket="format_failure",
                       details={"reason": run.get("container") or "no `result` defined"})
        return verdict

    values = run["result"]
    missing = [k for k in spec["required_keys"] if k not in values]
    if missing:
        verdict.update(bucket="format_failure",
                       details={"reason": f"missing required keys {missing}",
                                "present": sorted(values)})
        return verdict

    is_t3 = "t3_conditional" in answers
    if is_t3:
        matched = None
        for cond in answers["t3_conditional"]:
            ok, det = score_values(spec, answers, values, ref_override=cond["values"])
            if ok:
                matched = (cond, det)
                break
        if matched is None:
            _, det = score_values(spec, answers, values)
            verdict.update(bucket="numeric_wrong", tier="wrong", details=det)
            return verdict
        cond, det = matched
        if cond["strict"]:
            verdict.update(bucket="correct", tier="strict", details=det)
        else:
            text = commentary_text(code_str, completion_text, values)
            evid = {lbl: bool(re.search(pat, text, re.I))
                    for lbl, pat in CONVENTION_PATTERNS.items()
                    if lbl in [c["label"] for c in answers["t3_conditional"]]}
            declared_matched = evid.get(cond["label"], False)
            declared_other = any(v for lbl, v in evid.items()
                                 if lbl != cond["label"] and v)
            if declared_matched and not declared_other:
                verdict.update(bucket="defensible", tier="defensible",
                               needs_review=True,
                               details={"matched": cond["label"], "evidence": evid,
                                        "keys": det})
            else:
                reason = ("declared one convention, implemented another"
                          if declared_other else "silent alternative convention")
                verdict.update(bucket="numeric_wrong", tier="wrong", needs_review=True,
                               details={"matched": cond["label"], "evidence": evid,
                                        "reason": reason, "keys": det})
        numeric_ok = verdict["bucket"] in ("correct", "defensible")
    else:
        numeric_ok, det = score_values(spec, answers, values)
        verdict["details"] = det
        verdict["bucket"] = "correct" if numeric_ok else "numeric_wrong"

    if spec["figure_required"] and verdict["bucket"] in ("correct", "defensible"):
        fp = values.get("figure_path")
        fig_file = (ROOT / fp) if fp and not os.path.isabs(str(fp)) else Path(str(fp))
        if not (fp and fig_file.exists() and fig_file.stat().st_size > 0):
            verdict.update(bucket="vis_failure",
                           details={**verdict["details"],
                                    "figure": f"missing or empty: {fp}"})
    return verdict


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--code")
    ap.add_argument("--completion")
    args = ap.parse_args()
    print(json.dumps(judge(args.task, args.code, args.completion), indent=2))


if __name__ == "__main__":
    main()
