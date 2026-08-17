import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize  # 未实际使用，仅按题目要求导入

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场跌了5.8%
rf_annual = 0.047              # 年化无风险利率

# 将年化无风险利率转换为月利率（采用单利法，符合常见金融习题习惯）
rf_monthly = rf_annual / 12

# 按 CAPM 计算预期月收益率
# E(R) = Rf + beta * (Rm - Rf)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 将结果存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 可选打印，确保可复现
if __name__ == "__main__":
    print(result)
