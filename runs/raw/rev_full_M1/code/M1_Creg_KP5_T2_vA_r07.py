import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

def calculate_historical_var():
    # 设置随机种子以确保可复现性
    np.random.seed(42)

    # 模拟生成课程数据快照中的fund列日收益序列（假设有252个交易日数据）
    n_days = 252
    daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益率

    # 头寸金额
    position = 1_000_000  # 1,000,000元

    # 计算日损益
    daily_pnl = position * daily_returns

    # 设置置信水平（可调参数）
    confidence_level = 95  # 95%置信水平

    # 计算历史VaR
    var_1d = np.percentile(daily_pnl, 100 - confidence_level)

    # 创建结果字典
    result = {
        'hist_var_95_1d': -var_1d,  # VaR通常报告为正数（损失金额）
        'figure_path': 'var_histogram.png'
    }

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(x=var_1d, color='red', linestyle='--',
                label=f'{confidence_level}% 1-day Historical VaR: ¥{abs(var_1d):,.2f}')
    plt.title('Daily P&L Distribution with Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图形
    plt.savefig(result['figure_path'])
    plt.close()

    return result

# 执行计算并获取结果
result = calculate_historical_var()

# 输出结果（供验证）
print("Result dictionary:")
print(result)
