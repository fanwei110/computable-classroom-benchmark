import numpy as np

def main():
    # 债券参数
    face_value = 100.0       # 面值
    coupon_rate = 0.046      # 票息率 4.6%
    years = 7                # 期限 7 年
    ytm = 0.053              # 到期收益率 5.3%

    # 现金流：每年付息，到期一次还本（假设每年付息一次）
    coupon = face_value * coupon_rate
    t = np.arange(1, years + 1)
    cash_flows = np.full(years, coupon)
    cash_flows[-1] += face_value  # 最后一年加上本金

    # 贴现因子与现金流现值
    discount_factors = (1 + ytm) ** t
    pv = cash_flows / discount_factors

    # 1. 价格
    price = np.sum(pv)

    # 2. 麦考利久期
    macaulay_duration = np.sum(t * pv) / price

    # 3. 修正久期
    modified_duration = macaulay_duration / (1 + ytm)

    # 4. 凸性
    convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm) ** 2)

    # 结果字典
    result = {
        'price': round(price, 6),
        'macaulay_duration_years': round(macaulay_duration, 6),
        'modified_duration_years': round(modified_duration, 6),
        'convexity': round(convexity, 6)
    }

    print(result)

if __name__ == "__main__":
    main()
