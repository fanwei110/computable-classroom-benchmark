import numpy as np

# Given parameters
face_value = 100
coupon_rate = 0.046
ytm = 0.053
maturity = 7
coupon = face_value * coupon_rate

# Calculate price
price = sum([coupon / (1 + ytm)**t for t in range(1, maturity)]) + (coupon + face_value) / (1 + ytm)**maturity

# Calculate Macaulay Duration
macaulay_duration = sum([t * coupon / (1 + ytm)**t for t in range(1, maturity)]) + maturity * (coupon + face_value) / (1 + ytm)**maturity
macaulay_duration /= price
macaulay_duration_years = macaulay_duration  # in years

# Calculate Modified Duration
modified_duration_years = macaulay_duration / (1 + ytm)

# Calculate Convexity
convexity = sum([t * (t + 1) * coupon / (1 + ytm)**(t + 2) for t in range(1, maturity)]) + maturity * (maturity + 1) * (coupon + face_value) / (1 + ytm)**(maturity + 2)
convexity /= price

# Store results in dictionary
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

print(result)
