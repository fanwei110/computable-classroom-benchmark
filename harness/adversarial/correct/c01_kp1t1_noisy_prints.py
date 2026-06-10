# Correct solution with noisy prints and odd style (must be judged correct).
import numpy as np

print("=== STARTING ANALYSIS ===")
vols = np.array([0.187, 0.243, 0.312])
corr = np.array([[1.0, 0.21, -0.13], [0.21, 1.0, 0.37], [-0.13, 0.37, 1.0]])
cov = np.outer(vols, vols) * corr
print("covariance matrix:\n", cov)

ones = np.ones(3)
x = np.linalg.solve(cov, ones)
w = x / x.sum()
print("DEBUG weights ->", w, "sum:", w.sum())

vol = float(np.sqrt(w @ cov @ w))
for _ in range(3):
    print("progress ...")

result = {"mvp_weights": w.tolist(), "mvp_vol_annual": vol}
print("DONE!!!", result)
