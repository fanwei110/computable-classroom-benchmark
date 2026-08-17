import pandas as pd
import numpy as np

# ============================================================
# 1. 读取快照 CSV（假设文件名为 snapshot.csv）
# ============================================================
# 为满足自包含要求，若文件不存在则构造示例数据并发出提示
try:
    fund_returns = pd.read_csv('snapshot.csv', index_col=0, parse_dates=True)
except FileNotFoundError:
    # 构造示例数据：假设提供基金日收益序列（列名假定为 'fund_return'）
    dates = pd.date_range('2023-01-01', periods=252, freq='B')
    np.random.seed(42)
    daily_returns = np.random.normal(0.0005, 0.01, len(dates))
    fund_returns = pd.DataFrame({'fund_return': daily_returns}, index=dates)
    print("未找到 snapshot.csv，使用随机生成的示例数据。")

# 假定 CSV 中基金日收益列名为 'fund_return'
fund_daily = fund_returns['fund_return'].values

# -------------------- 无风险利率处理 --------------------
rf_annual = 0.021          # 年化无风险利率 2.1%
rf_daily = rf_annual / 252  # 日度无风险利率

# 超额收益 = 基金日收益 - 日无风险利率
excess_daily = fund_daily - rf_daily

# ============================================================
# 2. 计算年化夏普比率
# ============================================================
mean_excess_daily = np.mean(excess_daily)
std_excess_daily = np.std(excess_daily, ddof=1)  # 样本标准差

# 年化夏普比率（假设252个交易日）
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ============================================================
# 3. 业绩归因：配置效应、选择效应、交互效应
# ============================================================
# 组合权重
w_p = np.array([0.45, 0.35, 0.20])
# 行业（组合内各资产）收益
r_p = np.array([0.083, 0.021, -0.014])  # 8.3%, 2.1%, -1.4%

# 基准权重
w_b = np.array([0.40, 0.40, 0.20])
# 基准内各资产收益（行业基准收益）
r_b = np.array([0.067, 0.034, -0.009])  # 6.7%, 3.4%, -0.9%

# 组合总收益和基准总收益（加权和）
R_p = np.sum(w_p * r_p)
R_b = np.sum(w_b * r_b)

# 主动收益 = 组合收益 - 基准收益
active_return = R_p - R_b

# --- 效应分解（采用 Brinson 模型） ---
# 配置效应 = Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 验证三者之和等于主动收益（允许浮点误差）
check_sum = allocation_effect + selection_effect + interaction_effect
if not np.isclose(check_sum, active_return):
    print(f"警告：效应之和 ({check_sum:.6f}) 与主动收益 ({active_return:.6f}) 不一致！")

# ============================================================
# 4. 填充 result 字典
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（供课堂展示）
print("\n===== 风险调整后业绩分析 =====")
print(f"年化夏普比率: {sharpe_annual:.4f}")
print(f"配置效应: {allocation_effect:.6f} ({allocation_effect*100:.4f}%)")
print(f"选择效应: {selection_effect:.6f} ({selection_effect*100:.4f}%)")
print(f"交互效应: {interaction_effect:.6f} ({interaction_effect*100:.4f}%)")
print(f"主动收益合计: {allocation_effect+selection_effect+interaction_effect:.6f} "
      f"（组合: {R_p:.4%}, 基准: {R_b:.4%}）")
print("\nresult 字典内容：")
for k, v in result.items():
    print(f"  {k}: {v}")
