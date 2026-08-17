import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
WINDOW = 60                # 滚动窗口长度（交易日）
RISK_FREE_RATE = 0.021     # 年化无风险利率（小数）
TRADING_DAYS = 252         # 每年交易日数
# =================================================

def main():
    # 1. 读取数据
    data_path = "data/market_snapshot_v1.csv"
    df = pd.read_csv(data_path)
    
    # 如果存在日期列，则设为索引并转换为时间类型
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
    
    # 提取基金收益率序列（假设列名为 fund），并去除缺失值
    fund_returns = df['fund'].dropna()
    
    # 2. 计算日度无风险利率
    rf_daily = RISK_FREE_RATE / TRADING_DAYS
    
    # 3. 超额收益
    excess_returns = fund_returns - rf_daily
    
    # 4. 滚动年化夏普比率
    rolling_mean = excess_returns.rolling(window=WINDOW).mean()
    rolling_std  = excess_returns.rolling(window=WINDOW).std(ddof=1)   # 样本标准差
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)
    
    # 5. 最后一个窗口的夏普值
    last_valid = rolling_sharpe.dropna().iloc[-1]
    rolling_sharpe_last = float(last_valid)
    
    # 6. 绘制并保存图像
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_sharpe.index, rolling_sharpe.values, color='navy', linewidth=1.2)
    plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
    plt.xlabel('Date' if isinstance(rolling_sharpe.index, pd.DatetimeIndex) else 'Time Step')
    plt.ylabel('Annualized Sharpe Ratio')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    figure_filename = "rolling_sharpe.png"
    plt.savefig(figure_filename, dpi=200)
    plt.close()
    figure_path = os.path.abspath(figure_filename)
    
    # 7. 组装结果字典
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': figure_path
    }
    
    # 课堂展示：打印最终结果
    print("Result dictionary:")
    print(result)
    
    return result

if __name__ == "__main__":
    result = main()
