import pandas as pd
import numpy as np
import scipy, matplotlib  # 按题目要求导入，虽未直接使用

# ========== 用户可配置参数 ==========
DATA_FILE = 'fund_data.csv'   # 快照 CSV 文件名
RF_ANNUAL = 0.021             # 年化无风险利率 2.1%
ANNUAL_FACTOR = 252           # 假设日度数据，一年252个交易日
# ===================================

def load_and_prepare(filepath):
    """读取 CSV，假设包含 date 和 fund(净值) 列，计算日收益率"""
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.sort_values('date', inplace=True)
    df['return'] = df['fund'].pct_change()  # 简单收益率
    df.dropna(inplace=True)
    return df['return']

def annualized_sharpe(daily_returns, rf_annual, periods):
    """计算年化夏普比率"""
    rf_daily = rf_annual / periods                     # 近似日度无风险利率
    excess = daily_returns - rf_daily
    mean_excess = excess.mean()
    std_excess = excess.std(ddof=1)                    # 样本标准差
    sharpe = (mean_excess / std_excess) * np.sqrt(periods)
    return sharpe

def main():
    daily_ret = load_and_prepare(DATA_FILE)
    sharpe = annualized_sharpe(daily_ret, RF_ANNUAL, ANNUAL_FACTOR)
    result = {'sharpe_annual': sharpe}
    return result

if __name__ == '__main__':
    result = main()
    print(result)
