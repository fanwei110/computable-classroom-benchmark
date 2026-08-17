import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_rolling_sharpe(df, window=60, rf=0.021, trading_days=252):
    """
    计算60日滚动年化夏普比率并绘图
    
    参数:
    df: pandas.DataFrame, 必须包含 'fund' 列（净值或价格序列）
    window: int, 滚动窗口大小，默认为60（可调）
    rf: float, 年化无风险利率，小数表示，默认为0.021
    trading_days: int, 年交易日数，默认为252
    """
    # 1. 计算日收益率
    daily_returns = df['fund'].pct_change()
    
    # 2. 计算日无风险利率（按约定：期权无风险利率按连续复利折算日利率）
    daily_rf = rf / trading_days
    
    # 3. 计算日超额收益率
    daily_excess_returns = daily_returns - daily_rf
    
    # 4. 计算滚动均值和滚动样本标准差 (ddof=1)
    rolling_mean = daily_excess_returns.rolling(window=window).mean()
    rolling_std = daily_excess_returns.rolling(window=window).std(ddof=1)
    
    # 5. 计算滚动年化夏普比率 (年化乘以 sqrt(252))
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(trading_days)
    
    # 6. 提取最后一个窗口的数值
    rolling_sharpe_last = rolling_sharpe.iloc[-1]
    
    # 7. 绘制曲线并保存
    plt.figure(figsize=(10, 6))
    plt.plot(rolling_sharpe.index, rolling_sharpe, label=f'{window}-Day Rolling Annualized Sharpe', color='blue')
    plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf*100}%)')
    plt.xlabel('Date')
    plt.ylabel('Annualized Sharpe Ratio')
    plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    figure_path = 'rolling_sharpe_curve.png'
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. 构建输出契约字典
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': figure_path
    }
    
    return result

# ===== 使用示例 =====
# 假设您的数据已经加载为 df，包含 'fund' 列：
# df = pd.read_csv('your_data.csv', parse_dates=['date'], index_col='date')
# result = calculate_rolling_sharpe(df, window=60, rf=0.021)
# print(result)
