import pandas as pd
import numpy as np

# ==================== 1. 读取快照 CSV ====================
df = pd.read_csv('snapshot.csv')

# 提取 fund 列并清理缺失值
if 'fund' not in df.columns:
    raise ValueError("CSV文件中未找到 'fund' 列，请检查数据！")

fund_data = df['fund'].dropna()

# 内部一致假设1：自动判断 fund 列是净值还是收益率
# 若数据均为正且均值显著大于0（如接近1或更高），视作净值序列并转化为简单收益率
if (fund_data > 0).all() and fund_data.mean() > 0.5:
    returns = fund_data.pct_change().dropna()
else:
    returns = fund_data.copy()

# ==================== 2. 推断数据频率与无风险利率折算 ====================
# 内部一致假设2：自动推断数据频率（每年期数 k），以正确进行年化处理
k = 252  # 默认按A股交易日频率

# 尝试寻找日期列以精准推断频率
date_col = None
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower() or col.lower() == 'index':
        date_col = col
        break

if date_col is not None:
    try:
        dates = pd.to_datetime(df[date_col].dropna())
        if len(dates) > 1:
            # 计算平均间隔天数推断频率
            freq_days = (dates.iloc[-1] - dates.iloc[0]).days / (len(dates) - 1)
            if freq_days <= 7:
                k = 252   # 日频
            elif freq_days <= 35:
                k = 12    # 月频
            elif freq_days <= 100:
                k = 4     # 季频
            else:
                k = 1     # 年频
    except Exception:
        # 日期解析失败，按样本长度粗略推断
        k = 12 if len(returns) <= 120 else 252
else:
    # 无日期列，按样本量推断
    k = 12 if len(returns) <= 120 else 252

# 计入 2.1% 的无风险利率（年化），转化为期无风险利率
rf_annual = 0.021
rf_period = rf_annual / k

# ==================== 3. 计算全样本年化夏普比率 ====================
# 超额收益
excess_returns = returns - rf_period

# 均值与标准差（样本标准差，ddof=1）
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)

# 夏普比率年化公式：Sharpe_annual = (均值 / 标准差) * sqrt(k)
if std_excess == 0:
    sharpe_annual = np.nan
else:
    sharpe_annual = (mean_excess / std_excess) * np.sqrt(k)

# ==================== 4. 把结果存入 result ====================
result = {
    'sharpe_annual': sharpe_annual
}

# 控制台输出，便于课堂投屏展示
print(f"【假设处理】数据频率推断：每年 {k} 期")
print(f"【计算结果】全样本年化夏普比率: {sharpe_annual:.4f}")
