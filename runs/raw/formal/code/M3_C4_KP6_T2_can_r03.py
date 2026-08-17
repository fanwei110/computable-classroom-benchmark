import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1. 读取快照 CSV 数据
    file_path = 'data/market_snapshot_v1.csv'
    df = pd.read_csv(file_path)
    
    # 提取日收益率序列
    daily_returns = df['fund']
    
    # 课程参数设定
    rf_annual = 0.021                    # 年化无风险利率 2.1%
    rf_daily = rf_annual / 252           # 日无风险利率（简单除法）
    window = 60                          # 滚动窗口长度，可在此处调整
    
    # 2. 计算日超额收益
    excess_returns = daily_returns - rf_daily
    
    # 计算 60 日滚动均值和滚动标准差（样本估计 ddof=1）
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std(ddof=1)
    
    # 计算滚动年化夏普比率：[均值 / 标准差] * sqrt(252)
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
    
    # 3. 报告最后一个窗口的夏普值
    # dropna() 确保取到有效的完整窗口值
    rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]
    
    # 4. 绘制时间序列图
    plt.figure(figsize=(10, 6))
    plt.plot(rolling_sharpe.dropna(), color='dodgerblue', linewidth=1.5, 
             label=f'{window}-Day Rolling Annualized Sharpe Ratio')
    plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
    plt.xlabel('Time (Days)', fontsize=12)
    plt.ylabel('Sharpe Ratio', fontsize=12)
    plt.axhline(y=0, color='grey', linestyle='--', linewidth=0.8)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # 保存图形
    figure_path = 'rolling_sharpe.png'
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. 封装结果至字典
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': figure_path
    }
    
    return result

if __name__ == '__main__':
    result = main()
    print(result)
