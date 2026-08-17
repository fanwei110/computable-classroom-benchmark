import numpy as np
from scipy.optimize import newton

def calculate_bond_metrics(face_value, coupon_rate, years_to_maturity, ytm):
    """
    计算债券的价格、麦考利久期、修正久期和凸性。

    参数:
    - face_value: 面值
    - coupon_rate: 票息率（年化）
    - years_to_maturity: 到期年限
    - ytm: 到期收益率（年化）

    返回:
    - result: 包含价格、麦考利久期、修正久期和凸性的字典
    """
    # 票息每期支付频率（假设每年支付一次）
    frequency = 1
    periods = years_to_maturity * frequency
    coupon_payment = (coupon_rate * face_value) / frequency
    ytm_period = ytm / frequency

    # 计算债券价格
    def bond_price(y):
        cash_flows = np.array([coupon_payment] * int(periods) + [face_value + coupon_payment])
        time_periods = np.arange(1, int(periods) + 2)
        discounted_cash_flows = cash_flows / ((1 + y) ** time_periods)
        return np.sum(discounted_cash_flows)

    price = bond_price(ytm_period)

    # 计算麦考利久期
    def macaulay_duration(y):
        cash_flows = np.array([coupon_payment] * int(periods) + [face_value + coupon_payment])
        time_periods = np.arange(1, int(periods) + 2)
        discounted_cash_flows = cash_flows / ((1 + y) ** time_periods)
        weighted_cash_flows = discounted_cash_flows * time_periods
        return np.sum(weighted_cash_flows) / np.sum(discounted_cash_flows)

    mac_duration_periods = macaulay_duration(ytm_period)
    mac_duration_years = mac_duration_periods / frequency

    # 计算修正久期
    modified_duration_periods = mac_duration_periods / (1 + ytm_period)
    modified_duration_years = modified_duration_periods / frequency

    # 计算凸性
    def convexity(y):
        cash_flows = np.array([coupon_payment] * int(periods) + [face_value + coupon_payment])
        time_periods = np.arange(1, int(periods) + 2)
        discounted_cash_flows = cash_flows / ((1 + y) ** time_periods)
        weighted_cash_flows = discounted_cash_flows * time_periods * (time_periods + 1)
        return np.sum(weighted_cash_flows) / (np.sum(discounted_cash_flows) * (1 + y) ** 2)

    conv = convexity(ytm_period) / (frequency ** 2)

    result = {
        'price': price,
        'macaulay_duration_years': mac_duration_years,
        'modified_duration_years': modified_duration_years,
        'convexity': conv
    }

    return result

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053

# 计算结果
result = calculate_bond_metrics(face_value, coupon_rate, years_to_maturity, ytm)

# 输出结果
print(result)
