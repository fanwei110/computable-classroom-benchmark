import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# 参数设定（置信水平可在此处调整）
# ========================
CONFIDENCE_LEVEL = 0.95          # 置信水平
POSITION = 1_000_000             # 头寸（元）
DATA_FILE = 'data/market_snapshot_v1.csv'
FIGURE_FILE = 'hist_var.png'

# ========================
# 1. 读取数据并构造日损益
# ========================
df = pd.read_csv(DATA_FILE)

if 'fund' not in df.columns:
    raise KeyError("CSV文件中缺少 'fund' 列，请检查数据格式。")

# 提取日收益序列，剔除缺失值
raw_returns = df['fund'].dropna()

# 若收益率以百分比形式存储（如2.5代表2.5%），自动转换为小数
if (raw_returns.abs() > 1).any():
    returns = raw_returns / 100.0
else:
    returns = raw_returns

# 计算日损益（人民币）
pnl = POSITION * returns

# ========================
# 2. 历史模拟法计算 VaR
# ========================
# 计算损益的经验分位数（左侧尾部）
tail_percentile = (1 - CONFIDENCE_LEVEL) * 100
pnl_quantile = np.percentile(pnl, tail_percentile)

# 按照惯例，VaR 表示为损失金额的正数
var_amount = -pnl_quantile

# ========================
# 3. 绘制直方图并标注 VaR
# ========================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.7, color='steelblue', edgecolor='white',
         label='Daily P&L distribution')

# 在损益轴上，VaR 对应的位置是 -var_amount
plt.axvline(-var_amount, color='red', linestyle='--', linewidth=2,
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-day Historical VaR: ¥{var_amount:,.2f}')

plt.xlabel('Daily P&L (RMB)')
plt.ylabel('Frequency')
plt.title('Historical VaR - Daily P&L Distribution')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_FILE, dpi=150)
plt.close()

# ========================
# 4. 输出结果
# ========================
result = {
    'hist_var_95_1d': var_amount,
    'figure_path': FIGURE_FILE
}

print(result)
