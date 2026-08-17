import numpy as np

# ==================== 输入参数 ====================
rf = 0.023        # 无风险利率 2.3%
rm = 0.094        # 市场期望收益 9.4%
betas = np.array([0.62, 1.18, 1.51])  # 股票 X, Y, Z 的 beta
r_y_actual = 0.131 # 股票 Y 当年实际收益 13.1%

# ==================== 步骤 1: 计算 CAPM 期望收益 ====================
# E[Ri] = rf + beta * (E[Rm] - rf)
market_premium = rm - rf
expected_returns = rf + betas * market_premium

er_x = expected_returns[0]
er_y = expected_returns[1]
er_z = expected_returns[2]

# ==================== 步骤 2: 计算 Y 的 Alpha ====================
# Alpha = 实际收益 - CAPM 期望收益
alpha_y = r_y_actual - er_y

# ==================== 步骤 3: 填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以便投屏验证
if __name__ == "__main__":
    print("CAPM 计算结果：")
    for key, value in result.items():
        print(f"{key}: {value:.4f} (即 {value*100:.2f}%)")
