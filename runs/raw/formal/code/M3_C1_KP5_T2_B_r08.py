import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ---------------- 参数设置 ----------------
position = 1000000            # 头寸 100万
confidence_level = 0.95       # 置信度可调 (例如 0.95, 0.99)
alpha = 1 - confidence_level
file_path = 'data/market_snapshot_v1.csv'
figure_path = 'pnl_histogram_var.png'

# ---------------- 数据读取与处理 ----------------
# 读取数据
df = pd.read_csv(file_path)

# 提取 fund 列的日收益率（假设题目中的"日收益"即为收益率序列，若为净值需先计算收益率，此处按字面作为收益率处理）
returns = df['fund'].dropna()

# 计算损益 (PnL)
pnl = returns * position

# ---------------- 历史法 VaR 计算 ----------------
# 历史法：直接取损益序列的下 alpha 分位数，VaR 报告为正数
hist_var = -np.percentile(pnl, alpha * 100)

# ---------------- 绘图 ----------------
plt.figure(figsize=(10, 6))
# 绘制损益直方图
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='steelblue')

# 标出 95% 一日 VaR 竖线 (因为 VaR 是正数，竖线画在 -VaR 的位置代表左侧损失临界值)
plt.axvline(x=-hist_var, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-Day VaR: {hist_var:,.2f}')

plt.title('损益分布直方图及历史法VaR', fontsize=14)
plt.xlabel('损益金额', fontsize=12)
plt.ylabel('频数', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)

# 保存图片
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------------- 输出契约 ----------------
result = {
    'hist_var_95_1d': hist_var,
    'figure_path': figure_path
}

# 报告 VaR 数值
print(f"根据历史法计算，{confidence_level*100:.0f}% 置信度下的一日VaR为: {hist_var:,.2f} 元")
print(f"结果字典: {result}")
