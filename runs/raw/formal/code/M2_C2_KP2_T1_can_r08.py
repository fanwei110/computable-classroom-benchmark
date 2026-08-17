import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # 仅导入，未使用绘图
from scipy import constants      # 同样仅导入，保证允许使用的库已引入

# ---------- 给定参数 ----------
rf = 0.023                       # 无风险利率
E_Rm = 0.094                    # 市场期望收益
market_risk_premium = E_Rm - rf # 市场风险溢价

# 股票的 beta 值
beta_X = 0.62
beta_Y = 1.18
beta_Z = 1.51

# ---------- CAPM 期望收益 ----------
# E[Ri] = rf + beta_i * (E[Rm] - rf)
er_X = rf + beta_X * market_risk_premium
er_Y = rf + beta_Y * market_risk_premium
er_Z = rf + beta_Z * market_risk_premium

# ---------- 股票 Y 的 alpha ----------
actual_return_Y = 0.131         # 当年实际收益
alpha_Y = actual_return_Y - er_Y

# ---------- 按要求存入字典 ----------
result = {
    'er_x': er_X,
    'er_y': er_Y,
    'er_z': er_Z,
    'alpha_y': alpha_Y
}

# ---------- 课堂展示 ----------
# 用 pandas 展示表格，便于投屏观察
df = pd.DataFrame({
    'Stock': ['X', 'Y', 'Z'],
    'Beta': [beta_X, beta_Y, beta_Z],
    'E[Ri] (CAPM)': [er_X, er_Y, er_Z],
    'Actual Return': [None, actual_return_Y, None],   # 仅 Y 有实际值
    'Alpha': [None, alpha_Y, None]
})
print("===== CAPM 期望收益与 Alpha =====")
print(df.to_string(index=False))
print("\n结果字典 result =", result)
