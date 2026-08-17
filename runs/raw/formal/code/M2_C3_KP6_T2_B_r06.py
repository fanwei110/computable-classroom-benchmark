import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============ 参数 ============
rf = 0.021              # 年化无风险利率
window = 60             # 滚动窗口（可调整）
annual_factor = 252     # 年化交易日数

# ============ 假设数据 ============
# 请确保 df 已经存在，且包含 'fund' 列（这里假设是净值序列）
# 如果 df['fund'] 是净值，先计算日收益率
df['return'] = df['fund'].pct_change().dropna()

# 计算超额收益率（日度）
daily_rf = rf / annual_factor   # 假设无风险利率是年复利报价，日化处理
df['excess_return'] = df['return'] - daily_rf

# ============ 滚动夏普比率 ============
# 使用样本标准差（ddof=1）
rolling_mean = df['excess_return'].rolling(window=window).mean()
rolling_std = df['excess_return'].rolling(window=window).std(ddof=1)   # 默认ddof=1
rolling_sharpe = rolling_mean / rolling_std * np.sqrt(annual_factor)   # 年化

# ============ 最后一个窗口值 ============
last_value = rolling_sharpe.iloc[-1]   # 最后一个非空值

# ============ 绘图并保存 ============
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(rolling_sharpe.index, rolling_sharpe, label=f'{window}-Day Rolling Sharpe')
ax.axhline(y=0, color='gray', linestyle='--')
ax.set_title(f'Rolling Sharpe Ratio (rf={rf*100}%, window={window})')
ax.set_xlabel('Date')
ax.set_ylabel('Annualized Sharpe Ratio')
ax.legend()
fig.tight_layout()

# 保存图片
figure_path = 'rolling_sharpe.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# ============ 按契约输出字典 ============
result = {
    'rolling_sharpe_last': last_value,
    'figure_path': figure_path
}

print(f"最后一个窗口的滚动夏普值：{last_value:.4f}")
print(f"图片已保存至：{figure_path}")
print(f"result 字典内容：{result}")
