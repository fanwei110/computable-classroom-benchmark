import pandas as pd
import numpy as np

# ================= 假设处理说明 =================
# 1. 数据格式：假设快照文件名为 snapshot.csv，且包含列名为 'fund' 的数据列。
# 2. 净值/收益率判断：若 fund 列最大值 > 1.5，视为基金净值序列，自动计算收益率；否则视为收益率序列。
# 3. 数据频率推断：若样本量 > 100，视为日度数据（一年242个交易日）；否则视为月度数据（一年12期）。
# 4. 风险指标：使用样本标准差（ddof=1）衡量波动率，符合统计学与金融学惯例。
# =================================================

# 1. 读取快照 CSV
df = pd.read_csv('snapshot.csv')
fund_data = df['fund'].copy()

# 判断是净值还是收益率，并统一转换为收益率序列
if fund_data.max() > 1.5:
    # 极值大于1.5，判定为净值序列，计算环比收益率
    fund_returns = fund_data.pct_change().dropna()
else:
    # 否则判定为收益率序列
    fund_returns = fund_data

# 推断数据频率对应的年化因子
n_samples = len(fund_returns)
if n_samples > 100:
    periods_per_year = 242  # 日度数据
else:
    periods_per_year = 12   # 月度数据

# 2. 计算全样本年化夏普比率
# 计入 2.1% 的无风险利率
rf_annual = 0.021
# 转换为单期无风险利率
rf_period = rf_annual / periods_per_year

# 计算单期平均收益率与标准差
mean_return = fund_returns.mean()
std_return = fund_returns.std(ddof=1)  # 样本标准差

# 单期夏普比率
excess_return_period = mean_return - rf_period
sharpe_period = excess_return_period / std_return

# 年化夏普比率 = 单期夏普比率 * sqrt(一年中的期数)
sharpe_annual = sharpe_period * np.sqrt(periods_per_year)

# 3. 把结果存入 result
result = {'sharpe_annual': sharpe_annual}

# （可选：课堂投屏展示结果打印）
print(f"数据频率推断: {'日度(242期/年)' if n_samples > 100 else '月度(12期/年)'}")
print(f"全样本年化夏普比率: {sharpe_annual:.4f}")
