import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt

# 给定数据
risk_free = 0.023          # 无风险利率
market_return = 0.094      # 市场期望收益
market_premium = market_return - risk_free

beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

actual_return_y = 0.131    # 股票Y当年实际收益

# CAPM期望收益计算
er_x = risk_free + beta_x * market_premium
er_y = risk_free + beta_y * market_premium
er_z = risk_free + beta_z * market_premium

# Alpha计算
alpha_y = actual_return_y - er_y

# 按要求存储结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（可复现）
print(result)
