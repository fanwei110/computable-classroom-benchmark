import numpy as np
from scipy import stats

def calculate_var():
    """
    计算 delta-normal 模型下的 Value at Risk (VaR)
    """
    # 输入参数
    position_value = 1850000  # 头寸价值
    annual_volatility = 0.218  # 年化收益波动率
    
    # 时间转换因子
    trading_days_per_year = 252  # 假设每年252个交易日
    
    # 计算日波动率
    daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)
    
    # 计算10日波动率
    ten_day_volatility = daily_volatility * np.sqrt(10)
    
    # (i) 95% 一日 VaR
    # 95% 置信水平对应的标准正态分布分位数
    z_score_95 = stats.norm.ppf(0.05)  # 使用0.05因为VaR考虑左尾
    var_95_1d = position_value * z_score_95 * daily_volatility
    var_95_1d = abs(var_95_1d)  # VaR通常表示为正值
    
    # (ii) 99% 十日 VaR
    # 99% 置信水平对应的标准正态分布分位数
    z_score_99 = stats.norm.ppf(0.01)  # 使用0.01因为VaR考虑左尾
    var_99_10d = position_value * z_score_99 * ten_day_volatility
    var_99_10d = abs(var_99_10d)  # VaR通常表示为正值
    
    # 存储结果
    result = {
        'var_95_1d': var_95_1d,
        'var_99_10d': var_99_10d
    }
    
    return result

if __name__ == "__main__":
    result = calculate_var()
    
    # 输出结果
    print("Delta-Normal VaR 计算结果:")
    print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
    print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")
    
    # 验证结果
    print(f"\n结果字典: {result}")
