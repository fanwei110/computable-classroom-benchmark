import numpy as np
import pandas as pd

# ============================
# 配置：数据文件路径与参数
# ============================
DATA_FILE = "data.csv"        # 课程数据文件（包含 fund 列）
RISK_FREE_RATE = 0.021        # 年化无风险利率
TRADING_DAYS = 252            # 年交易日数，用于年化

# ============================
# 1. 读取数据
# ============================
df = pd.read_csv(DATA_FILE)
# 确保 fund 列存在
if 'fund' not in df.columns:
    raise ValueError("数据文件中缺少 'fund' 列")

# 假设 fund 列为日频净值（若已是收益率则可跳过此步，以下按净值处理）
# 计算对数收益率
log_returns = np.log(df['fund'] / df['fund'].shift(1)).dropna()

# ============================
# 2. 计算年化夏普比率
# ============================
# 日化无风险利率（连续复利近似）
daily_rf = RISK_FREE_RATE / TRADING_DAYS

# 超额收益率
excess_returns = log_returns - daily_rf

# 年化夏普比率
sharpe_annual = np.sqrt(TRADING_DAYS) * excess_returns.mean() / excess_returns.std()

# ============================
# 3. 输出结果字典
# ============================
result = {'sharpe_annual': sharpe_annual}

print(result)
