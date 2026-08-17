#!/usr/bin/env python3
"""
课堂演示：CAPM 与证券市场线
计算 XYZ 三只股票的期望收益，以及 Y 股票的实际 alpha。
"""

# 仅使用标准库即可完成计算，无需额外依赖
# 输入参数（均为小数形式）
rf = 0.023        # 无风险利率 2.3%
market_ret = 0.094  # 市场期望收益 9.4%

# 三只股票的 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# Y 的实际收益
real_y = 0.131    # 13.1%

# 1. CAPM 期望收益公式: E[Ri] = rf + beta_i * (E[Rm] - rf)
market_premium = market_ret - rf

er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. alpha_y = 实际收益 - CAPM 预测收益
alpha_y = real_y - er_y

# 3. 填充结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出字典，可直接被教师读取或进一步处理
print(result)

# 人性化显示，便于投屏
print("\n=== CAPM 结果 ===")
print(f"无风险利率 rf = {rf*100:.2f}%")
print(f"市场期望收益 E[Rm] = {market_ret*100:.2f}%")
print(f"市场风险溢价 = {market_premium*100:.2f}%")
print("------------------")
print(f"股票 X (beta={beta_x}) 期望收益 = {er_x*100:.4f}%")
print(f"股票 Y (beta={beta_y}) 期望收益 = {er_y*100:.4f}%")
print(f"股票 Z (beta={beta_z}) 期望收益 = {er_z*100:.4f}%")
print("------------------")
print(f"股票 Y 实际收益 = {real_y*100:.2f}%")
print(f"股票 Y 的 alpha = {alpha_y*100:.4f}% (即 {alpha_y:.6f})")
