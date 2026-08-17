import numpy as np
import pandas as pd
import os

# ------------- 1. 准备数据（如无CSV则生成模拟数据） -------------
csv_file = 'snapshot.csv'
if not os.path.exists(csv_file):
    np.random.seed(42)  # 保证可复现
    dates = pd.date_range(start='2023-01-01', periods=252, freq='B')
    # 模拟基金日收益：均值0.05%，日波动1%
    fund_daily = np.random.normal(loc=0.0005, scale=0.01, size=252)
    df_sim = pd.DataFrame({'date': dates, 'fund_daily_return': fund_daily})
    df_sim.to_csv(csv_file, index=False)
    print("已生成模拟数据文件 snapshot.csv")

# 读取快照 CSV
df = pd.read_csv(csv_file)
fund_returns = df['fund_daily_return'].values  # 基金日收益序列

# ------------- 2. 计算年化夏普比率 -------------
rf_annual = 0.021                # 年化无风险利率 2.1%
trading_days = 252               # 年交易日数
rf_daily = rf_annual / trading_days

# 超额日收益（计入无风险利率）
excess_daily = fund_returns - rf_daily

# 年化平均超额收益 & 年化波动率
annual_excess_mean = np.mean(excess_daily) * trading_days
annual_excess_std = np.std(excess_daily, ddof=1) * np.sqrt(trading_days)  # 样本标准差

sharpe_annual = annual_excess_mean / annual_excess_std

# ------------- 3. Brinson 绩效归因（配置、选择、交互效应） -------------
# 组合与基准权重
w_p = np.array([0.45, 0.35, 0.20])
w_b = np.array([0.40, 0.40, 0.20])

# 各资产实际收益率（组合）与基准收益率
R_p = np.array([0.083, 0.021, -0.014])
R_b = np.array([0.067, 0.034, -0.009])

# 配置效应 (Allocation Effect)
allocation_effect = np.sum((w_p - w_b) * R_b)  
# 选择效应 (Selection Effect)
selection_effect = np.sum(w_b * (R_p - R_b))   
# 交互效应 (Interaction Effect)
interaction_effect = np.sum((w_p - w_b) * (R_p - R_b))

# ------------- 4. 输出结果字典 -------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

if __name__ == "__main__":
    print("===== 计算结果 =====")
    for key, value in result.items():
        if 'sharpe' in key:
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value:.6f} ({value*100:.4f}%)")
