import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文字体与负号显示，防止图表乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ================= 1. 读取与处理数据 =================
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)

# 计算fund列的日收益率 (假设fund列为净值序列)
daily_returns = df['fund'].pct_change().dropna()

# ================= 2. 计算日损益与VaR =================
position = 1000000  # 100万元头寸
daily_pnl = position * daily_returns

# 置信水平可调参数
confidence_level = 0.95
alpha = 1 - confidence_level

# 历史模拟法：直接取经验分位数
# np.percentile 默认插值法为线性，符合标准历史法要求
var_threshold = np.percentile(daily_pnl, alpha * 100)

# VaR 报告为正的损失金额
hist_var_95_1d = -var_threshold

# ================= 3. 绘图与保存 =================
plt.figure(figsize=(10, 6))
plt.hist(daily_pnl, bins=50, alpha=0.75, edgecolor='black')

# 画出 VaR 阈值线 (注意：损失金额为正，对应损益轴的负方向 -hist_var_95_1d)
plt.axvline(x=var_threshold, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-day VaR: {hist_var_95_1d:.2f} 元')

plt.title('日损益直方图与历史法VaR')
plt.xlabel('日损益 (元)')
plt.ylabel('频数')
plt.legend()

# 保存图片
figure_path = 'pnl_hist_var_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 4. 构造输出契约字典 =================
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

# 打印 VaR 数值
print(f"=> 根据历史法计算，95%一日历史VaR的数值为: {hist_var_95_1d:.2f} 元")
print(f"=> 输出字典内容: {result}")
