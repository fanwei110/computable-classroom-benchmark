import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows用黑体，Mac可改为'Arial Unicode MS'
plt.rcParams['axes.unicode_minus'] = False

# ====== 1. 读取数据 ======
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取fund列作为日收益率（若fund列为净值，则需改为 df['fund'].pct_change().dropna()）
daily_returns = df['fund'].dropna()

# ====== 2. 参数设置 ======
position = 1_000_000  # 头寸100万
confidence_level = 0.95  # 置信度（可在此处调整，如0.99等）
alpha = 1 - confidence_level

# ====== 3. 计算损益 (PnL) 与 历史法VaR ======
pnl = daily_returns * position

# 计算历史法VaR：求PnL在alpha分位数的值（即最糟糕的5%情况下的阈值）
var_threshold = np.percentile(pnl, alpha * 100)
# VaR按惯例取绝对值报告，表示可能损失的最大金额
var_value = abs(var_threshold)

# ====== 4. 绘制损益直方图及VaR标根线 ======
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='steelblue')

# 画出VaR标根线（由于var_threshold是负数，代表损失阈值）
plt.axvline(x=var_threshold, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1日VaR: {var_value:,.2f} 元')

plt.title('损益分布直方图与历史模拟法VaR', fontsize=14)
plt.xlabel('损益金额 (元)', fontsize=12)
plt.ylabel('频数', fontsize=12)
plt.legend(fontsize=12)

# 保存图表
fig_path = 'hist_var_pnl.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ====== 5. 严格遵照输出契约存入字典 ======
result = {
    'hist_var_95_1d': var_value,
    'figure_path': fig_path
}

# 报告VaR数值
print(f"【报告】基于历史模拟法的 95%一日VaR 为: {var_value:,.2f} 元")
print(f"【输出契约】result = {result}")
