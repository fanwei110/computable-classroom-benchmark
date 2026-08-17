import numpy as np

def calculate_portfolio_volatility(weight_a, weight_b, vol_a, vol_b, correlation):
    """
    计算两资产组合的年化波动率
    
    参数:
    weight_a: 资产A的权重
    weight_b: 资产B的权重
    vol_a: 资产A的年化波动率
    vol_b: 资产B的年化波动率
    correlation: 资产A和B之间的相关系数
    """
    # 计算组合方差
    portfolio_variance = (weight_a**2 * vol_a**2 + 
                         weight_b**2 * vol_b**2 + 
                         2 * weight_a * weight_b * vol_a * vol_b * correlation)
    
    # 年化波动率
    portfolio_volatility = np.sqrt(portfolio_variance)
    
    return portfolio_volatility

# 参数设置
weight_a = 0.6  # 资产A权重60%
weight_b = 0.4  # 资产B权重40%
vol_a_annual = 0.184  # 资产A年化波动率18.4%
vol_b_annual = 0.297  # 资产B年化波动率29.7%

correlation_before = 0.3  # 变化前的相关系数
correlation_after = 0.8   # 变化后的相关系数

# 计算相关系数变化前的组合波动率
vol_before = calculate_portfolio_volatility(
    weight_a, weight_b, vol_a_annual, vol_b_annual, correlation_before
)

# 计算相关系数变化后的组合波动率
vol_after = calculate_portfolio_volatility(
    weight_a, weight_b, vol_a_annual, vol_b_annual, correlation_after
)

# 存储结果到字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 输出结果
print(f"资产A年化波动率: {vol_a_annual*100:.1f}%")
print(f"资产B年化波动率: {vol_b_annual*100:.1f}%")
print(f"组合权重: A={weight_a*100:.0f}%, B={weight_b*100:.0f}%")
print(f"\n相关系数为{correlation_before}时的组合年化波动率: {vol_before*100:.2f}%")
print(f"相关系数为{correlation_after}时的组合年化波动率: {vol_after*100:.2f}%")
print(f"波动率变化: {(vol_after - vol_before)*100:.2f}个百分点")
print(f"波动率增幅: {((vol_after/vol_before - 1)*100):.1f}%")
print(f"\n结果字典: {result}")
