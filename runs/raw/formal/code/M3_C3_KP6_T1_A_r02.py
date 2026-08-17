import pandas as pd
import numpy as np

# ========== 假设读取课程数据文件 ==========
# 请根据实际文件格式修改此处，确保列名为 'fund'
# df = pd.read_csv('your_course_data.csv') 
# R_fund = df['fund']

# ========== 第一部分：计算年化夏普比率 ==========
# 按约定：年化与去年化按252个交易日，债券收益率按年复利，标准差ddof=1
def calculate_annualized_sharpe(R_fund, annual_rf=0.021):
    # 1. 日无风险利率（年复利报价转日频）
    rf_daily = (1 + annual_rf) ** (1 / 252) - 1
    
    # 2. 日超额收益
    excess_returns = R_fund - rf_daily
    
    # 3. 均值与样本标准差(ddof=1)
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std(ddof=1)
    
    # 4. 年化夏普比率
    sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)
    return sharpe_annual

# sharpe_annual_val = calculate_annualized_sharpe(R_fund)

# ========== 第二部分：业绩归因 ==========
wp = np.array([0.45, 0.35, 0.20])
wb = np.array([0.40, 0.40, 0.20])
Rp = np.array([0.083, 0.021, -0.014])
Rb = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((wp - wb) * Rb)
selection_effect = np.sum(wb * (Rp - Rb))
interaction_effect = np.sum((wp - wb) * (Rp - Rb))

# ========== 构建输出字典 ==========
# 请将下方 sharpe_annual 的占位符替换为实际计算运行后的值
result = {
    'sharpe_annual': None,  # 运行代码后替换为 calculate_annualized_sharpe(R_fund) 的结果
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print(result)
