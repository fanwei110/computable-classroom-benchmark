import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- 1. 读取数据，构造日损益 --------------------
df = pd.read_csv('data/market_snapshot_v1.csv')
# 假设 fund 列直接为日收益率（小数形式，如 0.01 代表 1%）
returns = df['fund'].dropna()
position = 1_000_000  # 头寸 100 万元
pnl = position * returns  # 每日损益（元）

# -------------------- 2. 计算历史 VaR（可调置信水平） --------------------
confidence = 0.95                     # 置信水平，可调参数
alpha = 1 - confidence                # 左尾概率
quantile = np.percentile(pnl, alpha * 100)  # 经验分位数（通常为负值）
var_95 = -quantile                    # VaR 定义为损失的绝对值，正数

# -------------------- 3. 绘制直方图并标注 VaR 线 --------------------
plt.figure(figsize=(8, 5))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
plt.axvline(quantile, color='red', linestyle='dashed', linewidth=2,
            label=f'VaR {confidence*100:.0f}%: {var_95:,.2f} CNY')
plt.xlabel('Daily PnL (CNY)')
plt.ylabel('Frequency')
plt.title('Histogram of Daily PnL with Historical VaR')
plt.legend()
plt.tight_layout()

# -------------------- 4. 保存图形，填充结果 --------------------
figure_path = 'var_histogram.png'
plt.savefig(figure_path, dpi=150)
plt.close()

result = {
    'hist_var_95_1d': var_95,
    'figure_path': figure_path
}

# 输出结果供查验
print(f"95% 1-day Historical VaR: {var_95:,.2f} CNY")
print(f"Figure saved to: {figure_path}")
