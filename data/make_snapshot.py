"""Generate the frozen market-data snapshot (v1).

Two years (504 business days) of correlated daily simple returns for a fund
and its benchmark, simulated from a fixed-seed bivariate normal and written
with fixed 8-decimal formatting so the CSV is bit-for-bit reproducible.
The committed CSV is the source of truth; reference answers are computed
FROM THE CSV, never from the in-memory floats.

Reproducibility check: running this script twice must produce byte-identical
files (verified in stage-1 acceptance; SHA256 recorded in SHA256SUMS.txt).
"""

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260610
N_DAYS = 504
START = "2024-01-02"

MU_DAILY = np.array([0.00041, 0.00033])        # fund, benchmark
SIGMA_DAILY = np.array([0.0112, 0.0091])
RHO = 0.85

HERE = Path(__file__).resolve().parent
OUT = HERE / "market_snapshot_v1.csv"


def main():
    rng = np.random.default_rng(SEED)
    cov = np.array([[SIGMA_DAILY[0] ** 2, RHO * SIGMA_DAILY[0] * SIGMA_DAILY[1]],
                    [RHO * SIGMA_DAILY[0] * SIGMA_DAILY[1], SIGMA_DAILY[1] ** 2]])
    rets = rng.multivariate_normal(MU_DAILY, cov, size=N_DAYS, method="cholesky")
    dates = pd.bdate_range(START, periods=N_DAYS)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"),
                       "fund": rets[:, 0], "bench": rets[:, 1]})
    with open(OUT, "w", newline="\n", encoding="ascii") as f:
        f.write("date,fund,bench\n")
        for _, row in df.iterrows():
            f.write(f"{row['date']},{row['fund']:.8f},{row['bench']:.8f}\n")
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    (HERE / "SHA256SUMS.txt").write_text(
        f"{digest}  market_snapshot_v1.csv\n", encoding="ascii")
    print(f"wrote {OUT.name}: {N_DAYS} rows, sha256={digest}")


if __name__ == "__main__":
    main()
