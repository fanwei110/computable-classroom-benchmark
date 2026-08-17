# 计算市场风险溢价
market_risk_premium = 9.4% - 2.3%

# 计算各股票的期望收益率
er_x = 2.3% + 0.62 * market_risk_premium
er_y = 2.3% + 1.18 * market_risk_premium
er_z = 2.3% + 1.51 * market_risk_premium

# 计算Y的Alpha
alpha_y = 13.1% - er_y

# 存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

result
