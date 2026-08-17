import numpy as np

def main():
    # ----- 债券参数 -----
    face_value = 100.0       # 面值
    coupon_rate = 0.046      # 票息率 4.6%
    years = 7                # 期限（年）
    ytm = 0.053              # 到期收益率 5.3%

    coupon = face_value * coupon_rate  # 每年票息 = 4.6

    # ----- 各期现金流 -----
    t = np.arange(1, years + 1, dtype=float)         # 期数 [1,2,3,4,5,6,7]
    cf = np.full(years, coupon)                      # 各期票息
    cf[-1] += face_value                             # 最后一期加上面值

    # ----- 价格计算：P = Σ CF_t / (1+y)^t -----
    discount_factors = (1 + ytm) ** t
    pv_cf = cf / discount_factors
    price = np.sum(pv_cf)

    # ----- 麦考利久期：D_mac = (1/P) Σ t * CF_t / (1+y)^t -----
    macaulay_duration = np.sum(t * pv_cf) / price

    # ----- 修正久期：D_mod = D_mac / (1+y) -----
    modified_duration = macaulay_duration / (1 + ytm)

    # ----- 凸性：C = (1/P) Σ t(t+1) * CF_t / (1+y)^{t+2} -----
    # 分母的指数为 t+2
    convexity = np.sum(t * (t + 1) * cf / (1 + ytm) ** (t + 2)) / price

    # ----- 输出字典 -----
    result = {
        'price': price,
        'macaulay_duration_years': macaulay_duration,
        'modified_duration_years': modified_duration,
        'convexity': convexity
    }

    return result

if __name__ == "__main__":
    result = main()
    # 教师可直接投屏查看 result，此处打印以便课堂检验
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
