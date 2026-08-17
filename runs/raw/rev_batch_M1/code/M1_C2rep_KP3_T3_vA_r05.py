import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
years_to_maturity = 7
coupon_frequency = 2  # 半年付息一次

# 计算票息支付额和支付次数
coupon_payment = face_value * coupon_rate / coupon_frequency
num_payments = years_to_maturity * coupon_frequency

def bond_price(ytm, face_value, coupon_payment, num_payments):
    """计算债券价格"""
    periods = np.arange(1, num_payments + 1)
    cash_flows = np.full(num_payments, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期支付本金
    price = np.sum(cash_flows / ((1 + ytm/coupon_frequency) ** periods))
    return price

def bond_duration(ytm, face_value, coupon_payment, num_payments):
    """计算麦考利久期"""
    periods = np.arange(1, num_payments + 1)
    cash_flows = np.full(num_payments, coupon_payment)
    cash_flows[-1] += face_value
    discounted_cash_flows = cash_flows / ((1 + ytm/coupon_frequency) ** periods)
    weighted_cash_flows = discounted_cash_flows * periods
    macaulay_duration = np.sum(weighted_cash_flows) / np.sum(discounted_cash_flows)
    modified_duration = macaulay_duration / (1 + ytm/coupon_frequency)
    return macaulay_duration, modified_duration

def bond_convexity(ytm, face_value, coupon_payment, num_payments):
    """计算凸性"""
    periods = np.arange(1, num_payments + 1)
    cash_flows = np.full(num_payments, coupon_payment)
    cash_flows[-1] += face_value
    discounted_cash_flows = cash_flows / ((1 + ytm/coupon_frequency) ** periods)
    convexity = np.sum(discounted_cash_flows * periods * (periods + 1)) / \
                ((1 + ytm/coupon_frequency)**2 * np.sum(discounted_cash_flows))
    return convexity

# 1. 计算当前收益率下的利率敏感性
current_price = bond_price(ytm_current, face_value, coupon_payment, num_payments)
macaulay_dur, modified_dur = bond_duration(ytm_current, face_value, coupon_payment, num_payments)
convexity = bond_convexity(ytm_current, face_value, coupon_payment, num_payments)

# 2. 估算收益率上升80个基点的价格影响
ytm_change_bps = 80
ytm_change = ytm_change_bps / 10000  # 转换为小数

# 使用久期和凸性近似计算价格变化
price_drop_approx = (-modified_dur * ytm_change + 0.5 * convexity * (ytm_change**2)) * 100
price_drop_pct = price_drop_approx

# 精确计算新价格
new_ytm = ytm_current + ytm_change
new_price = bond_price(new_ytm, face_value, coupon_payment, num_payments)
exact_price_drop_pct = (current_price - new_price) / current_price * 100

# 存储结果
result = {
    'price_drop_pct': exact_price_drop_pct  # 使用精确计算的跌幅
}

# 输出验证信息（可选，不影响结果）
print(f"当前价格: {current_price:.4f}")
print(f"新价格: {new_price:.4f}")
print(f"精确跌幅: {exact_price_drop_pct:.4f}%")
print(f"久期-凸性近似跌幅: {price_drop_approx:.4f}%")
print(f"结果已存入result字典，键为'price_drop_pct'")
