import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- 参数设置 ----------
INVESTMENT = 1_000_000          # 头寸金额（人民币）
CONF_LEVEL = 0.95               # 置信水平，可调参数
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'hist_var_figure.png'

# ---------- 1. 读取数据并构造日损益 ----------
# 读取CSV，提取基金日收益序列
df = pd.read_csv(DATA_PATH)
returns_raw = df['fund'].dropna()   # 删除缺失值

# 判断收益率是否为百分比形式（若数值绝对值普遍大于1，大概率是百分比，需转为小数）
if (returns_raw.abs() > 1).any():
    returns = returns_raw / 100.0
    print("检测到百分比形式的收益率，已自动除以100转换为小数。")
else:
    returns = returns_raw
    print("收益率假定为小数形式。")

# 计算头寸每日损益
pnl = INVESTMENT * returns.values   # 一维numpy数组

# ---------- 2. 计算95%历史VaR ----------
var_cutoff = (1 - CONF_LEVEL) * 100  # 分位点，例如5
var_pnl = np.percentile(pnl, var_cutoff)  # 损益分布的低分位数（通常为负值）
hist_var = -var_pnl  # VaR定义为损失的正值

# 存入结果
result = {
    'hist_var_95_1d': hist_var,
    'figure_path': FIGURE_PATH
}

print(f"头寸金额: ¥{INVESTMENT:,.0f}")
print(f"置信水平: {CONF_LEVEL*100:.0f}%")
print(f"95% 一日历史VaR (人民币): ¥{hist_var:,.2f}")

# ---------- 3. 绘制直方图与VaR线 ----------
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(pnl, bins=50, alpha=0.7, color='steelblue',
                            edgecolor='white', label='日损益分布')

# 标记VaR竖线
plt.axvline(x=var_pnl, color='red', linestyle='--', linewidth=2,
            label=f'{int(CONF_LEVEL*100)}% 历史VaR: ¥{hist_var:,.0f}')

# 添加文本标注（定位在直方图上方合适位置，避免遮盖）
ymax = plt.ylim()[1]
plt.text(var_pnl, ymax * 0.92,
         f'VaR (95%)\n¥{hist_var:,.0f}',
         horizontalalignment='center',
         verticalalignment='top',
         color='red', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

# 图表装饰
plt.title('日损益分布与历史在险价值 (VaR)', fontsize=14, fontweight='bold')
plt.xlabel('日损益 (人民币)', fontsize=12)
plt.ylabel('频数', fontsize=12)
plt.legend(loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.6)

# 保存图形（自动创建目录，若不存在）
os.makedirs(os.path.dirname(FIGURE_PATH) if os.path.dirname(FIGURE_PATH) else '.', exist_ok=True)
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150)
print(f"图形已保存至: {FIGURE_PATH}")

# 如需在课堂展示，可以保留 plt.show() 注释掉，因为教师会自行运行
# plt.show()
