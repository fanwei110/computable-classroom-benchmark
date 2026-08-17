import numpy as np

# 已知参数
rf = 0.023       # 无风险利率 2.3%
erm = 0.094      # 市场期望收益 9.4%
beta_x = 0.62    # 股票 X 的 beta
beta_y = 1.18    # 股票 Y 的 beta
beta_z = 1.51    # 股票 Z 的 beta
actual_ry = 0.131 # 股票 Y 的实际收益 13.1%

# 1. 对每个 beta 套用 CAPM：E[Ri] = rf + beta * (E[Rm] - rf)
market_premium = erm - rf

er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 用 Y 的 CAPM 预测计算其 alpha：alpha = 实际收益 - 期望收益
alpha_y = actual_ry - er_y

# 3. 填充 result
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 投屏输出展示，方便课堂讲解
print("--- CAPM 与证券市场线计算结果 ---")
print(f"股票 X 的 CAPM 期望收益 (er_x): {er_x:.4f} (即 {er_x*100:.2f}%)")
print(f"股票 Y 的 CAPM 期望收益 (er_y): {er_y:.4f} (即 {er_y*100:.2f}%)")
print(f"股票 Z 的 CAPM 期望收益 (er_z): {er_z:.4f} (即 {er_z*100:.2f}%)")
print(f"股票 Y 的 Alpha (alpha_y): {alpha_y:.4f} (即 {alpha_y*100:.2f}%)")
print("\n返回的 result 字典如下：")
print(result)
