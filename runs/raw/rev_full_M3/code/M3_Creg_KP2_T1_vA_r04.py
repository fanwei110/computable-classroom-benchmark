import numpy as np

# 已知参数
rf = 0.023  # 无风险利率 2.3%
rm = 0.094  # 市场期望收益 9.4%
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131  # 股票 Y 的实际收益 13.1%

# 计算市场风险溢价
market_risk_premium = rm - rf

# 根据 CAPM 公式计算期望收益: E(Ri) = Rf + βi * (Rm - Rf)
er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# 计算 Alpha: Alpha = 实际收益 - 期望收益
alpha_y = actual_return_y - er_y

# 将所有要求的输出存入名为 result 的字典，键名严格为指定值
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}
