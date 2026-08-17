import numpy as np

# ==================== 已知参数 ====================
rf = 0.023       # 无风险利率 2.3%
erm = 0.094      # 市场期望收益 9.4%
beta_x = 0.62    # 股票 X 的 beta
beta_y = 1.18    # 股票 Y 的 beta
beta_z = 1.51    # 股票 Z 的 beta
r_y_actual = 0.131 # 股票 Y 的实际年收益 13.1%

# ==================== 步骤1：计算 CAPM 期望收益 ====================
# 市场风险溢价
market_risk_premium = erm - rf

# 套用 CAPM 公式: E[Ri] = rf + beta * (E[Rm] - rf)
er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# ==================== 步骤2：计算股票 Y 的 Alpha ====================
# Alpha 定义为实际收益与 CAPM 期望收益的偏差
alpha_y = r_y_actual - er_y

# ==================== 步骤3：填充结果字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 课堂投屏验证输出
if __name__ == "__main__":
    print("CAPM 与证券市场线计算结果：")
    for key, value in result.items():
        print(f"{key}: {value:.6f} (即 {value*100:.4f}%)")
