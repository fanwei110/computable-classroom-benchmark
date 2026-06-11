"""Deterministic mechanical error-coder.

Implements, as executable code, the codebook's preregistered mechanical
criterion: identify the convention a failed generation actually used by
recomputing the reference under every enumerated candidate convention and
checking which one explains ALL failed keys within the task's tolerances.

Output classes per item:
  CV:<variant>      a recognized convention swap explains every failed key
  CN:<pattern>      a known conceptual-error pattern explains them
                    (no convention has textbook standing)
  CN:hardcoded_constant   all failed keys within 0.2% of reference but not
                    explained by any swap - the hand-rounded-constant class,
                    ruled CN per the letter of the frozen codebook (analyst
                    pre-declared ruling, disclosed; share reported separately)
  UNMATCHED         no deterministic explanation - goes to the AI coders

Also emits declared_auto (commentary-only evidence) per item.
Writes coding/auto/mechanical_coded.csv.
"""

import io
import json
import math
import re
import sys
import tokenize
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import norm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reference_impl import portfolio, capm, bond, blackscholes, var, performance  # noqa: E402

LOG = ROOT / "runs" / "raw" / "formal" / "formal.jsonl"
ANSWERS = json.loads((ROOT / "tasks" / "answers" / "answers.json").read_text(encoding="utf-8"))
NEED = {"numeric_wrong", "defensible", "vis_failure"}


def spec(task_id):
    return yaml.safe_load((ROOT / "tasks" / f"{task_id}.yaml").read_text(encoding="utf-8"))


def tol(task_id, key, refv):
    for k in spec(task_id)["scoring"]["keys"]:
        if k["key"] == key:
            return max(k["tau_abs"], k["tau_rel"] * abs(refv))
    return max(1e-6, 1e-4 * abs(refv))


def fund():
    df = pd.read_csv(ROOT / "data" / "market_snapshot_v1.csv")
    return df["fund"].to_numpy()


def sharpe_v(r, rf_daily, periods, ddof):
    ex = r - rf_daily
    return float(ex.mean() / ex.std(ddof=ddof) * np.sqrt(periods))


def build_variants():
    """{task_id: [(label, kind, {key: value}), ...]} kind in {CV, CN}."""
    V = {}
    R = fund()

    def refs(t):
        return ANSWERS[t]["refs"]

    # ---- KP1 ----
    w_c = portfolio.min_variance_weights([[1, .21, -.13], [.21, 1, .37], [-.13, .37, 1]])
    corr = np.array([[1, .21, -.13], [.21, 1, .37], [-.13, .37, 1]])
    V["KP1_T1"] = [
        ("corr_as_cov", "CN", {"mvp_vol_annual": float(np.sqrt(w_c @ corr @ w_c))}),
        ("variance_as_vol", "CN", {"mvp_vol_annual": refs("KP1_T1")["mvp_vol_annual"] ** 2}),
    ]
    V["KP1_T2"] = [
        ("variance_as_vol", "CN", {k: refs("KP1_T2")[k] ** 2
                                   for k in ("mvp_vol_at_rho45", "frontier_vol_at_target")}),
    ]
    rev = next(c for c in ANSWERS["KP1_T3"]["t3_conditional"] if not c["strict"])
    V["KP1_T3"] = [
        ("reversed_40A_60B", "CV", dict(rev["values"])),
        ("variance_as_vol", "CN", {k: refs("KP1_T3")[k] ** 2
                                   for k in ("vol_before_annual", "vol_after_annual")}),
    ]

    # ---- KP2 ----
    erm, rf = 0.094, 0.023
    V["KP2_T1"] = [
        ("forgot_rf_term", "CN", {"er_x": .62 * erm, "er_y": 1.18 * erm, "er_z": 1.51 * erm,
                                  "alpha_y": .131 - 1.18 * erm}),
    ]
    V["KP2_T2"] = [("forgot_rf_term", "CN", {"er_at_beta_127": 1.27 * erm})]
    geo = next(c for c in ANSWERS["KP2_T3"]["t3_conditional"] if not c["strict"])
    V["KP2_T3"] = [
        ("rf_geometric", "CV", dict(geo["values"])),
        ("rf_unconverted_annual", "CV", {"capm_return_monthly": .047 + 1.42 * (-.058 - .047)}),
        ("rf_ignored", "CV", {"capm_return_monthly": 1.42 * -.058}),
    ]

    # ---- KP3 ----
    F, c, n, y = 100.0, .046, 7, .053
    # semiannual treatment of the annual bond
    per = n * 2
    cfs2 = [(t, F * c / 2 + (F if t == per else 0)) for t in range(1, per + 1)]
    p2 = sum(cf / (1 + y / 2) ** t for t, cf in cfs2)
    mac2 = sum(t * cf / (1 + y / 2) ** t for t, cf in cfs2) / p2 / 2
    cx2 = sum(t * (t + 1) * cf / (1 + y / 2) ** (t + 2) for t, cf in cfs2) / p2 / 4
    cx_var = sum(t * (t + 1) * (F * c + (F if t == n else 0)) / (1 + y) ** t
                 for t in range(1, n + 1)) / bond.price(F, c, n, y)
    p_cc = sum((F * c + (F if t == n else 0)) * math.exp(-y * t) for t in range(1, n + 1))
    V["KP3_T1"] = [
        ("semiannual", "CV", {"price": p2, "macaulay_duration_years": mac2,
                              "modified_duration_years": mac2 / (1 + y / 2),
                              "convexity": cx2}),
        ("convexity_no_div", "CV", {"convexity": cx_var}),
        ("macaulay_as_modified", "CN",
         {"modified_duration_years": bond.macaulay_duration(F, c, n, y)}),
        ("continuous_comp", "CV", {"price": p_cc}),
    ]
    dur1 = bond.price_change_duration(F, c, n, y, .01)
    dur2 = bond.price_change_duration_convexity(F, c, n, y, .01)
    exact = bond.price_change_exact(F, c, n, y, .01)
    V["KP3_T2"] = [
        ("dur_plus_convexity", "CV", {"dur_approx_change_up100bp": dur2}),
        ("exact_as_approx", "CV", {"dur_approx_change_up100bp": exact}),
        ("approx_price", "CV", {"price_at_up100bp": bond.price(F, c, n, y) * (1 + dur1)}),
        ("sign_dur", "CV", {"dur_approx_change_up100bp": -dur1}),
    ]
    V["KP3_T3"] = [(cc["label"], "CV", dict(cc["values"]))
                   for cc in ANSWERS["KP3_T3"]["t3_conditional"] if not cc["strict"]]
    V["KP3_T3"].append(("sign_drop", "CV",
                        {"price_drop_pct": -ANSWERS["KP3_T3"]["refs"]["price_drop_pct"]}))

    # ---- KP4 ----
    s_, k_, sg, r_, t_ = 103.7, 97.5, .276, .043, .58
    rr = math.log(1 + r_)
    V["KP4_T1"] = [
        ("vega_per_pct", "CV", {"call_vega": blackscholes.vega(s_, k_, sg, r_, t_) / 100}),
        ("discrete_discount", "CV",
         {"call_price": s_ * norm.cdf(blackscholes.d1(s_, k_, sg, r_, t_))
          - k_ * (1 + r_) ** -t_ * norm.cdf(blackscholes.d2(s_, k_, sg, r_, t_))}),
        ("rate_as_cc_of_simple", "CV",
         {"call_price": blackscholes.call_price(s_, k_, sg, rr, t_),
          "call_delta": blackscholes.call_delta(s_, k_, sg, rr, t_)}),
        ("put_instead_of_call", "CN",
         {"call_price": blackscholes.put_price(s_, k_, sg, r_, t_),
          "call_delta": blackscholes.call_delta(s_, k_, sg, r_, t_) - 1}),
        ("delta_n_d2", "CN",
         {"call_delta": float(norm.cdf(blackscholes.d2(s_, k_, sg, r_, t_)))}),
    ]
    V["KP4_T2"] = [
        ("delta_n_d2", "CN",
         {"delta_at_s110": float(norm.cdf(blackscholes.d2(110, k_, sg, r_, t_)))}),
    ]
    vega_ap = next(cc for cc in ANSWERS["KP4_T3"]["t3_conditional"] if not cc["strict"])
    V["KP4_T3"] = [("vega_approximation", "CV", dict(vega_ap["values"]))]

    # ---- KP5 ----
    def pv(value, sig, conf, hor, days):
        return float(value * norm.ppf(conf) * sig / np.sqrt(days) * np.sqrt(hor))

    V["KP5_T1"] = [
        ("ann_365", "CV", {"var_95_1d": pv(1.85e6, .218, .95, 1, 365),
                           "var_99_10d": pv(1.85e6, .218, .99, 10, 365)}),
        ("ann_250", "CV", {"var_95_1d": pv(1.85e6, .218, .95, 1, 250),
                           "var_99_10d": pv(1.85e6, .218, .99, 10, 250)}),
        ("two_tailed_z", "CN", {"var_95_1d": float(1.85e6 * norm.ppf(.975) * .218 / 15.8745),
                                "var_99_10d": float(1.85e6 * norm.ppf(.995) * .218 / 15.8745 * math.sqrt(10))}),
        ("horizon_in_days_not_sqrt", "CV",
         {"var_99_10d": pv(1.85e6, .218, .99, 1, 252) * 10}),
    ]
    pnl = np.sort(R * 1e6)
    V["KP5_T2"] = [
        ("interp_lower", "CV",
         {"hist_var_95_1d": float(-np.percentile(pnl, 5, method="lower"))}),
        ("interp_higher", "CV",
         {"hist_var_95_1d": float(-np.percentile(pnl, 5, method="higher"))}),
        ("return_not_pnl", "CV",
         {"hist_var_95_1d": float(-np.percentile(R, 5))}),
    ]
    V["KP5_T3"] = [(cc["label"], "CV", dict(cc["values"]))
                   for cc in ANSWERS["KP5_T3"]["t3_conditional"] if not cc["strict"]]
    V["KP5_T3"].append(("two_tailed_z", "CN",
                        {"var_95_1d": float(2.7e6 * norm.ppf(.975) * .24 / 15.8745)}))

    # ---- KP6 ----
    sh = ANSWERS["KP6_T1"]["refs"]["sharpe_annual"]
    wp, wb = np.array([.45, .35, .20]), np.array([.40, .40, .20])
    rp, rb = np.array([.083, .021, -.014]), np.array([.067, .034, -.009])
    rb_tot = float((wb * rb).sum())
    V["KP6_T1"] = [
        ("rf_zero", "CV", {"sharpe_annual": sharpe_v(R, 0, 252, 1)}),
        ("ddof_0", "CV", {"sharpe_annual": sharpe_v(R, .021 / 252, 252, 0)}),
        ("ann_250", "CV", {"sharpe_annual": sharpe_v(R, .021 / 250, 250, 1)}),
        ("rf_geometric", "CV",
         {"sharpe_annual": sharpe_v(R, (1.021) ** (1 / 252) - 1, 252, 1)}),
        ("not_annualized", "CV", {"sharpe_annual": sh / math.sqrt(252)}),
        ("attr_BF_allocation", "CV",
         {"allocation_effect": float(((wp - wb) * (rb - rb_tot)).sum())}),
    ]
    last = R[-60:]
    shl = ANSWERS["KP6_T2"]["refs"]["rolling_sharpe_last"]
    V["KP6_T2"] = [
        ("rf_zero", "CV", {"rolling_sharpe_last": sharpe_v(last, 0, 252, 1)}),
        ("ddof_0", "CV", {"rolling_sharpe_last": sharpe_v(last, .021 / 252, 252, 0)}),
        ("not_annualized", "CV", {"rolling_sharpe_last": shl / math.sqrt(252)}),
        ("window_annualized_by_window", "CV",
         {"rolling_sharpe_last": sharpe_v(last, .021 / 252, 60, 1)}),
    ]
    V["KP6_T3"] = [(cc["label"], "CV", dict(cc["values"]))
                   for cc in ANSWERS["KP6_T3"]["t3_conditional"] if not cc["strict"]]
    V["KP6_T3"] += [
        ("rf_zero", "CV", {"sharpe_annual": sharpe_v(R, 0, 252, 1)}),
        ("not_annualized", "CV",
         {"sharpe_annual": ANSWERS["KP6_T3"]["refs"]["sharpe_annual"] / math.sqrt(252)}),
    ]
    return V


VARIANTS = build_variants()

GENERIC = [("percent_x100", "CV", 100.0), ("percent_d100", "CV", 0.01),
           ("sign_flip", "CV", -1.0), ("currency_wan", "CV", 1e-4)]


def extract_failed(details):
    """{key: (submitted, strict_ref)} for keys judged not-ok vs strict refs."""
    inner = details.get("keys") if isinstance(details.get("keys"), dict) else details
    out = {}
    for k, d in inner.items():
        if isinstance(d, dict) and d.get("ok") is False and \
                isinstance(d.get("value"), (int, float)) and \
                isinstance(d.get("reference"), (int, float)):
            out[k] = (float(d["value"]), float(d["reference"]))
    return out


def commentary(code_str, completion):
    parts = []
    try:
        for tk in tokenize.generate_tokens(io.StringIO(code_str).readline):
            if tk.type in (tokenize.COMMENT, tokenize.STRING):
                parts.append(tk.string)
    except Exception:  # noqa: BLE001
        pass
    parts.append(re.sub(r"```.*?```", " ", completion, flags=re.S))
    return "\n".join(parts).lower()


DECL_PAT = re.compile(r"365|日历日|自然日|calendar|\b250\b|几何|geometric|总体标准差|"
                      r"population|ddof\s*=?\s*0|凸性|convexit|精确重定价|repric|"
                      r"vega.{0,12}(百分点|percent)|假设|采用|按照|约定|convention|assum",
                      re.I)


def classify(task_id, failed, strict_refs):
    keys = list(failed)
    # currency tasks for the wan transform
    cny = task_id.startswith("KP5") and "hist" not in "".join(keys) or task_id == "KP5_T2"
    # 1) generic uniform transforms across ALL failed keys
    for label, kind, f in GENERIC:
        if f == 1e-4 and not task_id.startswith("KP5"):
            continue
        ok = all(abs(sub - ref * f) <= tol(task_id, k, ref * f) or
                 (abs(ref * f) > 0 and abs(sub / (ref * f) - 1) < 1e-3)
                 for k, (sub, ref) in failed.items())
        if ok:
            return kind, label
    # 2) task-specific variants: every failed key must match the variant's
    #    value (keys outside the variant's domain cannot be failed keys
    #    unless near-miss)
    for label, kind, vals in VARIANTS.get(task_id, []):
        ok, covered = True, 0
        for k, (sub, ref) in failed.items():
            if k in vals:
                v = vals[k]
                if abs(sub - v) <= max(tol(task_id, k, v), abs(v) * 1e-3):
                    covered += 1
                else:
                    ok = False
                    break
            elif abs(sub / ref - 1) < 0.002 if ref else False:
                continue  # near-miss on an unrelated key is tolerated
            else:
                ok = False
                break
        if ok and covered:
            return kind, label
    # 3) hand-rounded constants: everything within 0.2% of strict reference
    if failed and all(ref and abs(sub / ref - 1) < 0.002
                      for sub, ref in failed.values()):
        return "CN", "hardcoded_constant"
    return None, None


def main():
    out_rows = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        j = r["judge"]
        if j["bucket"] not in NEED:
            continue
        det = j.get("details", {})
        code_path = ROOT / "runs" / "raw" / "formal" / "code" / f"{r['run_id']}.py"
        code = code_path.read_text(encoding="utf-8") if code_path.exists() else ""
        text = commentary(code, r["completion"])
        declared_auto = "Y" if DECL_PAT.search(text) else "N"

        if j["bucket"] == "defensible":
            cls, why = "CV", f"declared_alt:{det.get('matched')}"
        elif j["bucket"] == "vis_failure":
            cls, why = "VZ", "figure_missing"
        elif isinstance(det, dict) and det.get("reason") == \
                "declared one convention, implemented another":
            cls, why = "CV", f"impl:{det.get('matched')}|declared_mismatch"
            declared_auto = "N"
        elif isinstance(det, dict) and det.get("reason") == \
                "silent alternative convention":
            cls, why = "CV", f"silent_alt:{det.get('matched')}"
            declared_auto = "N"
        else:
            failed = extract_failed(det)
            if not failed:
                cls, why = None, "no_numeric_detail"
            else:
                kind, label = classify(r["task_id"],
                                       failed, ANSWERS[r["task_id"]]["refs"])
                cls, why = (kind, label) if kind else (None, "unmatched")
        out_rows.append({
            "run_id": r["run_id"], "task_id": r["task_id"],
            "condition": r["condition"], "model": r["model"],
            "bucket": j["bucket"],
            "mech_class": cls or "UNMATCHED", "mech_detail": why,
            "declared_auto": declared_auto,
        })

    df = pd.DataFrame(out_rows)
    outdir = ROOT / "coding" / "auto"
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir / "mechanical_coded.csv", index=False, encoding="utf-8-sig")
    n = len(df)
    matched = (df.mech_class != "UNMATCHED").sum()
    print(f"items: {n}; mechanically classified: {matched} "
          f"({100*matched/n:.0f}%); unmatched -> AI coders: {n - matched}")
    print("\nclass distribution (all conditions):")
    print(df.mech_class.value_counts().to_string())
    print("\ntop CV/CN detail labels:")
    print(df[df.mech_class != "UNMATCHED"].mech_detail.value_counts().head(20).to_string())


if __name__ == "__main__":
    main()
