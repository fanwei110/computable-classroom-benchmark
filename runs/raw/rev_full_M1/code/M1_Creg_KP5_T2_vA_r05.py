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

    # 计算历史VaR（95%分位数）
    var_95_1d = np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 绘制日损益分布直方图
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')

    # 添加95% VaR竖线标注
    plt.axvline(var_95_1d, color='red', linestyle='--', linewidth=2)
    plt.text(var_95_1d * 1.05, plt.ylim()[1] * 0.9,
             f'95% 1-day VaR: ¥{abs(var_95_1d):,.2f}',
             color='red', ha='left', va='top')

    # 图表美化
    plt.title('Daily P&L Distribution with 95% Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Density')
    plt.grid(True, alpha=0.3)

    # 保存图表
    figure_path = 'daily_pnl_histogram_with_var.png'
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()

    # 准备结果字典
    result = {
        'hist_var_95_1d': abs(var_95_1d),  # 以正数表示损失金额
        'figure_path': figure_path
    }

    return result

# 执行计算并获取结果
result = calculate_historical_var()

# 输出结果（供验证）
print("Result dictionary:")
print(result)
