import numpy as np

# 给定参数
vol_A = 0.184          # 资产 A 的年化波动率
vol_B = 0.297          # 资产 B 的年化波动率
w_A = 0.6              # 资产 A 的权重
w_B = 0.4              # 资产 B 的权重
corr_before = 0.3      # 变化前的相关系数
corr_after = 0.8       # 变化后的相关系数

# 计算投资组合方差的通用公式：
# variance = w_A^2 * vol_A^2 + w_B^2 * vol_B^2 + 2 * w_A * w_B * vol_A * vol_B * corr

# 1. 计算相关系数为 0.3 时的组合年化波动率
var_before = (w_A**2 * vol_A**2) + \
             (w_B**2 * vol_B**2) + \
             (2 * w_A * w_B * vol_A * vol_B * corr_before)
vol_before_annual = np.sqrt(var_before)

# 2. 计算相关系数为 0.8 时的组合年化波动率
var_after = (w_A**2 * vol_A**2) + \
            (w_B**2 * vol_B**2) + \
            (2 * w_A * w_B * vol_A * vol_B * corr_after)
vol_after_annual = np.sqrt(var_after)

# 按照输出契约，将结果存入字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 打印结果以供验证
print(f"相关性从 0.3 升至 0.8 时，60/40 组合的年化波动率变化：")
print(f"变化前: {result['vol_before_annual']:.4f} ({result['vol_before_annual']*100:.2f}%)")
print(f"变化后: {result['vol_after_annual']:.4f} ({result['vol_after_annual']*100:.2f}%)")
