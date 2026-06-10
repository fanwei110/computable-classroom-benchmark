# PLANTED ERROR (code): runtime shape mismatch in linalg.solve.
# Expected: code_error.
import numpy as np

vols = np.array([0.187, 0.243, 0.312])
corr = np.array([[1.0, 0.21, -0.13], [0.21, 1.0, 0.37], [-0.13, 0.37, 1.0]])
cov = np.outer(vols, vols) * corr

x = np.linalg.solve(cov, np.ones(4))   # wrong length -> LinAlgError
w = x / x.sum()
result = {"mvp_weights": w.tolist(), "mvp_vol_annual": float(np.sqrt(w @ cov @ w))}
