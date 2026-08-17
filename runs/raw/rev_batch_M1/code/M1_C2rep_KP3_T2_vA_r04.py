import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# Parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 100 basis points for reporting
yield_shift = yield_shift_bp / 10000  # Convert to decimal

# Step 1: Bond pricing function (exact)
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods)
    cash_flows[-1] += face_value  # Add face value to last coupon
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 1)
    price = np.sum(cash_flows / discount_factors)
    return price

# Generate yield grid from 2% to 9%
yield_grid = np.linspace(0.02, 0.09, 100)
prices_exact = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# Step 2: Duration and convexity at current yield (5.3%)
def bond_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods)
    cash_flows[-1] += face_value
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 1)
    discounted_cash_flows = cash_flows / discount_factors
    weights = discounted_cash_flows / np.sum(discounted_cash_flows)
    duration = np.sum(weights * np.arange(1, periods + 1))
    return duration / (1 + yield_to_maturity)  # Macaulay to modified duration

def bond_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods)
    cash_flows[-1] += face_value
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 1)
    discounted_cash_flows = cash_flows / discount_factors
    convexity = np.sum(discounted_cash_flows * np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1)) / (1 + yield_to_maturity)**2
    convexity /= np.sum(discounted_cash_flows)
    return convexity

duration = bond_duration(current_yield, face_value, coupon_rate, years_to_maturity)
convexity = bond_convexity(current_yield, face_value, coupon_rate, years_to_maturity)

# Duration-based approximation
price_current = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
yield_approx = np.linspace(current_yield - 0.02, current_yield + 0.02, 50)
price_approx = price_current * (1 - duration * (yield_approx - current_yield) + 0.5 * convexity * (yield_approx - current_yield)**2)

# Step 3: Report +100bp exact price and duration-based relative change
price_up100bp = bond_price(current_yield + yield_shift, face_value, coupon_rate, years_to_maturity)
dur_approx_change_up100bp = -duration * yield_shift * 100  # in percentage

# Step 4: Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, prices_exact, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_approx * 100, price_approx, label='Duration-based Approximation', color='red', linestyle='--')
plt.scatter(current_yield * 100, price_current, color='green', zorder=5, label=f'Current Yield ({current_yield*100:.1f}%)')
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
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

result
