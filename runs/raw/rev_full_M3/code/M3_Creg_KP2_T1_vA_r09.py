import numpy as np

# 已知参数
risk_free_rate = 0.023      # 无风险利率 2.3%
market_return = 0.094       # 市场期望收益 9.4%
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131     # 股票Y当年实际收益 13.1%

# 计算市场风险溢价
market_risk_premium = market_return - risk_free_rate

# 计算各股票的 CAPM 期望年收益
# CAPM 公式: E(R_i) = R_f + beta_i * (E(R_m) - R_f)
er_x = risk_free_rate + beta_x * market_risk_premium
er_y = risk_free_rate + beta_y * market_risk_premium
er_z = risk_free_rate + beta_z * market_risk_premium

# 计算股票 Y 的 alpha
# Alpha 公式: Alpha = 实际收益 - 期望收益
alpha_y = actual_return_y - er_y

# 将结果存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以供验证
print(result)
