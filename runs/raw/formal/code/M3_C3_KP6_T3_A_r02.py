import numpy as np
import pandas as pd

# 假设课程数据已加载到 DataFrame df 中，且包含 'fund' 列
# 如果 'fund' 列是净值数据，需先计算日收益率；如果是日收益率则直接使用
# returns = df['fund'].pct_change().dropna()  # 若为净值
# returns = df['fund']                       # 若为日收益率

# --- 以下为核心计算逻辑 ---
rf = 0.021  # 无风险利率，小数表示
trading_days = 252

# 1. 计算年化平均收益率
ann_return = returns.mean() * trading_days

# 2. 计算年化波动率（使用样本标准估计量 ddof=1）
ann_std = returns.std(ddof=1) * np.sqrt(trading_days)

# 3. 计算年化夏普比率
sharpe_annual = (ann_return - rf) / ann_std

# 4. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
