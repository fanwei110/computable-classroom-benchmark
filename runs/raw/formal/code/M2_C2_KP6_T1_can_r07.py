import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 第一部分：读取基金日收益，计算年化夏普比率
# ------------------------------------------------------------
# 1) 读取数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')      # 假设列名 'fund' 存在
fund_daily = df['fund'].values                       # 日收益率（小数形式）

# 2) 无风险利率处理
rf_annual = 0.021                    # 年化无风险利率
trading_days = 252                   # 假设一年252个交易日
rf_daily = rf_annual / trading_days  # 日度无风险利率

# 3) 计算日超额收益
excess_daily = fund_daily - rf_daily

# 4) 年化夏普比率
mean_excess_daily = np.mean(excess_daily)
# 使用总体标准差 (ddof=0)，这是时间序列风险度量的常见做法
std_excess_daily = np.std(excess_daily, ddof=0)
sharpe_annual = np.sqrt(trading_days) * mean_excess_daily / std_excess_daily

# ------------------------------------------------------------
# 第二部分：业绩归因 —— 配置效应、选择效应、交互效应
# ------------------------------------------------------------
# 组合与基准的行业权重与收益
w_p = np.array([0.45, 0.35, 0.20])          # 组合权重
r_p = np.array([0.083, 0.021, -0.014])      # 组合中各行业收益
w_b = np.array([0.40, 0.40, 0.20])          # 基准权重
r_b = np.array([0.067, 0.034, -0.009])      # 基准中各行业收益

# 归因计算（Brinson 模型）
allocation_effect  = np.sum((w_p - w_b) * r_b)
selection_effect   = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ------------------------------------------------------------
# 将结果存入字典
# ------------------------------------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出到控制台以便课堂投屏查看
print("=== 计算结果 ===")
print(f"年化夏普比率      : {sharpe_annual:.6f}")
print(f"配置效应          : {allocation_effect:.6f}")
print(f"选择效应          : {selection_effect:.6f}")
print(f"交互效应          : {interaction_effect:.6f}")
print("\nresult 字典内容:")
print(result)
