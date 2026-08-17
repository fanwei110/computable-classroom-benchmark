import numpy as np
import pandas as pd

# ============================================================
# 第一部分：年化夏普比率计算
# ============================================================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 确保 'fund' 列存在并剔除缺失值
fund_returns = df['fund'].dropna().values

# 参数设定
rf_annual = 0.021           # 年化无风险利率
trading_days = 252          # 年交易日数
rf_daily = rf_annual / trading_days

# 日度超额收益
excess_returns = fund_returns - rf_daily

# 年化夏普比率（使用样本标准差 ddof=1）
sharpe_annual = np.mean(excess_returns) / np.std(excess_returns, ddof=1) * np.sqrt(trading_days)

# ============================================================
# 第二部分：业绩归因（Brinson 模型）
# ============================================================
# 组合与基准数据
pw = np.array([0.45, 0.35, 0.20])   # 组合权重
pr = np.array([0.083, 0.021, -0.014])  # 行业收益（组合）
bw = np.array([0.40, 0.40, 0.20])   # 基准权重
br = np.array([0.067, 0.034, -0.009])  # 行业收益（基准）

# 基准总收益
Rb = np.sum(bw * br)

# 配置效应： (w_p - w_b) * (r_b - R_b)
allocation_effect = np.sum((pw - bw) * (br - Rb))

# 选择效应： w_b * (r_p - r_b)
selection_effect = np.sum(bw * (pr - br))

# 交互效应： (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((pw - bw) * (pr - br))

# ============================================================
# 输出结果
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 仅用于课堂投屏查看（实际使用时教师可直接调用 result 字典）
print("=== 风险调整后业绩与归因结果 ===")
for key, value in result.items():
    print(f"{key}: {value:.6f}")
