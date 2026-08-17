import pandas as pd
import numpy as np

# ==============================================
# 第一问：年化夏普比率
# 假设数据文件名为 "课程数据文件.csv"，其中包含 "fund" 列
# 若无文件，可将 df 替换为你的实际数据
# ==============================================
try:
    df = pd.read_csv("课程数据文件.csv")
    fund_daily = df["fund"]  # 日收益（小数形式，如 0.01 表示 1%）
except FileNotFoundError:
    # 如果文件不存在，此处用随机数演示，实际计算请替换为真实数据
    np.random.seed(42)
    fund_daily = pd.Series(np.random.normal(0.0005, 0.012, 1000))

rf_annual = 0.021           # 年化无风险利率
days = 252                  # 年交易日数

mean_daily = fund_daily.mean()
std_daily = fund_daily.std(ddof=1)          # 样本标准差 (ddof=1)
mean_annual = mean_daily * days
std_annual = std_daily * np.sqrt(days)

sharpe_annual = (mean_annual - rf_annual) / std_annual

# ==============================================
# 第二问：业绩归因（Brinson 模型）
# ==============================================
wP = np.array([0.45, 0.35, 0.20])   # 组合权重
wB = np.array([0.40, 0.40, 0.20])   # 基准权重
rP = np.array([0.083, 0.021, -0.014])  # 组合行业收益
rB = np.array([0.067, 0.034, -0.009])  # 基准行业收益

allocation_effect = np.sum((wP - wB) * rB)
selection_effect   = np.sum(wB * (rP - rB))
interaction_effect = np.sum((wP - wB) * (rP - rB))

# ==============================================
# 存入结果字典
# ==============================================
result = {
    "sharpe_annual": sharpe_annual,
    "allocation_effect": allocation_effect,
    "selection_effect": selection_effect,
    "interaction_effect": interaction_effect
}

print(result)
