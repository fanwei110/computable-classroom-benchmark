import numpy as np
import pandas as pd

"""
债券定价、久期与凸性计算脚本
7年期债券：面值100，票息率4.6%，收益率5.3%
计算收益率上升80个基点时的价格跌幅
"""

# 债券基本参数
face_value = 100.0  # 面值
coupon_rate = 0.046  # 票息率（小数形式）
yield_rate = 0.053   # 到期收益率（小数形式）
maturity = 7         # 期限（年）
dy = 0.008           # 收益率变动80个基点

# 第一步：计算当前价格（所有现金流的现值之和）
cash_flows = np.full(maturity, face_value * coupon_rate)  # 前6年的票息
cash_flows[-1] += face_value  # 最后一年加上本金

# 计算每个现金流的时间
time_periods = np.arange(1, maturity + 1)

# 计算每个现金流的现值
present_values = cash_flows / ((1 + yield_rate) ** time_periods)

# 当前债券价格
current_price = np.sum(present_values)

print(f"当前债券价格: {current_price:.4f}")

# 第二步：计算麦考利久期
# 麦考利久期 = Σ(t × PV(CF_t)) / P
weighted_time = np.sum(time_periods * present_values)
macaulay_duration = weighted_time / current_price

print(f"麦考利久期: {macaulay_duration:.2f} 年")

# 第三步：计算修正久期
# 修正久期 = 麦考利久期 / (1 + y)
modified_duration = macaulay_duration / (1 + yield_rate)

print(f"修正久期: {modified_duration:.4f}")

# 第四步：计算凸性（验证准确性）
# 凸性 = Σ[t(t+1) × PV(CF_t)] / [P × (1+y)²] 单位为年的平方
convexity_numerator = np.sum(time_periods * (time_periods + 1) * present_values)
convexity = convexity_numerator / (current_price * (1 + yield_rate)**2)

print(f"凸性: {convexity:.4f} 年²")

# 第五步：应用课程经验法则 dP/P = -D_mod × dy
price_change_pct = -modified_duration * dy

# 跌幅大小作为正数
price_drop_pct = abs(price_change_pct)

print(f"\n收益率变动: {dy*100:.0f} 个基点")
print(f"使用一阶近似 dP/P = -D_mod × dy")
print(f"价格变动百分比: {price_change_pct*100:.2f}% (负值表示价格下跌)")
print(f"价格跌幅绝对值: {price_drop_pct*100:.2f}%")

# 存储结果
result = {
    'price_drop_pct': float(price_drop_pct)
}

print(f"\n最终结果：")
print(f"收益率上升80个基点，债券价格大约下跌 {result['price_drop_pct']*100:.2f}%")
print(f"\nresult 字典内容: {result}")
