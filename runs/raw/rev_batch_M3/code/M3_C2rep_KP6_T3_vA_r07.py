import pandas as pd
import numpy as np

# ==================== 假设说明 ====================
# 1. 题目指明使用 "fund" 列，根据金融数据分析惯例，假设该列为基金的净值/价格序列，需先计算简单收益率。
# 2. 无风险利率年化为 2.1%，计算周期利率时采用简单算术折算（即 Rf_periodic = 0.021 / n_periods）。
# 3. 样本标准差使用 ddof=1（即无偏估计），这是计算夏普比率时的标准做法。
# 4. 数据频率：优先通过识别日期列自动推断（日度252，周度52，月度12）；若无日期列，默认按月度（12期）年化。
# ==================================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列并计算简单收益率
fund_prices = df['fund']
returns = fund_prices.pct_change().dropna()

# 2. 推断数据频率（以决定年化周期数 n_periods）
# 默认假设为月度数据（n_periods = 12）
n_periods = 12  
date_cols = ['date', 'Date', 'datetime', 'time', 'timestamp', 'trade_date']
date_col = None

for col in date_cols:
    if col in df.columns:
        date_col = col
        break

if date_col:
    # 尝试解析日期并按时间排序
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col]).sort_values(by=date_col).reset_index(drop=True)
    diffs = df[date_col].diff().dt.days.dropna()
    median_diff = diffs.median()
    
    if median_diff <= 3:      # 包含周末缺失的日度数据
        n_periods = 252
    elif median_diff <= 10:   # 周度数据
        n_periods = 52
    elif median_diff <= 31:   # 月度数据
        n_periods = 12
    else:                    # 其他情况保守按月度处理
        n_periods = 12

# 3. 计算全样本年化夏普比率
rf_annual = 0.021
# 将年化无风险利率折算为周期利率
rf_periodic = rf_annual / n_periods

mean_periodic = returns.mean()
std_periodic = returns.std(ddof=1)  # 使用样本标准差

# 计算周期夏普比率
sharpe_periodic = (mean_periodic - rf_periodic) / std_periodic

# 年化夏普比率
sharpe_annual = sharpe_periodic * np.sqrt(n_periods)

# 4. 把结果存入 result
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果以供验证
print(result)
