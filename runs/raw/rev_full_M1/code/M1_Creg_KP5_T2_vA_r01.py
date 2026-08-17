import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

def calculate_historical_var():
    # 设置随机种子以确保可复现性
    np.random.seed(42)

    # 模拟生成课程数据快照中的fund日收益序列（假设有1000个交易日数据）
    num_days = 1000
    daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=num_days)  # 模拟日收益率

    # 初始头寸（人民币）
    initial_position = 1_000_000

    # 计算日损益（人民币）
    daily_pnl = initial_position * daily_returns

    # 设置置信水平（可调参数）
    confidence_level = 95

    # 计算历史VaR（95%置信水平下的一日VaR）
    var_95_1d = np.percentile(daily_pnl, 100 - confidence_level)

    # 创建直方图
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(daily_pnl, bins=50, density=False, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR竖线标注
    plt.axvline(var_95_1d, color='red', linestyle='dashed', linewidth=2)
    plt.text(var_95_1d * 1.05, max(n) * 0.9,
             f'95% 1-day VaR: ¥{abs(var_95_1d):,.2f}',
             color='red', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    # 图表美化
    plt.title('Daily P&L Distribution with 95% 1-day Historical VaR', fontsize=14)
    plt.xlabel('Daily P&L (RMB)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, alpha=0.3)

    # 保存图表
    figure_path = 'daily_pnl_histogram_with_var.png'
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()

    # 准备结果字典
    result = {
        'hist_var_95_1d': abs(var_95_1d),  # 以正数形式报告VaR
        'figure_path': figure_path
    }

    return result

# 执行计算并获取结果
result = calculate_historical_var()

# 输出结果（供验证）
print("Result dictionary:")
print(result)
