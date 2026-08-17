import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def bond_price(y, face_value, coupon_rate, years_to_maturity):
    """Calculate bond price using discounted cash flows."""
    coupon = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon)
    cash_flows[-1] += face_value  # Add face value at maturity
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 1)
    price = np.sum(cash_flows / discount_factors)
    return price

def macaulay_duration(y, face_value, coupon_rate, years_to_maturity):
    """Calculate Macaulay duration."""
    coupon = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 1)
    discounted_cf = cash_flows / discount_factors
    weights = discounted_cf / np.sum(discounted_cf)
    duration = np.sum(weights * np.arange(1, years_to_maturity + 1))
    return duration

def convexity(y, face_value, coupon_rate, years_to_maturity):
    """Calculate convexity."""
    coupon = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 2)
    convexity_sum = np.sum(cash_flows * np.arange(1, years_to_maturity + 1) *
                          (np.arange(1, years_to_maturity + 1) + 1) / discount_factors[1:])
    price = bond_price(y, face_value, coupon_rate, years_to_maturity)
    return convexity_sum / (price * (1 + y)**2)

# Bond parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100 basis points = 1%

# Step 1: Calculate exact prices over yield grid
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# Step 2: Calculate duration and convexity at current yield
mac_dur = macaulay_duration(current_yield, face_value, coupon_rate, years_to_maturity)
mod_dur = mac_dur / (1 + current_yield)
conv = convexity(current_yield, face_value, coupon_rate, years_to_maturity)
current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)

# Calculate approximate prices using duration and duration+convexity
dy = yield_grid - current_yield
dur_approx = current_price * (1 - mod_dur * dy)
dur_conv_approx = current_price * (1 - mod_dur * dy + 0.5 * conv * dy**2)

# Step 3: Calculate exact price and duration approximation for +100bp
new_yield = current_yield + yield_change_bp / 10000
price_at_up100bp = bond_price(new_yield, face_value, coupon_rate, years_to_maturity)
dur_approx_change_up100bp = -mod_dur * (yield_change_bp / 10000)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_grid * 100, dur_approx, '--', label='Duration Approximation', color='red')
plt.plot(yield_grid * 100, dur_conv_approx, '--', label='Duration+Convexity Approximation', color='green')

# Mark current point
plt.scatter(current_yield * 100, current_price, color='black', zorder=5)
plt.text(current_yield * 100, current_price * 0.99, f'Current ({current_yield*100:.1f}%)',
         horizontalalignment='center', color='black')

plt.title('Bond Price-Yield Curve with Duration Approximations')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.gca().xaxis.set_major_formatter(PercentFormatter())
plt.gca().yaxis.set_major_formatter('${x:.2f}')
plt.legend()
plt.grid(True)

# Save figure
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# Prepare results
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# For demonstration, print the result (in actual use, this would be returned)
print(result)
