import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy  # 仅导入以满足允许库要求，实际操作中未必需

# ---------- 可调参数 ----------
CONFIDENCE_LEVEL = 0.95        # 置信水平，可改为 0.99 等
POSITION = 1_000_000           # 头寸，1,000,000 元人民币

# ---------- 1. 获取日收益率序列 ----------
try:
    # 读取课程数据快照中的 "fund" 列
    data = pd.read_csv('fund_data.csv')
    returns = data['fund']
    print("已成功读取外部数据文件。")
except FileNotFoundError:
    print("未找到 'fund_data.csv'，使用可复现的模拟数据。")
    rng = np.random.default_rng(42)          # 固定种子，保证可复现
    n_days = 1000
    # 模拟日收益率：均值 0.05%，标准差 2%
    returns = pd.Series(rng.normal(loc=0.0005, scale=0.02, size=n_days))

# ---------- 2. 计算每日损益及历史 VaR ----------
daily_pnl = returns * POSITION          # 每日损益 （元）

alpha = 1 - CONFIDENCE_LEVEL           # 左尾概率
var_threshold = np.quantile(daily_pnl, alpha)  # 损益分位数（负值代表损失）
var_amount = -var_threshold             # VaR 值，以正的人民币损失报告

# ---------- 3. 绘制直方图并标注 VaR ----------
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(daily_pnl, bins=50, color='skyblue', edgecolor='black',
        alpha=0.7, label='日损益频数')

# 竖线标出 VaR 阈值
ax.axvline(var_threshold, color='red', linestyle='--', linewidth=2,
           label=f'{int(CONFIDENCE_LEVEL*100)}% 1-Day VaR: ¥{var_amount:,.2f}')

# 在上方添加文字标注
ylim = ax.get_ylim()
xrange = daily_pnl.max() - daily_pnl.min()
ax.text(var_threshold + xrange * 0.02, ylim[1] * 0.92,
        f'VaR = ¥{var_amount:,.2f}', color='red', fontweight='bold',
        fontsize=12)

ax.set_xlabel('日损益 (人民币元)')
ax.set_ylabel('频数')
ax.set_title(f'每日损益分布（{int(CONFIDENCE_LEVEL*100)}% 置信水平）')
ax.legend()

# 保存图像
figure_path = 'var_histogram.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- 4. 构建结果字典 ----------
result = {
    'hist_var_95_1d': var_amount,   # 95% 一日历史 VaR（人民币）
    'figure_path': figure_path
}

print(result)
