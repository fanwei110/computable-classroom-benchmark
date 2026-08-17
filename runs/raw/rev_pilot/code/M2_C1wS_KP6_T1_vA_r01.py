import pandas as pd
import numpy as np
import os

# ------------------------------ 1. 读取数据 ------------------------------
# 优先使用 'snapshot.csv'，否则选取当前目录下唯一的 CSV 文件
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
if len(csv_files) == 1:
    file_path = csv_files[0]
else:
    file_path = 'snapshot.csv'  # 请根据实际文件名修改

df = pd.read_csv(file_path)
# 假设 fund 列直接存储日收益率（小数，例如 0.001 代表 0.1%）
fund_daily = df['fund'].values

# ------------------------------ 2. 年化夏普比率 ------------------------------
rf_annual = 0.021          # 年化无风险利率
trading_days = 252         # 年交易日数
rf_daily = rf_annual / trading_days   # 简单单利日化
excess_daily = fund_daily - rf_daily

mean_excess = np.mean(excess_daily)
# 使用样本标准差 (ddof=1)
std_excess = np.std(excess_daily, ddof=1)
sharpe_annual = np.sqrt(trading_days) * mean_excess / std_excess

# ------------------------------ 3. 业绩归因 ------------------------------
# 组合与基准的行业权重
w_p = np.array([0.45, 0.35, 0.20])
w_b = np.array([0.40, 0.40, 0.20])
# 行业收益率（百分比数值转换为小数）
R_p = np.array([8.3, 2.1, -1.4]) / 100.0
R_b = np.array([6.7, 3.4, -0.9]) / 100.0

allocation_effect  = np.sum((w_p - w_b) * R_b)          # 配置效应
selection_effect   = np.sum(w_b * (R_p - R_b))          # 选择效应
interaction_effect = np.sum((w_p - w_b) * (R_p - R_b))  # 交互效应

# ------------------------------ 4. 输出结果 ------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print(result)
