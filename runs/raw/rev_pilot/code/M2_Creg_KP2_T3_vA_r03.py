import numpy as np  # 虽然计算简单，但按题目要求导入可能需要的库
import scipy
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 题目给定参数
# ============================================================
beta = 1.42                     # 股票的 beta
market_return_monthly = -0.058  # 上个月市场收益（-5.8%）
risk_free_annual = 0.047        # 年化无风险利率（4.7%）

# 将年化无风险利率转换为月利率（简单按月分摊）
risk_free_monthly = risk_free_annual / 12

# ============================================================
# CAPM 公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
# ============================================================
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# ============================================================
# 按照输出契约将结果存入字典
# ============================================================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 可选：打印结果以便核查
if __name__ == "__main__":
    print(result)
