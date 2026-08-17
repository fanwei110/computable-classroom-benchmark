import numpy as np
from scipy.stats import norm
import json

# ==================== 参数设定 ====================
# 头寸价值
position_value = 1_850_000  # 1,850,000 元
# 年化波动率
annual_vol = 0.218  # 21.8%
# 交易日
trading_days = 252
# 置信水平
confidence_95 = 0.95
confidence_99 = 0.99

# ==================== 计算过程 ====================
# 1. 将年化波动率转换为日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 计算单尾正态分位数 (注意：VaR关注左尾损失，所以用单尾分位数)
z_95 = norm.ppf(1 - confidence_95)  # 95%单尾分位数 ≈ 1.6449
z_99 = norm.ppf(1 - confidence_99)  # 99%单尾分位数 ≈ 2.3263

# 3. 均值取零，计算VaR
# 一日VaR计算 (均值取零)
var_95_1d_loss = position_value * daily_vol * z_95  # 一日95%VaR损失金额

# 十日VaR计算 (均值取零，波动率按sqrt(10)缩放)
var_99_10d_loss = position_value * daily_vol * np.sqrt(10) * z_99  # 十日99%VaR损失金额

# 4. 确保VaR报告为正的损失金额
var_95_1d = abs(round(var_95_1d_loss, 2))
var_99_10d = abs(round(var_99_10d_loss, 2))

# ==================== 输出结果 ====================
result = {
    'var_95_1d': float(var_95_1d),
    'var_99_10d': float(var_99_10d)
}

# 打印结果（方便检查）
print("=== 在险价值计算结果 ===")
print(f"头寸价值: ¥{position_value:,.2f}")
print(f"年化波动率: {annual_vol*100:.1f}%")
print(f"日波动率: {daily_vol*100:.4f}%")
print(f"\n计算结果:")
print(f"95% 一日 VaR: ¥{var_95_1d:,.2f}")
print(f"99% 十日 VaR: ¥{var_99_10d:,.2f}")

print("\n变量名：result")
print(f"准确结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
