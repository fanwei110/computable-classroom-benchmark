import numpy as np
import pandas as pd
import os

# ------------------------------
# 1. 读取数据
# ------------------------------
DATA_FILE = 'fund.csv'   # 教师提供的快照CSV文件名（根据实际调整）
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"找不到文件 {DATA_FILE}，请确认文件路径")

df = pd.read_csv(DATA_FILE)

# 确保存在 fund 列
if 'fund' not in df.columns:
    # 尝试使用第一列
    fund_col = df.columns[0]
else:
    fund_col = 'fund'

raw = df[fund_col].astype(float)

# ------------------------------
# 2. 收益率预处理
# ------------------------------
# 检测数据形态：若最大值 > 1 且无负值，可能是价格/净值，需计算收益率
if raw.max() > 1 and raw.min() >= 0:
    # 视为价格序列，计算日收益率
    returns = raw.pct_change().dropna()
else:
    # 已经是收益率形式
    returns = raw.copy()
    # 若收益率数值偏大（如表示百分比），转换为小数
    if returns.abs().mean() > 0.5:   # 平均绝对值超过0.5，大概率是百分比形式
        returns = returns / 100.0

returns = returns.dropna()

# ------------------------------
# 3. 全样本年化夏普比率计算
# ------------------------------
rf_annual = 0.021                # 2.1% 无风险利率
DAYS_PER_YEAR = 252              # 采用252个交易日年化

# 每日无风险利率
rf_daily = rf_annual / DAYS_PER_YEAR

# 每日超额收益
excess_return = returns - rf_daily

# 年化夏普比率 = (日均超额收益 * 252) / (日超额收益标准差 * sqrt(252))
# 等价于 sqrt(252) * 均值/标准差
sharpe_annual = (excess_return.mean() / excess_return.std()) * np.sqrt(DAYS_PER_YEAR)

# ------------------------------
# 4. 输出结果
# ------------------------------
result = {
    'sharpe_annual': sharpe_annual
}

# 可直接查看
print(result)
