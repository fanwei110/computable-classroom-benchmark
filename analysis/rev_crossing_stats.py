"""Revision-1 crossing experiment: FORMAL statistics for the wording x scaffold
2x2 (no-convention row), 18 tasks x 3 models x 10 repetitions per cell.

ANALYSIS SET = four cells collected in adjacent short windows in August 2026:

    Creg, C1wS       -- collected August 4-5
    C1rep, C2rep     -- collected August 6; byte-identical frozen-prompt replays

The short-window design reduces temporal separation relative to the June cells,
but does not eliminate within-period date or provider-routing imbalance.
A separate drift audit compares the June formal C1/C2 cells with their August
replays; it is not interpreted as proof that drift is absent.


Inference mirrors the pre-registered plan (analysis/analysis_plan.md):
  PRIMARY   : mixed-effects LOGISTIC (BinomialBayesMixedGLM), task random
              intercept, model fixed effects -- same estimator as
              analysis/mixed_logit.py
  ROBUSTNESS: GEE logit, exchangeable working correlation, task clusters,
              model fixed effects
All percentages carry task-cluster bootstrap CIs (B = 10,000), including a CI
for the interaction contrast.

Output -> runs/rev_crossing_stats.txt
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "rev_crossing_stats.txt"
RNG = np.random.default_rng(20260805)
B = 10_000

lines = []


def say(s=""):
    print(s)
    lines.append(s)


def load_jsonl_tags(prefix):
    rows = []
    for m in ("M1", "M2", "M3"):
        p = ROOT / "runs" / "raw" / f"{prefix}_{m}" / f"{prefix}_{m}.jsonl"
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                meta = r.get("api_response_meta") or {}
                b = r["judge"]["bucket"]
                rows.append({
                    "model": r["model"], "condition": r["condition"],
                    "task_id": r["task_id"], "bucket": b,
                    "exec_ok": int(r["code_extracted"] and b != "code_error"),
                    "correct": int(b == "correct"),
                    "provider": meta.get("provider") or "unknown",
                    "returned_model_id": meta.get("model_id") or "unknown",
                    "timestamp_utc": r.get("timestamp_utc")})
    return pd.DataFrame(rows)


def cluster_ci(df, col="correct"):
    per = df.groupby("task_id")[col].agg(["sum", "count"])
    s, c = per["sum"].to_numpy(float), per["count"].to_numpy(float)
    idx = RNG.integers(0, len(s), size=(B, len(s)))
    boots = s[idx].sum(1) / c[idx].sum(1) * 100
    return np.percentile(boots, [2.5, 97.5])


def _task_rates(df):
    per = df.groupby("task_id").correct.agg(["sum", "count"])
    return per["sum"].to_numpy(float), per["count"].to_numpy(float)


def cluster_diff_ci(df_a, df_b):
    """Paired-over-tasks cluster bootstrap CI for mean(a) - mean(b), in pp."""
    tasks = sorted(set(df_a.task_id) & set(df_b.task_id))
    a = df_a[df_a.task_id.isin(tasks)].groupby("task_id").correct.agg(["sum", "count"]).loc[tasks]
    b = df_b[df_b.task_id.isin(tasks)].groupby("task_id").correct.agg(["sum", "count"]).loc[tasks]
    n = len(tasks)
    idx = RNG.integers(0, n, size=(B, n))
    am = a["sum"].to_numpy(float)[idx].sum(1) / a["count"].to_numpy(float)[idx].sum(1)
    bm = b["sum"].to_numpy(float)[idx].sum(1) / b["count"].to_numpy(float)[idx].sum(1)
    return np.percentile((am - bm) * 100, [2.5, 97.5])


def interaction_ci(dat, c00, c10, c01, c11):
    """Cluster bootstrap CI for the difference-in-differences
    (c11 - c01) - (c10 - c00), resampling tasks jointly across all cells."""
    cells = {k: dat[dat.condition == k] for k in (c00, c10, c01, c11)}
    tasks = sorted(set.intersection(*[set(v.task_id) for v in cells.values()]))
    agg = {k: v[v.task_id.isin(tasks)].groupby("task_id").correct
           .agg(["sum", "count"]).loc[tasks] for k, v in cells.items()}
    n = len(tasks)
    idx = RNG.integers(0, n, size=(B, n))

    def m(k):
        a = agg[k]
        return (a["sum"].to_numpy(float)[idx].sum(1)
                / a["count"].to_numpy(float)[idx].sum(1))
    d = ((m(c11) - m(c01)) - (m(c10) - m(c00))) * 100
    return np.percentile(d, [2.5, 97.5])


def main():
    new = load_jsonl_tags("rev_full")      # Creg, C1wS   (August)
    batch = load_jsonl_tags("rev_batch")   # C1rep, C2rep (August)
    formal = pd.read_csv(ROOT / "runs" / "results_formal.csv")
    f12 = formal[formal.condition.isin(["C1", "C2"])][
        ["model", "condition", "task_id", "correct"]].copy()

    if batch.empty:
        say("!! rev_batch_* logs not found: C1/C2 replay cells are missing.")
        return

    keep = ["model", "condition", "task_id", "correct", "provider",
            "returned_model_id", "timestamp_utc"]
    dat = pd.concat([new[keep], batch[keep]],
                    ignore_index=True)
    dat["timestamp_utc"] = pd.to_datetime(
        dat["timestamp_utc"], errors="coerce", utc=True)

    say("=== Revision-1 crossing: wording x scaffold, no-convention row ===")
    say("ANALYSIS SET: four cells collected in adjacent August 2026 windows;")
    say("this reduces temporal separation but does not eliminate date/routing imbalance.")
    say(f"n per cell: {dat.groupby('condition').size().to_dict()}; "
        f"tasks: {dat.task_id.nunique()}; models: {dat.model.nunique()}")
    say("observed UTC timestamp ranges:")
    for condition, sub in dat.groupby("condition"):
        say(f"  {condition}: {sub.timestamp_utc.min()} to {sub.timestamp_utc.max()}")
    say()

    CELLS = [("C1rep", "improvised", "none"), ("C1wS", "improvised", "scaffold"),
             ("Creg", "regularized", "none"), ("C2rep", "regularized", "scaffold")]
    cells = {}
    say("--- strict correctness, adjacent-window cells (cluster-bootstrap 95% CI) ---")
    for c, w, s in CELLS:
        sub = dat[dat.condition == c]
        mval = sub.correct.mean() * 100
        lo, hi = cluster_ci(sub)
        cells[c] = mval
        say(f"{c:6} [{w:11} x {s:8}]: {mval:5.1f}  [{lo:.1f}, {hi:.1f}]  (n={len(sub)})")
    say()

    say("--- simple effects (pp, paired task-cluster bootstrap 95% CI) ---")
    for name, a, b_ in [
            ("wording  | no scaffold  (Creg  - C1rep)", "Creg", "C1rep"),
            ("wording  | + scaffold   (C2rep - C1wS) ", "C2rep", "C1wS"),
            ("scaffold | improvised   (C1wS  - C1rep)", "C1wS", "C1rep"),
            ("scaffold | regularized  (C2rep - Creg) ", "C2rep", "Creg"),
            ("bundle                  (C2rep - C1rep)", "C2rep", "C1rep")]:
        d = cells[a] - cells[b_]
        lo, hi = cluster_diff_ci(dat[dat.condition == a], dat[dat.condition == b_])
        say(f"{name}: {d:+5.1f}  [{lo:+.1f}, {hi:+.1f}]")
    inter = (cells["C2rep"] - cells["Creg"]) - (cells["C1wS"] - cells["C1rep"])
    ilo, ihi = interaction_ci(dat, "C1rep", "C1wS", "Creg", "C2rep")
    say(f"interaction (difference-in-differences)  : {inter:+5.1f}  [{ilo:+.1f}, {ihi:+.1f}]")
    say()

    # ---- inference: pre-registered order (mixed logit primary, GEE robustness)
    d2 = dat.copy()
    d2["wording_reg"] = d2.condition.isin(["Creg", "C2rep"]).astype(int)
    d2["scaffold"] = d2.condition.isin(["C1wS", "C2rep"]).astype(int)
    d2["model_provider"] = d2["model"] + "::" + d2["provider"].fillna("unknown")

    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

    say("--- MIXED-EFFECTS LOGISTIC: variational approximation, task random")
    say("    intercept and model fixed effects; specification mirrors mixed_logit.py ---")
    try:
        mg = BinomialBayesMixedGLM.from_formula(
            "correct ~ wording_reg * scaffold + C(model)",
            {"task": "0 + C(task_id)"}, d2).fit_vb(verbose=False)
        names = list(mg.model.exog_names)
        for t in ("wording_reg", "scaffold", "wording_reg:scaffold"):
            i = names.index(t)
            mean, sd = mg.fe_mean[i], mg.fe_sd[i]
            say(f"{t:22}: OR={np.exp(mean):5.2f}  "
                f"[{np.exp(mean - 1.96 * sd):.2f}, {np.exp(mean + 1.96 * sd):.2f}]"
                f"  (variational posterior mean, approximate 95% interval)")
    except Exception as e:  # noqa: BLE001
        say(f"mixed logit failed: {e!r}")
    say()

    say("--- ROBUSTNESS: GEE logit, exchangeable, task clusters, model FE ---")
    gee = smf.gee("correct ~ wording_reg * scaffold + C(model)", groups="task_id",
                  data=d2, family=sm.families.Binomial(),
                  cov_struct=sm.cov_struct.Exchangeable()).fit()
    for t in ("wording_reg", "scaffold", "wording_reg:scaffold"):
        lo, hi = np.exp(gee.conf_int().loc[t])
        say(f"{t:22}: OR={np.exp(gee.params[t]):5.2f}  [{lo:.2f}, {hi:.2f}]  "
            f"p={gee.pvalues[t]:.4f}")
    say()
    # 路由提供方可能随采集日变化；以“请求模型×提供方”固定效应作事后审计。
    say("--- POST-HOC ROUTING SENSITIVITY: GEE with model-provider fixed effects ---")
    say("condition x requested-model/provider counts:")
    say(pd.crosstab(d2["condition"], d2["model_provider"]).to_string())
    try:
        gee_route = smf.gee(
            "correct ~ wording_reg * scaffold + C(model_provider)",
            groups="task_id", data=d2, family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable()
        ).fit()
        for t in ("wording_reg", "scaffold", "wording_reg:scaffold"):
            lo, hi = np.exp(gee_route.conf_int().loc[t])
            say(
                f"{t:22}: OR={np.exp(gee_route.params[t]):5.2f}  "
                f"[{lo:.2f}, {hi:.2f}]  p={gee_route.pvalues[t]:.4f}"
            )
    except Exception as exc:  # noqa: BLE001
        say(f"provider-adjusted GEE failed: {exc!r}")
    say()


    # ---- drift check: June formal vs August replay -------------------------
    say("--- DRIFT CHECK: June 2026 formal cells vs August 2026 replays ---")
    for june, aug in (("C1", "C1rep"), ("C2", "C2rep")):
        j = f12[f12.condition == june]
        a = dat[dat.condition == aug]
        dj, da = j.correct.mean() * 100, a.correct.mean() * 100
        lo, hi = cluster_diff_ci(a.assign(correct=a.correct), j.assign(correct=j.correct))
        say(f"{june} (June) {dj:5.1f}  vs  {aug} (Aug) {da:5.1f}   "
            f"diff {da - dj:+5.1f} pp  [{lo:+.1f}, {hi:+.1f}]")
    say("(These are descriptive drift-audit intervals; including zero does not "
        "establish absence of drift.)")
    say()

    say("--- per model (strict correctness %, adjacent-window cells) ---")
    say(f"{'model':6} {'C1rep':>7} {'C1wS':>7} {'Creg':>7} {'C2rep':>7}")
    for m in ("M1", "M2", "M3"):
        v = [dat[(dat.condition == c) & (dat.model == m)].correct.mean() * 100
             for c in ("C1rep", "C1wS", "Creg", "C2rep")]
        say(f"{m:6} {v[0]:7.1f} {v[1]:7.1f} {v[2]:7.1f} {v[3]:7.1f}")
    say()

    say("--- per task type (strict correctness %, adjacent-window cells) ---")
    d2["ttype"] = d2.task_id.str.extract(r"_(T\d)")
    say(f"{'type':5} {'C1rep':>7} {'C1wS':>7} {'Creg':>7} {'C2rep':>7}")
    for t in ("T1", "T2", "T3"):
        v = [d2[(d2.condition == c) & (d2.ttype == t)].correct.mean() * 100
             for c in ("C1rep", "C1wS", "Creg", "C2rep")]
        say(f"{t:5} {v[0]:7.1f} {v[1]:7.1f} {v[2]:7.1f} {v[3]:7.1f}")
    say()

    say("--- executability / bucket mix, all August cells ---")
    allaug = pd.concat([new, batch], ignore_index=True)
    for c in ("C1rep", "C1wS", "Creg", "C2rep"):
        sub = allaug[allaug.condition == c]
        say(f"{c:6}: exec_ok={sub.exec_ok.mean()*100:5.1f}%  "
            f"buckets={sub.bucket.value_counts().to_dict()}")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
