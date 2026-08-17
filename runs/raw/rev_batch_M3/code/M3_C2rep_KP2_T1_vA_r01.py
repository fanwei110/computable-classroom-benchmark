# 《证券投资学》课堂实时编程 - CAPM 与证券市场线计算

# 给定参数
rf = 0.023          # 无风险利率 (每年 2.3%)
rm = 0.094          # 市场期望收益 (每年 9.4%)
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
actual_return_y = 0.131  # 股票 Y 的实际年收益 (13.1%)

# 1. 套用 CAPM 公式：E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = rm - rf

er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# 2. 计算 Y 的 alpha：实际收益 - CAPM 预期收益
alpha_y = actual_return_y - er_y

# 3. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 课堂投屏展示（可选输出，便于学生理解）
if __name__ == '__main__':
    print("CAPM 期望收益与 Alpha 计算结果：")
    for key, value in result.items():
        print(f"{key}: {value:.4f} ({value*100:.2f}%)")
