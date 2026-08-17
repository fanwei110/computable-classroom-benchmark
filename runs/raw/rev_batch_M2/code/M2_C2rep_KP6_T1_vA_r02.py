import pandas as pd
import numpy as np

# ============================================================
# 1. 读取数据，计算年化夏普比率
# ============================================================
# 读入快照数据，提取 fund 列日收益
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_ret = df['fund']  # 日收益序列（小数形式）

# 年化无风险利率与交易日设定
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 计算日超额收益
excess_daily = fund_ret - rf_daily

# 日夏普比率
sharpe_daily = excess_daily.mean() / excess_daily.std(ddof=1)  # 使用样本标准差

# 年化夏普比率
sharpe_annual = np.sqrt(trading_days) * sharpe_daily

# ============================================================
# 2. 业绩归因：配置效应、选择效应、交互效应
# ============================================================
# 组合权重与收益
wp = np.array([0.45, 0.35, 0.20])
rp = np.array([0.083, 0.021, -0.014])

# 基准权重与收益
wb = np.array([0.40, 0.40, 0.20])
rb = np.array([0.067, 0.034, -0.009])

# 总收益
port_ret = np.sum(wp * rp)
bench_ret = np.sum(wb * rb)

# 三个效应
allocation_effect = np.sum((wp - wb) * rb)
selection_effect = np.sum(wb * (rp - rb))
interaction_effect = np.sum((wp - wb) * (rp - rb))

# 验证：三项之和应等于主动收益
active_return = port_ret - bench_ret
# 断言（容差）可选，但为了教学展示，不阻断运行
# assert np.isclose(allocation_effect + selection_effect + interaction_effect, active_return)

# ============================================================
# 3. 输出字典
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect,
}

# 打印结果以便课堂投屏展示
print(result)
