import numpy as np

# 输入参数 (以小数形式表示百分比)
risk_free_rate = 0.023
market_return = 0.094

beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

actual_return_y = 0.131

# 计算市场风险溢价
market_risk_premium = market_return - risk_free_rate

# 根据 CAPM 公式计算各股票的期望收益: E(R) = r_f + beta * (E(R_m) - r_f)
er_x = risk_free_rate + beta_x * market_risk_premium
er_y = risk_free_rate + beta_y * market_risk_premium
er_z = risk_free_rate + beta_z * market_risk_premium

# 计算股票 Y 的 Alpha: Alpha = 实际收益 - 期望收益
alpha_y = actual_return_y - er_y

# 将结果存入字典，键名严格符合要求
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以供验证
print(result)
