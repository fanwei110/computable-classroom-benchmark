import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
POSITION = 1_000_000          # 头寸金额（人民币）
CONFIDENCE_LEVEL = 0.95       # 置信水平（可调参数，例如可改为 0.99 等）

# ==================== 步骤 1：读取 CSV，构造日损益 ====================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列的日收益率序列，并剔除可能的缺失值
returns = df['fund'].dropna()

# 计算头寸的日损益 (P&L)
pnl = POSITION * returns

# ==================== 步骤 2：由经验分布计算历史 VaR ====================
alpha = 1 - CONFIDENCE_LEVEL

# 损益分布的损失分位数：先求 P&L 的 alpha 分位数（即最坏情况下的损益阈值），
# 取其相反数即为在险价值 VaR（以正数表示最大可能损失）
pnl_quantile = np.percentile(pnl, alpha * 100)
hist_var = -pnl_quantile

# ==================== 步骤 3：画直方图并加带标注的 VaR 线 ====================
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益分布直方图
ax.hist(pnl, bins=50, edgecolor='black', alpha=0.75, color='steelblue')

# 绘制 VaR 对应的竖线（位置为 P&L 的 alpha 分位数），并加上标注
ax.axvline(x=pnl_quantile, color='red', linestyle='--', linewidth=2, 
           label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day VaR = {hist_var:,.2f} RMB')

ax.set_title('Daily P&L Distribution and Historical VaR')
ax.set_xlabel('Daily P&L (RMB)')
ax.set_ylabel('Frequency')
ax.legend()
ax.grid(True, alpha=0.3)

# ==================== 步骤 4：保存图形并填充 result ====================
figure_path = 'hist_var_95_1d.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

result = {
    'hist_var_95_1d': hist_var,
    'figure_path': figure_path
}
