import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def calculate_historical_var(confidence_level=0.95):
    # 读取数据
    df = pd.read_csv('data/market_snapshot_v1.csv')

    # 计算日收益率
    df['daily_return'] = df['fund'].pct_change()

    # 去除空值
    returns = df['daily_return'].dropna()

    # 计算历史VaR
    position = 1_000_000  # 头寸100万元
    var = np.percentile(returns, 100 * (1 - confidence_level)) * position

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.hist(returns * position, bins=50, alpha=0.75, color='blue', edgecolor='black')

    # 添加VaR线
    plt.axvline(x=var, color='red', linestyle='--', linewidth=2, label=f'{confidence_level*100:.0f}% 1日历史VaR: {var:,.2f}元')

    plt.title('日损益分布与历史VaR')
    plt.xlabel('日损益(元)')
    plt.ylabel('频率')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图片
    if not os.path.exists('output'):
        os.makedirs('output')
    figure_path = 'output/historical_var_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # 准备结果
    result = {
        'hist_var_95_1d': var,
        'figure_path': figure_path
    }

    return result

# 计算95%置信水平的VaR
result = calculate_historical_var(confidence_level=0.95)

# 输出结果
print("95% 1日历史VaR:", result['hist_var_95_1d'])
print("图片保存路径:", result['figure_path'])
