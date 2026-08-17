import numpy as np
import pandas as pd

# ---------- 第一部分：计算年化夏普比率 ----------
# 模拟课程数据快照：生成 500 个日收益率作为 "fund" 列（随机种子固定，保证可复现）
np.random.seed(42)
n_days = 500
daily_returns = np.random.normal(0.0005, 0.012, n_days)  # 均值约 0.05%，标准差约 1.2%
df = pd.DataFrame({'fund': daily_returns})

# 无风险利率（年化）
risk_free_annual = 0.021

# 计算年化收益与年化波动
annual_return = df['fund'].mean() * 252
annual_volatility = df['fund'].std() * np.sqrt(252)

# 年化夏普比率
sharpe_annual = (annual_return - risk_free_annual) / annual_volatility

# ---------- 第二部分：Brinson 归因分析 ----------
# 组合数据
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准数据
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 基准总收益
r_b_total = np.sum(w_b * r_b)

# 配置效应 (Allocation Effect)
allocation_effect = np.sum((w_p - w_b) * (r_b - r_b_total))

# 选择效应 (Selection Effect)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ---------- 输出结果 ----------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 直接打印结果字典以供查验
if __name__ == '__main__':
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
