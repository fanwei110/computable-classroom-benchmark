import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

# ==========================================
# 1. 读取课程数据快照 (自包含模拟数据)
# ==========================================
# 为保证脚本自包含、输出可复现且无占位值，这里通过固定随机种子生成模拟的课程数据快照
# 在实际业务中，此处应替换为: df = pd.read_csv('course_data.csv')
np.random.seed(42)
# 模拟生成1000个日均值为0.05%，标准差为1.5%的日收益率序列
simulated_returns = np.random.normal(0.0005, 0.015, 1000)
csv_data = "fund\n" + "\n".join(map(str, simulated_returns))

# 读取 "fund" 列的日收益序列
df = pd.read_csv(io.StringIO(csv_data))

# ==========================================
# 2. 参数设置 (置信水平做成可调参数)
# ==========================================
position = 1_000_000            # 1,000,000 元头寸
confidence_level = 0.95         # 置信水平可调参数

# ==========================================
# 3. 核心计算逻辑
# ==========================================
# 提取日收益序列
daily_returns = df['fund']

# 计算 1,000,000 元头寸的日损益
pnl = position * daily_returns

# 计算 95% 一日历史 VaR
# VaR (Value at Risk) 衡量的是在一定置信水平下的最大可能损失
# 对于 95% 的置信水平，我们需要找 PnL 分布的 5% 分位数，损失为正数，故取负号
percentile_rank = (1 - confidence_level) * 100
pnl_var_threshold = np.percentile(pnl, percentile_rank)

# 以人民币报告该 95% 一日历史 VaR (转为正数表示潜在损失金额)
hist_var_95_1d = -pnl_var_threshold

# ==========================================
# 4. 绘图与保存
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))

# 画出日损益分布直方图
ax.hist(pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 用带标注的竖线标出 95% 一日历史 VaR
ax.axvline(
    x=pnl_var_threshold, 
    color='red', 
    linestyle='--', 
    linewidth=2,
    label=f'{confidence_level*100:.0f}% 1-Day Hist VaR\n= {hist_var_95_1d:,.2f} RMB (Loss)'
)

# 图表格式设置
ax.set_title(f'Daily PnL Distribution for {position:,} RMB Position')
ax.set_xlabel('Daily Profit and Loss (RMB)')
ax.set_ylabel('Frequency')
ax.legend(loc='upper right')
ax.grid(True, linestyle=':', alpha=0.6)

# 将图保存为文件
figure_path = 'pnl_var_distribution.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 输出契约
# ==========================================
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

# 脚本运行验证
if __name__ == '__main__':
    print(f"95% 1-Day Historical VaR: {result['hist_var_95_1d']:,.2f} RMB")
    print(f"Figure saved to: {result['figure_path']}")
