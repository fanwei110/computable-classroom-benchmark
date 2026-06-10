"""Confirmatory hypothesis tests (preregistered): mixed-effects logistic
regressions with task random effects.

H1: full templating improves numerical correctness over improvised
    generation (C4 > C1).
H2: convention information has a positive main effect (C3 > C1 and C4 > C2).

Model: correct ~ conv + struct + conv:struct + model, random intercept by
task. conv = 1 for C3/C4; struct = 1 for C2/C4. Primary inference reads the
`conv` and `struct` main effects; the interaction is reported.

Implementation: statsmodels BinomialBayesMixedGLM (variational); a GEE with
exchangeable working correlation clustered on task is run alongside as a
frequentist robustness check. Coefficients reported as odds ratios.

Everything outside H1/H2 (model ordering, spread compression, task-type
differences) is EXPLORATORY and reported descriptively only.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

CONDITION_FACTORS = {  # condition -> (conv, struct)
    "C1": (0, 0), "C2": (0, 1), "C3": (1, 0), "C4": (1, 1),
}


def prepare(df):
    df = df.copy()
    df["conv"] = df["condition"].map(lambda c: CONDITION_FACTORS[c][0])
    df["struct"] = df["condition"].map(lambda c: CONDITION_FACTORS[c][1])
    return df


def fit_mixed(df):
    """Variational Bayes mixed logistic with task random intercepts."""
    df = prepare(df)
    model = BinomialBayesMixedGLM.from_formula(
        "correct ~ conv + struct + conv:struct + C(model)",
        {"task": "0 + C(task_id)"}, df)
    fit = model.fit_vb()
    return fit


def fit_gee(df):
    """Frequentist check: GEE logit, exchangeable correlation, task clusters."""
    df = prepare(df)
    model = smf.gee("correct ~ conv + struct + conv:struct + C(model)",
                    groups="task_id", data=df,
                    family=sm.families.Binomial(),
                    cov_struct=sm.cov_struct.Exchangeable())
    return model.fit()


def report(df):
    gee = fit_gee(df)
    print("=== GEE logit (task clusters) ===")
    print(gee.summary())
    params = gee.params
    print("\nOdds ratios:")
    for name in ("conv", "struct", "conv:struct"):
        if name in params.index:
            print(f"  {name}: OR = {np.exp(params[name]):.3f}")
    print("\n=== Mixed-effects logistic (variational Bayes) ===")
    mixed = fit_mixed(df)
    print(mixed.summary())


if __name__ == "__main__":
    import sys
    df = pd.read_parquet(sys.argv[1]) if sys.argv[1].endswith(".parquet") \
        else pd.read_csv(sys.argv[1])
    report(df)
