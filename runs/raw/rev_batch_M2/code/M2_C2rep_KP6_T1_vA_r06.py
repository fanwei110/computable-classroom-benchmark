import pandas as pd
import numpy as np

# ======================
# 1. 读取数据与预处理
# ======================
# 读取课程快照CSV文件
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益
fund_returns = df['fund'].values

# 无风险利率设定（年化2.1%）
annual_rf = 0.021

# 假设一年有252个交易日，计算日化无风险利率
trading_days = 252
daily_rf = (1 + annual_rf) ** (1/trading_days) - 1

# 计算超额收益（基金日收益 - 日化无风险利率）
excess_returns = fund_returns - daily_rf

# ======================
# 2. 计算年化夏普比率
# ======================
# 日度夏普比率均值
daily_mean_excess = np.mean(excess_returns)

# 日度超额收益标准差
daily_std_excess = np.std(excess_returns, ddof=1)  # 使用样本标准差

# 年化转换（假设收益服从独立同分布）
annual_mean_excess = daily_mean_excess * trading_days
annual_std_excess = daily_std_excess * np.sqrt(trading_days)

# 年化夏普比率
sharpe_annual = annual_mean_excess / annual_std_excess

# ======================
# 3. 业绩归因分析
# ======================
# 组合权重
w_p = np.array([0.45, 0.35, 0.20])
# 行业收益（组合）
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重
w_b = np.array([0.40, 0.40, 0.20])
# 行业收益（基准）
r_b = np.array([0.067, 0.034, -0.009])

# 计算组合总收益与基准总收益
R_p = np.sum(w_p * r_p)
R_b = np.sum(w_b * r_b)

# 总主动收益
total_active = R_p - R_b

# 配置效应 (Allocation Effect)
# 公式：Sum[(w_p_i - w_b_i) * (r_b_i - R_b)]
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b))

# 选择效应 (Selection Effect)
# 公式：Sum[w_b_i * (r_p_i - r_b_i)]
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect)
# 公式：Sum[(w_p_i - w_b_i) * (r_p_i - r_b_i)]
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 验证总和是否等于总主动收益（处理浮点误差）
total_attribution = allocation_effect + selection_effect + interaction_effect

# ======================
# 4. 输出结果
# ======================
result = {
    'sharpe_annual': round(sharpe_annual, 6),
    'allocation_effect': round(allocation_effect, 6),
    'selection_effect': round(selection_effect, 6),
    'interaction_effect': round(interaction_effect, 6)
}

# 打印结果以供验证
print("=" * 50)
print(f"年化夏普比率: {result['sharpe_annual']:.6f}")
print(f"配置效应 (Allocation): {result['allocation_effect']:.6f}")
print(f"选择效应 (Selection):  {result['selection_effect']:.6f}")
print(f"交互效应 (Interaction):{result['interaction_effect']:.6f}")
print(f"总归因效应之和: {total_attribution:.6f}")
print(f"总主动收益: {total_active:.6f}")
print("=" * 50)
