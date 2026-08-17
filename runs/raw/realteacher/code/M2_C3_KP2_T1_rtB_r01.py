# 给定参数
rf = 0.023       # 无风险利率
rm = 0.094       # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131

# 市场风险溢价
mrp = rm - rf  # 0.071

# CAPM 期望收益
er_x = rf + beta_x * mrp
er_y = rf + beta_y * mrp
er_z = rf + beta_z * mrp

# Y 的 Alpha
alpha_y = actual_return_y - er_y

# 输出字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印查看（实际任务中输出此字典即可）
import json
print(json.dumps(result, indent=4))
