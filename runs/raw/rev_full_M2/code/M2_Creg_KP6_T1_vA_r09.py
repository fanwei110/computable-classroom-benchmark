import numpy as np
import pandas as pd
import scipy   # 按要求导入，未直接使用
import matplotlib  # 按要求导入，未直接使用

# ====================== 第一部分：年化夏普比率 ======================
RISK_FREE = 0.021          # 年化无风险利率
TRADING_DAYS = 252         # 年交易日数

try:
    # 尝试读取课程数据快照
    df = pd.read_csv('fund_data.csv')
    fund_returns = df['fund'].values
    print("已从 fund_data.csv 读取 fund 列日收益。")
except FileNotFoundError:
    # 若缺失文件则生成确定性的示例数据，保证可复现
    np.random.seed(42)
    fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=1000)
    print("未找到 fund_data.csv，使用种子42生成的示例日收益（1000个交易日）。")

# 日收益转为小数形式（若为百分比则自动转换：如果绝对值均值>1则视为百分比）
if np.abs(fund_returns).mean() > 1.0:
    fund_returns = fund_returns / 100.0

# 年化收益率与年化标准差
annual_return = fund_returns.mean() * TRADING_DAYS
annual_vol = fund_returns.std(ddof=1) * np.sqrt(TRADING_DAYS)

# 年化夏普比率
sharpe_annual = (annual_return - RISK_FREE) / annual_vol

# ====================== 第二部分：Brinson 归因 ======================
# 组合数据
wp = np.array([0.45, 0.35, 0.20])   # 组合行业权重
rp = np.array([0.083, 0.021, -0.014])  # 组合行业收益

# 基准数据
wb = np.array([0.40, 0.40, 0.20])   # 基准行业权重
rb = np.array([0.067, 0.034, -0.009]) # 基准行业收益

# 总体收益
portfolio_return = np.dot(wp, rp)
benchmark_return = np.dot(wb, rb)

# 配置效应：Σ (wp_i - wb_i) * (rb_i - benchmark_return)
allocation_effect = np.dot(wp - wb, rb - benchmark_return)

# 选择效应：Σ wb_i * (rp_i - rb_i)
selection_effect = np.dot(wb, rp - rb)

# 交互效应：Σ (wp_i - wb_i) * (rp_i - rb_i)
interaction_effect = np.dot(wp - wb, rp - rb)

# ====================== 输出字典 ======================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（可选，方便查看）
print("\n========== 计算结果 ==========")
for key, val in result.items():
    print(f"{key}: {val:.6f}")
