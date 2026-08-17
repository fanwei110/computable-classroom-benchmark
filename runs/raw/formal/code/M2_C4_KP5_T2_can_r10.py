#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《证券投资学》课堂实时编程助手 —— 历史在险价值（VaR）计算与可视化
数据文件：data/market_snapshot_v1.csv
要求：计算 1,000,000 元头寸的 95% 一日历史 VaR，并绘制日损益分布直方图。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------- 1. 参数设置 ----------------------------
POSITION_VALUE = 1_000_000          # 头寸金额（人民币）
CONFIDENCE_LEVEL = 0.95             # 置信水平（可调参数）
ALPHA = 1 - CONFIDENCE_LEVEL        # 损失分位数对应的概率（左侧尾部）
BINS = 50                           # 直方图的柱子数量
FIGURE_FILENAME = 'var_figure.png'  # 输出图形文件名

# ---------------------------- 2. 读取数据并构造日损益 ----------------------------
# 读取课程数据快照，假定 CSV 中有一列名为 'fund'，存储日收益率（小数）
df = pd.read_csv('data/market_snapshot_v1.csv')

# 检查 'fund' 列是否存在
if 'fund' not in df.columns:
    raise KeyError("CSV 文件中未找到 'fund' 列，请检查数据格式。")

# 日损益序列 = 头寸金额 × 日收益率
pnl = POSITION_VALUE * df['fund'].values

# ---------------------------- 3. 计算历史 VaR （线性插值经验分位数）-----------------
# numpy 的 percentile 默认使用线性插值，与题目要求一致
# VaR 定义为正的损失金额：取损益分布的 ALPHA 分位数，取负号即得损失
loss_percentile = np.percentile(pnl, 100 * ALPHA)
hist_var_95_1d = -loss_percentile  # 若分位数为负，VaR为正；若分位数为正，理论上损失为负，但不会出现

# 打印计算结果
print(f"95% 一日历史 VaR (历史模拟法): ￥{hist_var_95_1d:,.2f}")

# ---------------------------- 4. 绘制直方图并标记 VaR ----------------------------
plt.style.use('seaborn-v0_8-whitegrid')  # 好看且课堂投屏清晰的样式
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
ax.hist(pnl, bins=BINS, color='steelblue', edgecolor='white', alpha=0.8, label='日损益分布')

# 标出 VaR 竖线
ax.axvline(x=loss_percentile, color='red', linestyle='--', linewidth=2,
           label=f'{CONFIDENCE_LEVEL*100:.0f}% 历史 VaR = ￥{hist_var_95_1d:,.2f}')

# 在 VaR 线旁添加文本标注（避免遮盖）
y_min, y_max = ax.get_ylim()
ax.text(loss_percentile, y_max * 0.95, f'VaR\n￥{hist_var_95_1d:,.2f}',
        ha='right', va='top', color='red', fontsize=11, fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='red'))

# 标注、标题与轴标签
ax.set_xlabel('日损益（人民币）', fontsize=12)
ax.set_ylabel('频数', fontsize=12)
ax.set_title(f'头寸 {POSITION_VALUE:,.0f} 元的日损益分布\n'
             f'置信水平 {CONFIDENCE_LEVEL*100:.0f}% 的历史 VaR（历史模拟法）',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper left')

# 保存图形
plt.tight_layout()
fig.savefig(FIGURE_FILENAME, dpi=150)
plt.close(fig)

# ---------------------------- 5. 填充结果字典 ----------------------------
result = {
    'hist_var_95_1d': round(hist_var_95_1d, 2),  # 保留两位小数
    'figure_path': os.path.abspath(FIGURE_FILENAME)  # 图片的绝对路径
}

print("\n结果字典：")
print(result)
