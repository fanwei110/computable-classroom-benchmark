import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------- 参数设置 ----------
data_path = 'data/market_snapshot_v1.csv'      # 数据文件路径
position = 1_000_000                           # 头寸 100 万元
confidence_level = 0.95                        # 置信水平（可调）
alpha = 1 - confidence_level                   # 显著性水平
figure_path = 'var_histogram.png'              # 图片保存路径

# ---------- 读取数据 ----------
df = pd.read_csv(data_path)
# 假设 'fund' 列为小数形式的日收益率（例如 0.01 代表 1%）
returns = df['fund']

# ---------- 计算日损益 ----------
# 头寸乘以收益率，得到每日盈亏金额
pnl = position * returns

# ---------- 计算历史法 VaR ----------
# 使用 np.percentile 求左尾分位数（亏损为负值）
var_percentile = np.percentile(pnl, alpha * 100)
# VaR 通常以正数报告，取绝对值
hist_var_95_1d = abs(var_percentile)

# ---------- 绘制日损益直方图并标注 VaR ----------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7, label='Daily P&L')
plt.axvline(x=var_percentile, color='red', linestyle='dashed', linewidth=2,
            label=f'Historical VaR (95% 1-day)\n{hist_var_95_1d:,.2f} CNY')
plt.title('Daily Profit & Loss Distribution with Historical VaR')
plt.xlabel('Profit & Loss (CNY)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------- 输出结果字典 ----------
result = {
    'hist_var_95_1d': hist_var_95_1d,   # VaR 数值（正数）
    'figure_path': os.path.abspath(figure_path)   # 图片绝对路径
}

# 查看结果
print(result)
