# PLANTED ERROR (visualization): the numeric outputs are correct, but the
# figure is never actually saved - figure_path points to a file that does
# not exist. Expected: vis_failure.
import numpy as np

mus = np.array([0.071, 0.124])
vols = np.array([0.163, 0.289])
rho = 0.45
c12 = rho * vols[0] * vols[1]
cov = np.array([[vols[0] ** 2, c12], [c12, vols[1] ** 2]])

x = np.linalg.solve(cov, np.ones(2))
w_mvp = x / x.sum()
mvp_vol = float(np.sqrt(w_mvp @ cov @ w_mvp))

w_a = (0.10 - mus[1]) / (mus[0] - mus[1])
w_t = np.array([w_a, 1 - w_a])
target_vol = float(np.sqrt(w_t @ cov @ w_t))

# (figure code "accidentally" skipped)

result = {
    "mvp_vol_at_rho45": mvp_vol,
    "frontier_vol_at_target": target_vol,
    "figure_path": "harness/_tmp/p20_this_file_was_never_written.png",
}
