import pandas as pd
import numpy as np

# ===================== 配置 =====================
DATA_FILE = 'course_data.csv'   # 课程数据文件路径（可按需修改）
RISK_FREE_RATE = 0.021          # 年化无风险利率 2.1%
TRADING_DAYS = 252              # 一年交易日数，用于年化
# =================================================

def annualized_sharpe(series: pd.Series, rf: float, periods: int = 252) -> float:
    """
    计算给定收益率序列的年化夏普比率。
    参数:
        series: 资产净值序列（非收益率）
        rf: 年化无风险利率
        periods: 年化倍数（默认每年252个交易日）
    返回:
        年化夏普比率
    """
    # 计算日简单收益率
    daily_returns = series.pct_change().dropna()
    
    # 年化平均收益率与年化波动率
    mean_ret = daily_returns.mean() * periods
    vol = daily_returns.std() * np.sqrt(periods)
    
    # 年化夏普比率 = (年化收益率 - 无风险利率) / 年化波动率
    sharpe = (mean_ret - rf) / vol
    return sharpe

def main():
    # 读取数据，假设文件中包含 'fund' 列
    df = pd.read_csv(DATA_FILE)
    
    if 'fund' not in df.columns:
        raise ValueError(f"数据文件 {DATA_FILE} 中未找到 'fund' 列，请检查列名。")
    
    # 计算夏普比率
    sharpe_val = annualized_sharpe(df['fund'], RISK_FREE_RATE, TRADING_DAYS)
    
    # 按要求存入字典
    result = {'sharpe_annual': sharpe_val}
    
    # 输出结果（可选，便于查看）
    print(f"年化夏普比率: {sharpe_val:.6f}")
    return result

if __name__ == '__main__':
    result = main()
