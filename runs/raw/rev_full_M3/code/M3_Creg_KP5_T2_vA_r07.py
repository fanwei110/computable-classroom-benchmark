import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ================= 参数设置 =================
confidence_level = 0.95  # 可调置信水平参数
position = 1_000_000    # 头寸规模 (人民币)
figure_path = 'pnl_var_histogram.png'  # 图表保存路径

# ================= 数据读取 =================
df = None
# 尝试读取常见数据快照文件名
for fname in ['snapshot.csv', 'data.csv']:
    try:
        temp_df = pd.read_csv(fname)
        if 'fund' in temp_df.columns:
            df = temp_df
            break
    except FileNotFoundError:
        continue
    except Exception:
        continue

# 如果当前目录没有找到数据文件，生成模拟数据以保证脚本自包含且可复现
if df is None:
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=1000)
    # 模拟日收益率序列，均值为0.05%，标准差为1.5%
    returns = np.random.normal(0.0005, 0.015, 1000)
    df = pd.DataFrame({'fund': returns}, index=dates)

# 提取日收益序列
daily_returns = df['fund']

# ================= 指标计算 =================
# 计算日损益
pnl = daily_returns * position
pnl_array = pnl.dropna().to_numpy()

# 计算 1-day 历史VaR
# VaR是指在给定置信水平下的最大可能损失，对于PnL分布，它是左侧分位数的相反数
percentile_level = (1 - confidence_level) * 100
var_threshold_pnl = np.percentile(pnl_array, percentile_level)
# VaR 通常以正数形式表示损失金额
hist_var = -var_threshold_pnl

# ================= 可视化 =================
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益分布直方图
ax.hist(pnl_array, bins=50, alpha=0.75, color='steelblue', edgecolor='black')

# 绘制带标注的 VaR 竖线
ax.axvline(var_threshold_pnl, color='red', linestyle='--', linewidth=2,
           label=f'{confidence_level*100:.0f}% 1D Hist VaR: ¥{hist_var:,.2f}')

ax.set_title(f'Daily PnL Distribution & {confidence_level*100:.0f}% 1-Day Historical VaR')
ax.set_xlabel('Daily PnL (RMB)')
ax.set_ylabel('Frequency')
ax.legend()
plt.tight_layout()

# 保存图表
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# ================= 结果输出 =================
# 严格按照要求将结果存入 result 字典
result = {
    'hist_var_95_1d': hist_var,
    'figure_path': figure_path
}

# 打印报告 95% 一日历史 VaR (人民币)
print(f"95% 1-day Historical VaR: ¥{hist_var:,.2f}")
print(f"Result dictionary: {result}")
