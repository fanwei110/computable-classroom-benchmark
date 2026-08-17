import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 100 basis points for reporting
yield_shift = yield_shift_bp / 10000  # Convert to decimal

# Step 1: Compute exact prices over yield grid (2% to 9%)
yield_grid = np.linspace(0.02, 0.09, 100)
prices_exact = np.zeros_like(yield_grid)

for i, y in enumerate(yield_grid):
    cash_flows = np.array([face_value * coupon_rate] * (years_to_maturity - 1) + [face_value * (1 + coupon_rate)])
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 1)
    prices_exact[i] = np.sum(cash_flows / discount_factors)

# Step 2: Compute Macaulay duration, modified duration, and convexity at current yield (5.3%)
def compute_duration_convexity(y, face_value, coupon_rate, years_to_maturity):
    cash_flows = np.array([face_value * coupon_rate] * (years_to_maturity - 1) + [face_value * (1 + coupon_rate)])
    times = np.arange(1, years_to_maturity + 1)
    discount_factors = (1 + y) ** times
    discounted_cash_flows = cash_flows / discount_factors
    price = np.sum(discounted_cash_flows)

    # Macaulay duration
    mac_dur = np.sum(times * discounted_cash_flows) / price
    # Modified duration
    mod_dur = mac_dur / (1 + y)
    # Convexity
    conv = np.sum(times * (times + 1) * discounted_cash_flows / (1 + y)**2) / price

    return mac_dur, mod_dur, conv, price

mac_dur, mod_dur, conv, price_current = compute_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)

# Step 3: Compute approximate prices using duration and convexity
prices_dur_approx = price_current * (1 - mod_dur * (yield_grid - current_yield))
prices_dur_conv_approx = price_current * (1 - mod_dur * (yield_grid - current_yield) + 0.5 * conv * (yield_grid - current_yield)**2)

# Step 4: Compute exact price at +100bp and duration-based relative change
price_up100bp = compute_duration_convexity(current_yield + yield_shift, face_value, coupon_rate, years_to_maturity)[3]
dur_approx_change_up100bp = -mod_dur * yield_shift

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, prices_exact, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_grid * 100, prices_dur_approx, '--', label='Duration Approximation', color='red')
plt.plot(yield_grid * 100, prices_dur_conv_approx, '--', label='Duration + Convexity Approximation', color='green')

# Mark current yield point
plt.scatter(current_yield * 100, price_current, color='black', zorder=5)
plt.axvline(x=current_yield * 100, color='gray', linestyle=':', alpha=0.5)

# Formatting
plt.title('Bond Price-Yield Curve with Duration and Convexity Approximations')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.legend()
plt.grid(True)

# Format y-axis as percentage
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}%'))

# Save figure
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')

# Prepare result dictionary
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# For demonstration, print result (in actual use, this would be returned or saved)
print(result)
