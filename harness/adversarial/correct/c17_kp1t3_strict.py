# T3 solution under the course convention (60% in first-named asset A).
# Expected verdict: correct at the STRICT tier.
import numpy as np

va, vb = 0.184, 0.297
w = np.array([0.6, 0.4])


def port_vol(rho):
    cov = np.array([[va**2, rho * va * vb], [rho * va * vb, vb**2]])
    return float(np.sqrt(w @ cov @ w))


result = {
    "vol_before_annual": port_vol(0.3),
    "vol_after_annual": port_vol(0.8),
}
