"""Cluster-bootstrap confidence intervals (preregistered analysis tool).

The unit of independent variation is the TASK (18 clusters); repetitions
within a task-model-condition cell are correlated. Every percentage in the
paper is therefore reported with a 95% CI from a cluster bootstrap over
tasks: resample the 18 tasks with replacement, keep all generations of each
sampled task, recompute the proportion; percentile interval over B draws.

Input format (stage 3): a tidy table with one row per generation -
columns: task_id, model, condition, correct (0/1), plus any filter columns.
"""

import numpy as np
import pandas as pd

SEED = 20260610          # fixed for reproducibility (preregistered)
B = 10_000


def cluster_bootstrap_ci(df, value_col="correct", cluster_col="task_id",
                         b=B, seed=SEED, alpha=0.05):
    """95% percentile CI for the mean of value_col, clustering on cluster_col."""
    rng = np.random.default_rng(seed)
    clusters = df[cluster_col].unique()
    groups = {c: df.loc[df[cluster_col] == c, value_col].to_numpy() for c in clusters}
    stats = np.empty(b)
    for i in range(b):
        draw = rng.choice(clusters, size=len(clusters), replace=True)
        vals = np.concatenate([groups[c] for c in draw])
        stats[i] = vals.mean()
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return df[value_col].mean(), lo, hi


def condition_table(df):
    """Headline table: proportion correct with CI, by condition (pooled) and
    by model x condition."""
    rows = []
    for keys, sub in df.groupby(["condition"]):
        m, lo, hi = cluster_bootstrap_ci(sub)
        rows.append({"model": "pooled", "condition": keys[0],
                     "p": m, "ci_lo": lo, "ci_hi": hi, "n": len(sub)})
    for (model, cond), sub in df.groupby(["model", "condition"]):
        m, lo, hi = cluster_bootstrap_ci(sub)
        rows.append({"model": model, "condition": cond,
                     "p": m, "ci_lo": lo, "ci_hi": hi, "n": len(sub)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import sys
    df = pd.read_parquet(sys.argv[1]) if sys.argv[1].endswith(".parquet") \
        else pd.read_csv(sys.argv[1])
    print(condition_table(df).to_string(index=False))
