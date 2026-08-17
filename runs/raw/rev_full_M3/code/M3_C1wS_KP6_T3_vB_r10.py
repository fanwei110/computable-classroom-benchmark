import pandas as pd
import numpy as np

# ==========================================
# 假设声明（内部一致）：
# 1. CSV文件名为 'snapshot.csv'，包含 'fund' 列，代表基金收益率序列。
# 2. 'fund' 列为小数形式的月度收益率（如0.01代表1%）。
# 3. 基于月度数据假设，一年包含12期，年化因子为 12。
# 4. 无风险利率 2.1% 为年化利率，折算到月度为 rf_annual / 12。
# 5. 标准差计算采用样本标准差 (ddof=1)。
# ==========================================

# 【自包含数据生成】
# 为了确保脚本在任何环境下均可直接运行并复现结果，此处先生成模拟的 snapshot.csv
# 实际课堂运行时，若环境中已有该文件，此段代码会覆盖原文件，可根据需要注释掉
np.random.seed(42)
dates = pd.date_range(start='2018-01-31', periods=60, freq='M')
# 模拟一个月均收益约0.8%，月波动率约4%的基金净值序列
fund_returns = np.random.normal(loc=0.008, scale=0.04, size=60)
mock_df = pd.DataFrame({'date': dates, 'fund': fund_returns})
mock_df.to_csv('snapshot.csv', index=False)

# 1. 读取快照 CSV
df = pd.read_csv('snapshot.csv')

# 2. 计入 2.1% 的无风险利率
rf_annual = 0.021
periods_per_year = 12  # 假设为月度数据
rf_period = rf_annual / periods_per_year

# 3. 计算全样本年化夏普比率
fund = df['fund']

# 计算每期超额收益
excess_returns = fund - rf_period

# 计算超额收益的均值和样本标准差
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)

# 计算每期夏普比率并年化
sharpe_period = mean_excess / std_excess
sharpe_annual = sharpe_period * np.sqrt(periods_per_year)

# 4. 把结果存入 result
result = {
    'sharpe_annual': sharpe_annual
}

# 课堂投屏输出展示
print("="*50)
print(f"无风险利率 (年化): {rf_annual:.1%}")
print(f"数据频率假设: 月度 (一年{periods_per_year}期)")
print(f"全样本年化夏普比率: {sharpe_annual:.4f}")
print("="*50)
print(f"result字典内容: {result}")
