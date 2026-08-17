import numpy as np

def main():
    # 债券参数
    face_value = 100.0
    coupon_rate = 0.046      # 票息 4.6%
    maturity = 7             # 7年期
    ytm = 0.053              # 到期收益率 5.3%
    coupon = face_value * coupon_rate  # 每年票息 4.6

    # 现金流时间点（年）
    t = np.arange(1, maturity + 1)
    # 现金流：前期为票息，最后一期加上本金
    cf = np.full(maturity, coupon)
    cf[-1] += face_value

    # 贴现因子
    discount = (1 + ytm) ** t
    pv = cf / discount

    # 1. 价格
    price = np.sum(pv)

    # 2. 麦考利久期
    weights = pv / price
    macaulay_duration = np.sum(t * weights)

    # 修正久期（年付息一次）
    modified_duration = macaulay_duration / (1 + ytm)

    # 3. 凸性
    # 凸性 = 1/(P*(1+y)^2) * sum( t*(t+1)*CF/(1+y)^t )
    convexity = np.sum(t * (t + 1) * cf / discount) / (price * (1 + ytm) ** 2)

    # 结果存入字典
    result = {
        'price': round(price, 6),                # 保留合理小数
        'macaulay_duration_years': round(macaulay_duration, 6),
        'modified_duration_years': round(modified_duration, 6),
        'convexity': round(convexity, 6)
    }

    # 输出 result 供教师检查
    print(result)
    return result

if __name__ == "__main__":
    main()
