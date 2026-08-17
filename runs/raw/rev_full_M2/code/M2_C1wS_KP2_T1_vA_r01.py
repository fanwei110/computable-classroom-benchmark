import numpy as np

# 输入参数（以小数表示）
rf = 0.023          # 无风险利率 2.3%
E_Rm = 0.094        # 市场期望收益 9.4%
beta_X = 0.62
beta_Y = 1.18
beta_Z = 1.51
actual_return_Y = 0.131  # Y 实际年收益 13.1%

# 市场风险溢价
market_premium = E_Rm - rf  # 0.071

# CAPM 期望收益
er_x = rf + beta_X * market_premium
er_y = rf + beta_Y * market_premium
er_z = rf + beta_Z * market_premium

# Y 的 alpha
alpha_y = actual_return_Y - er_y

# 汇总结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

print("CAPM 计算结果：")
for key, value in result.items():
    print(f"  {key}: {value:.6f} ({value*100:.4f}%)")
