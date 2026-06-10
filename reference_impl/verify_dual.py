"""Dual-path verification of the reference answers (stage-1 acceptance check #2).

Every numerical ground-truth value in tasks/answers/answers.json is recomputed
here through an INDEPENDENT second path - different algorithm and different
library from the reference implementation - and must agree to 1e-8:

  KP1  closed-form Sigma^-1 1 / (1'Sigma^-1 1) and A,B,C,D frontier scalars
       vs. KKT linear systems solved in 50-digit mpmath arithmetic
       (plus a scipy SLSQP solver cross-check at 1e-6)
  KP2  float arithmetic vs. decimal.Decimal arithmetic
  KP3  analytic cashflow sums vs. mpmath high-precision derivatives of the
       price function (D_mac = -P'(y)(1+y)/P, convexity = P''(y)/P)
  KP4  scipy.stats.norm formulas vs. mpmath erfc-based normal cdf/pdf and
       numerical differentiation for delta and vega
  KP5  scipy norm.ppf vs. mpmath sqrt(2)*erfinv(2c-1); numpy percentile vs.
       a hand-written sorted linear interpolation
  KP6  numpy vectorized stats vs. pure-Python math.fsum loops

Writes dual_verification_report.txt and exits nonzero on any failure.
"""

import json
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path

import mpmath as mp
import numpy as np
import pandas as pd
import yaml
from scipy import optimize
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
ANSWERS = json.loads((ROOT / "tasks" / "answers" / "answers.json").read_text(encoding="utf-8"))
TOL = 1e-8
mp.mp.dps = 50
getcontext().prec = 50

checks = []


def record(name, ref_value, alt_value, tol=TOL):
    diff = abs(float(ref_value) - float(alt_value))
    checks.append((name, float(ref_value), float(alt_value), diff, diff < tol))


def task_inputs(task_id):
    spec = yaml.safe_load((ROOT / "tasks" / f"{task_id}.yaml").read_text(encoding="utf-8"))
    return spec["inputs"], spec


def mp_normcdf(x):
    return 0.5 * mp.erfc(-x / mp.sqrt(2))


def mp_normpdf(x):
    return mp.exp(-x * x / 2) / mp.sqrt(2 * mp.pi)


# ---- KP1 ------------------------------------------------------------------
def kp1():
    i, _ = task_inputs("KP1_T1")
    vols, corr = i["vols_annual"], i["corr"]
    n = len(vols)
    cov = mp.matrix(n, n)
    for a in range(n):
        for b in range(n):
            cov[a, b] = mp.mpf(str(vols[a])) * mp.mpf(str(vols[b])) * mp.mpf(str(corr[a][b]))
    # KKT for min variance s.t. 1'w = 1:  [2C 1; 1' 0][w; l] = [0; 1]
    kkt = mp.matrix(n + 1, n + 1)
    rhs = mp.matrix(n + 1, 1)
    for a in range(n):
        for b in range(n):
            kkt[a, b] = 2 * cov[a, b]
        kkt[a, n] = kkt[n, a] = 1
    rhs[n] = 1
    sol = mp.lu_solve(kkt, rhs)
    w = sol[:n]
    variance = sum(w[a] * cov[a, b] * w[b] for a in range(n) for b in range(n))
    record("KP1_T1.mvp_vol_annual", ANSWERS["KP1_T1"]["refs"]["mvp_vol_annual"], mp.sqrt(variance))
    for a in range(n):
        record(f"KP1_T1.mvp_weights[{a}]", ANSWERS["KP1_T1"]["refs"]["mvp_weights"][a], w[a])
    record("KP1_T1.objective.min_variance", ANSWERS["KP1_T1"]["objective"]["min_variance"], variance)

    i, _ = task_inputs("KP1_T2")
    s1, s2 = i["vols_annual"]
    rho = mp.mpf(str(i["rho_for_numbers"]))
    s1m, s2m = mp.mpf(str(s1)), mp.mpf(str(s2))
    c12 = rho * s1m * s2m
    # 2-asset MVP weight, independent closed form
    w1 = (s2m ** 2 - c12) / (s1m ** 2 + s2m ** 2 - 2 * c12)
    var2 = w1 ** 2 * s1m ** 2 + (1 - w1) ** 2 * s2m ** 2 + 2 * w1 * (1 - w1) * c12
    record("KP1_T2.mvp_vol_at_rho45", ANSWERS["KP1_T2"]["refs"]["mvp_vol_at_rho45"], mp.sqrt(var2))
    # frontier at target via 2x2 equality system: with 2 assets and both
    # constraints (sum=1, mu'w=target) weights are fully determined
    mus = i["mus_annual"]
    wA = (mp.mpf(str(i["target_return_annual"])) - mp.mpf(str(mus[1]))) / \
         (mp.mpf(str(mus[0])) - mp.mpf(str(mus[1])))
    varT = wA ** 2 * s1m ** 2 + (1 - wA) ** 2 * s2m ** 2 + 2 * wA * (1 - wA) * c12
    record("KP1_T2.frontier_vol_at_target",
           ANSWERS["KP1_T2"]["refs"]["frontier_vol_at_target"], mp.sqrt(varT))

    # solver cross-check (SLSQP), looser tolerance
    cov_np = np.outer([s1, s2], [s1, s2]) * np.array([[1, float(rho)], [float(rho), 1]])
    res = optimize.minimize(lambda w: w @ cov_np @ w, [0.5, 0.5],
                            constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
                            method="SLSQP", options={"ftol": 1e-14, "maxiter": 500})
    record("KP1_T2.mvp_vol_at_rho45 (SLSQP)",
           ANSWERS["KP1_T2"]["refs"]["mvp_vol_at_rho45"], math.sqrt(res.fun), tol=1e-6)

    i, _ = task_inputs("KP1_T3")
    for cond in ANSWERS["KP1_T3"]["t3_conditional"]:
        wgt = [0.6, 0.4] if cond["label"].startswith("strict") else [0.4, 0.6]
        for tag, rho_v in (("vol_before_annual", i["rho_before"]),
                           ("vol_after_annual", i["rho_after"])):
            sa = mp.mpf(str(i["vol_a_annual"]))
            sb = mp.mpf(str(i["vol_b_annual"]))
            w1m = mp.mpf(str(wgt[0]))
            v = (w1m ** 2 * sa ** 2 + (1 - w1m) ** 2 * sb ** 2
                 + 2 * w1m * (1 - w1m) * mp.mpf(str(rho_v)) * sa * sb)
            record(f"KP1_T3[{cond['label']}].{tag}", cond["values"][tag], mp.sqrt(v))


# ---- KP2 ------------------------------------------------------------------
def kp2():
    i, _ = task_inputs("KP2_T1")
    rf, erm = Decimal(str(i["rf_annual"])), Decimal(str(i["expected_market_return_annual"]))
    for stock in ("x", "y", "z"):
        beta = Decimal(str(i["betas"][stock]))
        record(f"KP2_T1.er_{stock}", ANSWERS["KP2_T1"]["refs"][f"er_{stock}"],
               rf + beta * (erm - rf))
    er_y = rf + Decimal(str(i["betas"]["y"])) * (erm - rf)
    record("KP2_T1.alpha_y", ANSWERS["KP2_T1"]["refs"]["alpha_y"],
           Decimal(str(i["realized_return_y_annual"])) - er_y)

    i, _ = task_inputs("KP2_T2")
    rf, erm = Decimal(str(i["rf_annual"])), Decimal(str(i["expected_market_return_annual"]))
    record("KP2_T2.sml_slope", ANSWERS["KP2_T2"]["refs"]["sml_slope"], erm - rf)
    record("KP2_T2.er_at_beta_127", ANSWERS["KP2_T2"]["refs"]["er_at_beta_127"],
           rf + Decimal(str(i["beta_for_number"])) * (erm - rf))

    i, _ = task_inputs("KP2_T3")
    beta = mp.mpf(str(i["beta"]))
    rm = mp.mpf(str(i["market_return_monthly"]))
    rf_simple = mp.mpf(str(i["rf_annual"])) / 12
    rf_geo = mp.power(1 + mp.mpf(str(i["rf_annual"])), mp.mpf(1) / 12) - 1
    for cond in ANSWERS["KP2_T3"]["t3_conditional"]:
        rf_m = rf_simple if cond["label"].startswith("strict") else rf_geo
        record(f"KP2_T3[{cond['label']}]", cond["values"]["capm_return_monthly"],
               rf_m + beta * (rm - rf_m))


# ---- KP3 ------------------------------------------------------------------
def kp3():
    i, _ = task_inputs("KP3_T1")
    face = mp.mpf(str(i["face"]))
    c = face * mp.mpf(str(i["coupon_rate_annual"]))
    n = i["n_years"]
    y0 = mp.mpf(str(i["ytm_annual"]))

    def P(y):
        return sum((c + (face if t == n else 0)) / (1 + y) ** t for t in range(1, n + 1))

    p = P(y0)
    dP = mp.diff(P, y0)
    d2P = mp.diff(P, y0, 2)
    record("KP3_T1.price", ANSWERS["KP3_T1"]["refs"]["price"], p)
    record("KP3_T1.macaulay_duration_years",
           ANSWERS["KP3_T1"]["refs"]["macaulay_duration_years"], -dP * (1 + y0) / p)
    record("KP3_T1.modified_duration_years",
           ANSWERS["KP3_T1"]["refs"]["modified_duration_years"], -dP / p)
    record("KP3_T1.convexity", ANSWERS["KP3_T1"]["refs"]["convexity"], d2P / p)

    i2, _ = task_inputs("KP3_T2")
    dy = mp.mpf(str(i2["dy_for_numbers"]))
    record("KP3_T2.price_at_up100bp", ANSWERS["KP3_T2"]["refs"]["price_at_up100bp"], P(y0 + dy))
    record("KP3_T2.dur_approx_change_up100bp",
           ANSWERS["KP3_T2"]["refs"]["dur_approx_change_up100bp"], (dP / p) * dy)

    i3, _ = task_inputs("KP3_T3")
    dy = mp.mpf(str(i3["dy"]))
    # drop magnitude = -(relative price change); P' < 0 so -(dP/p)*dy > 0
    expected = {
        "strict_duration_only": -(dP / p) * dy,
        "duration_plus_convexity": -(dP / p) * dy - (d2P / p) / 2 * dy ** 2,
        "exact_repricing": -(P(y0 + dy) - p) / p,
    }
    for cond in ANSWERS["KP3_T3"]["t3_conditional"]:
        record(f"KP3_T3[{cond['label']}]", cond["values"]["price_drop_pct"],
               expected[cond["label"]])


# ---- KP4 ------------------------------------------------------------------
def kp4():
    i, _ = task_inputs("KP4_T1")
    s = mp.mpf(str(i["spot"]))
    k = mp.mpf(str(i["strike"]))
    sig = mp.mpf(str(i["sigma_annual"]))
    r = mp.mpf(str(i["r_annual_cc"]))
    t = mp.mpf(str(i["t_years"]))

    def call(spot, sigma):
        d1 = (mp.log(spot / k) + (r + sigma ** 2 / 2) * t) / (sigma * mp.sqrt(t))
        d2 = d1 - sigma * mp.sqrt(t)
        return spot * mp_normcdf(d1) - k * mp.exp(-r * t) * mp_normcdf(d2)

    record("KP4_T1.call_price", ANSWERS["KP4_T1"]["refs"]["call_price"], call(s, sig))
    record("KP4_T1.call_delta", ANSWERS["KP4_T1"]["refs"]["call_delta"],
           mp.diff(lambda x: call(x, sig), s))
    record("KP4_T1.call_vega", ANSWERS["KP4_T1"]["refs"]["call_vega"],
           mp.diff(lambda v: call(s, v), sig))

    i2, _ = task_inputs("KP4_T2")
    s110 = mp.mpf(str(i2["spot_for_number"]))
    record("KP4_T2.delta_at_s110", ANSWERS["KP4_T2"]["refs"]["delta_at_s110"],
           mp.diff(lambda x: call(x, sig), s110))

    i3, _ = task_inputs("KP4_T3")
    ds = mp.mpf(str(i3["dsigma"]))
    for cond in ANSWERS["KP4_T3"]["t3_conditional"]:
        if cond["label"].startswith("strict"):
            alt = call(s, sig + ds) - call(s, sig)
        else:
            alt = mp.diff(lambda v: call(s, v), sig) * ds
        record(f"KP4_T3[{cond['label']}]", cond["values"]["price_change"], alt)


# ---- KP5 ------------------------------------------------------------------
def kp5():
    def mp_z(conf):
        return mp.sqrt(2) * mp.erfinv(2 * mp.mpf(str(conf)) - 1)

    record("z(0.95): scipy vs mpmath", norm.ppf(0.95), mp_z(0.95))
    record("z(0.99): scipy vs mpmath", norm.ppf(0.99), mp_z(0.99))

    i, _ = task_inputs("KP5_T1")
    v = mp.mpf(str(i["position_value_cny"]))
    sig = mp.mpf(str(i["sigma_annual"]))
    record("KP5_T1.var_95_1d", ANSWERS["KP5_T1"]["refs"]["var_95_1d"],
           v * mp_z(0.95) * sig / mp.sqrt(252), tol=1e-6)
    record("KP5_T1.var_99_10d", ANSWERS["KP5_T1"]["refs"]["var_99_10d"],
           v * mp_z(0.99) * sig / mp.sqrt(252) * mp.sqrt(10), tol=1e-6)

    i, spec = task_inputs("KP5_T2")
    df = pd.read_csv(ROOT / spec["data_file"])
    pnl = sorted(float(x) * i["position_value_cny"] for x in df[i["data_column"]])
    # hand-rolled linear-interpolated percentile (numpy 'linear' definition)
    q = (1 - i["confidence"]) * (len(pnl) - 1)
    lo = int(math.floor(q))
    frac = q - lo
    manual = pnl[lo] + frac * (pnl[lo + 1] - pnl[lo])
    record("KP5_T2.hist_var_95_1d", ANSWERS["KP5_T2"]["refs"]["hist_var_95_1d"],
           -manual, tol=1e-6)

    i, _ = task_inputs("KP5_T3")
    v = mp.mpf(str(i["position_value_cny"]))
    sig = mp.mpf(str(i["sigma_annual"]))
    days = {"strict_252": 252, "alt_250": 250, "alt_365": 365}
    for cond in ANSWERS["KP5_T3"]["t3_conditional"]:
        record(f"KP5_T3[{cond['label']}]", cond["values"]["var_95_1d"],
               v * mp_z(0.95) * sig / mp.sqrt(days[cond["label"]]), tol=1e-6)


# ---- KP6 ------------------------------------------------------------------
def kp6():
    i, spec = task_inputs("KP6_T1")
    df = pd.read_csv(ROOT / spec["data_file"])
    r = [float(x) for x in df[i["data_column"]]]

    def sharpe_pure(series, rf_daily, periods, ddof):
        n = len(series)
        ex = [x - rf_daily for x in series]
        mean = math.fsum(ex) / n
        ss = math.fsum((x - mean) ** 2 for x in ex)
        sd = math.sqrt(ss / (n - ddof))
        return mean / sd * math.sqrt(periods)

    record("KP6_T1.sharpe_annual", ANSWERS["KP6_T1"]["refs"]["sharpe_annual"],
           sharpe_pure(r, i["rf_annual"] / 252, 252, 1))
    wp, wb = i["w_portfolio"], i["w_benchmark"]
    rp, rb = i["r_portfolio"], i["r_benchmark"]
    record("KP6_T1.allocation_effect", ANSWERS["KP6_T1"]["refs"]["allocation_effect"],
           math.fsum((Decimal(str(wp[j])) - Decimal(str(wb[j]))) * Decimal(str(rb[j]))
                     for j in range(3)))
    record("KP6_T1.selection_effect", ANSWERS["KP6_T1"]["refs"]["selection_effect"],
           math.fsum(Decimal(str(wb[j])) * (Decimal(str(rp[j])) - Decimal(str(rb[j])))
                     for j in range(3)))
    record("KP6_T1.interaction_effect", ANSWERS["KP6_T1"]["refs"]["interaction_effect"],
           math.fsum((Decimal(str(wp[j])) - Decimal(str(wb[j])))
                     * (Decimal(str(rp[j])) - Decimal(str(rb[j]))) for j in range(3)))

    i2, _ = task_inputs("KP6_T2")
    record("KP6_T2.rolling_sharpe_last", ANSWERS["KP6_T2"]["refs"]["rolling_sharpe_last"],
           sharpe_pure(r[-i2["window_days"]:], i2["rf_annual"] / 252, 252, 1))

    i3, _ = task_inputs("KP6_T3")
    variants = {
        "strict_252_ddof1_rfsimple": (i3["rf_annual"] / 252, 252, 1),
        "rf_geometric": ((1 + i3["rf_annual"]) ** (1 / 252) - 1, 252, 1),
        "ddof_0": (i3["rf_annual"] / 252, 252, 0),
        "alt_250": (i3["rf_annual"] / 250, 250, 1),
    }
    for cond in ANSWERS["KP6_T3"]["t3_conditional"]:
        rf_d, periods, ddof = variants[cond["label"]]
        record(f"KP6_T3[{cond['label']}]", cond["values"]["sharpe_annual"],
               sharpe_pure(r, rf_d, periods, ddof))


def main():
    for fn in (kp1, kp2, kp3, kp4, kp5, kp6):
        fn()
    lines = ["Dual-path verification report",
             f"checks: {len(checks)}", ""]
    n_fail = 0
    for name, ref, alt, diff, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            n_fail += 1
        lines.append(f"[{status}] {name}: ref={ref:.12g} alt={alt:.12g} |diff|={diff:.3g}")
    lines.append("")
    lines.append(f"RESULT: {len(checks) - n_fail}/{len(checks)} passed")
    report = "\n".join(lines)
    (Path(__file__).resolve().parent / "dual_verification_report.txt").write_text(
        report + "\n", encoding="utf-8")
    print(report)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
