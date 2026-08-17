import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------- 参数设置 ----------------------------
DATA_PATH = 'data/market_snapshot_v1.csv'
POSITION = 1_000_000          # 头寸 100 万元
CONF_LEVEL = 0.95             # 置信水平（可调）
OUTPUT_FIG = 'var_histogram.png'
# ----------------------------------------------------------------

# 1. 读取数据
df = pd.read_csv(DATA_PATH)
fund_data = df['fund'].dropna()

# 2. 判断 fund 列是价格还是收益率，并计算日收益率
if fund_data.iloc[0] > 1:    # 假设价格序列
    returns = fund_data.pct_change().dropna()
else:                        # 已经是收益率（小数）
    returns = fund_data.copy()

# 3. 计算每日损益（元）
pnl = POSITION * returns

# 4. 历史法 VaR（正数损失金额）
var_cutoff = (1 - CONF_LEVEL) * 100   # 95% -> 5th percentile
var_loss = -np.percentile(pnl, var_cutoff)
# 如果分位数为正（盈利），VaR 应定义为 0 或负损失？按约定报告正损失，
# 通常此时 VaR 为负损失，但我们保持 abs 逻辑
var_loss = max(var_loss, 0)   # 若分位数对应盈利，VaR 可视为 0

# 5. 构建结果字典
result = {
    'hist_var_95_1d': round(var_loss, 2),
    'figure_path': OUTPUT_FIG
}

# 6. 绘制直方图并保存
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='k', alpha=0.7, label='Daily PnL')
plt.axvline(-var_loss, color='red', linestyle='--', linewidth=2,
            label=f'{CONF_LEVEL*100:.0f}% 1-Day Hist VaR = {var_loss:,.2f}')
plt.xlabel('Daily PnL (CNY)')
plt.ylabel('Frequency')
plt.title('Historical VaR - Daily PnL Distribution')
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_FIG, dpi=150)
plt.close()

print("计算完成，结果字典：")
print(result)
