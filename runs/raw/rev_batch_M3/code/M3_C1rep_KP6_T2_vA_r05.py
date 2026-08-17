import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ================= 1. 模拟数据 (如果你的环境已有df，请替换此部分) =================
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', end='2024-01-01', freq='D')
# 模拟一个基金净值序列
fund_prices = np.cumprod(1 + np.random.normal(0.0005, 0.012, len(dates))) 
df = pd.DataFrame({'date': dates, 'fund': fund_prices})
# =================================================================================

def calculate_rolling_sharpe(df, window=60, rf=0.021):
    """
    计算滚动年化夏普比率
    :param df: 包含基金数据的DataFrame，需含有'fund'列
    :param window: 滚动窗口大小，默认60
    :param rf: 年化无风险利率，默认2.1%
    :return: result字典
    """
    # 计算日度收益率
    df['daily_return'] = df['fund'].pct_change()
    
    # 将年化无风险利率转换为日度无风险利率
    rf_daily = rf / 252
    
    # 计算滚动日度平均收益率与滚动日度标准差
    rolling_mean = df['daily_return'].rolling(window=window).mean()
    rolling_std = df['daily_return'].rolling(window=window).std()
    
    # 计算滚动年化夏普比率：(日均收益 - 日无风险) / 日标准差 * sqrt(252)
    df['rolling_sharpe'] = (rolling_mean - rf_daily) / rolling_std * np.sqrt(252)
    
    # 获取最后一个有效窗口的数值（去除因窗口期产生的NaN）
    last_valid_sharpe = df['rolling_sharpe'].dropna().iloc[-1]
    
    # 绘制曲线
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['rolling_sharpe'], label=f'{window}-Day Rolling Annualized Sharpe (rf={rf*100}%)', color='blue')
    plt.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.8)
    plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio')
    plt.xlabel('Date')
    plt.ylabel('Sharpe Ratio')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 保存图片
    fig_path = 'rolling_sharpe_curve.png'
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 构建输出契约字典
    result = {
        'rolling_sharpe_last': last_valid_sharpe,
        'figure_path': os.path.abspath(fig_path)
    }
    
    return result

# 执行计算（窗口可调，此处按要求设为60）
result = calculate_rolling_sharpe(df, window=60, rf=0.021)

# 打印结果验证
print(result)
