import numpy as np
from scipy.stats import norm

# ================= 输入参数 =================
sigma_annual = 0.24          # 24% 年化波动率
position_value = 2700000     # 270万元头寸
confidence_level = 0.95      # 95% 置信水平

# ================= 假设处理 =================
# 假设：一年包含252个交易日（国际与国内金融市场计算VaR的通用标准假设）
trading_days = 252

# ================= 步骤1：年化波动率换算到一日期限 =================
# 根据平方根时间法则
sigma_daily = sigma_annual / np.sqrt(trading_days)

# ================= 步骤2：套用 95% 正态分位数 =================
# 使用 Delta-Normal (参数法) 假设损益服从正态分布，求95%分位数
z_score = norm.ppf(confidence_level)

# ================= 步骤3：计算 VaR 金额并存入 result =================
# VaR = Z * sigma_daily * Position
var_95_1d = z_score * sigma_daily * position_value

# 按照输出契约存入字典
result = {
    'var_95_1d': var_95_1d
}

# ================= 课堂投屏展示 =================
print("="*50)
print("《证券投资学》课堂实时编程：在险价值 计算")
print("="*50)
print(f"1. 年化波动率换算：")
print(f"   假设交易日：{trading_days} 天/年")
print(f"   日波动率  = {sigma_annual:.2%} / sqrt({trading_days}) = {sigma_daily:.4%}")
print(f"\n2. 95% 正态分位数：")
print(f"   Z-score = norm.ppf(0.95) = {z_score:.4f}")
print(f"\n3. VaR 金额计算：")
print(f"   头寸金额 = {position_value:,.0f} 元")
print(f"   95%一日VaR = {z_score:.4f} × {sigma_daily:.4%} × {position_value:,.0f}")
print(f"   95%一日VaR = {result['var_95_1d']:,.2f} 元")
print("="*50)
print(f"最终输出字典：{result}")
