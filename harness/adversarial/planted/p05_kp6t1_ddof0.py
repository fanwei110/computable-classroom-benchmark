# PLANTED ERROR (conventional): population standard deviation (ddof=0)
# where the course convention is the sample estimator (ddof=1).
# Expected: numeric_wrong.
import numpy as np
import pandas as pd

df = pd.read_csv("data/market_snapshot_v1.csv")
r = df["fund"].to_numpy()
excess = r - 0.021 / 252

wp = np.array([0.45, 0.35, 0.20]); rp = np.array([0.083, 0.021, -0.014])
wb = np.array([0.40, 0.40, 0.20]); rb = np.array([0.067, 0.034, -0.009])

result = {
    "sharpe_annual": float(excess.mean() / excess.std() * np.sqrt(252)),  # ddof=0 default
    "allocation_effect": float(((wp - wb) * rb).sum()),
    "selection_effect": float((wb * (rp - rb)).sum()),
    "interaction_effect": float(((wp - wb) * (rp - rb)).sum()),
}
