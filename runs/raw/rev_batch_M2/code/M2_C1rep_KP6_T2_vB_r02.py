import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===== 示例数据（请替换为你的真实数据） =====
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=300, freq='B')
df = pd.DataFrame({'fund': np.random.normal(0.0005, 0.015, len(dates))}, index=dates)

# ===== 参数设置 =====
rf_annual = 0.021          # 无风险利率 2.1%
window = 60                # 滚动窗口（可调）
rf_daily = rf_annual / 252 # 日化无风险利率

# ===== 计算滚动年化夏普比率 =====
rolling_mean = df['fund'].rolling(window).mean()
rolling_std  = df['fund'].rolling(window).std()
rolling_sharpe = ((rolling_mean - rf_daily) / rolling_std) * np.sqrt(252)

# 最后一个窗口值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ===== 画图并保存 =====
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe, label=f'{window}-Day Rolling Sharpe', color='steelblue')
plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
plt.title('Rolling Sharpe Ratio (Fund)')
plt.xlabel('Date')
plt.ylabel('Annualized Sharpe')
plt.legend()
fig_path = 'rolling_sharpe.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ===== 输出契约要求的字典 =====
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 4),
    'figure_path': fig_path
}

print(result)
