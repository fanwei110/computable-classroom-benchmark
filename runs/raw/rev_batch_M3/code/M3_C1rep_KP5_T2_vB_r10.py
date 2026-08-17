import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 参数设置 ---
POSITION = 1000000             # 头寸100万
CONFIDENCE_LEVEL = 0.95        # 置信度可调（例如调为0.99即为99%VaR）
FILE_PATH = 'data/market_snapshot_v1.csv'
FIG_SAVE_PATH = 'pnl_var_histogram.png'

# --- 1. 读取数据 ---
df = pd.read_csv(FILE_PATH)

# --- 2. 计算日收益率与损益 ---
# 假设fund列为基金净值/价格，计算其日收益率；若fund列本身已是日收益率，则可直接使用 df['fund']
daily_returns = df['fund'].pct_change().dropna()
pnl = daily_returns * POSITION

# --- 3. 历史法计算VaR ---
# 历史法VaR即取损益序列在(1 - 置信度)分位数的值
var_percentile = 1 - CONFIDENCE_LEVEL
var_value = pnl.quantile(var_percentile)

# VaR通常以正数报告潜在的最大损失金额
hist_var_95_1d = abs(var_value)

# --- 4. 绘制损益直方图并标出VaR线 ---
# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black', color='steelblue')

# 画VaR标根线（使用var_value原值，在直方图x轴左侧负域显示）
plt.axvline(x=var_value, color='red', linestyle='--', linewidth=2, 
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-day VaR: {hist_var_95_1d:.2f} 元')

plt.title('损益(PnL)直方图及历史法VaR')
plt.xlabel('损益金额 (元)')
plt.ylabel('频数')
plt.legend()

# 保存图片
plt.savefig(FIG_SAVE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# --- 5. 按照输出契约封装结果 ---
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': FIG_SAVE_PATH
}

# 打印报告VaR数值
print(f"【报告】头寸: {POSITION}元, 置信度: {CONFIDENCE_LEVEL*100:.0f}%")
print(f"【报告】历史法一日VaR值为: {hist_var_95_1d:.2f} 元")
