import pandas as pd
import numpy as np

# ------------------------------ 配置 ------------------------------
DATA_PATH = 'data.csv'          # 课程数据文件路径
RISK_FREE_ANNUAL = 0.021       # 年化无风险利率
# ------------------------------------------------------------------

# 读取数据
df = pd.read_csv(DATA_PATH)

# 提取基金收益列（假设列名为 'fund'）
fund_returns = df['fund'].astype(float)

# ---------- 推断数据频率 ----------
# 尝试利用日期列推断每年期数，无日期列则默认月度(12)
if 'date' in df.columns:
    try:
        dates = pd.to_datetime(df['date'])
        # 通过连续日期间隔的中位数推断频率
        median_delta = dates.diff().median()
        if median_delta <= pd.Timedelta(days=1):
            periods_per_year = 252   # 日度
        elif median_delta <= pd.Timedelta(days=7):
            periods_per_year = 52    # 周度
        elif median_delta <= pd.Timedelta(days=31):
            periods_per_year = 12    # 月度
        else:
            periods_per_year = 4     # 季度或更低频率（保守按季度）
    except Exception:
        periods_per_year = 12        # 推断失败，回退到月度
else:
    # 无日期列，默认月度频率
    periods_per_year = 12

# ---------- 计算年化夏普比率 ----------
# 每期无风险利率（简单比例）
rf_period = RISK_FREE_ANNUAL / periods_per_year

# 每期超额收益
excess_returns = fund_returns - rf_period

# 年化夏普比率 = (每期均值 / 每期标准差) * sqrt(年化期数)
sharpe_period = excess_returns.mean() / excess_returns.std()
sharpe_annual = sharpe_period * np.sqrt(periods_per_year)

# 按契约存储结果
result = {
    'sharpe_annual': sharpe_annual
}
