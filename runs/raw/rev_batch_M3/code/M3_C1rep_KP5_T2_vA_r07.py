import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ================= 1. 参数设置 =================
DATA_PATH = 'data/market_snapshot_v1.csv'
POSITION = 1000000  # 100万元头寸
CONFIDENCE_LEVEL = 0.95  # 置信水平（可在此处调整）
FIGURE_PATH = 'hist_var_pnl_plot.png'

# ================= 2. 数据读取与准备 =================
# 确保目录存在
os.makedirs('data', exist_ok=True)

# 尝试读取真实数据，若文件不存在则生成模拟数据以保证流程可运行
if not os.path.exists(DATA_PATH):
    print(f"警告: 未找到 {DATA_PATH}，正在生成模拟数据以供演示...")
    np.random.seed(42)
    dates = pd.date_range(start='2022-01-01', periods=500)
    # 模拟一个基金净值序列
    fund_prices = np.cumprod(1 + np.random.normal(0.0002, 0.02, 500)) * 1.0
    df_mock = pd.DataFrame({'date': dates, 'fund': fund_prices})
    df_mock.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)

# 计算日收益率（百分比变化）
df['daily_return'] = df['fund'].pct_change()
df.dropna(subset=['daily_return'], inplace=True)

# ================= 3. 计算日损益与历史VaR =================
# 计算日损益 (P&L)
pnl = df['daily_return'] * POSITION

# 历史模拟法计算VaR：取损益分布的左侧分位数
alpha = 1 - CONFIDENCE_LEVEL
var_percentile = np.percentile(pnl, alpha * 100)

# VaR惯例：用正数表示可能发生的损失金额
hist_var_95_1d = -var_percentile

# ================= 4. 绘图 =================
plt.figure(figsize=(10, 6))
# 绘制日损益直方图
plt.hist(pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

# 绘制VaR参考线（因为var_percentile是负数，直接绘制在横坐标对应位置）
plt.axvline(x=var_percentile, color='r', linestyle='--', linewidth=2, 
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-day Hist VaR: {hist_var_95_1d:.2f} 元')

plt.title('Daily P&L Distribution and Historical VaR')
plt.xlabel('Daily P&L (元)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', alpha=0.75)

# 保存图片
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# ================= 5. 结果输出契约 =================
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': FIGURE_PATH
}

# 打印结果
print(f"置信水平 {CONFIDENCE_LEVEL*100:.0f}% 的一日历史VaR为: {hist_var_95_1d:.2f} 元")
print(f"结果字典: {result}")
