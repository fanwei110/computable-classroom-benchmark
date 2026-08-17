import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# Parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 100 basis points = 1%

# Step 1: Bond pricing function (exact)
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 2)
    price = np.sum(cash_flows / discount_factors)
    return price

# Step 2: Duration and convexity calculation
def bond_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    times = np.arange(1, periods + 2)
    discount_factors = (1 + yield_to_maturity) ** times
    discounted_cash_flows = cash_flows / discount_factors
    price = np.sum(discounted_cash_flows)

    # Duration (Macaulay)
    weighted_cash_flows = discounted_cash_flows * times
    macaulay_duration = np.sum(weighted_cash_flows) / price
    modified_duration = macaulay_duration / (1 + yield_to_maturity)

    # Convexity
    convexity = np.sum(discounted_cash_flows * times * (times + 1)) / (price * (1 + yield_to_maturity)**2)

    return modified_duration, convexity

# Step 3: Generate yield grid and exact prices
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# Step 4: Duration-based approximation around current yield
modified_duration, convexity = bond_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)
approx_prices = bond_price(current_yield, face_value, coupon_rate, years_to_maturity) * (
    1 - modified_duration * (yield_grid - current_yield)
    + 0.5 * convexity * (yield_grid - current_yield)**2
)

# Step 5: Calculate exact price and duration-based change for +100bp
yield_up100bp = current_yield + yield_shift_bp / 10000
price_at_up100bp = bond_price(yield_up100bp, face_value, coupon_rate, years_to_maturity)
price_current = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
dur_approx_change_up100bp = -modified_duration * (yield_up100bp - current_yield) * 100  # in percentage

# Step 6: Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_grid * 100, approx_prices, label='Duration-based Approximation', color='red', linestyle='--')
plt.scatter(current_yield * 100, price_current, color='green', zorder=5, label='Current Yield (5.3%)')
plt.xlabel('Yield to Maturity (%)')
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
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# Output the result (for verification)
print(result)
