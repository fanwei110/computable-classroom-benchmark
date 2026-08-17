# 《证券投资学》课堂实时编程 - CAPM与证券市场线计算

# 已知参数设定（以小数形式表示百分比利率）
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
actual_ry = 0.131   # 股票 Y 的实际收益 13.1%

# 1. 对每个 beta 套用 CAPM：E[Ri] = rf + beta * (E[Rm] - rf)
# 计算市场风险溢价
market_premium = rm - rf

# 计算各股票的 CAPM 期望年收益
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 用 Y 的 CAPM 预测计算其 alpha
# Alpha = 实际收益 - CAPM期望收益
alpha_y = actual_ry - er_y

# 3. 填充 result
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 课堂投屏展示辅助输出（格式化为百分比便于阅读）
if __name__ == '__main__':
    print("--- CAPM 期望收益与 Alpha 计算 ---")
    print(f"市场风险溢价 (E[Rm] - rf): {market_premium:.4f} ({market_premium*100:.2f}%)")
    print(f"股票 X 期望收益 (er_x): {er_x:.4f} ({er_x*100:.2f}%)")
    print(f"股票 Y 期望收益 (er_y): {er_y:.4f} ({er_y*100:.2f}%)")
    print(f"股票 Z 期望收益 (er_z): {er_z:.4f} ({er_z*100:.2f}%)")
    print(f"股票 Y Alpha (alpha_y):  {alpha_y:.4f} ({alpha_y*100:.2f}%)")
    print("----------------------------------")
    print("result 字典原始输出:", result)
