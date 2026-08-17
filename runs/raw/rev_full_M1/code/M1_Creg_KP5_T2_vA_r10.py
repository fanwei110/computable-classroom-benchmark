import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_historical_var():
    # 设置随机种子以确保可复现性
    np.random.seed(42)

    # 模拟生成课程数据快照中的fund列日收益序列（假设有1000个交易日数据）
    n_days = 1000
    daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益率

    # 头寸金额（1,000,000元）
    position = 1_000_000

    # 计算日损益（头寸 * 日收益率）
    daily_pnl = position * daily_returns

    # 设置置信水平（可调参数）
    confidence_level = 0.95

    # 计算历史VaR（95%置信水平）
    var_95_1d = np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 绘制日损益分布直方图
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')

    # 添加95% VaR竖线标注
    plt.axvline(var_95_1d, color='red', linestyle='dashed', linewidth=2,
                label=f'95% 1-day VaR: ¥{var_95_1d:,.2f}')

    # 添加图例和标签
    plt.title('Daily P&L Distribution with 95% Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图形到文件
    figure_path = 'daily_pnl_var_histogram.png'
    plt.savefig(figure_path)
    plt.close()

    # 将结果存入字典
    result = {
        'hist_var_95_1d': var_95_1d,
        'figure_path': figure_path
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
