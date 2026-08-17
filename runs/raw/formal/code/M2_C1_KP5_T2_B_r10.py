import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------- 可调参数 --------------------
CONFIDENCE = 0.95          # 置信度，可修改为其他值（如0.99）
POSITION = 1_000_000       # 头寸金额
DATA_PATH = 'data/market_snapshot_v1.csv'
OUTPUT_DIR = 'output'
FIGURE_NAME = 'hist_var_95_1d.png'
# -------------------------------------------------

# 1. 读取数据，提取 fund 列日收益率（假设为小数形式，如 0.01 表示 1%）
df = pd.read_csv(DATA_PATH)
returns = df['fund'].dropna()

# 2. 计算历史损益序列（头寸 × 日收益率）
pnl = POSITION * returns

# 3. 计算历史模拟 VaR（左尾分位数对应的损失）
percentile = (1 - CONFIDENCE) * 100
var_pnl = np.percentile(pnl, percentile)          # 损益分位数（负数）
var_loss = -var_pnl                               # 转换为正数损失金额

# 4. 绘制损益直方图并标注 VaR 线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, density=False)
plt.axvline(var_pnl, color='red', linestyle='dashed', linewidth=2,
            label=f'{CONFIDENCE*100:.0f}% 1-Day VaR: ${var_loss:,.0f}')
plt.xlabel('Profit / Loss ($)')
plt.ylabel('Frequency')
plt.title('Historical VaR – 1-Day P&L Distribution')
plt.legend()
plt.grid(True, alpha=0.3)

# 5. 保存图片
os.makedirs(OUTPUT_DIR, exist_ok=True)
figure_path = os.path.join(OUTPUT_DIR, FIGURE_NAME)
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 6. 按要求构建结果字典
result = {
    'hist_var_95_1d': var_loss,
    'figure_path': figure_path
}

# 7. 输出 VaR 数值
print(f"历史模拟法 95% 1 日 VaR (100 万头寸): ${var_loss:,.2f}")
print(f"图片已保存至: {figure_path}")
