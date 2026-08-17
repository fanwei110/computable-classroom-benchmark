import pandas as pd
import numpy as np

# ==========================================
# 第一部分：读取数据与年化夏普比率计算
# ==========================================

# 1. 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金的日收益率序列（假设数据已为小数形式，如0.01代表1%）
daily_returns = df['fund'].values

# 无风险利率参数设置（年化 2.1%）
rf_annual = 0.021

# 假设：一年按252个交易日计算，采用精确复利方式折算日无风险利率
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 计算日超额收益（在基金收益中计入无风险利率）
excess_returns_daily = daily_returns - rf_daily

# 计算日超额收益均值
mean_excess_daily = np.mean(excess_returns_daily)

# 计算日收益率的标准差（总风险，使用样本标准差 ddof=1）
std_daily = np.std(daily_returns, ddof=1)

# 计算年化夏普比率：年化超额收益 / 年化总风险 = (均值 * 252) / (标准差 * sqrt(252)) = (均值 / 标准差) * sqrt(252)
sharpe_daily = mean_excess_daily / std_daily
sharpe_annual = sharpe_daily * np.sqrt(252)


# ==========================================
# 第二部分：业绩归因计算 (Brinson-Hood-Beebower 模型)
# ==========================================

# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 (Allocation Effect): 衡量因权重偏离基准带来的超额收益
# 公式：sum((w_p - w_b) * r_b)
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 (Selection Effect): 衡量因收益超越基准带来的超额收益
# 公式：sum(w_b * (r_p - r_b))
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect): 衡量权重偏离与收益偏离共同作用带来的超额收益
# 公式：sum((w_p - w_b) * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 输出契约：填充 result 字典
# ==========================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# ==========================================
# 课堂投屏验证与展示区
# ==========================================
if __name__ == '__main__':
    print("="*50)
    print("《证券投资学》课堂实时编程结果")
    print("="*50)
    
    print("\n【第一部分：风险调整后业绩】")
    print(f"年化夏普比率 (Sharpe Ratio): {result['sharpe_annual']:.6f}")
    
    print("\n【第二部分：业绩归因分解】")
    print(f"配置效应 (Allocation Effect): {result['allocation_effect']:.6f}")
    print(f"选择效应 (Selection Effect): {result['selection_effect']:.6f}")
    print(f"交互效应 (Interaction Effect): {result['interaction_effect']:.6f}")
    
    # 逻辑自洽性验证：主动收益应等于三种效应之和
    active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
    total_effect = result['allocation_effect'] + result['selection_effect'] + result['interaction_effect']
    print("-" * 50)
    print(f"主动收益直接计算值: {active_return:.6f}")
    print(f"归因三效应加总值:   {total_effect:.6f}")
    print(f"验证状态: {'通过' if np.isclose(active_return, total_effect) else '未通过'}")
    print("="*50)
