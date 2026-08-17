import numpy as np

# 给定参数
rf = 0.023          # 无风险利率 (2.3%)
rm = 0.094          # 市场期望收益 (9.4%)
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131    # 股票 Y 当年实际收益

# CAPM 公式: E[Ri] = rf + beta * (rm - rf)
risk_premium = rm - rf

er_x = rf + beta_x * risk_premium
er_y = rf + beta_y * risk_premium
er_z = rf + beta_z * risk_premium

# Alpha = 实际收益 - CAPM 预测收益
alpha_y = actual_y - er_y

# 按要求存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 可选：打印结果以便课堂投屏查看
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.4f} ({value*100:.2f}%)")
