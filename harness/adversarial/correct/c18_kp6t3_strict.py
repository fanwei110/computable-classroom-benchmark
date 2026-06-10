# T3 solution under all course conventions (rf/252, ddof=1, sqrt(252)).
# Expected verdict: correct at the STRICT tier.
import numpy as np
import pandas as pd

df = pd.read_csv("data/market_snapshot_v1.csv")
r = df["fund"].to_numpy()
excess = r - 0.021 / 252

result = {"sharpe_annual": float(excess.mean() / excess.std(ddof=1) * np.sqrt(252))}
