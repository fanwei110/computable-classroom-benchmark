import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ---------- Black-Scholes delta for European call ----------
def delta_call(S, K, T, r, sigma):
    """Return delta of a European call (no dividends)."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)


# ---------- option parameters ----------
K = 97.5          # strike
r = 0.043         # continuously compounded risk-free rate
T = 0.58          # time to maturity (years)

# ---------- adjustable volatility set ----------
# Teachers can easily change the list below to use other values.
vols = [0.15, 0.276, 0.40]

# ---------- underlying grid ----------
S_grid = np.linspace(70, 140, 300)

# ---------- compute delta for each volatility ----------
deltas = {}
for vol in vols:
    deltas[vol] = delta_call(S_grid, K, T, r, vol)

# ---------- plot ----------
plt.figure(figsize=(8, 5))
for vol in vols:
    plt.plot(S_grid, deltas[vol], label=f'σ = {vol:.3f}')
plt.xlabel('Underlying price S')
plt.ylabel('Delta')
plt.title('Delta of European Call (K=97.5, r=4.3%, T=0.58yr)')
plt.legend()
plt.grid(True)

# ---------- save figure ----------
figure_filename = 'delta_curve.png'
plt.savefig(figure_filename, dpi=150)
plt.close()

# ---------- specific point ----------
S_target = 110
vol_target = 0.276
delta_at_target = delta_call(S_target, K, T, r, vol_target)

# ---------- output contract ----------
result = {
    'delta_at_s110': delta_at_target,
    'figure_path': os.path.abspath(figure_filename)
}

# Optional: print result so the teacher can verify immediately
print(result)
