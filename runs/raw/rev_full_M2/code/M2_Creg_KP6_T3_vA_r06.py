import numpy as np
import pandas as pd
import sys

def main():
    # ---------- 参数 ----------
    data_file = "data.csv"          # 默认数据文件，可按需修改
    fund_col = "fund"               # 数据列名
    annual_risk_free = 0.021        # 年化无风险利率（2.1%）
    trading_days = 252              # 年交易日数

    # ---------- 读取数据 ----------
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        print(f"错误：文件 {data_file} 未找到。请检查路径。")
        sys.exit(1)

    if fund_col not in df.columns:
        print(f"错误：文件中缺少 '{fund_col}' 列。可用列：{list(df.columns)}")
        sys.exit(1)

    # 假设 fund 列为每日净值（价格），计算日简单收益率
    prices = df[fund_col].dropna().values
    if len(prices) < 2:
        print("错误：数据点不足，无法计算收益率。")
        sys.exit(1)

    daily_returns = np.diff(prices) / prices[:-1]

    # ---------- 计算年化夏普比率 ----------
    mean_daily_return = np.mean(daily_returns)
    std_daily_return = np.std(daily_returns, ddof=1)  # 样本标准差

    if std_daily_return == 0:
        print("警告：收益率标准差为零，无法计算夏普比率。")
        sharpe_annual = np.nan
    else:
        # 年化收益率与年化波动率
        annual_return = mean_daily_return * trading_days
        annual_volatility = std_daily_return * np.sqrt(trading_days)
        sharpe_annual = (annual_return - annual_risk_free) / annual_volatility

    # ---------- 输出契约 ----------
    result = {
        'sharpe_annual': sharpe_annual
    }

    print(f"年化夏普比率: {sharpe_annual:.4f}")
    return result

if __name__ == "__main__":
    main()
