import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== 参数（可根据需要调整） ==========
window = 60               # 滚动窗口（交易日天数）
rf_annual = 0.021         # 年化无风险利率 2.1%
# ===========================================

# 假设 df 是已经存在的包含 'fund' 列的 DataFrame
# 如果数据不存在，可用下面注释掉的代码生成示例数据用于测试：
# import numpy as np
# dates = pd.date_range('2020-01-01', periods=500, freq='B')
# np.random.seed(42)
# prices = 100 + np.cumsum(np.random.randn(500) * 0.5)
# df = pd.DataFrame({'fund': prices}, index=dates)

# 计算日频数据
rf_daily = rf_annual / 252
returns = df['fund'].pct_change().dropna()          # 日收益率
excess_returns = returns - rf_daily                 # 超额收益率

# 滚动年化夏普比率
rolling_sharpe = (
    excess_returns.rolling(window).mean()
    / returns.rolling(window).std()
    * np.sqrt(252)
)

# 提取最后一个窗口的有效值
valid_sharpe = rolling_sharpe.dropna()
last_sharpe = valid_sharpe.iloc[-1] if not valid_sharpe.empty else np.nan

# 画图并保存
fig_path = 'rolling_sharpe.png'
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(grid=True)
plt.title(f'{window}-Day Rolling Sharpe Ratio (rf={rf_annual:.1%})')
plt.ylabel('Annualized Sharpe Ratio')
plt.tight_layout()
plt.savefig(fig_path)
plt.close()

# 按要求输出结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': fig_path
}

print(result)
