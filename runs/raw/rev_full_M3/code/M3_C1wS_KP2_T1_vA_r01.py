# 《证券投资学》课堂实时编程 - CAPM 与证券市场线计算

# ==================== 1. 参数设定 ====================
# 无风险利率与市场期望收益（转为小数）
rf = 0.023
erm = 0.094

# 三只股票的 Beta 值
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# Y 股票的实际年收益
actual_return_y = 0.131

# ==================== 2. CAPM 期望收益计算 ====================
# 市场风险溢价
market_premium = erm - rf

# 对每个 beta 套用 CAPM：E[Ri] = rf + beta * (E[Rm] - rf)
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ==================== 3. Y 的 Alpha 计算 ====================
# Alpha = 实际收益 - CAPM 预期收益
alpha_y = actual_return_y - er_y

# ==================== 4. 结果封装 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# （可选）课堂投屏展示打印
if __name__ == "__main__":
    print("CAPM 计算结果：")
    print(f"股票 X 期望收益 (er_x): {result['er_x']:.4f} ({result['er_x']*100:.2f}%)")
    print(f"股票 Y 期望收益 (er_y): {result['er_y']:.4f} ({result['er_y']*100:.2f}%)")
    print(f"股票 Z 期望收益 (er_z): {result['er_z']:.4f} ({result['er_z']*100:.2f}%)")
    print(f"股票 Y 的 Alpha (alpha_y): {result['alpha_y']:.4f} ({result['alpha_y']*100:.2f}%)")
