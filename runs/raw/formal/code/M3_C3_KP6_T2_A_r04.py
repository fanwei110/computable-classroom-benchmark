import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 生成模拟数据（实际使用时请替换为您的数据）
# ==========================================
np.random.seed(42)
dates = pd.date_range(start='2021-01-01', periods=500, freq='B')
daily_returns = np.random.normal(loc=0.0005, scale=0.015, size=500)
fund_prices = 100 * np.cumprod(1 + daily_returns)
df = pd.DataFrame({'fund': fund_prices}, index=dates)

# ==========================================
# 2. 计算滚动年化夏普比率
# ==========================================
def calculate_rolling_sharpe(df, window=60, rf_annual=0.021):
    """
    计算滚动年化夏普比率
    :param df: 包含 'fund' 列的 DataFrame（基金净值或价格）
    :param window: 滚动窗口大小，可调
    :param rf_annual: 年化无风险利率（小数表示，债券年复利报价）
    """
    # 约定：债券收益率按年复利报价，转换为日复利无风险利率
    rf_daily = (1 + rf_annual) ** (1/252) - 1
    
    # 计算日收益率
    daily_ret = df['fund'].pct_change()
    
    # 计算日超额收益率
    excess_ret = daily_ret - rf_daily
    
    # 计算滚动均值与标准差（约定：标准差用样本估计量 ddof=1）
    rolling_mean = excess_ret.rolling(window=window).mean()
    rolling_std = excess_ret.rolling(window=window).std(ddof=1)
    
    # 年化处理（均值*252，标准差*sqrt(252)），得到滚动年化夏普
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
    
    return rolling_sharpe

# 设定窗口大小（窗口可调，此处默认为60）
window_size = 60
rolling_sharpe = calculate_rolling_sharpe(df, window=window_size)

# 获取最后一个窗口的数值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ==========================================
# 3. 绘图并保存
# ==========================================
fig_path = 'rolling_sharpe.png'

plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.dropna(), label=f'{window_size}-Day Rolling Annualized Sharpe', color='blue')
plt.title(f'Rolling {window_size}-Day Annualized Sharpe Ratio (rf=2.1%)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 4. 按照输出契约存入 result 字典
# ==========================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': fig_path
}

print(result)
