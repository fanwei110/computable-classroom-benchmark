import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# 1. 读取数据并构造日损益
print("正在读取数据...")
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund'].values
initial_position = 1000000  # 1,000,000元头寸

# 计算日损益（假设头寸为100万的投资）
daily_pnl = initial_position * fund_returns / 100  # 假设returns已是百分比形式

# 2. 计算历史VaR
def calculate_historical_var(pnl_data, confidence_level=0.95):
    """
    使用历史模拟法计算VaR
    :param pnl_data: 损益数据（负数表示损失）
    :param confidence_level: 置信水平
    :return: VaR值（正数表示损失金额）
    """
    # 历史VaR为损益分布中对应置信水平的分位数（左尾）
    var = np.percentile(pnl_data, (1 - confidence_level) * 100)
    # 返回正数的VaR值（表示损失）
    return -var

# 计算95%置信水平的VaR
confidence_level = 0.95
var_95 = calculate_historical_var(daily_pnl, confidence_level)

# 3. 绘图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(12, 7))

# 绘制直方图
n, bins, patches = ax.hist(daily_pnl, bins=50, color='steelblue', 
                            alpha=0.7, edgecolor='black', linewidth=0.5)

# 计算VaR线对应的位置（负数表示损失）
var_value = -var_95  # 转换为负数用于绘图

# 绘制VaR线
ax.axvline(x=var_value, color='red', linestyle='--', linewidth=2.5, 
           label=f'{int(confidence_level*100)}% 历史VaR = ¥{var_95:,.0f}')

# 添加阴影区域表示损失区域
ax.fill_between([var_value, min(daily_pnl)], min(daily_pnl), 
                color='red', alpha=0.05)

# 添加标签和标题
ax.set_xlabel('日损益（元）', fontsize=12)
ax.set_ylabel('频数', fontsize=12)
ax.set_title(f'头寸日损益分布直方图 (初始投资 ¥{initial_position:,})\n{int(confidence_level*100)}% 历史VaR = ¥{var_95:,.0f}', 
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

# 在VaR线附近添加文本标注
y_max = max(n)  # 获取直方图的最大高度
ax.annotate(f'VaR(95%)=¥{var_95:,.0f}', 
            xy=(var_value, y_max*0.9), 
            xytext=(var_value + (max(daily_pnl) - var_value)*0.3, y_max*0.85),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=11, color='darkred',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.8))

# 保存图形
figure_path = 'var_histogram.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.show()

# 4. 计算和报告统计信息
loss_ratio = np.sum(daily_pnl < -var_95) / len(daily_pnl) * 100
print(f"\n===== 历史VaR分析结果 =====")
print(f"数据样本数: {len(daily_pnl)}")
print(f"初始投资头寸: ¥{initial_position:,}")
print(f"置信水平: {int(confidence_level*100)}%")
print(f"历史VaR (95%): ¥{var_95:,.0f}")
print(f"损失超过VaR的天数: {np.sum(daily_pnl < -var_95)} ({loss_ratio:.1f}%)")
print(f"历史数据验证: {loss_ratio:.1f}%")
print(f"\n图形已保存至: {os.path.abspath(figure_path)}")

# 5. 输出结果到字典
result = {
    'hist_var_95_1d': var_95,
    'figure_path': figure_path
}

# 验证输出
print(f"\n===== 输出验证 =====")
print(f"hist_var_95_1d: ¥{result['hist_var_95_1d']:,.0f}")
print(f"figure_path: {result['figure_path']}")
print(f"\n结果字典:\n{result}")
