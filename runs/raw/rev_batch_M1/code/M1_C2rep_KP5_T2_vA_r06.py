import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
INITIAL_POSITION = 1_000_000  # 初始头寸100万元
CONFIDENCE_LEVEL = 0.95       # 默认置信水平95%
DATA_PATH = "data/market_snapshot_v1.csv"
FIGURE_PATH = "var_histogram.png"

def calculate_historical_var():
    # 1. 读取数据并构造日损益
    try:
        df = pd.read_csv(DATA_PATH)
        daily_returns = df['fund'].dropna().values
    except FileNotFoundError:
        raise FileNotFoundError(f"数据文件未找到: {DATA_PATH}")
    except KeyError:
        raise KeyError("CSV文件中未找到'fund'列")

    # 计算日损益（头寸 × 日收益率）
    daily_pnl = INITIAL_POSITION * daily_returns

    # 2. 计算历史VaR
    var_percentile = (1 - CONFIDENCE_LEVEL) * 100
    historical_var = np.percentile(daily_pnl, var_percentile)

    # 3. 绘制直方图并标注VaR
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR竖线
    plt.axvline(x=historical_var, color='red', linestyle='--',
                label=f'{CONFIDENCE_LEVEL:.0%} VaR: ¥{historical_var:,.2f}')

    # 图形美化
    plt.title(f'Daily P&L Distribution with {CONFIDENCE_LEVEL:.0%} Historical VaR')
    plt.xlabel('Daily Profit & Loss (RMB)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图形
    plt.savefig(FIGURE_PATH, dpi=300, bbox_inches='tight')
    plt.close()

    # 4. 准备结果
    result = {
        'hist_var_95_1d': round(historical_var, 2),
        'figure_path': str(Path(FIGURE_PATH).absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
