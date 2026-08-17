import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列（假设该列为基金净值 NAV）
fund_nav = df['fund']

# 计算每期简单收益率
fund_returns = fund_nav.pct_change().dropna()

# 2. 确定年化因子
# 尝试从数据中寻找日期列以推断频率；若无日期列，按课程惯例默认日频(252个交易日/年)
annu_factor = 252  
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower():
        dates = pd.to_datetime(df[col])
        if len(dates) > 1:
            avg_days = (dates.iloc[-1] - dates.iloc[0]).days / (len(dates) - 1)
            if avg_days <= 7:      # 日频或周频，按252处理
                annu_factor = 252
            elif avg_days <= 31:   # 月频
                annu_factor = 12
            else:                  # 季频或更低
                annu_factor = 4
        break

# 3. 计算全样本年化夏普比率
rf_annual = 0.021  # 无风险利率 2.1%

mean_ret = fund_returns.mean()       # 每期平均收益率
std_ret = fund_returns.std()         # 每期收益率标准差 (ddof=1 样本标准差)

# 年化收益率与年化波动率
annu_ret = mean_ret * annu_factor
annu_std = std_ret * np.sqrt(annu_factor)

# 年化夏普比率 = (年化收益率 - 年化无风险利率) / 年化波动率
sharpe_annual = (annu_ret - rf_annual) / annu_std

# 4. 把结果存入 result
result = {
    'sharpe_annual': sharpe_annual
}

# 课堂投屏演示打印
print(f"采用年化因子: {annu_factor}")
print(f"年化夏普比率: {sharpe_annual:.4f}")
print("result字典内容:", result)
