import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Bond parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bps = 100  # 100 basis points = 1%

# Step 1: Calculate exact prices over yield grid
yield_grid = np.linspace(0.02, 0.09, 100)
prices_exact = np.zeros_like(yield_grid)

for i, y in enumerate(yield_grid):
    cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
    cash_flows[-1] += face_value  # Add face value to last payment
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 1)
    prices_exact[i] = np.sum(cash_flows / discount_factors)

# Step 2: Calculate duration and convexity at current yield (5.3%)
def calculate_duration_convexity(y, face_value, coupon_rate, years_to_maturity):
    cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
    cash_flows[-1] += face_value
    times = np.arange(1, years_to_maturity + 1)
    discount_factors = (1 + y) ** times
    pv_cash_flows = cash_flows / discount_factors

    # Macaulay duration
    mac_duration = np.sum(times * pv_cash_flows) / np.sum(pv_cash_flows)

    # Modified duration
    mod_duration = mac_duration / (1 + y)

    # Convexity
    convexity = np.sum(times * (times + 1) * cash_flows / ((1 + y) ** (times + 2))) / np.sum(pv_cash_flows)

    return mac_duration, mod_duration, convexity

mac_dur, mod_dur, convexity = calculate_duration_convexity(
    current_yield, face_value, coupon_rate, years_to_maturity
)

# Calculate duration-based approximations
yield_perturbation = np.linspace(-0.02, 0.02, 50)  # ±2% around current yield
yield_approx = current_yield + yield_perturbation

# First-order approximation (duration only)
price_approx_dur = prices_exact[np.argmin(np.abs(yield_grid - current_yield))] * (
    1 - mod_dur * yield_perturbation
)

# Second-order approximation (duration + convexity)
price_approx_dur_convex = prices_exact[np.argmin(np.abs(yield_grid - current_yield))] * (
    1 - mod_dur * yield_perturbation + 0.5 * convexity * (yield_perturbation ** 2)
)

# Step 3: Calculate +100bp exact price and duration approximation
yield_up100bp = current_yield + yield_change_bps / 10000
cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
cash_flows[-1] += face_value
discount_factors = (1 + yield_up100bp) ** np.arange(1, years_to_maturity + 1)
price_at_up100bp = np.sum(cash_flows / discount_factors)

dur_approx_change_up100bp = -mod_dur * (yield_change_bps / 10000)

# Step 4: Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, prices_exact, label='Exact Price-Yield Curve', color='blue')

# Find the index closest to current yield for plotting approximations
current_idx = np.argmin(np.abs(yield_grid - current_yield))
plt.plot(yield_approx * 100, price_approx_dur,
         label=f'Duration Approximation (D_mod={mod_dur:.3f})', linestyle='--', color='red')
plt.plot(yield_approx * 100, price_approx_dur_convex,
         label=f'Duration+Convexity Approx (Conv={convexity:.3f})', linestyle=':', color='green')

plt.scatter(current_yield * 100, prices_exact[current_idx],
            color='black', zorder=5, label=f'Current Yield ({current_yield*100:.1f}%)')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve with Duration/Convexity Approximations')
plt.legend()
plt.grid(True)

# Format x-axis as percentage
plt.gca().xaxis.set_major_formatter(PercentFormatter())

# Save figure
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')

# Prepare results
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# Print results for verification
print("Results:")
print(f"Price at +100bp: {result['price_at_up100bp']:.4f}")
print(f"Duration approx change: {result['dur_approx_change_up100bp']:.6f}")
print(f"Figure saved to: {result['figure_path']}")
