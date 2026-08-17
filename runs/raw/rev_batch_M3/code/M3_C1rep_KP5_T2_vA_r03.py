import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ================= 1. 读取与处理数据 =================
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)

# 题目要求“取fund列的日收益”，这里假定fund列为基金净值，计算日收益率
# 若fund列本身直接就是日收益率，则pct_change()后含义仍一致（变成收益的变动，不符合常理）
# 因此按业界常规：fund列为净值/价格
daily_returns = df['fund'].pct_change().dropna()

# ================= 2. 计算日损益与VaR =================
position = 1000000  # 头寸100万元
pnl = position * daily_returns  # 日损益序列

# 置信水平（可调参数，默认95%）
confidence_level = 0.95 

# 历史法VaR：取损益序列的 (1 - 置信水平) 分位数
# 例如95%置信度，取5%分位数（通常是负数，代表极端损失）
percentile_point = (1 - confidence_level) * 100
var_value = np.percentile(pnl, percentile_point)

# VaR按惯例以正数报告损失绝对值
var_report = abs(var_value)

print(f"置信水平 {confidence_level*100:.0f}% 下的一日历史VaR为: {var_report:.2f} 元")

# ================= 3. 绘制直方图与标线 =================
plt.figure(figsize=(10, 6))
# 绘制日损益直方图
plt.hist(pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

# 画出VaR标线（在真实的分位点画线，通常是负值一侧）
plt.axvline(var_value, color='red', linestyle='dashed', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-day VaR: {var_report:.2f} RMB')

plt.title('Daily P&L Distribution & Historical VaR')
plt.xlabel('Daily P&L (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', alpha=0.75)

# 保存图片
fig_path = 'hist_var_plot.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 4. 按契约组装输出 =================
result = {
    'hist_var_95_1d': var_report,
    'figure_path': fig_path
}

print("\n输出契约结果 result 字典：")
print(result)
