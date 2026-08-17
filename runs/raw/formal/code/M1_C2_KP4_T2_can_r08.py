import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# Black-Scholes European call option delta calculation
def black_scholes_call_delta(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# Parameters
K = 97.5          # Strike price
r = 0.043         # Risk-free rate
T = 0.58          # Time to maturity in years
S_range = np.linspace(70, 140, 100)  # Underlying price range
volatilities = [0.15, 0.276, 0.40]  # Volatility values

# Calculate deltas for each volatility
deltas = {}
for sigma in volatilities:
    deltas[sigma] = black_scholes_call_delta(S_range, K, T, r, sigma)

# Plotting
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    plt.plot(S_range, deltas[sigma], label=f'Volatility = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# Save figure
figure_path = 'bs_delta_plot.png'
plt.savefig(figure_path)
plt.close()

# Calculate specific delta at S=110, sigma=27.6%
S_target = 110
sigma_target = 0.276
delta_at_s110 = black_scholes_call_delta(S_target, K, T, r, sigma_target)

# Prepare result dictionary
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# For demonstration, print the result (in actual use, this would be returned)
print(result)
