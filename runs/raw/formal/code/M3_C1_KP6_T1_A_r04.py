import numpy as np
import pandas as pd

# ============ 第一问计算逻辑 (请替换为您实际的数据文件读取) ============
# df = pd.read_csv('您的课程数据文件.csv')
# daily_returns = df['fund']
# rf_daily = 0.021 / 252
# sharpe_daily = (daily_returns.mean() - rf_daily) / daily_returns.std()
# sharpe_annual_calc = sharpe_daily * np.sqrt(252)

# ============ 第二问计算结果 ============
allocation = 0.00165
selection = 0.0002
interaction = 0.00145

# ============ 严格按要求存入字典 ============
result = {
    'sharpe_annual': None,  # 请将 None 替换为上方算出的 sharpe_annual_calc
    'allocation_effect': allocation,
    'selection_effect': selection,
    'interaction_effect': interaction
}
