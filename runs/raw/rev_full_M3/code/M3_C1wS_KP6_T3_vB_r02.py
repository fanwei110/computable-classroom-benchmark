import pandas as pd
import numpy as np

# ==========================================
# 1. 生成模拟快照CSV (保证脚本自包含可运行)
# 假设: fund列为基金单位净值，数据频率为月度
# ==========================================
np.random.seed(42) # 固定随机种子以确保结果确定可复现
n_months = 60 # 模拟5年期的月度数据
dates = pd.date_range(start='2018-01-31', periods=n_months + 1, freq='M')

# 模拟月度收益率并生成净值序列
monthly_ret_sim = np.random.normal(loc=0.01, scale=0.04, size=n_months)
nav = np.cumprod(1 + monthly_ret_sim)
nav = np.insert(nav, 0, 1.0) # 初始净值为1.0

df_sim = pd.DataFrame({'date': dates, 'fund': nav})
df_sim.to_csv('snapshot.csv', index=False)

# ==========================================
# 2. 读取快照 CSV
# ==========================================
df = pd.read_csv('snapshot.csv')

# ==========================================
# 3. 计算全样本年化夏普比率
# ==========================================
# 假设处理说明：
# - 假设'fund'列为基金净值序列，通过 pct_change() 计算简单收益率。
# - 假设数据频率为月度（每年12期），此为金融数据最常见的未说明频率。
# - 给定年化无风险利率 rf = 2.1%，则月度无风险利率 = 2.1% / 12。

periods_per_year = 12
rf_annual = 0.021
rf_period = rf_annual / periods_per_year

# 计算基金月度收益率
returns = df['fund'].pct_change().dropna()

# 计算月度超额收益
excess_returns = returns - rf_period

# 计算周期（月度）夏普比率
# 分母采用收益率序列的标准差（总风险），这是计算夏普比率的标准做法
sharpe_period = excess_returns.mean() / returns.std()

# 年化夏普比率 = 周期夏普比率 * sqrt(一年中的周期数)
sharpe_annual = sharpe_period * np.sqrt(periods_per_year)

# ==========================================
# 4. 结果存入 result 字典
# ==========================================
result = {
    'sharpe_annual': round(sharpe_annual, 4)
}

# 课堂投屏展示输出
print(f"无风险利率(年化): {rf_annual * 100:.1f}%")
print(f"全样本年化夏普比率: {result['sharpe_annual']}")
print(f"结果字典: {result}")
