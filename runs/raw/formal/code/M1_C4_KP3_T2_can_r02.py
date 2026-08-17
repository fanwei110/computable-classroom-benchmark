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

# Create yield changes for approximation
dy = 0.0001  # Small change for derivative approximation
yield_approx = np.linspace(current_yield - 0.02, current_yield + 0.02, 50)
price_approx_dur = current_price * (1 - mod_dur * (yield_approx - current_yield))
price_approx_dur_conv = current_price * (1 - mod_dur * (yield_approx - current_yield) +
                                        0.5 * conv * (yield_approx - current_yield)**2)

# Step 3: Calculate +100bp exact price and duration approximation
yield_up100bp = current_yield + yield_change_bp / 10000
price_up100bp = bond_price(yield_up100bp, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -mod_dur * (yield_up100bp - current_yield)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid, exact_prices, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_approx, price_approx_dur, '--', label='Duration Approximation', color='red')
plt.plot(yield_approx, price_approx_dur_conv, '--', label='Duration+Convexity Approximation', color='green')
plt.scatter(current_yield, current_price, color='black', zorder=5, label='Current Yield (5.3%)')
plt.xlabel('Yield to Maturity (Annual)')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve with Duration and Convexity Approximations')
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
plt.gca().yaxis.set_major_formatter('${x:.2f}')
plt.legend()
plt.grid(True)

# Save figure
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# Prepare results
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# For demonstration, print the result (in actual use, this would be returned)
print(result)
