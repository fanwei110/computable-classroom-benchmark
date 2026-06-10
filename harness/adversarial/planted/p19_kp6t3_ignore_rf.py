# PLANTED ERROR (T3, conventional): silently ignores the stated 2.1%
# risk-free rate (computes a gross Sharpe). Ignoring stated task data is not
# an enumerated defensible convention. Expected: numeric_wrong, tier wrong.
import numpy as np
import pandas as pd

df = pd.read_csv("data/market_snapshot_v1.csv")
r = df["fund"].to_numpy()

result = {"sharpe_annual": float(r.mean() / r.std(ddof=1) * np.sqrt(252))}
