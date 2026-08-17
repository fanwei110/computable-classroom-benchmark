import numpy as np

# 定义已知参数
w_A = 0.6          # 资产 A 的权重
w_B = 0.4          # 资产 B 的权重
vol_A = 0.184      # 资产 A 的年化波动率
vol_B = 0.297      # 资产 B 的年化波动率
rho_before = 0.3   # 变化前的相关系数
rho_after = 0.8    # 变化后的相关系数

# 定义计算投资组合波动率的函数
# 公式: sigma_p = sqrt(w_A^2 * sigma_A^2 + w_B^2 * sigma_B^2 + 2 * w_A * w_B * sigma_A * sigma_B * rho)
def calculate_portfolio_vol(w_A, w_B, vol_A, vol_B, rho):
    variance = (w_A**2 * vol_A**2 + 
                w_B**2 * vol_B**2 + 
                2 * w_A * w_B * vol_A * vol_B * rho)
    return np.sqrt(variance)

# 计算相关系数变化前后的组合波动率
vol_before_annual = calculate_portfolio_vol(w_A, w_B, vol_A, vol_B, rho_before)
vol_after_annual = calculate_portfolio_vol(w_A, w_B, vol_A, vol_B, rho_after)

# 按照输出契约存入字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 打印结果以供验证
print(result)
