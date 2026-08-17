import numpy as np

# 给定条件
rf = 0.023         # 无风险利率
erm = 0.094        # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131  # 股票Y当年实际收益

# 市场风险溢价
risk_premium = erm - rf

# 1. CAPM 期望收益计算
er_x = rf + beta_x * risk_premium
er_y = rf + beta_y * risk_premium
er_z = rf + beta_z * risk_premium

# 2. 股票Y的 alpha
alpha_y = actual_return_y - er_y

# 3. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（小数点后保留足以复现的精度）
print("CAPM 计算结果：")
print(f"股票X的CAPM期望年收益: {er_x:.6f} ({er_x*100:.4f}%)")
print(f"股票Y的CAPM期望年收益: {er_y:.6f} ({er_y*100:.4f}%)")
print(f"股票Z的CAPM期望年收益: {er_z:.6f} ({er_z*100:.4f}%)")
print(f"股票Y的alpha: {alpha_y:.6f} ({alpha_y*100:.4f}%)")
print("\nresult 字典内容:")
print(result)
