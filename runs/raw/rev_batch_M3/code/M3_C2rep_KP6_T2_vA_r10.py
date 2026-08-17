import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # ==================== 1. 读取快照 CSV；计入无风险利率 ====================
    df = pd.read_csv('data/market_snapshot_v1.csv')
    
    # 提取 'fund' 列的日收益
    returns = df['fund']
    
    # 尝试识别日期列以作为时间轴，若无则使用默认索引
    if 'date' in df.columns:
        time_axis = pd.to_datetime(df['date'])
    elif 'Date' in df.columns:
        time_axis = pd.to_datetime(df['Date'])
    else:
        time_axis = df.index

    # ==================== 2. 计算 60 日滚动年化夏普，窗口可调 ====================
    window = 60  # 滚动窗口长度，设为变量以便调整
    trading_days = 252  # 假设一年有252个交易日
    rf_annual = 0.021   # 年化无风险利率 2.1%
    rf_daily = rf_annual / trading_days  # 日化无风险利率（简单平均假设）

    # 计算滚动均值与滚动标准差
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()

    # 计算滚动日度夏普比率
    rolling_sharpe_daily = (rolling_mean - rf_daily) / rolling_std

    # 年化滚动夏普比率
    rolling_sharpe_annualized = rolling_sharpe_daily * np.sqrt(trading_days)

    # ==================== 3. 报告最后一个窗口的值；画出时间序列 ====================
    # 提取最后一个完整窗口的夏普比率
    rolling_sharpe_last = float(rolling_sharpe_annualized.iloc[-1])

    # 画图设置与绘制
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(time_axis, rolling_sharpe_annualized, 
            label=f'{window}-Day Rolling Annualized Sharpe Ratio', 
            color='tab:blue', linewidth=1.2)
    
    # 添加零轴参考线
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    
    ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio (Fund)', fontsize=14)
    ax.set_xlabel('Date / Index', fontsize=12)
    ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)

    # ==================== 4. 保存图形并填充 result ====================
    figure_path = 'rolling_sharpe_ratio.png'
    fig.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 按照输出契约构建字典
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': figure_path
    }
    
    # 控制台打印结果以供课堂展示
    print(f"最后一个{window}日窗口的年化夏普比率为: {rolling_sharpe_last:.4f}")
    print(f"图形已保存至: {figure_path}")

    return result

if __name__ == '__main__':
    result = main()
