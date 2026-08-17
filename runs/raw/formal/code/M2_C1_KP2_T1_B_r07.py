# ç»å®åæ°
rf = 0.023        # æ é£é©å©ç 2.3%
rm = 0.094        # å¸åºæ¶çç 9.4%
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131  # Yçå®éæ¶çç 13.1%

# å¸åºé£é©æº¢ä»·
market_premium = rm - rf  # 0.071

# CAPMæææ¶ç
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# Alpha (Y)
alpha_y = actual_y - er_y

# æçå¥çº¦å­åå­å
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}
