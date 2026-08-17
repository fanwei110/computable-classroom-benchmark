import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================
# 可调参数
# ============================
CONFIDENCE = 0.95            # 置信水平（95%）
POSITION = 1_000_000         # 头寸金额（人民币）
DATA_PATH = 'data/market_snapshot_v1.csv'

# ============================
# 1. 读取数据并计算日损益
# ============================
df = pd.read_csv(DATA_PATH)

if 'fund' not in df.columns:
    raise ValueError("CSV 文件中缺少 'fund' 列，请检查数据。")

# 假设 'fund' 列存储日收益率（小数形式，例如 0.01 表示 1%）
returns = df['fund'].dropna().values
pnl = POSITION * returns   # 每日头寸损益（元）

# ============================
# 2. 计算历史 VaR
# ============================
# 损益分布的左尾分位数（对应 1 - 置信水平）
var_threshold = np.percentile(pnl, 100 * (1 - CONFIDENCE))
hist_var_95_1d = -var_threshold   # VaR 报告为正的损失金额

# ============================
# 3. 绘制直方图并标出 VaR
# ============================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7,
         label='Daily P&L distribution')
plt.axvline(var_threshold, color='red', linestyle='--', linewidth=2,
            label=f'{CONFIDENCE*100:.0f}% Historical VaR: {hist_var_95_1d:,.2f} CNY')

# 标注
plt.xlabel('Daily Profit & Loss (CNY)')
plt.ylabel('Frequency')
plt.title(f'Daily P&L Distribution with {CONFIDENCE*100:.0f}% Historical VaR')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = 'var_histogram.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ============================
# 4. 构造输出字典
# ============================
result = {
    'hist_var_95_1d': hist_var_95_1d,          # 95% 一日历史 VaR（人民币）
    'figure_path': os.path.abspath(figure_path) # 图片的绝对路径
}

# 打印结果，便于教师投屏展示
print("=== 计算结果 ===")
print(f"95% 一日历史 VaR : {hist_var_95_1d:,.2f} CNY")
print(f"图形保存路径     : {result['figure_path']}")
