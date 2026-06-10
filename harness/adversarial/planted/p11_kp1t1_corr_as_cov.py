# PLANTED ERROR (conceptual): treats the CORRELATION matrix as if it were
# the covariance matrix (never scales by volatilities). Expected:
# numeric_wrong (both the volatility and the objective check fail).
import numpy as np

corr = np.array([[1.0, 0.21, -0.13], [0.21, 1.0, 0.37], [-0.13, 0.37, 1.0]])

x = np.linalg.solve(corr, np.ones(3))
w = x / x.sum()

result = {
    "mvp_weights": w.tolist(),
    "mvp_vol_annual": float(np.sqrt(w @ corr @ w)),
}
