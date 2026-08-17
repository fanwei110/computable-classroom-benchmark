import numpy as np

# ==================== 已知参数 ====================
rf = 2.3 / 100          # 无风险利率 (年化)
er_m = 9.4 / 100        # 市场期望收益 (年化)
betas = np.array([0.62, 1.18, 1.51])  # 股票 X, Y, Z 的 beta
actual_r_y = 13.1 / 100 # 股票 Y 的实际收益 (年化)

# ==================== 步骤 1: 套用 CAPM 计算期望收益 ====================
# E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = er_m - rf
expected_returns = rf + betas * market_risk_premium

er_x = expected_returns[0]
er_y = expected_returns[1]
er_z = expected_returns[2]

# ==================== 步骤 2: 计算 Y 的 alpha ====================
# alpha = 实际收益 - CAPM 预测的期望收益
alpha_y = actual_r_y - er_y

# ==================== 步骤 3: 填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# (可选) 课堂投屏展示打印
if __name__ == '__main__':
    print("CAPM 计算结果：")
    for key, value in result.items():
        print(f"{key}: {value:.4%}")
