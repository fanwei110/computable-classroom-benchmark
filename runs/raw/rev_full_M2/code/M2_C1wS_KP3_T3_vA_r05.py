import numpy as np
from scipy.optimize import brentq

# ============================================================
# 债券参数
# ============================================================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（年化）
ytm = 0.053                 # 当前到期收益率（年化）
years_to_maturity = 7.0     # 剩余期限（年）
delta_y = 0.0080            # 收益率变动（80个基点 = 0.80%）

# ============================================================
# 现金流时间与金额
# ============================================================
# 假设每年付息一次，最后一次现金流包含本金+最后一期票息
periods = np.arange(1, years_to_maturity + 1)  # 1, 2, ..., 7
coupon_payment = face_value * coupon_rate
cash_flows = np.full(len(periods), coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上本金

# ============================================================
# 价格函数：给定收益率，计算债券价格
# ============================================================
def bond_price(y):
    """计算给定收益率y下的债券价格"""
    return np.sum(cash_flows / (1 + y) ** periods)

# 当前价格
price_current = bond_price(ytm)

# ============================================================
# 利率敏感性指标：久期与凸性
# ============================================================
# 修正久期：-(1/P) * dP/dy
# 使用中心差分近似导数，步长取1e-6
h = 1e-6
price_up = bond_price(ytm + h)
price_down = bond_price(ytm - h)
dP_dy = (price_up - price_down) / (2 * h)
modified_duration = -dP_dy / price_current

# 凸性：(1/P) * d²P/dy²
d2P_dy2 = (price_up - 2 * price_current + price_down) / (h ** 2)
convexity = d2P_dy2 / price_current

# ============================================================
# 价格变动估算
# ============================================================
# 一阶近似（仅久期）：ΔP/P ≈ -修正久期 * Δy
price_change_pct_order1 = -modified_duration * delta_y

# 二阶近似（久期+凸性）：ΔP/P ≈ -修正久期 * Δy + 0.5 * 凸性 * (Δy)^2
price_change_pct_order2 = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# 真实价格变动（精确计算）
price_new = bond_price(ytm + delta_y)
price_change_pct_true = (price_new - price_current) / price_current

# ============================================================
# 输出结果
# ============================================================
# 题目要求：收益率上升80个基点，价格大概跌多少（跌幅用正数表示）
# 使用二阶近似作为"大概"估计值
price_drop_pct = -price_change_pct_order2 * 100  # 转换为百分比，跌幅为正数

result = {
    'price_drop_pct': round(price_drop_pct, 4)
}

# 打印详细结果供课堂展示
print("=" * 60)
print("债券定价与利率敏感性分析")
print("=" * 60)
print(f"面值: {face_value}元")
print(f"票息率: {coupon_rate*100:.2f}%")
print(f"到期收益率: {ytm*100:.2f}%")
print(f"剩余期限: {years_to_maturity}年")
print(f"付息频率: 每年一次")
print()
print(f"当前债券价格: {price_current:.4f}元")
print(f"修正久期: {modified_duration:.4f}年")
print(f"凸性: {convexity:.4f}")
print()
print(f"收益率变动: +{delta_y*100:.0f}个基点")
print(f"一阶近似价格变动: {price_change_pct_order1*100:.4f}%")
print(f"二阶近似价格变动: {price_change_pct_order2*100:.4f}%")
print(f"真实价格变动: {price_change_pct_true*100:.4f}%")
print()
print(f"估算价格跌幅: {price_drop_pct:.4f}%")
print("=" * 60)

# 最终输出字典
print("\nresult =", result)
