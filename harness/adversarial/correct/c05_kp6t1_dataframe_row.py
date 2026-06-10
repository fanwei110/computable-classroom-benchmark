# Correct solution that stores `result` as a SINGLE-ROW DataFrame
# (must be judged correct).
import numpy as np
import pandas as pd

df = pd.read_csv("data/market_snapshot_v1.csv")
r = df["fund"].to_numpy()
excess = r - 0.021 / 252
sharpe = excess.mean() / excess.std(ddof=1) * np.sqrt(252)

wp = np.array([0.45, 0.35, 0.20])
rp = np.array([0.083, 0.021, -0.014])
wb = np.array([0.40, 0.40, 0.20])
rb = np.array([0.067, 0.034, -0.009])

result = pd.DataFrame([{
    "sharpe_annual": sharpe,
    "allocation_effect": ((wp - wb) * rb).sum(),
    "selection_effect": (wb * (rp - rb)).sum(),
    "interaction_effect": ((wp - wb) * (rp - rb)).sum(),
}])
