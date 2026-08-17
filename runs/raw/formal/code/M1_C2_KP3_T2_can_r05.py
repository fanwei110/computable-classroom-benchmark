import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# Parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100 basis points = 1%

# Step 1: Calculate exact bond prices over a yield grid from 2% to 9%
yield_grid = np.linspace(0.02, 0.09, 100)
periods_per_year = 2  # Assuming semi-annual coupons
total_periods = years_to_maturity * periods_per_year
coupon_payment = (face_value * coupon_rate) / periods_per_year

def bond_price(yield_per_period, periods, coupon, face_value):
    """Calculate bond price given periodic yield, periods, coupon, and face value."""
    price = sum([coupon / ((1 + yield_per_period) ** t) for t in range(1, periods + 1)]) + \
            face_value / ((1 + yield_per_period) ** periods)
    return price

# Convert annual yield to periodic yield
yield_per_period_grid = yield_grid / periods_per_year
exact_prices = np.array([bond_price(y, total_periods, coupon_payment, face_value) for y in yield_per_period_grid])

# Step 2: Calculate duration and convexity at current yield (5.3%)
current_yield_per_period = current_yield / periods_per_year

def bond_duration(yield_per_period, periods, coupon, face_value):
    """Calculate Macaulay duration."""
    cash_flows = np.array([coupon] * periods + [face_value])
    times = np.arange(1, periods + 2)
    discounted_cash_flows = cash_flows / ((1 + yield_per_period) ** times)
    price = np.sum(discounted_cash_flows)
    weighted_cash_flows = discounted_cash_flows * times
    macaulay_duration = np.sum(weighted_cash_flows) / price
    modified_duration = macaulay_duration / (1 + yield_per_period)
    return macaulay_duration, modified_duration

def bond_convexity(yield_per_period, periods, coupon, face_value):
    """Calculate convexity."""
    cash_flows = np.array([coupon] * periods + [face_value])
    times = np.arange(1, periods + 2)
    discounted_cash_flows = cash_flows / ((1 + yield_per_period) ** times)
    price = np.sum(discounted_cash_flows)
    weighted_cash_flows = discounted_cash_flows * times * (times + 1)
    convexity = np.sum(weighted_cash_flows) / (price * (1 + yield_per_period)**2)
    return convexity

macaulay_dur, modified_dur = bond_duration(current_yield_per_period, total_periods, coupon_payment, face_value)
convexity = bond_convexity(current_yield_per_period, total_periods, coupon_payment, face_value)

# Duration-based approximation
current_price = bond_price(current_yield_per_period, total_periods, coupon_payment, face_value)
yield_change = yield_change_bp / 10000  # Convert basis points to decimal
approx_prices = current_price * (1 - modified_dur * yield_change + 0.5 * convexity * (yield_change ** 2))

# Generate approximation around current yield
yield_approx_grid = np.linspace(current_yield - 0.02, current_yield + 0.02, 50)
yield_approx_per_period_grid = yield_approx_grid / periods_per_year
approx_prices_grid = current_price * (1 - modified_dur * (yield_approx_grid - current_yield) +
                                      0.5 * convexity * (yield_approx_grid - current_yield)**2)

# Step 3: Report +100bp exact price and duration-based relative change
new_yield = current_yield + yield_change
new_yield_per_period = new_yield / periods_per_year
new_exact_price = bond_price(new_yield_per_period, total_periods, coupon_payment, face_value)
dur_approx_change = -modified_dur * yield_change * 100  # in percentage

# Step 4: Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_approx_grid * 100, approx_prices_grid, label='Duration-Based Approximation', color='red', linestyle='--')
plt.scatter(current_yield * 100, current_price, color='green', zorder=5, label=f'Current Yield ({current_yield*100:.1f}%)')
plt.xlabel('Yield (%)')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve with Duration Approximation')
plt.legend()
plt.grid(True)

# Save figure
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# Prepare result dictionary
result = {
    'price_at_up100bp': new_exact_price,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# For demonstration, print result (in actual use, this would be returned or used directly)
print(result)
