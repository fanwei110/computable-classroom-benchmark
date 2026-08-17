import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 计算fund列的日收益率（假设fund列为基金净值，计算日收益率；若其本身就是日收益率，请直接使用df['fund']）
# 为严谨起见，此处使用pct_change计算日收益率
returns = df['fund'].pct_change().dropna()

# 设置参数
position = 1_000_000  # 头寸100万
confidence_level = 0.95  # 置信度可调
alpha = 1 - confidence_level

# 计算历史法VaR：取收益率的alpha分位数，乘以头寸，取正数表示损失金额
var_return = returns.quantile(alpha)
var_95_1d = -var_return * position

# 计算每日损益（PnL）
pnl = returns * position

# 绘制损益直方图
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black')

# 标出95%一日VaR线（在PnL直方图中，VaR是正数损失，对应的分界线在负的VaR处）
plt.axvline(x=-var_95_1d, color='r', linestyle='--', linewidth=2, 
            label=f'95% 1-Day VaR = {var_95_1d:.2f}')

plt.title('PnL Histogram & 95% 1-Day Historical VaR')
plt.xlabel('Profit and Loss (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图表
fig_path = 'pnl_hist_var.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约存入字典
result = {
    'hist_var_95_1d': var_95_1d,
    'figure_path': fig_path
}

# 报告VaR数值
print(f"95% 一日历史法VaR: {var_95_1d:.2f} 元")
print(f"结果字典: {result}")
