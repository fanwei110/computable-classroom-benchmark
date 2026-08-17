import numpy as np

def main():
    # ---------- 债券参数 ----------
    face_value = 100.0          # 面值
    coupon_rate = 0.046         # 票息率（年化）
    n_years = 7                 # 剩余年限
    ytm = 0.053                 # 到期收益率（年化）

    # ---------- 现金流与时间轴 ----------
    coupon = face_value * coupon_rate
    # 每年年末付息，最后一年加还本金
    cash_flows = np.full(n_years, coupon)
    cash_flows[-1] += face_value
    t = np.arange(1, n_years + 1)   # 现金流发生时间（年）

    # ---------- 1. 定价 ----------
    discount_factors = (1 + ytm) ** (-t)
    pv_cf = cash_flows * discount_factors
    price = np.sum(pv_cf)

    # ---------- 2. 麦考利久期 & 修正久期 ----------
    weights = pv_cf / price
    macaulay_dur = np.sum(t * weights)
    modified_dur = macaulay_dur / (1 + ytm)

    # ---------- 3. 凸性 ----------
    # 凸性 = (1/P) * Σ [t*(t+1) * CF_t / (1+y)^(t+2)]
    convexity_sum = np.sum(
        t * (t + 1) * cash_flows * (1 + ytm) ** (-(t + 2))
    )
    convexity = convexity_sum / price

    # ---------- 输出契约 ----------
    result = {
        'price': price,
        'macaulay_duration_years': macaulay_dur,
        'modified_duration_years': modified_dur,
        'convexity': convexity
    }

    # 打印结果以便教师投屏查看
    for key, value in result.items():
        print(f"{key}: {value:.6f}")

    return result

if __name__ == "__main__":
    result = main()
