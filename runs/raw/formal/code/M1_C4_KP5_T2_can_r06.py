import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# 设置参数
position_size = 1_000_000  # 头寸规模（元）
confidence_level = 0.95    # 置信水平（可调参数）

# 1. 读取数据并构造日损益
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path)
daily_returns = df['fund'].dropna().values  # 获取fund列的日收益率序列
daily_pnl = position_size * daily_returns   # 计算日损益（元）

# 2. 计算95%历史VaR（线性插值经验分位数）
var_percentile = 100 * (1 - confidence_level)
historical_var = np.percentile(daily_pnl, var_percentile, method='linear')
historical_var_positive = -historical_var  # 转换为正的损失金额

# 3. 绘制直方图并标注VaR线
plt.figure(figsize=(10, 6))
plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

# 添加VaR竖线和标注
plt.axvline(x=-historical_var_positive, color='red', linestyle='--', linewidth=2)
plt.text(-historical_var_positive * 1.05, plt.ylim()[1] * 0.9,
         f'{confidence_level:.0%} VaR: ¥{historical_var_positive:,.2f}',
         color='red', ha='left', va='top')

plt.title(f'Daily P&L Distribution with {confidence_level:.0%} Historical VaR')
plt.xlabel('Daily P&L (RMB)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = 'var_histogram.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 4. 填充result字典
result = {
    'hist_var_95_1d': historical_var_positive,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
