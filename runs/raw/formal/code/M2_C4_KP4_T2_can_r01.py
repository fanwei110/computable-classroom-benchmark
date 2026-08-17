import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ---------- Black-Scholes delta for a European call ----------
def bs_call_delta(S, K, T, r, sigma, q=0.0):
    """
    S: underlying price (scalar or array)
    K: strike
    T: time to maturity (years)
    r: risk-free rate (continuous compounding, decimal)
    sigma: volatility (decimal)
    q: dividend yield (decimal, default 0)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ---------- Parameters ----------
K = 97.5
r = 0.043
T = 0.58
q = 0.0

# Volatility parameter list
volatilities = [0.15, 0.276, 0.40]

# Underlying price grid
S_grid = np.linspace(70, 140, 500)

# ---------- Plotting ----------
fig, ax = plt.subplots(figsize=(8, 5))

for sigma in volatilities:
    delta = bs_call_delta(S_grid, K, T, r, sigma, q)
    ax.plot(S_grid, delta, label=f'σ = {sigma*100:.1f}%')

ax.set_xlabel('Underlying Price')
ax.set_ylabel('Delta')
ax.set_title('European Call Delta vs Underlying Price')
ax.legend()
ax.grid(True)

# Save figure
figure_filename = 'delta_curve.png'
fig.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close(fig)  # free memory

figure_path = os.path.abspath(figure_filename)

# ---------- Delta at S=110, sigma=27.6% ----------
S_specific = 110.0
sigma_specific = 0.276
delta_specific = bs_call_delta(S_specific, K, T, r, sigma_specific, q)

# ---------- Result dictionary ----------
result = {
    'delta_at_s110': delta_specific,
    'figure_path': figure_path
}

# Print for verification
if __name__ == '__main__':
    print(f"Delta at S=110, σ=27.6%: {delta_specific:.6f}")
    print(f"Figure saved to: {figure_path}")
