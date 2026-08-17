import pandas as pd
import numpy as np

# ==================== 配置 ====================
DATA_PATH = "data.csv"       # 课程数据文件路径，可按实际情况修改
RF_ANNUAL = 0.021            # 年化无风险利率 2.1%
TRADING_DAYS = 252           # 年交易日数，用于年化
# =============================================

def load_returns(data_path: str, price_col: str = "fund") -> pd.Series:
    """
    读取数据文件并计算日收益率。
    假设文件第一列为日期，price_col 列为净值/价格。
    """
    # 读取数据，自动解析日期并将第一列作为索引
    df = pd.read_csv(data_path, parse_dates=True, index_col=0)
    
    if price_col not in df.columns:
        raise KeyError(f"数据中缺少 '{price_col}' 列，实际列为：{list(df.columns)}")
    
    # 计算日简单收益率并剔除缺失值
    returns = df[price_col].pct_change().dropna()
    if returns.empty:
        raise ValueError("无法计算收益率，请检查数据是否包含足够的净值数据。")
    return returns

def annual_sharpe(returns: pd.Series, rf_annual: float, trading_days: int = 252) -> float:
    """
    给定日收益率序列，计算年化夏普比率。
    使用单利方式将年化无风险利率转为日化。
    """
    rf_daily = rf_annual / trading_days                # 日无风险利率
    excess = returns - rf_daily                       # 日超额收益
    mean_excess_daily = excess.mean()                 # 日平均超额收益
    std_daily = returns.std(ddof=1)                   # 日收益率标准差（样本标准差）
    if std_daily == 0:
        return np.nan
    sharpe_daily = mean_excess_daily / std_daily      # 日夏普比率
    return np.sqrt(trading_days) * sharpe_daily       # 年化

def main():
    # 加载收益率
    returns = load_returns(DATA_PATH, price_col="fund")
    
    # 计算年化夏普比率
    sharpe_val = annual_sharpe(returns, RF_ANNUAL, TRADING_DAYS)
    
    # 严格按契约输出
    result = {"sharpe_annual": sharpe_val}
    print(result)
    return result

if __name__ == "__main__":
    main()
