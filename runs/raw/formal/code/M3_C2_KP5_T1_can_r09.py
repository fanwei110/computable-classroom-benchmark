import numpy as np
from scipy.stats import norm

# ========================================================
# 输入参数
# ========================================================
position_value = 1_850_000  # 头寸价值（元）
sigma_annual = 0.218        # 年化收益波动率
# 假设：一年有252个交易日（金融市场标准假设）
trading_days_per_year = 252 

# ========================================================
# 计算步骤
# ========================================================

# 1. 年化波动率换算到一日期限
# 在 Delta-Normal 模型下，假设收益率服从正态分布且独立同分布，
# 波动率随时间的平方根规则缩放：sigma_t = sigma_annual * sqrt(t / T)
sigma_1d = sigma_annual / np.sqrt(trading_days_per_year)

# 2. 对两个置信水平套用正态分位数
# 95% 置信水平对应的下界分位数（取正值表示损失）
z_95 = norm.ppf(0.95)
# 99% 置信水平对应的下界分位数
z_99 = norm.ppf(0.99)

# 3. 以合适方式缩放到十日期限，并计算 VaR
# 10日波动率 = 1日波动率 * sqrt(10)
sigma_10d = sigma_1d * np.sqrt(10)

# VaR = 头寸价值 × Z分位数 × 对应期限波动率
var_95_1d = position_value * z_95 * sigma_1d
var_99_10d = position_value * z_99 * sigma_10d

# 4. 填充 result
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# ========================================================
# 课堂投屏展示辅助信息
# ========================================================
print("="*40)
print("《证券投资学》- 在险价值计算演示")
print("="*40)
print(f"头寸价值: {position_value:,.2f} 元")
print(f"年化波动率: {sigma_annual:.2%}")
print(f"假设一年交易日: {trading_days_per_year} 天")
print("-"*40)
print(f"1日波动率: {sigma_1d:.6f}")
print(f"10日波动率: {sigma_10d:.6f}")
print("-"*40)
print(f"Z(95%): {z_95:.4f}")
print(f"Z(99%): {z_99:.4f}")
print("-"*40)
print(f"95% 1日 VaR: {var_95_1d:,.2f} 元")
print(f"99% 10日 VaR: {var_99_10d:,.2f} 元")
print("="*40)
print("输出字典 result:")
print(result)
