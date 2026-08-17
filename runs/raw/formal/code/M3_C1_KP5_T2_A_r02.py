import pandas as pd
import numpy as np
# 解决中文显示问题，设置中中文字格式
plt.rcParams['font.sans-serif'] = [' # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示中文标签

# 1. 读取数据
try:
df = pd.read_csv('data/market_snapshot_v1.csv')
# 2如果计算日收益率（假设fund列为基金净值，计算百分比收益率；如果是日收益率，pct_change().dropna())
# 4. 计算日损益
pnl = daily_returns * position
# 5. 计算历史VaR (95%置信水平对应损益分布的5%分位数)
var_quantile_val = np.percentile(pnl, 5)
var_value = -var_quantile_val

# 6. 绘图
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black')
plt.axvline(var_quantile, color='r', linestyle='--', linewidth=2,
plt.title('Daily P&L Distribution & Historical VaR')
plt.xlabel('Daily P&L (CNY)')
plt.grid(True, alpha=0.3)

# 7. 保存图片
figure_path = 'hist_var_pnl.png'
plt.savefig(figure_path)
plt.close()

# 8. 返回结果
result = {
    'hist_var_95_1d': var_value,
    'figure_path': figure_path
}
