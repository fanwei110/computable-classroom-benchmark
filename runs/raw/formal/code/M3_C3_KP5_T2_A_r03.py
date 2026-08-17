import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 2. 计算fund列的日收益率（小数表示）和日损益
position = 1000000  # 100万元头寸
returns = df['fund'].pct_change().dropna()  # 日收益率，以小数表示
pnl = returns * position  # 日损益

# 3. 计算历史法VaR
confidence_level = 0.95  # 置信水平（可在此处调整）
alpha = 1 - confidence_level

# 历史法：取损益分布的alpha分位数
pnl_quantile = pnl.quantile(alpha)

# 按约定：VaR报告为正的损失金额
hist_var_95_1d = -pnl_quantile

# 4. 画日损益的直方图并标出VaR线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black', color='steelblue')

# 画VaR线（在PnL坐标系中，VaR对应的是-pnl_quantile的损失，即x轴上的pnl_quantile位置）
plt.axvline(pnl_quantile, color='red', linestyle='dashed', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1日历史VaR = {hist_var_95_1d:,.2f} 元')

plt.title('基金日损益分布直方图及历史VaR')
plt.xlabel('日损益 (元)')
plt.ylabel('频数')
plt.legend()

# 5. 保存图片
fig_path = 'hist_var_pnl.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 6. 按照输出契约构建result字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': fig_path
}

# 打印VaR的数值
print(f"基于历史法计算，95%一日VaR的数值为: {hist_var_95_1d:,.2f} 元")
