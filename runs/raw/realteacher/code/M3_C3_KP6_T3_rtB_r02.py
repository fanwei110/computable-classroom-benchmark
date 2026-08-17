import pandas as pd
import numpy as np

# ===== 1. 读取数据 =====
# 请将 'your_data_file.csv' 替换为你真实的课程数据文件路径及文件名
# 如果是 Excel 文件，可使用 pd.read_excel('your_data_file.xlsx')
df = pd.read_csv('your_data_file.csv')

# ===== 2. 提取基金日收益率并确保为小数表示 =====
# 假设数据已经是小数（如 0.05 表示 5%）；如果原始数据是百分数（如 5 表示 5%），请加上下面一行：
# df['fund'] = df['fund'] / 100
R_daily = df['fund']

# ===== 3. 计算统计量 =====
# 日收益率样本均值
mean_daily = R_daily.mean()

# 日收益率样本标准差（严格遵照 ddof=1 的样本估计量约定）
std_daily = R_daily.std(ddof=1)

# 无风险利率参数
rf_annual = 0.021

# 日化无风险利率（通常采用简单除法，与年化时直接减 rf_annual 完全等效）
rf_daily = rf_annual / 252

# 如果你的课程严格要求期权无风险利率按连续复利日化，请注释上一行，改用下一行：
# rf_daily = np.exp(rf_annual / 252) - 1

# ===== 4. 计算年化 Sharpe Ratio =====
# 日超额收益均值
excess_mean_daily = mean_daily - rf_daily

# 日夏普比率
sharpe_daily = excess_mean_daily / std_daily

# 年化夏普比率（乘以 sqrt(252)）
sharpe_annual = sharpe_daily * np.sqrt(252)

# ===== 5. 构建输出契约字典 =====
result = {'sharpe_annual': sharpe_annual}

# 打印结果以供检查
print(result)
