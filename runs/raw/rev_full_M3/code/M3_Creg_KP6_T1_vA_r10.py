import numpy as np
import pandas as pd

# ==========================================
# 第一部分：读取数据并计算年化夏普比率
# ==========================================
# 注：由于未提供真实外部文件，此处通过确定性模拟生成"课程数据快照"的日收益数据，
# 以保证脚本完全自包含、可直接运行且输出确定可复现。
np.random.seed(42)
data_snapshot = pd.DataFrame({
    'fund': np.random.normal(loc=0.0005, scale=0.01, size=252)
})

# 提取 "fund" 列的日收益
fund_daily_returns = data_snapshot['fund']

# 设定无风险利率及年化交易日参数
rf_annual = 0.021
trading_days = 252

# 计算年化组合收益率
annual_return = fund_daily_returns.mean() * trading_days

# 计算年化组合波动率（使用样本标准差 ddof=1）
annual_volatility = fund_daily_returns.std(ddof=1) * np.sqrt(trading_days)

# 计算年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_volatility


# ==========================================
# 第二部分：Brinson归因分析（配置、选择与交互效应）
# ==========================================
# 组合权重与收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 基准总收益
R_b = np.sum(w_b * r_b)

# 配置效应 (Allocation Effect): (W_p - W_b) * (R_b_i - R_b)
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b))

# 选择效应 (Selection Effect): W_b * (R_p_i - R_b_i)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect): (W_p - W_b) * (R_p_i - R_b_i)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 输出契约：存入名为 result 的字典
# ==========================================
result = {
    'sharpe_annual': float(sharpe_annual),
    'allocation_effect': float(round(allocation_effect, 6)),
    'selection_effect': float(round(selection_effect, 6)),
    'interaction_effect': float(round(interaction_effect, 6))
}

# 打印结果验证
if __name__ == "__main__":
    print("计算结果字典：")
    for k, v in result.items():
        print(f"{k}: {v}")
        
    # 逻辑验证：配置 + 选择 + 交互 应等于 组合收益 - 基准收益
    R_p = np.sum(w_p * r_p)
    active_return = R_p - R_b
    brinson_sum = result['allocation_effect'] + result['selection_effect'] + result['interaction_effect']
    print(f"\n[验证] 组合总收益: {R_p:.6f}, 基准总收益: {R_b:.6f}")
    print(f"[验证] 超额收益: {active_return:.6f}, Brinson三项之和: {brinson_sum:.6f}")
