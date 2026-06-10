# Correct T2 solution: draws the required figure and reports the number
# (must be judged correct, with the figure file present).
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

K, R, T = 97.5, 0.043, 0.58
spots = np.linspace(70, 140, 200)

os.makedirs("harness/_tmp", exist_ok=True)
fig, ax = plt.subplots()
for sig in (0.15, 0.276, 0.40):
    d1 = (np.log(spots / K) + (R + 0.5 * sig**2) * T) / (sig * np.sqrt(T))
    ax.plot(spots, norm.cdf(d1), label=f"sigma={sig}")
ax.set_xlabel("spot"); ax.set_ylabel("call delta"); ax.legend()
path = "harness/_tmp/c14_delta_curves.png"
fig.savefig(path, dpi=100)
plt.close(fig)

sig = 0.276
d1_110 = (np.log(110.0 / K) + (R + 0.5 * sig**2) * T) / (sig * np.sqrt(T))
result = {"delta_at_s110": float(norm.cdf(d1_110)), "figure_path": path}
