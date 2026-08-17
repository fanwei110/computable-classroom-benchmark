import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===== 使用您的实际数据替换此示例 =====
# 示例：生成随机每日收益率数据（仅供演示）
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2023-12-31')
fund_returns = np.random.normal(0.0005, 0.02, len(dates))   # 日均收益率0.05%，标准差2%
df = pd.DataFrame({'fund': fund_returns}, index=dates)
# =====================================

# 参数设置
rf_annual = 0.021                # 无风险利率（年化）
window = 60                      # 滚动窗口（可调）
rf_daily = (1 + rf_annual) ** (1/252) - 1   # 转换为日度

# 超额收益率
df['excess'] = df['fund'] - rf_daily

# 滚动年化夏普比率
def annualized_sharpe(series):
    """计算年化夏普比率"""
    return np.mean(series) / np.std(series) * np.sqrt(252)

rolling_sharpe = df['excess'].rolling(window).apply(annualized_sharpe, raw=True)

# 最后一个窗口的夏普值
last_sharpe = rolling_sharpe.dropna().iloc[-1]

# 画图
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe, label=f'Rolling {window}-Day Sharpe', color='blue')
plt.axhline(y=0, color='red', linestyle='--', linewidth=0.8)
plt.title('Rolling 60-Day Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
plt.savefig('rolling_sharpe.png', dpi=150)
plt.close()

# 输出契约
result = {
    'rolling_sharpe_last': round(last_sharpe, 6),
    'figure_path': 'rolling_sharpe.png'
}

print(result)
