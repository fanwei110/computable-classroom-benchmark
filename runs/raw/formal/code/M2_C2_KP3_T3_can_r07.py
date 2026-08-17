import numpy as np

# =============================================================================
# 债券定价、久期与凸性 —— 课堂演示脚本
# =============================================================================
# 假设：票息按年支付（Annual coupon），面值 100，票息率 4.6%，收益率 5.3%，期限 7 年。
# 收益率上升 80 个基点 (0.80%)，估算债券价格跌幅。
# =============================================================================

# ---------- 参数 ----------
FACE = 100.0               # 面值
COUPON_RATE = 0.046        # 票息率
YTM = 0.053                # 到期收益率
MATURITY = 7               # 期限（年）
FREQ = 1                   # 付息频率（1：年付）
DY = 0.0080                # 收益率变化（80 基点）

# ---------- 现金流 ----------
times = np.arange(1, MATURITY * FREQ + 1) / FREQ
coupons = np.full(MATURITY * FREQ, FACE * COUPON_RATE / FREQ)
coupons[-1] += FACE                               # 最后一期归还本金

# ---------- 债券价格 ----------
discounts = (1 + YTM / FREQ) ** (-times * FREQ)   # 匹配复利频率
pv_cf = coupons * discounts
price = np.sum(pv_cf)

# ---------- 麦考利久期 & 修正久期 ----------
macaulay_duration = np.sum(times * pv_cf) / price
modified_duration = macaulay_duration / (1 + YTM / FREQ)

# ---------- 凸性（年付息对应公式） ----------
# 凸性 = Σ[ t(t+1/f)*CF/(1+y)^(t+2) ] / P   （此处 f=1）
convexity = np.sum(
    times * (times + 1 / FREQ) * coupons * (1 + YTM / FREQ) ** (-times * FREQ - 2)
) / price

# ---------- 价格变化估算 ----------
# ΔP/P ≈ -MD * Δy + 0.5 * Conv * (Δy)^2
delta_p_pct = -modified_duration * DY + 0.5 * convexity * DY**2

# 跌幅（下跌幅度的百分数，取正数）
price_drop_pct = -delta_p_pct * 100.0

# ---------- 输出契约 ----------
result = {
    'price_drop_pct': price_drop_pct   # 例如：4.51 表示价格约下跌 4.51%
}

if __name__ == '__main__':
    print(result)
