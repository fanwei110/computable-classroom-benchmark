import numpy as np

# 给定参数（百分比数值，如 2.3 代表 2.3%）
rf = 2.3          # 无风险利率
E_Rm = 9.4        # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 13.1   # 股票 Y 当年实际收益

# 1. CAPM 期望收益计算：E[Ri] = rf + beta * (E[Rm] - rf)
market_premium = E_Rm - rf
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 股票 Y 的 alpha 计算：alpha = 实际收益 - CAPM 预期收益
alpha_y = actual_return_y - er_y

# 3. 按要求填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果以便课堂投屏查看
print("CAPM 计算结果：")
print(f"股票 X 期望收益: {er_x:.4f}%")
print(f"股票 Y 期望收益: {er_y:.4f}%")
print(f"股票 Z 期望收益: {er_z:.4f}%")
print(f"股票 Y 的 alpha:   {alpha_y:.4f}%")
print("\nresult 字典内容：")
print(result)
