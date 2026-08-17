import pandas as pd
import numpy as np

def main():
    # 配置
    file_path = "data/market_snapshot_v1.csv"
    risk_free_annual = 0.021   # 2.1%
    # 假设日频交易数据，年化交易日为252天
    trading_days_per_year = 252
    risk_free_daily = risk_free_annual / trading_days_per_year

    # 读取数据
    df = pd.read_csv(file_path, parse_dates=['date'])
    # 确保按日期排序
    df.sort_values('date', inplace=True)
    
    # 计算日收益率，fund列应为基金净值
    df['fund_return'] = df['fund'].pct_change()
    # 去掉第一个NaN
    returns = df['fund_return'].dropna()
    
    # 超额收益率
    excess_returns = returns - risk_free_daily
    
    # 年化夏普比率
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std()
    
    sharpe_annual = (mean_excess / std_excess) * np.sqrt(trading_days_per_year)
    
    # 保存结果
    result = {
        'sharpe_annual': sharpe_annual
    }
    
    print(f"年化夏普比率: {sharpe_annual:.6f}")
    return result

if __name__ == "__main__":
    result = main()
