import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main(confidence_level=0.95):
    """
    计算历史在险价值（Historical VaR）并绘图。
    
    参数
    ----
    confidence_level : float
        置信水平，默认为 0.95。
    
    返回
    ----
    result : dict
        keys: 'hist_var_95_1d', 'figure_path'
    """
    # 1. 读取快照 CSV，构造头寸日损益
    df = pd.read_csv('data/market_snapshot_v1.csv')
    # 题目要求“取 fund 列的日收益”，假设该列直接为日收益率（小数形式）
    returns = df['fund'].dropna()          # 去除缺失值，保证数据清洁
    position = 1_000_000                   # 头寸 100 万元
    pnl = position * returns               # 日损益序列

    # 2. 由经验分布计算历史 VaR（损失金额，正数）
    tail_percentile = 100 * (1 - confidence_level)
    var_cutoff = np.percentile(pnl, tail_percentile)   # 损益分布的左尾分位数（负值）
    hist_var = -var_cutoff                              # 转为正数表示损失

    # 3. 画直方图并加带标注的 VaR 线
    plt.figure(figsize=(10, 6))
    plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(x=var_cutoff, color='red', linestyle='--', linewidth=2,
                label=f'{confidence_level*100:.0f}% 1-Day Historical VaR: ¥{hist_var:,.2f}')
    plt.xlabel('Daily P&L (¥)')
    plt.ylabel('Frequency')
    plt.title('Historical VaR')
    plt.legend()
    plt.tight_layout()

    # 4. 保存图形
    figure_path = 'hist_var_plot.png'
    plt.savefig(figure_path, dpi=150)
    plt.close()

    # 构造输出
    result = {
        'hist_var_95_1d': hist_var,
        'figure_path': figure_path
    }
    print(f"Historical VaR (95%, 1-day): ¥{hist_var:,.2f}")
    print(f"Figure saved to: {figure_path}")
    return result

if __name__ == "__main__":
    result = main(confidence_level=0.95)
