import numpy as np
import pandas as pd

# 给定的参数
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 股票 beta 值
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 股票 Y 的实际收益
actual_return_y = 0.131  # 13.1%

# 计算 CAPM 期望收益: E(R_i) = R_f + beta_i * (E(R_m) - R_f)
market_risk_premium = market_return - risk_free_rate

er_x = risk_free_rate + beta_x * market_risk_premium
er_y = risk_free_rate + beta_y * market_risk_premium
er_z = risk_free_rate + beta_z * market_risk_premium

# 计算 alpha: alpha = 实际收益 - CAPM 期望收益
alpha_y = actual_return_y - er_y

# 存入结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果
print("CAPM 期望年收益与 Alpha 计算结果：")
print(f"股票 X 的期望收益 (er_x): {er_x:.6f} ({er_x*100:.4f}%)")
print(f"股票 Y 的期望收益 (er_y): {er_y:.6f} ({er_y*100:.4f}%)")
print(f"股票 Z 的期望收益 (er_z): {er_z:.6f} ({er_z*100:.4f}%)")
print(f"股票 Y 的 Alpha (alpha_y): {alpha_y:.6f} ({alpha_y*100:.4f}%)")
print("\n结果字典：")
print(result)
