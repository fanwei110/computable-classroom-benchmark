import numpy as np

# =========================
# 债券参数定义（年付息）
# =========================
face_value = 100.0
coupon_rate = 0.046          # 票面利率
ytm = 0.053                  # 当前到期收益率
maturity = 7                 # 剩余期限（年）
coupon = face_value * coupon_rate  # 每年票息

# 构造现金流时间点和金额
t = np.arange(1, maturity + 1)
cashflow = np.full_like(t, coupon, dtype=float)
cashflow[-1] += face_value   # 最后一期加上本金

# 折现因子与现值
discount = (1 + ytm) ** (-t)
pv = cashflow * discount
price = np.sum(pv)

# =========================
# 1. 利率敏感性计算
# =========================
# 麦考利久期
D_mac = np.sum(t * pv) / price
# 修正久期
D_mod = D_mac / (1 + ytm)
# 凸性（标准闭合式定义）
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm) ** 2)

# =========================
# 2. 估算收益率上升80基点的影响
# =========================
delta_y = 0.008  # 80个基点 = 0.8%
# 价格变动的二阶近似：ΔP/P ≈ -D_mod·Δy + 0.5·C·(Δy)^2
# 价格跌幅（百分比）取负号
price_drop_pct = (D_mod * delta_y - 0.5 * convexity * delta_y ** 2) * 100

# =========================
# 3. 将跌幅存入 result
# =========================
result = {
    'price_drop_pct': round(price_drop_pct, 4)  # 保留4位小数便于展示
}

if __name__ == "__main__":
    print("债券当前价格：{:.4f}".format(price))
    print("修正久期：{:.4f}".format(D_mod))
    print("凸性：{:.4f}".format(convexity))
    print("收益率上升80bps时估算的价格跌幅(%)：{:.4f}".format(price_drop_pct))
    print("\n要求输出的字典：")
    print(result)
