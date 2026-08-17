import pandas as pd
import numpy as np

# 0. 参数设定
RISK_FREE_RATE = 0.021          # 年化无风险利率

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 2. 准备收益率序列
# 自动检测数据频率：若存在日期列，解析并推断频率；否则默认日频、252个交易日
if 'date' in df.columns or 'Date' in df.columns:
    date_col = 'date' if 'date' in df.columns else 'Date'
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(date_col, inplace=True)
    df.set_index(date_col, inplace=True)
    # 推断频率
    inferred_freq = pd.infer_freq(df.index[:5])
else:
    inferred_freq = None

# 若fund列为价格（数值较大，典型净值）则转换为收益率；若已是收益率则直接使用
if df['fund'].max() > 1:   # 视作价格
    returns = df['fund'].pct_change().dropna()
else:
    returns = df['fund'].dropna()
    if (returns <= -1).any() or (returns > 2).any():
        # 异常值检查，若出现极端值也尝试作为价格处理
        returns = df['fund'].pct_change().dropna()

# 3. 确定年化因子
if inferred_freq is not None:
    if 'D' in inferred_freq or 'B' in inferred_freq:
        annual_factor = 252
    elif 'W' in inferred_freq:
        annual_factor = 52
    elif 'M' in inferred_freq:
        annual_factor = 12
    elif 'Q' in inferred_freq:
        annual_factor = 4
    elif 'Y' in inferred_freq or 'A' in inferred_freq:
        annual_factor = 1
    else:
        annual_factor = 252   # 默认日频
else:
    # 没有日期信息，根据收益率序列长度与标准差量级粗略判断：常见教学数据多为日频
    annual_factor = 252

# 4. 计算年化夏普比率
# 将年化无风险利率转换为单期无风险利率
risk_free_period = (1 + RISK_FREE_RATE) ** (1 / annual_factor) - 1   # 对数等价也可，此处使用几何转化
excess_returns = returns - risk_free_period
# 年化超额收益
annual_excess_mean = excess_returns.mean() * annual_factor
annual_excess_std = excess_returns.std() * np.sqrt(annual_factor)
sharpe_annual = annual_excess_mean / annual_excess_std

# 备选计算（更常见做法，直接用算术平均转换）：
# 若收益率很小，几何与算术差异微小，两种方式均可，这里使用连续复利框架也可改为：
# excess_returns = returns - RISK_FREE_RATE/annual_factor
# 为保持一致，采用简单减法（算术方法），因为超额收益通常以简单差形式出现
# 重算以保证标准做法：
excess_returns_simple = returns - RISK_FREE_RATE / annual_factor
sharpe_annual = (excess_returns_simple.mean() / excess_returns_simple.std()) * np.sqrt(annual_factor)

# 5. 存储结果
result = {
    'sharpe_annual': round(sharpe_annual, 6)
}

# 如需在控制台查看
print(result)
