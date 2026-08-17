import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 配置参数 ----------------------------------------------------------------
DATA_PATH = "data/market_snapshot_v1.csv"          # 课程数据快照路径
POSITION_VALUE = 1_000_000.0                       # 头寸市值（人民币）
CONFIDENCE = 0.95                                  # VaR 置信水平（可调参数）
FIGURE_FILENAME = "var_histogram.png"              # 输出图形文件名

# 1. 读取数据并构建日损益序列 -----------------------------------------------
# 读取 CSV 文件，仅提取 "fund" 列的日收益率
df = pd.read_csv(DATA_PATH)
# 确保日收益率列存在，并转换为数值类型，丢弃缺失值
daily_returns = pd.to_numeric(df["fund"], errors="coerce").dropna().values

# 计算日损益序列：损益 = 头寸价值 × 日收益率
daily_pnl = POSITION_VALUE * daily_returns

# 2. 计算 95% 历史 VaR ----------------------------------------------------
# 线性插值经验分位数（numpy 默认方法）
alpha = 1.0 - CONFIDENCE                           # 左尾概率
vaR_percentile = np.percentile(daily_pnl, 100.0 * alpha)

# VaR 定义为正损失金额：左尾分位数为负时取绝对值，非负时设为 0
if vaR_percentile < 0:
    var_value = -vaR_percentile
else:
    var_value = 0.0

# 3. 绘制直方图并标出 VaR 线 ------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益直方图
ax.hist(daily_pnl, bins='auto', color='steelblue', edgecolor='white',
        alpha=0.8, label='Daily PnL Distribution')

# 画出 VaR 阈值竖线（位置在损益分位数处）
ax.axvline(x=vaR_percentile, color='red', linestyle='--', linewidth=2,
           label=f'{int(CONFIDENCE*100)}% Historical VaR\n¥ {var_value:,.2f}')

# 图形装饰
ax.set_xlabel('Daily Profit & Loss (RMB)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title(f'Historical VaR at {int(CONFIDENCE*100)}% Confidence Level',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, linestyle=':', alpha=0.6)

# 保存图形
plt.tight_layout()
plt.savefig(FIGURE_FILENAME, dpi=150)
plt.close()   # 释放内存，避免在交互环境中重复显示

# 4. 组装结果字典 ---------------------------------------------------------
result = {
    'hist_var_95_1d': round(var_value, 2),
    'figure_path': os.path.abspath(FIGURE_FILENAME)
}

# 简单打印确认（课堂投屏时也可在控制台看到数值）
if __name__ == "__main__":
    print(f"95% 1-day Historical VaR: ¥ {result['hist_var_95_1d']:,.2f}")
    print(f"Figure saved to: {result['figure_path']}")
