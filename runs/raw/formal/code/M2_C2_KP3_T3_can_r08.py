"""
债券定价与久期、凸性 — 课堂演示脚本
假设：面值 100，票息率 4.6%（年付息一次），到期收益率 5.3%，期限 7 年。
计算收益率上升 80 个基点 (0.8%) 时，价格跌幅的近似估计。
"""
import numpy as np

# ==================== 债券参数 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（年化）
ytm = 0.053                 # 到期收益率（年化）
maturity = 7                # 剩余期限（年）
delta_y = 0.0080            # 收益率变动（80 bp）

# 假设每年付息一次，现金流时间点
t = np.arange(1, maturity + 1)
coupon = face_value * coupon_rate
cash_flows = np.full(maturity, coupon)
cash_flows[-1] += face_value  # 最后一年包含本金

# ==================== 当前价格 ====================
discount_factors = (1 + ytm) ** t
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# ==================== 利率敏感性 ====================
# 麦考利久期
weighted_t = t * pv_cash_flows
macaulay_duration = np.sum(weighted_t) / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 凸性（年化、传统公式）
# 凸性 = Σ [t*(t+1)*PV(CF)] / [P * (1+y)^2]
convexity = np.sum(t * (t + 1) * pv_cash_flows) / (price * (1 + ytm) ** 2)

# ==================== 价格跌幅估算（久期+凸性） ====================
# 价格相对变动近似:  ΔP/P ≈ -D_mod * Δy + 0.5 * C * (Δy)^2
price_change_approx = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)
price_drop_pct_approx = price_change_approx * 100.0   # 转换为百分比

# 也可计算精确价格以验证（选做）
new_ytm = ytm + delta_y
new_discount = (1 + new_ytm) ** t
new_price = np.sum(cash_flows / new_discount)
actual_price_change_pct = (new_price - price) / price * 100.0

# ==================== 结果汇总 ====================
result = {
    'price_drop_pct': price_drop_pct_approx
}

# 投屏友好输出
print("=" * 60)
print("债券定价与敏感度分析")
print("=" * 60)
print(f"面值: {face_value}")
print(f"票息率: {coupon_rate*100}%")
print(f"到期收益率 (YTM): {ytm*100}%")
print(f"期限: {maturity} 年")
print(f"当前价格: {price:.4f}")
print("-" * 40)
print("【利率敏感性】")
print(f"麦考利久期:   {macaulay_duration:.4f} 年")
print(f"修正久期:     {modified_duration:.4f}")
print(f"凸性:         {convexity:.4f}")
print("-" * 40)
print(f"收益率变动 Δy = +{delta_y*100:.0f} bp")
print(f"基于久期+凸性估算的价格跌幅: {price_drop_pct_approx:.4f}%")
print(f"（供参考：精确价格跌幅: {actual_price_change_pct:.4f}%）")
print("=" * 60)
print("最终结果存入字典 result =", result)
