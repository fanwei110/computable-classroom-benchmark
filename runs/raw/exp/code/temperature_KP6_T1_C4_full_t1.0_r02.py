import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

# -------------------- 第一部分：读取快照并计算夏普比率 --------------------
# 构造快照数据（自包含，不可联网）
# 模拟 CSV 内容：两列，'date' 和 'fund'
# 为演示目的，使用随机但可复现的收益序列（教师可现场替换为真实文件）
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=500, freq='B')  # 500个交易日
fund_returns = np.random.normal(0.0008, 0.012, size=500)  # 日收益，均值0.08%，标准差1.2%

# 构建 DataFrame
df = pd.DataFrame({'date': dates, 'fund': fund_returns})

# 保存为 CSV（模拟读取快照）
df.to_csv('fund_snapshot.csv', index=False)

# 读取 CSV
data = pd.read_csv('fund_snapshot.csv', parse_dates=['date'])
daily_returns = data['fund'].values

# 无风险利率年化2.1%
rf_annual = 0.021
rf_daily = rf_annual / 252  # 日无风险利率

# 超额收益
excess_daily = daily_returns - rf_daily

# 样本标准差 (ddof=1)
std_daily = np.std(excess_daily, ddof=1)

# 年化夏普比率
sharpe_annual = np.mean(excess_daily) / std_daily * np.sqrt(252)

# -------------------- 第二部分：Brinson-Hood-Beebower 归因 --------------------
# 组合与基准参数
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
w_b = np.array([0.40, 0.40, 0.20])    # 基准权重
r_b = np.array([0.067, 0.034, -0.009]) # 基准行业收益

# 配置效应：Σ(w_p - w_b) * r_b
allocation = np.sum((w_p - w_b) * r_b)

# 选择效应：Σ w_b * (r_p - r_b)
selection = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ (w_p - w_b) * (r_p - r_b)
interaction = np.sum((w_p - w_b) * (r_p - r_b))

# -------------------- 输出结果字典 --------------------
result = {
    'sharpe_annual': round(sharpe_annual, 6),
    'allocation_effect': round(allocation, 6),
    'selection_effect': round(selection, 6),
    'interaction_effect': round(interaction, 6)
}

# 打印结果（教师投屏用）
print("计算结果：")
print(result)
