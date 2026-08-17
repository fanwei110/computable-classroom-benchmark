import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os

# ============================================
# BOND PARAMETERS
# ============================================
FACE_VALUE = 100.0        # Face value
COUPON_RATE = 0.046       # 4.6% annual coupon rate
MATURITY = 7               # 7 years to maturity
CURRENT_YIELD = 0.053      # Current yield rate (5.3%)
ANNUAL_COUPON = FACE_VALUE * COUPON_RATE  # Annual coupon payment

# ============================================
# FUNCTION DEFINITIONS
# ============================================
def bond_price(ytm, face, coupon_rate, maturity, coupon_freq=1):
    """
    Calculate bond price for given YTM using discounted cash flow method.
    
    Parameters:
    ytm: Yield to maturity (decimal)
    face: Face value
    coupon_rate: Annual coupon rate (decimal)
    maturity: Years to maturity
    coupon_freq: Coupon payments per year (1 for annual)
    """
    coupon = face * coupon_rate / coupon_freq
    periods = int(maturity * coupon_freq)
    price = 0
    
    # Present value of coupon payments
    for t in range(1, periods + 1):
        price += coupon / (1 + ytm/coupon_freq)**t
    
    # Present value of face value
    price += face / (1 + ytm/coupon_freq)**periods
    
    return price

def macaulay_duration(price, ytm, face, coupon_rate, maturity):
    """
    Calculate Macaulay duration for annual coupon bond.
    
    Returns duration in years.
    """
    pv_cashflows = []
    weights = []
    
    for t in range(1, maturity + 1):
        cf = ANNUAL_COUPON
        if t == maturity:
            cf += face
        pv = cf / (1 + ytm)**t
        pv_cashflows.append(pv)
        weights.append(t * pv)
    
    macaulay_dur = sum(weights) / price
    return macaulay_dur

def modified_duration(macaulay_dur, ytm):
    """Calculate modified duration."""
    return macaulay_dur / (1 + ytm)

def convexity(price, ytm, face, coupon_rate, maturity):
    """
    Calculate convexity for annual coupon bond.
    Formula: convexity = Σ[t(t+1)CF_t/(1+y)^(t+2)] / P
    """
    conv_sum = 0
    
    for t in range(1, maturity + 1):
        cf = ANNUAL_COUPON
        if t == maturity:
            cf += face
        conv_sum += t * (t + 1) * cf / (1 + ytm)**(t + 2)
    
    return conv_sum / price

# ============================================
# COMPUTE BOND METRICS AT CURRENT YIELD
# ============================================
price_current = bond_price(CURRENT_YIELD, FACE_VALUE, COUPON_RATE, MATURITY)
macaulay_dur = macaulay_duration(price_current, CURRENT_YIELD, FACE_VALUE, COUPON_RATE, MATURITY)
modified_dur = modified_duration(macaulay_dur, CURRENT_YIELD)
conv = convexity(price_current, CURRENT_YIELD, FACE_VALUE, COUPON_RATE, MATURITY)

print(f"Current bond price (YTM=5.3%): ${price_current:.4f}")
print(f"Macaulay duration: {macaulay_dur:.4f} years")
print(f"Modified duration: {modified_dur:.4f}")
print(f"Convexity: {conv:.4f}")

# ============================================
# PRICE-YIELD CURVE (2% to 9%)
# ============================================
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = [bond_price(y, FACE_VALUE, COUPON_RATE, MATURITY) for y in yield_grid]

# ============================================
# APPROXIMATIONS NEAR CURRENT YIELD
# ============================================
# First-order duration approximation (tangent line at CURRENT_YIELD)
delta_y = yield_grid - CURRENT_YIELD
duration_approx = price_current - modified_dur * price_current * delta_y

# Second-order duration+convexity approximation
dur_conv_approx = price_current - modified_dur * price_current * delta_y + 0.5 * conv * price_current * delta_y**2

# ============================================
# SCENARIO: YIELD INCREASE BY 100bp
# ============================================
yield_up100bp = CURRENT_YIELD + 0.01  # +100bp
price_up100bp = bond_price(yield_up100bp, FACE_VALUE, COUPON_RATE, MATURITY)

# First-order approximation of relative price change
# dP/P = -Modified_Duration * dy
dy = 0.01  # 100bp increase
dur_approx_change = -modified_dur * dy

print(f"\n--- Scenario: Yield increase by 100bp ---")
print(f"Exact price at YTM={yield_up100bp*100:.1f}%: ${price_up100bp:.4f}")
print(f"Duration-based relative price change (approximation): {dur_approx_change:.6f} ({dur_approx_change*100:.2f}%)")

# Verify with actual relative change
actual_relative_change = (price_up100bp - price_current) / price_current
print(f"Actual relative price change: {actual_relative_change:.6f} ({actual_relative_change*100:.2f}%)")
print(f"Approximation error: {abs(dur_approx_change - actual_relative_change):.6f}")

# ============================================
# PLOTTING
# ============================================
fig, ax = plt.subplots(figsize=(12, 8))

# Plot exact price-yield curve
ax.plot(yield_grid * 100, exact_prices, 'b-', linewidth=2.5, label='Exact Price-Yield Curve')

# Plot duration approximation (tangent line)
# Show approximation in a range around current yield
yield_near = np.linspace(max(0.03, CURRENT_YIELD - 0.02), CURRENT_YIELD + 0.02, 50)
exact_near = [bond_price(y, FACE_VALUE, COUPON_RATE, MATURITY) for y in yield_near]
dur_approx_near = [price_current - modified_dur * price_current * (y - CURRENT_YIELD) for y in yield_near]
dur_conv_near = [price_current - modified_dur * price_current * (y - CURRENT_YIELD) + 0.5 * conv * price_current * (y - CURRENT_YIELD)**2 for y in yield_near]

ax.plot(yield_near * 100, dur_approx_near, 'r--', linewidth=2, label='Duration Approximation')
ax.plot(yield_near * 100, dur_conv_near, 'g:', linewidth=2, label='Duration+Convexity Approximation')

# Mark current yield point
ax.plot(CURRENT_YIELD * 100, price_current, 'ro', markersize=10, label=f'Current YTM ({CURRENT_YIELD*100:.1f}%)')

# Mark yield+100bp point
ax.plot(yield_up100bp * 100, price_up100bp, 'bs', markersize=10, label=f'YTM+100bp ({yield_up100bp*100:.1f}%)')

# Add vertical line at current yield
ax.axvline(x=CURRENT_YIELD * 100, color='gray', linestyle='--', alpha=0.3)

ax.set_xlabel('Yield to Maturity (%)', fontsize=12)
ax.set_ylabel('Bond Price ($)', fontsize=12)
ax.set_title('Bond Price-Yield Curve with Duration and Convexity Approximations\n' +
             f'(Face={FACE_VALUE}, Coupon={COUPON_RATE*100:.1f}%, Maturity={MATURITY}yrs)',
             fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# Add text box with key metrics
metrics_text = f'Current Price: ${price_current:.2f}\nMac. Duration: {macaulay_dur:.2f} yrs\nMod. Duration: {modified_dur:.2f}\nConvexity: {conv:.2f}'
ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()

# Save figure
figure_path = 'bond_pricing_challenge.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigure saved to: {figure_path}")

# ============================================
# STORE RESULTS
# ============================================
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

print("\n=== RESULT DICTIONARY ===")
print(result)
