# 给定参数
Rf = 0.023
Rm = 0.094
market_premium = Rm - Rf  # 0.071

beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# CAPM期望收益计算
er_x = Rf + beta_x * market_premium
er_y = Rf + beta_y * market_premium
er_z = Rf + beta_z * market_premium

# Y的实际收益与Alpha
actual_y = 0.131
alpha_y = actual_y - er_y

# 存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以便查看
import json
print(json.dumps(result, indent=4))
