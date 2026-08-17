import numpy as np

def main():
    # 债券参数
    face_value = 100.0          # 面值
    coupon_rate = 0.046         # 票息率
    years = 7                   # 期限（年）
    ytm = 0.053                 # 到期收益率（年化）

    # 生成现金流：每年付息，到期还本
    coupon = face_value * coupon_rate
    cash_flows = np.full(years, coupon, dtype=float)
    cash_flows[-1] += face_value  # 最后一期加入本金

    # 时间向量 1, 2, ..., years
    t = np.arange(1, years + 1, dtype=float)

    # 贴现因子与现金流现值
    discount = (1 + ytm) ** t
    pv = cash_flows / discount

    # 1. 价格
    price = np.sum(pv)

    # 2. 麦考利久期
    macaulay_duration = np.sum(t * pv) / price

    # 3. 修正久期
    modified_duration = macaulay_duration / (1 + ytm)

    # 4. 凸性
    # convexity = (1/P) * Σ [ CF_t * t(t+1) / (1+y)^{t+2} ]
    convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm) ** 2)

    # 按要求存入字典
    result = {
        'price': price,
        'macaulay_duration_years': macaulay_duration,
        'modified_duration_years': modified_duration,
        'convexity': convexity
    }

    # 输出结果，方便课堂投屏查看
    for key, value in result.items():
        print(f"{key}: {value:.6f}")

    return result

if __name__ == "__main__":
    result = main()
