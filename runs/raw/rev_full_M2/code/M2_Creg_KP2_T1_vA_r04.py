import numpy as np

# 市场参数
risk_free_rate = 0.023          # 无风险利率 2.3%
market_expected_return = 0.094  # 市场期望收益 9.4%
market_premium = market_expected_return - risk_free_rate

# 各股票的 beta 系数
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 股票 Y 的实际年收益
actual_return_y = 0.131

# 根据 CAPM 计算期望收益
er_x = risk_free_rate + beta_x * market_premium
er_y = risk_free_rate + beta_y * market_premium
er_z = risk_free_rate + beta_z * market_premium

# 计算股票 Y 的 alpha
alpha_y = actual_return_y - er_y

# 按要求组织结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}
