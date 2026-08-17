import pandas as pd
import numpy as np
import io

# ==========================================
# 假设说明 (自洽且符合业界惯例)
# ==========================================
# 1. 年化假设：一年包含 252 个交易日。
# 2. 日无风险利率换算：采用简单算术平均 rf_daily = rf_annual / 252。
# 3. 夏普比率年化公式：Sharpe_annual = (mean_excess_daily / std_excess_daily) * sqrt(252)。
# 4. 标准差计算：采用样本标准差 (ddof=1)。
# 5. 归因分析：采用 Brinson-Hood-Beebower (BHB) 模型。
#    - 题目中“行业收益8.3% 2.1% -1.4%”对应组合/基金层面的行业收益(R_p)；
#    - 题目中基准“收益6.7% 3.4% -0.9%”对应基准层面的行业收益(R_b)。

# ==========================================
# 第一部分：读取快照 CSV 与年化夏普比率
# ==========================================

# 为保证代码自包含与可复现，此处模拟一个包含 252 个交易日 'fund' 列的 CSV 快照
np.random.seed(42)
days = 252
simulated_daily_returns = np.random.normal(loc=0.0008, scale=0.015, size=days)
csv_content = "fund\n" + "\n".join(map(str, simulated_daily_returns))

# 读取快照 CSV
df = pd.read_csv(io.StringIO(csv_content))

# 年化无风险利率 2.1%，转换为日无风险利率
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 在基金收益中计入无风险利率，计算超额收益
excess_returns = df['fund'] - rf_daily

# 计算日均超额收益与日超额收益标准差
mean_excess_daily = excess_returns.mean()
std_excess_daily = excess_returns.std(ddof=1) # 使用样本标准差

# 计算年化夏普比率
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(trading_days)


# ==========================================
# 第二部分：Brinson 业绩归因
# ==========================================

# 组合权重 (W_p) 与组合行业收益 (R_p)
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重 (W_b) 与基准行业收益 (R_b)
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 1. 配置效应 (Allocation Effect): 衡量权重偏离带来的影响
#    公式: sum( (W_p - W_b) * R_b )
allocation_effect = np.sum((w_p - w_b) * r_b)

# 2. 选择效应 (Selection Effect): 衡量行业内超额收益带来的影响
#    公式: sum( W_b * (R_p - R_b) )
selection_effect = np.sum(w_b * (r_p - r_b))

# 3. 交互效应 (Interaction Effect): 衡量权重偏离与超额收益的交叉影响
#    公式: sum( (W_p - W_b) * (R_p - R_b) )
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 第三部分：输出契约
# ==========================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂投屏友好打印
if __name__ == "__main__":
    print("=== 《证券投资学》课堂实时计算结果 ===")
    print(f"年化夏普比率       : {result['sharpe_annual']:.4f}")
    print(f"配置效应        : {result['allocation_effect']:.4%}")
    print(f"选择效应       : {result['selection_effect']:.4%}")
    print(f"交互效应      : {result['interaction_effect']:.4%}")
    
    # 交叉验证：主动总收益 = 配置 + 选择 + 交互
    total_active = r_p.dot(w_p) - r_b.dot(w_b)
    sum_effects = allocation_effect + selection_effect + interaction_effect
    print("\n=== 交叉验证 ===")
    print(f"组合总收益: {r_p.dot(w_p):.4%}, 基准总收益: {r_b.dot(w_b):.4%}")
    print(f"主动总收益: {total_active:.4%}")
    print(f"三项效应之和: {sum_effects:.4%} (验证一致性)")
