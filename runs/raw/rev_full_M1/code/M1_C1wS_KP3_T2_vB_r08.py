import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt
import os

# Parameters
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
ytm_initial = 0.053
yield_grid = np.linspace(0.02, 0.09, 100)  # 2% to 9%
yield_shift = 0.01  # 100bp shift for reporting

# Cash flows
coupon_payment = face_value * coupon_rate
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # Add face value to last payment

# Exact pricing function
def bond_price(yield_to_maturity, cash_flows, years_to_maturity):
    periods = np.arange(1, years_to_maturity + 1)
    present_values = cash_flows / ((1 + yield_to_maturity) ** periods)
    return np.sum(present_values)

# Calculate exact prices
exact_prices = np.array([bond_price(y, cash_flows, years_to_maturity) for y in yield_grid])

# Duration and convexity at initial YTM (5.3%)
def bond_duration_convexity(yield_to_maturity, cash_flows, years_to_maturity):
    periods = np.arange(1, years_to_maturity + 1)
    discounted_cash_flows = cash_flows / ((1 + yield_to_maturity) ** periods)
    duration = np.sum(periods * discounted_cash_flows) / np.sum(discounted_cash_flows)
    convexity = np.sum(periods * (periods + 1) * discounted_cash_flows) / ((1 + yield_to_maturity) ** 2 * np.sum(discounted_cash_flows))
    return duration, convexity

duration, convexity = bond_duration_convexity(ytm_initial, cash_flows, years_to_maturity)
modified_duration = duration / (1 + ytm_initial)

# Duration-based approximation
def duration_approx_price(yield_change, initial_price, modified_duration):
    return initial_price * (1 - modified_duration * yield_change)

initial_price = bond_price(ytm_initial, cash_flows, years_to_maturity)
approx_prices = duration_approx_price(yield_grid - ytm_initial, initial_price, modified_duration)

# Reporting for +100bp
ytm_up100bp = ytm_initial + yield_shift
price_at_up100bp = bond_price(ytm_up100bp, cash_flows, years_to_maturity)
dur_approx_change_up100bp = -modified_duration * yield_shift * 100  # in percentage

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price', color='blue')
plt.plot(yield_grid * 100, approx_prices, label='Duration Approximation', linestyle='--', color='red')
plt.scatter(ytm_initial * 100, initial_price, color='green', zorder=5, label='Initial YTM (5.3%)')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.title('Bond Price vs Yield to Maturity')
plt.legend()
plt.grid(True)

# Save figure
figure_path = 'bond_price_vs_ytm.png'
plt.savefig(figure_path)
plt.close()

# Prepare result dictionary
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': os.path.abspath(figure_path)
}

# For demonstration, print result (in actual use, this would be returned)
print(result)
