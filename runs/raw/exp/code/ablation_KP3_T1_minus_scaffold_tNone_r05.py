import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize

# 债券参数
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率 4.6%
maturity = 7              # 期限（年）
yield_rate = 0.053        # 到期收益率 5.3%

# 现金流生成
# 每年付息一次，共maturity次付息，最后一次包含本金
coupon_payment = face_value * coupon_rate  # 每期票息
cash_flows = np.full(maturity, coupon_payment)  # 每年票息
cash_flows[-1] += face_value  # 最后一次加上本金

# 时间向量（从1到maturity，单位：年）
time_periods = np.arange(1, maturity + 1)

# 贴现因子
discount_factors = 1 / (1 + yield_rate) ** time_periods

# 债券价格
price = np.sum(cash_flows * discount_factors)

# 麦考利久期 (Macauley Duration)
# 公式: D_mac = [Σ t*CF_t / (1+y)^t] / P
macaulay_duration = np.sum(time_periods * cash_flows * discount_factors) / price

# 修正久期 (Modified Duration)
# 公式: D_mod = D_mac / (1 + y)
modified_duration = macaulay_duration / (1 + yield_rate)

# 凸性 (Convexity)
# 公式: C = [Σ t(t+1)*CF_t / (1+y)^(t+2)] / P
convexity = np.sum(time_periods * (time_periods + 1) * cash_flows / 
                   (1 + yield_rate) ** (time_periods + 2)) / price

# 输出结果
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

print("=" * 50)
print("债券定价与风险度量结果")
print("=" * 50)
print(f"债券信息:")
print(f"  面值: {face_value:.1f}")
print(f"  票息率: {coupon_rate*100:.2f}%")
print(f"  期限: {maturity} 年")
print(f"  到期收益率: {yield_rate*100:.2f}%")
print("-" * 50)
print(f"价格 (Price): {price:.4f}")
print(f"麦考利久期 (Macauley Duration): {macaulay_duration:.4f} 年")
print(f"修正久期 (Modified Duration): {modified_duration:.4f} 年")
print(f"凸性 (Convexity): {convexity:.4f} 年²")
print("=" * 50)

# 验证：展示各期现金流和贴现
print("\n现金流明细:")
print("-" * 70)
print(f"{'期数':>5} {'时间(年)':>8} {'现金流':>10} {'贴现因子':>10} {'现值':>10} {'权重':>10} {'t*权重':>10}")
print("-" * 70)

pv_values = cash_flows * discount_factors
weight = pv_values / price
t_weight = time_periods * weight

for t, cf, df, pv, w, tw in zip(range(1, maturity+1), cash_flows, discount_factors, pv_values, weight, t_weight):
    print(f"{t:5d} {t:8.0f} {cf:10.4f} {df:10.6f} {pv:10.4f} {w:10.6f} {tw:10.6f}")

print("-" * 70)
print(f"{'合计':>13} {'':>10} {np.sum(pv_values):>10.4f} {np.sum(weight):>10.6f} {np.sum(t_weight):>10.6f}")
print("\n验证: 权重之和应为1.0000")

# 可视化：价格与收益率的关系
rates = np.linspace(0.01, 0.10, 100)
prices = []
for r in rates:
    df = 1 / (1 + r) ** time_periods
    p = np.sum(cash_flows * df)
    prices.append(p)

plt.figure(figsize=(10, 6))
plt.plot(rates * 100, prices, 'b-', linewidth=2, label='债券价格曲线')
plt.axvline(x=yield_rate * 100, color='r', linestyle='--', 
            label=f'当前收益率 {yield_rate*100:.2f}%')
plt.axhline(y=price, color='g', linestyle=':', 
            label=f'当前价格 {price:.4f}')
plt.xlabel('到期收益率 (%)', fontsize=12)
plt.ylabel('债券价格', fontsize=12)
plt.title('债券价格与收益率关系图', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

print("\n最终结果字典:")
print(result)
