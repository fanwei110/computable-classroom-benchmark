import numpy as np
from scipy.stats import norm

# ==================
# 1. 参数设定
# ==================
sigma_annual = 0.24          # 年化波动率 (小数表示)
position = 2_700_000         # 头寸金额 (人民币)
trading_days = 252           # 每年交易日数
confidence_level = 0.95      # 置信水平

# ==================
# 2. 计算步骤
# ==================
# 步骤1: 将年化波动率去年化为一日波动率
# 波动率按 sqrt(252) 缩放
sigma_daily = sigma_annual / np.sqrt(trading_days)

# 步骤2: 使用单尾95%正态分位数，均值取零
z_95 = norm.ppf(confidence_level)

# 步骤3: 计算 95% 一日 VaR，报告为正的损失金额
# VaR = 头寸 × 分位数 × 日波动率
var_95_1d = position * z_95 * sigma_daily

# ==================
# 3. 存储与输出
# ==================
result = {
    'var_95_1d': var_95_1d
}

# 课堂投屏友好打印
print("="*40)
print("《证券投资学》- 在险价值 计算演示")
print("="*40)
print(f"年化波动率:   {sigma_annual:.2%}")
print(f"日化波动率:   {sigma_daily:.6%} (计算: {sigma_annual} / sqrt({trading_days}))")
print(f"头寸金额:     {position:,.2f} 元")
print(f"95%正态分位数: {z_95:.6f}")
print("-" * 40)
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print("="*40)
print(f"result字典输出: {result}")
