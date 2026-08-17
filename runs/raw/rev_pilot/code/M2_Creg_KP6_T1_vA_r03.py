import pandas as pd
import numpy as np

# =========================
# 第一部分：年化夏普比率
# =========================

# 假设课程数据快照已加载为 DataFrame 'data'，其包含 'fund' 列代表日收益
# 这里模拟数据以便脚本自包含运行
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2021-12-31', freq='B')
fund_daily = pd.Series(np.random.normal(0.0005, 0.015, len(dates)), index=dates, name='fund')
data = pd.DataFrame({'fund': fund_daily})

# 无风险利率
rf_annual = 0.021
rf_daily = (1 + rf_annual) ** (1/252) - 1

# 日超额收益
excess_daily = data['fund'] - rf_daily

# 年化平均超额收益
ann_excess = excess_daily.mean() * 252

# 年化波动率
ann_vol = excess_daily.std() * np.sqrt(252)

# 年化夏普比率
sharpe_annual = ann_excess / ann_vol

# =========================
# 第二部分：绩效归因
# =========================

# 组合与基准参数
p_weights = np.array([0.45, 0.35, 0.20])
b_weights = np.array([0.40, 0.40, 0.20])
p_returns = np.array([0.083, 0.021, -0.014])
b_returns = np.array([0.067, 0.034, -0.009])

# 总收益
Rp = np.sum(p_weights * p_returns)
Rb = np.sum(b_weights * b_returns)

# 配置效应 (Allocation effect)
# 公式: sum( (w_p,i - w_b,i) * (R_b,i - Rb) )
allocation_effect = np.sum((p_weights - b_weights) * (b_returns - Rb))

# 选择效应 (Selection effect)
# 公式: sum( w_b,i * (R_p,i - R_b,i) )
selection_effect = np.sum(b_weights * (p_returns - b_returns))

# 交互效应 (Interaction effect)
# 公式: sum( (w_p,i - w_b,i) * (R_p,i - R_b,i) )
interaction_effect = np.sum((p_weights - b_weights) * (p_returns - b_returns))

# =========================
# 结果输出
# =========================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果以供查验
for k, v in result.items():
    print(f"{k}: {v:.6f}")
