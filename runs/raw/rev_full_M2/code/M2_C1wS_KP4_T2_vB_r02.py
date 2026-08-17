import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ---------- Black-Scholes Delta for a European call ----------
def bs_call_delta(S, K, T, r, sigma):
    """
    S     : spot price (scalar or array)
    K     : strike price
    T     : time to maturity (years)
    r     : risk-free interest rate (continuous compounding)
    sigma : volatility
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ---------- Given market parameters ----------
K      = 97.5        # strike price
r      = 0.043       # risk-free rate (4.3%)
T      = 0.58        # time to maturity (years)
sigmas = [0.15, 0.276, 0.40]   # volatilities: 15%, 27.6%, 40%

# ---------- Spot grid ----------
S_values = np.linspace(70, 140, 500)

# ---------- Plotting ----------
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    delta = bs_call_delta(S_values, K, T, r, sigma)
    plt.plot(S_values, delta, linewidth=2, label=f'σ = {sigma*100:.1f}%')

plt.xlabel('Spot Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('Black–Scholes Call Delta vs. Spot Price', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ---------- Save figure ----------
figure_path = os.path.abspath('delta_curves.png')
plt.savefig(figure_path, dpi=150)
plt.close()   # free memory, avoid showing during automatic execution

# ---------- Delta at S=110, sigma=27.6% ----------
S_target      = 110.0
sigma_target  = 0.276
delta_target  = bs_call_delta(S_target, K, T, r, sigma_target)

# ---------- Assemble final output ----------
result = {
    'delta_at_s110': delta_target,
    'figure_path': figure_path
}

# Display the result so the teacher sees it immediately in the console
print("Output dictionary:")
print(result)
