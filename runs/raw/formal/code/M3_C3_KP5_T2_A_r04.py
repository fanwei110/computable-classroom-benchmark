import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ================= 1. 读取与处理数据 =================
# 读取CSV文件
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)

# 计算fund列的日收益率 (百分比变化)
df['daily_return'] = df['fund'].pct_change()

# 删除缺失值
df = df.dropna(subset=['daily_return'])

# 头寸100万元
position = 1_000_000

# 计算日损益
df['daily_pnl'] = df['daily_return'] * position

# ================= 2. 计算历史法VaR =================
# 可调的置信水平
confidence_level = 0.95

# 计算分位数 (历史法VaR)：对应分布的左尾
# alpha = 1 - 0.95 = 0.05，即5%分位数
alpha = 1 - confidence_level
pnl_percentile = np.percentile(df['daily_pnl'], alpha * 100)

# VaR报告为正的损失金额
hist_var_95_1d = -pnl_percentile

print(f"在{confidence_level*100}%置信水平下，1日历史VaR的数值为: {hist_var_95_1d:,.2f} 元")

# ================= 3. 绘制直方图并标出VaR线 =================
plt.figure(figsize=(10, 6))
# 绘制日损益直方图
plt.hist(df['daily_pnl'], bins=50, color='skyblue', edgecolor='black', alpha=0.75)

# 标出95%一日历史VaR线 (由于VaR是正数，对应的损失点为 -VaR)
plt.axvline(x=-hist_var_95_1d, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-Day Hist VaR: {hist_var_95_1d:,.2f} RMB')

plt.title('Daily PnL Histogram & Historical VaR')
plt.xlabel('Daily PnL (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'pnl_hist_var_plot.png'
plt.savefig(figure_path)
plt.close()

# ================= 4. 封装输出契约 =================
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

# 验证输出
print("输出的 result 字典为:")
print(result)
