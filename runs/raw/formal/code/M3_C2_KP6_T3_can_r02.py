import pandas as pd
import numpy as np

# ==================== 1. 读取数据与预处理 ====================
# 读取快照CSV文件
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列并剔除缺失值
fund_series = df['fund'].dropna()

# ==================== 2. 内部一致的假设处理 ====================
# 假设1：若fund列为净值序列（特征为所有值均为正且均值显著大于1），则通过pct_change计算日收益率；否则直接视为日收益率序列。
# 假设2：若收益率数值量级偏大（均值>0.05），视为百分比形式（如1.5代表1.5%），将其除以100转换为小数形式（如0.015）。
# 假设3：样本数据为日频交易数据，按照中国市场惯例，一年按242个交易日进行年化。

if (fund_series > 0).all() and fund_series.mean() > 0.5:
    # 视为净值序列，计算日度收益率
    returns = fund_series.pct_change().dropna()
else:
    # 视为日度收益率序列
    returns = fund_series.copy()

if returns.mean() > 0.05:
    # 量级过大，视为百分比数值，转为小数
    returns = returns / 100.0

# ==================== 3. 计算全样本年化夏普比率 ====================
# 给定无风险利率年化 2.1%
rf_annual = 0.021
trading_days = 242

# 计算日度无风险利率
rf_daily = rf_annual / trading_days

# 计算日度收益率的均值与标准差（默认ddof=1，为样本标准差，符合金融惯例）
mean_daily = returns.mean()
std_daily = returns.std()

# 计算日度夏普比率
sharpe_daily = (mean_daily - rf_daily) / std_daily

# 年化夏普比率 = 日度夏普比率 * sqrt(一年交易日数)
# 推导：Sharpe_annual = (mean_daily * 242 - rf_annual) / (std_daily * sqrt(242)) 
#                     = (mean_daily - rf_daily) / std_daily * sqrt(242)
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# ==================== 4. 存入结果 ====================
result = {'sharpe_annual': sharpe_annual}

# (投屏展示辅助，正式契约仅需result字典)
print(f"全样本年化夏普比率: {sharpe_annual:.4f}")
