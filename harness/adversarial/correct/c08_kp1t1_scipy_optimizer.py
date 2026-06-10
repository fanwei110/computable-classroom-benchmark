# Correct solution via a numerical optimizer rather than the closed form.
# Weights differ from the analytic solution in late decimals; the harness
# must accept them through the objective-value comparison.
import numpy as np
from scipy.optimize import minimize

vols = np.array([0.187, 0.243, 0.312])
corr = np.array([[1.0, 0.21, -0.13], [0.21, 1.0, 0.37], [-0.13, 0.37, 1.0]])
cov = np.outer(vols, vols) * corr

res = minimize(lambda w: w @ cov @ w, np.ones(3) / 3,
               constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
               method="SLSQP", options={"ftol": 1e-12, "maxiter": 200})
w = res.x / res.x.sum()

result = {"mvp_weights": w.tolist(),
          "mvp_vol_annual": float(np.sqrt(w @ cov @ w))}
