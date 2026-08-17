import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize

# --- 给定的参数 ---
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌了5.8%
risk_free_annual = 0.047        # 无风险利率 每年4.7%

# --- 计算月度无风险利率 ---
# 按实际天数或复利转换：将年利率换算为等效的月利率（复利）
risk_free_monthly = (1 + risk_free_annual) ** (1/12) - 1

# --- 按CAPM计算预期月度收益 ---
# CAPM: E(R) = Rf + beta * (Rm - Rf)
capm_expected_monthly_return = (
    risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)
)

# --- 存入结果字典 ---
result = {
    'capm_return_monthly': capm_expected_monthly_return
}

# 输出结果以验证（脚本自包含，可直接运行）
if __name__ == "__main__":
    print("CAPM 预期上个月收益（月利率）:", result['capm_return_monthly'])
    print("结果字典:", result)
