import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

# ==========================================
# 参数与假设设置
# ==========================================
# 假设备注：
# 1. 关于 "fund" 列数据性质：若原序列包含负数，视为已是日收益率序列；若全为正数，视为基金净值(NAV)序列，需计算日收益率。
# 2. 历史 VaR 为经验分位数。95%置信水平对应损益分布的 5% 分位数（左尾）。报告时取绝对值代表可能的最大损失额。
# 3. 置信水平设为可调参数，当前为 0.95。

POSITION = 1_000_000          # 头寸（人民币元）
CONFIDENCE_LEVEL = 0.95       # 可调置信水平
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'hist_var_pnl_distribution.png'

# ==========================================
# 1. 读取数据并构造日损益
# ==========================================
df = pd.read_csv(DATA_PATH)

# 自适应处理 'fund' 列：判断是净值序列还是收益率序列
if (df['fund'] <= 0).any():
    # 包含非正值，通常代表已经是日收益率序列
    daily_returns = df['fund']
else:
    # 皆为正值，极大概率是基金净值(NAV)序列，需计算百分比变化
    daily_returns = df['fund'].pct_change().dropna()

# 构造头寸的日损益 (PnL)，单位：人民币
pnl = POSITION * daily_returns

# ==========================================
# 2. 计算历史 VaR (人民币)
# ==========================================
# 置信水平 alpha 下的 VaR 对应损益分布的 (1 - alpha) 分位数
percentile_level = 100 * (1 - CONFIDENCE_LEVEL)
var_critical_pnl = np.percentile(pnl, percentile_level)

# 按金融惯例，VaR 报告为正数（代表损失的风险敞口）
hist_var_95_1d = abs(var_critical_pnl)

# ==========================================
# 3. 画直方图并加带标注的 VaR 线
# ==========================================
# 设置中文字体支持，确保投屏不出现方块字
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

plt.figure(figsize=(10, 6))

# 绘制直方图
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.75)

# 绘制 VaR 竖线 (在 PnL 的实际临界值处画线，通常为负值)
plt.axvline(var_critical_pnl, color='red', linestyle='--', linewidth=2,
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 历史 VaR = {hist_var_95_1d:,.2f} 元')

# 添加标注与排版
plt.title(f'日损益分布直方图与 {CONFIDENCE_LEVEL*100:.0f}% 一日历史 VaR', fontsize=14)
plt.xlabel('日损益 (人民币)', fontsize=12)
plt.ylabel('频数', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# 构造输出契约字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': FIGURE_PATH
}

# 为课堂投屏演示方便，打印输出结果（可选）
if __name__ == '__main__':
    print(f"计算完成：{CONFIDENCE_LEVEL*100:.0f}% 一日历史 VaR 为 {result['hist_var_95_1d']:,.2f} 元")
    print(f"图形已保存至: {result['figure_path']}")
