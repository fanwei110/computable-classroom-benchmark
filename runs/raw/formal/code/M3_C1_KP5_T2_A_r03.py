import pandas as pd
import matplotlib.pyplot as plt

# ================= 1. 参数设置 =================
# 置信水平（可调参数，如需修改其他置信水平，改此处即可）
confidence_level = 0.95
alpha = 1 - confidence_level

# 头寸规模（100万元）
position = 1000000

# 文件路径
file_path = 'data/market_snapshot_v1.csv'

# ================= 2. 数据处理与计算 =================
# 读取数据
df = pd.read_csv(file_path)

# 提取fund列并计算日收益率
df = df.dropna(subset=['fund'])
returns = df['fund'].pct_change().dropna()

# 计算日损益 (P&L)
pnl = returns * position

# 使用历史模拟法计算VaR：取收益分布的左端分位数
var_cutoff = pnl.quantile(alpha)

# 按照惯例，VaR通常表示为正数（代表可能损失的最大金额）
hist_var_value = abs(var_cutoff)

# 告知VaR的数值
print(f"在 {confidence_level*100:.0f}% 置信水平下，1日历史VaR为: {hist_var_value:.2f} 元")

# ================= 3. 可视化画图 =================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black', color='steelblue')

# 画出95%一日历史VaR的竖线
plt.axvline(x=var_cutoff, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-day VaR: {hist_var_value:.2f} RMB')

plt.title('Daily P&L Histogram & Historical VaR')
plt.xlabel('Daily P&L (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', alpha=0.5)

# 保存图片
figure_path = 'pnl_var_histogram.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 4. 输出契约封装 =================
result = {
    'hist_var_95_1d': hist_var_value,
    'figure_path': figure_path
}
