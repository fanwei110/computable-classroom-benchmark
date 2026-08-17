import numpy as np

# 给定参数
annual_volatility = 0.24  # 年化波动率 24%
position_value = 2_700_000  # 头寸金额 2,700,000 元
confidence_level = 0.95  # 置信水平 95%
days = 1  # 持有期 1 天

# 步骤1：将年化波动率转换为1日波动率
# 假设一年有252个交易日
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 步骤2：计算1日VaR（正态分布假设下，使用单尾Z值）
# 对于95%置信水平，单尾正态分布分位数为约1.645
z_score = np.percentile(np.random.standard_normal(1000000), confidence_level * 100)
# 但为了确定性和精确性，使用scipy的ppf会更精确，但题目限定仅numpy，
# 因此使用解析值或固定随机种子+大样本模拟近似，但这里为了避免随机波动，
# 我们直接使用已知的解析值：norm.ppf(0.95) = 约1.6448536269514722
# 由于不能使用scipy，我们硬编码该值以保证确定可复现。
z_95 = 1.6448536269514722  

# 或者可以使用numpy生成一个非常大的固定种子样本来逼近，但直接使用已知常数更可靠。
# 我们采用已知常数。

# 计算VaR = 头寸价值 * 日波动率 * Z值
var_95_1d = position_value * daily_volatility * z_95

# 输出结果字典
result = {
    'var_95_1d': var_95_1d
}

# 打印结果
print(result)
