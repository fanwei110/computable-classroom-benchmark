```python
import numpy as np

# 给定参数（小数表示）
rf = 0.023       # 无风险利率 2.3%
er_m = 0.094      # 市场期望收益 9.4%

# 股票 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 1. CAPM 计算期望收益：E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = er_m - rf   # 市场风险溢价

er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# 2. 股票 Y 实际收益及 alpha 计算
real_return_y = 0.131   # 13.1%
alpha_y = real_return_y - er_y

# 3. 填入 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以便投屏展示
print("=== CAPM 计算结果 ===")
print(f"无风险利率 (rf): {rf:.4f} ({rf*100:.2f}%)")
print(f"市场期望收益 (E[Rm]): {er_m:.4f} ({er_m*100:.2f}%)")
print(f"市场风险