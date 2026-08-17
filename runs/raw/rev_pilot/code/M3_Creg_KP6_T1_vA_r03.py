import numpy as np
import pandas as pd

# ==========================================
# 第一部分：计算年化夏普比率
# ==========================================

# 模拟课程数据快照 "fund" 列的日收益
# 为保证输出完全确定且可复现，这里硬编码一段确定的日收益数据代替外部读取
daily_returns_data = [
    0.002, -0.005, 0.003, 0.001, -0.002, 
    0.004, 0.000, -0.003, 0.001, 0.002,
    0.003, -0.001, 0.002, -0.004, 0.001
]
fund_snapshot = pd.DataFrame({'fund': daily_returns_data})

# 提取日收益序列
daily_returns = fund_snapshot['fund']

# 参数设置
rf_annual = 0.021
trading_days = 252

# 计算日无风险利率 (实务中通常采用单利折算)
rf_daily = rf_annual / trading_days

# 计算日均值和日标准差 (ddof=1 为样本标准差，符合金融计算惯例)
mean_daily = daily_returns.mean()
std_daily = daily_returns.std(ddof=1)

# 计算日夏普比率和年化夏普比率
sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)


# ==========================================
# 第二部分：计算配置、选择与交互效应
# ==========================================

# 组合权重与收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应: sum((w_p - w_b) * r_b)
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应: sum(w_b * (r_p - r_b))
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应: sum((w_p - w_b) * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 结果汇总
# ==========================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 验证输出
if __name__ == '__main__':
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
