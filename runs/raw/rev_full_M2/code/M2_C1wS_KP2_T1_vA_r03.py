import numpy as np

# 给定参数
rf = 0.023          # 无风险利率
rm = 0.094          # 市场期望收益
betas = np.array([0.62, 1.18, 1.51])   # X, Y, Z 的 beta
actual_y = 0.131    # Y 的实际年收益

# 市场风险溢价
mrp = rm - rf

# 用 CAPM 计算三只股票的期望收益
expected_returns = rf + betas * mrp
er_x, er_y, er_z = expected_returns

# 计算 Y 的 alpha
alpha_y = actual_y - er_y

# 按契约组织输出
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以便投屏展示
print("CAPM 计算结果:")
print(f"市场风险溢价 (rm - rf) = {mrp:.4f} ({mrp*100:.2f}%)")
print(f"X 期望收益: {er_x:.6f} ({er_x*100:.4f}%)")
print(f"Y 期望收益: {er_y:.6f} ({er_y*100:.4f}%)")
print(f"Z 期望收益: {er_z:.6f} ({er_z*100:.4f}%)")
print(f"Y 实际收益: {actual_y:.4f} ({actual_y*100:.2f}%)")
print(f"Y 的 alpha: {alpha_y:.6f} ({alpha_y*100:.4f}%)")
print("\n字典结果 ==>\n", result)
