import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并构造日损益
def calculate_var():
    # 读取CSV文件
    data_path = Path('data/market_snapshot_v1.csv')
    df = pd.read_csv(data_path)

    # 提取fund列的日收益率
    daily_returns = df['fund'].dropna().values

    # 计算1,000,000元头寸的日损益（人民币）
    position = 1_000_000
    daily_pnl = position * daily_returns

    # 2. 计算95%历史VaR（线性插值经验分位数）
    confidence_level = 0.95
    var_quantile = 1 - confidence_level
    historical_var = np.quantile(daily_pnl, var_quantile, method='linear')

    # VaR报告为正的损失金额
    var_loss = -historical_var

    # 3. 绘制直方图并标注VaR线
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.7, color='skyblue', edgecolor='black')

    # 添加VaR竖线
    plt.axvline(x=historical_var, color='red', linestyle='--', linewidth=2)
    plt.text(historical_var, plt.ylim()[1]*0.9,
             f'95% 1-day VaR: ¥{var_loss:,.2f}',
             color='red', ha='right', va='top')

    plt.title('Daily P&L Distribution with 95% Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)

    # 保存图形
    figure_path = 'var_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # 4. 填充result字典
    result = {
        'hist_var_95_1d': var_loss,
        'figure_path': figure_path
    }

    return result

# 执行计算并输出结果
result = calculate_var()
print(result)
