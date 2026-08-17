import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')
# 提取fund列的日收益率，并去除缺失值
returns = df['fund'].dropna()

# 2. 参数设置
position = 1_000_000  # 头寸100万
confidence_level = 0.95  # 置信度（可在此处调整，例如改为0.99）

# 3. 计算损益 (PnL)
# 假设fund列为日收益率（小数形式），若为百分比形式需除以100
pnl = returns * position

# 4. 计算历史法VaR
# 取左尾 (1 - confidence_level) 分位数，VaR取正数
var_value = -np.percentile(pnl, 100 * (1 - confidence_level))

# 5. 绘制损益直方图并标出VaR线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black', color='steelblue')

# 画95%一日VaR标根线
plt.axvline(x=-var_value, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-Day VaR: {var_value:,.2f}')

plt.title('损益直方图及历史法VaR', fontsize=14)
plt.xlabel('损益金额', fontsize=12)
plt.ylabel('频数', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.5)

# 保存图表
figure_path = 'pnl_hist_var.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 6. 按照输出契约存入字典
result = {
    'hist_var_95_1d': var_value,
    'figure_path': figure_path
}

# 报告VaR数值
print(f"基于历史法，头寸100万，{confidence_level*100:.0f}% 一日VaR数值为: {var_value:,.2f}")
