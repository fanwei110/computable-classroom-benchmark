import numpy as np

# 假设 fund 是基金的日收益率序列（全样本）
# rf 是年化无风险利率（2.1%，即 0.021）

def calculate_sharpe(fund, rf):
    # 计算日收益率的均值和标准差
    mean_daily_return = np.mean(fund)
    std_daily_return = np.std(fund, ddof=1)  # 样本标准差（ddof=1）

    # 年化收益率和波动率
    annualized_return = (1 + mean_daily_return) ** 252 - 1
    annualized_volatility = std_daily_return * np.sqrt(252)

    # 年化夏普比率
    sharpe_annual = (annualized_return - rf) / annualized_volatility

    # 存入结果字典
    result = {
        'sharpe_annual': sharpe_annual
    }
    return result

# 示例调用（假设 fund 是已有的日收益率序列）
# fund = ...  # 基金的日收益率序列
# rf = 0.021  # 无风险利率 2.1%
# result = calculate_sharpe(fund, rf)
