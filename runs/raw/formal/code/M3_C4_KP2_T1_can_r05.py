import numpy as np

# ==========================================
# 《证券投资学》课堂实时编程：CAPM 与证券市场线
# ==========================================

# 1. 已知参数设定（所有比率均用小数表示）
rf = 0.023          # 无风险利率 2.3%
erm = 0.094         # 市场期望收益 9.4%
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
actual_ry = 0.131   # 股票 Y 当年实际收益 13.1%

# 2. 计算市场风险溢价
market_premium = erm - rf

# 3. 对每个 beta 套用 CAPM 公式：E[Ri] = rf + beta * (E[Rm] - rf)
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 4. 用 Y 的 CAPM 预测计算其 alpha（实际收益 - 期望收益）
alpha_y = actual_ry - er_y

# 5. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 课堂投屏输出展示
if __name__ == "__main__":
    print("CAPM 期望收益与 Alpha 计算结果：")
    print("-" * 35)
    print(f"市场风险溢价 [E(Rm) - Rf]: {market_premium:.4f}")
    print(f"股票 X 期望收益 (er_x)   : {result['er_x']:.5f}")
    print(f"股票 Y 期望收益 (er_y)   : {result['er_y']:.5f}")
    print(f"股票 Z 期望收益 (er_z)   : {result['er_z']:.5f}")
    print(f"股票 Y 的 Alpha (alpha_y): {result['alpha_y']:.5f}")
    print("-" * 35)
