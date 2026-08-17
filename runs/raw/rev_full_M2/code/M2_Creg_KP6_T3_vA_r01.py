import pandas as pd
import numpy as np

def load_returns(filepath='data.csv'):
    """
    读取数据文件，返回 fund 列对应的收益率序列和年化周期数。
    假设文件为 CSV 格式，包含 'fund' 列；若存在日期列（date/Date/DATE），
    则按日期排序并推断数据频率。
    """
    df = pd.read_csv(filepath)

    # 识别日期列
    date_col = None
    for col in ['date', 'Date', 'DATE']:
        if col in df.columns:
            date_col = col
            break

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col).sort_index()

    fund = df['fund']

    # 判断 fund 列是价格还是收益率：若大多数值 > 1，视为价格，计算简单收益率
    if fund.dropna().median() > 1:
        ret = fund.pct_change().dropna()
    else:
        ret = fund.dropna().copy()

    # 推断数据频率（年化周期数）
    if isinstance(ret.index, pd.DatetimeIndex):
        # 计算相邻时间戳的中位数间隔
        delta = pd.Series(ret.index).diff().median()
        days = delta.days
        if days >= 365:
            periods_per_year = 1
        elif 28 <= days <= 31:
            periods_per_year = 12
        elif 5 <= days <= 7:
            periods_per_year = 52
        elif days == 1:
            periods_per_year = 252  # 交易日
        else:
            # 其他情况按实际天数折算
            periods_per_year = 365 / days
    else:
        raise ValueError("缺少日期列，无法自动推断数据频率，请提供包含日期列的数据文件。")

    return ret, periods_per_year


def main():
    # 加载数据
    returns, periods = load_returns('data.csv')

    # 年化无风险利率
    rf_annual = 0.021
    # 单期无风险利率（简单年化折算）
    rf_period = rf_annual / periods

    # 超额收益率
    excess = returns - rf_period

    # 年化夏普比率 = (超额收益均值 / 超额收益标准差) * sqrt(年化周期数)
    sharpe_annual = excess.mean() / excess.std() * np.sqrt(periods)

    # 按要求存入字典
    result = {'sharpe_annual': sharpe_annual}
    print(result)
    return result

if __name__ == '__main__':
    result = main()
