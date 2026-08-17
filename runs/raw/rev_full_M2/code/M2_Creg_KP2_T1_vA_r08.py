import numpy as np

# 给定数据
risk_free_rate = 0.023      # 无风险利率
market_return = 0.094       # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

actual_return_y = 0.131     # 股票Y当年实际收益

# CAPM期望收益计算公式: E(R_i) = R_f + beta_i * (E(R_m) - R_f)
market_premium = market_return - risk_free_rate

er_x = risk_free_rate + beta_x * market_premium
er_y = risk_free_rate + beta_y * market_premium
er_z = risk_free_rate + beta_z * market_premium

# Alpha计算: alpha = 实际收益 - CAPM期望收益
alpha_y = actual_return_y - er_y

# 构建结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果字典
print(result)
