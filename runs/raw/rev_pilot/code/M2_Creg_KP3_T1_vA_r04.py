import numpy as np

def main():
    # 债券参数
    face_value = 100.0          # 面值
    coupon_rate = 0.046          # 票息率 4.6%
    years = 7                    # 期限 7 年
    ytm = 0.053                  # 到期收益率 5.3%
    coupon = face_value * coupon_rate  # 每年票息

    # 现金流发生的时间（年末：1,2,...,7）
    t = np.arange(1, years + 1, dtype=float)

    # 各期现金流：票息，最后一年加上本金
    cash_flows = np.full(years, coupon)
    cash_flows[-1] += face_value

    # 贴现因子
    discount_factors = (1 + ytm) ** (-t)

    # 现金流现值
    present_values = cash_flows * discount_factors

    # 1. 债券价格
    price = np.sum(present_values)

    # 2. 麦考利久期（加权平均时间）
    weighted_times = t * present_values
    macaulay_duration = np.sum(weighted_times) / price

    # 3. 修正久期
    modified_duration = macaulay_duration / (1 + ytm)

    # 4. 凸性
    # 凸性公式： sum( t*(t+1)*PV ) / ( price * (1+ytm)^2 )
    weighted_convexity = t * (t + 1) * present_values
    convexity = np.sum(weighted_convexity) / (price * (1 + ytm)**2)

    # 存入字典，键名严格按要求
    result = {
        'price': float(price),
        'macaulay_duration_years': float(macaulay_duration),
        'modified_duration_years': float(modified_duration),
        'convexity': float(convexity)
    }

    return result

if __name__ == "__main__":
    res = main()
    # 输出结果以便查看
    for key, value in res.items():
        print(f"{key}: {value:.6f}")
