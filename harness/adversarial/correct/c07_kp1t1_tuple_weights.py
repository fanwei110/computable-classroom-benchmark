# Correct solution returning weights as a TUPLE (must be judged correct).
import numpy as np

vols = np.array([0.187, 0.243, 0.312])
corr = np.array([[1.0, 0.21, -0.13], [0.21, 1.0, 0.37], [-0.13, 0.37, 1.0]])
cov = np.outer(vols, vols) * corr
x = np.linalg.solve(cov, np.ones(3))
w = x / x.sum()

result = {
    "mvp_weights": tuple(float(v) for v in w),
    "mvp_vol_annual": float(np.sqrt(w @ cov @ w)),
}
