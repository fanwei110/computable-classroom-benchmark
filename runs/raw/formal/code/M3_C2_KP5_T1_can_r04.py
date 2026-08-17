import numpy as np
from scipy.stats import norm

# ==================== 参数设置 ====================
position_value = 1_850_000  # 头寸价值（人民币元）
annual_vol = 0.218         # 年化收益波动率
trading_days = 252         # 假设一年有252个交易日，用于年化到日化的换算

# ==================== 步骤1：年化波动率换算到一日期限 ====================
# Delta-normal模型下，波动率随时间的平方根缩放：sigma_daily = sigma_annual / sqrt(T)
daily_vol = annual_vol / np.sqrt(trading_days)

# ==================== 步骤2：套用正态分位数 ====================
# 95%和99%置信水平下的标准正态分布分位数（右尾，取正值）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤3：计算并缩放VaR ====================
# (i) 95% 一日 VaR
# VaR = 头寸价值 × 日波动率 × 对应分位数
var_95_1d = position_value * daily_vol * z_95

# (ii) 99% 十日 VaR
# 期限缩放：将一日的VaR乘以 sqrt(10) 扩展至十日
var_99_10d = position_value * daily_vol * np.sqrt(10) * z_99

# ==================== 步骤4：填充结果 ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# ==================== 课堂投屏打印 ====================
print("="*45)
print("《证券投资学》- 在险价值计算演示")
print("="*45)
print(f"头寸价值:       {position_value:>15,.2f} 元")
print(f"年化波动率:     {annual_vol:>15.2%}")
print(f"假设年交易日:   {trading_days:>15d} 天")
print(f"日化波动率:     {daily_vol:>15.4%}")
print("-"*45)
print(f"正态分布 Z(95%):{z_95:>15.4f}")
print(f"正态分布 Z(99%):{z_99:>15.4f}")
print("-"*45)
print(f"(i)  95% 一日 VaR: {result['var_95_1d']:>12,.2f} 元")
print(f"(ii) 99% 十日 VaR: {result['var_99_10d']:>12,.2f} 元")
print("="*45)
