import numpy as np

# 给定参数
rf = 0.023          # 无风险利率
E_Rm = 0.094        # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131    # 股票Y当年实际收益

# 市场风险溢价
market_premium = E_Rm - rf

# 利用CAPM计算期望收益
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 计算股票Y的alpha
alpha_y = actual_y - er_y

# 按要求构建结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 便于课堂查看，打印结果
print("CAPM计算结果：")
print(f"股票X期望收益: {er_x:.4%}")
print(f"股票Y期望收益: {er_y:.4%}")
print(f"股票Z期望收益: {er_z:.4%}")
print(f"股票Y的alpha: {alpha_y:.4%}")
print("\n结果字典:")
print(result)
