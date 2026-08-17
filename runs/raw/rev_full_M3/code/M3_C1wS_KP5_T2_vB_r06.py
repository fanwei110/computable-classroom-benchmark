import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= 参数设置 =================
POSITION = 1_000_000             # 头寸：100万人民币
CONFIDENCE_LEVEL = 0.95          # 置信度：95%，可调参数
DATA_PATH = 'data/market_snapshot_v1.csv'
FIG_SAVE_PATH = 'var_histogram.png'

# ================= 1. 读取数据，构造日损益 =================
df = pd.read_csv(DATA_PATH)
# 提取 fund 列日收益率并剔除缺失值，保证计算稳健
daily_returns = df['fund'].dropna()
# 构造头寸的日损益 (PnL)
daily_pnl = POSITION * daily_returns

# ================= 2. 由经验分布计算历史 VaR =================
# VaR 通常表示为正数（代表损失金额），即损益分布的左尾分位数取负
alpha = 1 - CONFIDENCE_LEVEL
var_95_1d = -np.percentile(daily_pnl, alpha * 100)

# ================= 3. 画直方图并加带标注的 VaR 线 =================
plt.figure(figsize=(10, 6))

# 绘制损益直方图
plt.hist(daily_pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 绘制 VaR 线 (PnL = -VaR)
var_line_x = -var_95_1d
plt.axvline(x=var_line_x, color='red', linestyle='--', linewidth=2, 
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day VaR: {var_95_1d:,.2f} RMB')

# 标注与美化
plt.title(f'Daily PnL Distribution & Historical VaR (Position: {POSITION/1e6:.1f}M RMB)', fontsize=14)
plt.xlabel('Daily Profit and Loss (RMB)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)

# ================= 4. 保存图形并填充 result =================
plt.savefig(FIG_SAVE_PATH, dpi=150, bbox_inches='tight')
plt.close()

result = {
    'hist_var_95_1d': var_95_1d,
    'figure_path': FIG_SAVE_PATH
}

# 课堂展示打印（可选，便于投屏直接看到数值）
print(f"95% 1-Day Historical VaR: {var_95_1d:,.2f} RMB")
print(f"Figure saved to: {FIG_SAVE_PATH}")
