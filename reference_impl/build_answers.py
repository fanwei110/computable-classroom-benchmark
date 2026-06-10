"""Build the reference answer file tasks/answers/answers.json from tasks/*.yaml.

For every task: reference values for each scored key (computed via the
reference implementations under the course conventions). For T3 tasks:
the conditional answer set - one (convention label, values) pair per
enumerated defensible convention, with exactly one strict entry.

Safety property enforced here: for every T3 task and every scored key, any
two conditional answers must be separated by more than the sum of their
acceptance bands, so the harness can never confuse two conventions.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reference_impl import portfolio, capm, bond, blackscholes, var, performance  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
OUT = TASKS / "answers" / "answers.json"


def load(task_id):
    return yaml.safe_load((TASKS / f"{task_id}.yaml").read_text(encoding="utf-8"))


def fund_returns(spec):
    df = pd.read_csv(ROOT / spec["data_file"])
    return df[spec["inputs"]["data_column"]].to_numpy()


def sharpe_variant(r, rf_annual, periods, ddof, rf_mode):
    rf_daily = (1 + rf_annual) ** (1 / periods) - 1 if rf_mode == "geometric" else rf_annual / periods
    excess = r - rf_daily
    return float(excess.mean() / excess.std(ddof=ddof) * np.sqrt(periods))


def build():
    answers = {}

    # ---- KP1 -------------------------------------------------------------
    s = load("KP1_T1")
    cov = portfolio.cov_from_vols_corr(s["inputs"]["vols_annual"], s["inputs"]["corr"])
    w = portfolio.min_variance_weights(cov)
    answers["KP1_T1"] = {
        "refs": {"mvp_vol_annual": portfolio.portfolio_vol(w, cov),
                 "mvp_weights": [float(x) for x in w]},
        "objective": {"key": "mvp_weights", "cov": cov.tolist(),
                      "min_variance": portfolio.portfolio_variance(w, cov)},
    }

    s = load("KP1_T2")
    i = s["inputs"]
    cov45 = portfolio.two_asset_cov(i["vols_annual"][0], i["vols_annual"][1], i["rho_for_numbers"])
    w45 = portfolio.min_variance_weights(cov45)
    answers["KP1_T2"] = {
        "refs": {"mvp_vol_at_rho45": portfolio.portfolio_vol(w45, cov45),
                 "frontier_vol_at_target": portfolio.frontier_vol_at_target(
                     i["mus_annual"], cov45, i["target_return_annual"])},
    }

    s = load("KP1_T3")
    i = s["inputs"]

    def vols_for(weights):
        out = {}
        for tag, rho in (("vol_before_annual", i["rho_before"]), ("vol_after_annual", i["rho_after"])):
            c = portfolio.two_asset_cov(i["vol_a_annual"], i["vol_b_annual"], rho)
            out[tag] = portfolio.portfolio_vol(weights, c)
        return out

    answers["KP1_T3"] = {
        "refs": vols_for(i["weights_strict"]),
        "t3_conditional": [
            {"label": "strict_60A_40B", "strict": True, "values": vols_for([0.6, 0.4])},
            {"label": "reversed_40A_60B", "strict": False, "values": vols_for([0.4, 0.6])},
        ],
    }

    # ---- KP2 -------------------------------------------------------------
    s = load("KP2_T1")
    i = s["inputs"]
    rf, erm = i["rf_annual"], i["expected_market_return_annual"]
    answers["KP2_T1"] = {"refs": {
        "er_x": capm.expected_return(rf, i["betas"]["x"], erm),
        "er_y": capm.expected_return(rf, i["betas"]["y"], erm),
        "er_z": capm.expected_return(rf, i["betas"]["z"], erm),
        "alpha_y": capm.alpha(i["realized_return_y_annual"], rf, i["betas"]["y"], erm),
    }}

    s = load("KP2_T2")
    i = s["inputs"]
    answers["KP2_T2"] = {"refs": {
        "sml_slope": i["expected_market_return_annual"] - i["rf_annual"],
        "er_at_beta_127": capm.expected_return(
            i["rf_annual"], i["beta_for_number"], i["expected_market_return_annual"]),
    }}

    s = load("KP2_T3")
    i = s["inputs"]
    strict_v = capm.capm_period_return(i["rf_annual"], i["beta"], i["market_return_monthly"], 12)
    rf_geo = (1 + i["rf_annual"]) ** (1 / 12) - 1
    geo_v = rf_geo + i["beta"] * (i["market_return_monthly"] - rf_geo)
    answers["KP2_T3"] = {
        "refs": {"capm_return_monthly": strict_v},
        "t3_conditional": [
            {"label": "strict_rf_simple", "strict": True,
             "values": {"capm_return_monthly": strict_v}},
            {"label": "rf_geometric", "strict": False,
             "values": {"capm_return_monthly": geo_v}},
        ],
    }

    # ---- KP3 -------------------------------------------------------------
    s = load("KP3_T1")
    i = s["inputs"]
    args = (i["face"], i["coupon_rate_annual"], i["n_years"], i["ytm_annual"])
    answers["KP3_T1"] = {"refs": {
        "price": bond.price(*args),
        "macaulay_duration_years": bond.macaulay_duration(*args),
        "modified_duration_years": bond.modified_duration(*args),
        "convexity": bond.convexity(*args),
    }}

    s = load("KP3_T2")
    i = s["inputs"]
    args = (i["face"], i["coupon_rate_annual"], i["n_years"], i["ytm_annual"])
    answers["KP3_T2"] = {"refs": {
        "price_at_up100bp": bond.price(i["face"], i["coupon_rate_annual"], i["n_years"],
                                       i["ytm_annual"] + i["dy_for_numbers"]),
        "dur_approx_change_up100bp": bond.price_change_duration(*args, i["dy_for_numbers"]),
    }}

    s = load("KP3_T3")
    i = s["inputs"]
    args = (i["face"], i["coupon_rate_annual"], i["n_years"], i["ytm_annual"])
    dy = i["dy"]
    strict_v = -bond.price_change_duration(*args, dy)            # positive magnitude
    conv_v = -bond.price_change_duration_convexity(*args, dy)
    exact_v = -bond.price_change_exact(*args, dy)
    answers["KP3_T3"] = {
        "refs": {"price_drop_pct": strict_v},
        "t3_conditional": [
            {"label": "strict_duration_only", "strict": True,
             "values": {"price_drop_pct": strict_v}},
            {"label": "duration_plus_convexity", "strict": False,
             "values": {"price_drop_pct": conv_v}},
            {"label": "exact_repricing", "strict": False,
             "values": {"price_drop_pct": exact_v}},
        ],
    }

    # ---- KP4 -------------------------------------------------------------
    s = load("KP4_T1")
    i = s["inputs"]
    args = (i["spot"], i["strike"], i["sigma_annual"], i["r_annual_cc"], i["t_years"])
    answers["KP4_T1"] = {"refs": {
        "call_price": blackscholes.call_price(*args),
        "call_delta": blackscholes.call_delta(*args),
        "call_vega": blackscholes.vega(*args),
    }}

    s = load("KP4_T2")
    i = s["inputs"]
    answers["KP4_T2"] = {"refs": {
        "delta_at_s110": blackscholes.call_delta(
            i["spot_for_number"], i["strike"], i["sigma_for_number"],
            i["r_annual_cc"], i["t_years"]),
    }}

    s = load("KP4_T3")
    i = s["inputs"]
    args = (i["spot"], i["strike"], i["sigma_annual"], i["r_annual_cc"], i["t_years"])
    exact_v = blackscholes.call_price_change_vol_bump(*args, i["dsigma"])
    vega_v = blackscholes.vega(*args) * i["dsigma"]
    answers["KP4_T3"] = {
        "refs": {"price_change": exact_v},
        "t3_conditional": [
            {"label": "strict_exact_reprice", "strict": True,
             "values": {"price_change": exact_v}},
            {"label": "vega_approximation", "strict": False,
             "values": {"price_change": vega_v}},
        ],
    }

    # ---- KP5 -------------------------------------------------------------
    s = load("KP5_T1")
    i = s["inputs"]
    answers["KP5_T1"] = {"refs": {
        "var_95_1d": var.parametric_var(i["position_value_cny"], i["sigma_annual"],
                                        i["conf_a"], i["horizon_a_days"]),
        "var_99_10d": var.parametric_var(i["position_value_cny"], i["sigma_annual"],
                                         i["conf_b"], i["horizon_b_days"]),
    }}

    s = load("KP5_T2")
    i = s["inputs"]
    answers["KP5_T2"] = {"refs": {
        "hist_var_95_1d": var.historical_var(fund_returns(s), i["position_value_cny"],
                                             i["confidence"]),
    }}

    s = load("KP5_T3")
    i = s["inputs"]

    def pvar(days):
        return var.parametric_var(i["position_value_cny"], i["sigma_annual"],
                                  i["confidence"], 1, periods_per_year=days)

    answers["KP5_T3"] = {
        "refs": {"var_95_1d": pvar(252)},
        "t3_conditional": [
            {"label": "strict_252", "strict": True, "values": {"var_95_1d": pvar(252)}},
            {"label": "alt_250", "strict": False, "values": {"var_95_1d": pvar(250)}},
            {"label": "alt_365", "strict": False, "values": {"var_95_1d": pvar(365)}},
        ],
    }

    # ---- KP6 -------------------------------------------------------------
    s = load("KP6_T1")
    i = s["inputs"]
    r = fund_returns(s)
    alloc, sel, inter = performance.brinson_bhb(
        i["w_portfolio"], i["w_benchmark"], i["r_portfolio"], i["r_benchmark"])
    answers["KP6_T1"] = {"refs": {
        "sharpe_annual": performance.sharpe_annual(r, i["rf_annual"]),
        "allocation_effect": alloc, "selection_effect": sel, "interaction_effect": inter,
    }}

    s = load("KP6_T2")
    i = s["inputs"]
    r = fund_returns(s)
    answers["KP6_T2"] = {"refs": {
        "rolling_sharpe_last": performance.sharpe_annual(r[-i["window_days"]:], i["rf_annual"]),
    }}

    s = load("KP6_T3")
    i = s["inputs"]
    r = fund_returns(s)
    answers["KP6_T3"] = {
        "refs": {"sharpe_annual": sharpe_variant(r, i["rf_annual"], 252, 1, "simple")},
        "t3_conditional": [
            {"label": "strict_252_ddof1_rfsimple", "strict": True,
             "values": {"sharpe_annual": sharpe_variant(r, i["rf_annual"], 252, 1, "simple")}},
            {"label": "rf_geometric", "strict": False,
             "values": {"sharpe_annual": sharpe_variant(r, i["rf_annual"], 252, 1, "geometric")}},
            {"label": "ddof_0", "strict": False,
             "values": {"sharpe_annual": sharpe_variant(r, i["rf_annual"], 252, 0, "simple")}},
            {"label": "alt_250", "strict": False,
             "values": {"sharpe_annual": sharpe_variant(r, i["rf_annual"], 250, 1, "simple")}},
        ],
    }

    return answers


def tolerance_band(spec, key, value):
    for k in spec["scoring"]["keys"]:
        if k["key"] == key:
            return max(k["tau_abs"], k["tau_rel"] * abs(value))
    raise KeyError(key)


def check_distinguishability(answers):
    """Any two conditional answers must sit further apart than the sum of
    their acceptance bands on at least... no: on EVERY differing key we
    require full separation, so a single submission can match at most one
    convention."""
    problems = []
    for task_id, entry in answers.items():
        if "t3_conditional" not in entry:
            continue
        spec = load(task_id)
        conds = entry["t3_conditional"]
        labels = [c["label"] for c in conds]
        if sum(c["strict"] for c in conds) != 1:
            problems.append(f"{task_id}: not exactly one strict entry")
        yaml_labels = [c["label"] for c in spec["t3_defensible_conventions"]]
        if labels != yaml_labels:
            problems.append(f"{task_id}: labels disagree with YAML enumeration")
        keys = list(conds[0]["values"].keys())
        for a in range(len(conds)):
            for b in range(a + 1, len(conds)):
                for key in keys:
                    va, vb = conds[a]["values"][key], conds[b]["values"][key]
                    band = tolerance_band(spec, key, va) + tolerance_band(spec, key, vb)
                    if abs(va - vb) <= band:
                        problems.append(
                            f"{task_id}.{key}: {labels[a]}={va:.8g} vs {labels[b]}={vb:.8g} "
                            f"separated by {abs(va-vb):.3g} <= band {band:.3g}")
    return problems


def main():
    answers = build()
    problems = check_distinguishability(answers)
    if problems:
        print("DISTINGUISHABILITY FAILURES:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(answers, indent=2), encoding="utf-8")
    n_t3 = sum(1 for a in answers.values() if "t3_conditional" in a)
    print(f"OK: wrote {OUT.relative_to(ROOT)} with {len(answers)} tasks, "
          f"{n_t3} conditional answer sets; all convention pairs distinguishable.")
    for tid, a in sorted(answers.items()):
        for k, v in a["refs"].items():
            if isinstance(v, list):
                print(f"  {tid}.{k} = {[round(x, 6) for x in v]}")
            else:
                print(f"  {tid}.{k} = {v:.8g}")


if __name__ == "__main__":
    main()
