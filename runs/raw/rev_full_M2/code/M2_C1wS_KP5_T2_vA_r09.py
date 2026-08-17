import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 参数设置 ====================
CONFIDENCE = 0.95                # 置信水平，可调
POSITION_VALUE = 1_000_000.0     # 头寸本金（人民币）
DATA_PATH = "data/market_snapshot_v1.csv"
FIGURE_NAME = "hist_var_95_1d.png"

# ==================== 1. 读取数据并计算日损益 ====================
# 读取快照 CSV，假设包含 'fund' 列（价格或净值）
df = pd.read_csv(DATA_PATH)

# 如果存在日期列，按日期排序，确保收益计算正确
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)

# 计算日收益率，假设 fund 列为价格序列
returns = df['fund'].pct_change().dropna()

# 日损益（人民币）
daily_pnl = POSITION_VALUE * returns

# ==================== 2. 计算历史 VaR ====================
# 损失分位数对应的百分比（例如 95% 置信 → 5% 分位数）
percentile = 100 * (1 - CONFIDENCE)
var_loss = np.percentile(daily_pnl, percentile)          # 损益分位数（负值）
hist_var_amount = -var_loss                              # VaR 金额（正数）

# ==================== 3. 绘图 ====================
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(daily_pnl, bins=50, color='steelblue', edgecolor='white',
        alpha=0.8, label='Daily P&L Distribution')

# 绘制 VaR 线（在损益分位数位置）
ax.axvline(var_loss, color='red', linestyle='--', linewidth=2,
           label=f'{CONFIDENCE*100:.0f}% 1-Day Hist VaR: ¥{hist_var_amount:,.2f}')

# 添加标注
ax.annotate(f'VaR = {hist_var_amount:,.2f}',
            xy=(var_loss, 0),
            xytext=(var_loss - ax.get_xlim()[1]*0.15, ax.get_ylim()[1]*0.85),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=12, color='red', fontweight='bold')

ax.set_xlabel('Daily P&L (¥)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title(f'Historical VaR (Confidence = {CONFIDENCE*100:.0f}%)', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

# 保存图形
plt.tight_layout()
plt.savefig(FIGURE_NAME, dpi=150)
plt.close()

# ==================== 4. 输出结果 ====================
result = {
    'hist_var_95_1d': round(hist_var_amount, 2),
    'figure_path': os.path.abspath(FIGURE_NAME)
}

print("VaR 计算结果：")
print(f"  历史模拟法 95% 1日 VaR = ¥{result['hist_var_95_1d']:,.2f}")
print(f"  图形已保存至：{result['figure_path']}")
