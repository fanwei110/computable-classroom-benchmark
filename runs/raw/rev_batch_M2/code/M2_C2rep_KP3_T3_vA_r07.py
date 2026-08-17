import numpy as np

def main():
    # ---------- 债券参数 ----------
    face_value = 100.0          # 面值
    coupon_rate = 0.046         # 票面利率（年化）
    ytm = 0.053                 # 到期收益率（年化）
    n_years = 7                 # 剩余年限
    delta_y = 0.0080            # 收益率上升 80 个基点

    # ---------- 假设：每年付息一次，复利频率与付息频率一致 ----------
    coupon = face_value * coupon_rate       # 每年票息

    # 构建现金流数组（1 ~ n_years）
    t = np.arange(1, n_years + 1, dtype=float)
    cashflows = np.full(n_years, coupon)
    cashflows[-1] += face_value             # 最后一年还本

    # ---------- 1. 价格 ----------
    discount_factors = (1 + ytm) ** t
    pv = cashflows / discount_factors
    price = np.sum(pv)

    # ---------- 2. 麦考利久期、修正久期 ----------
    weights = pv / price
    macaulay_duration = np.sum(t * weights)
    modified_duration = macaulay_duration / (1 + ytm)

    # ---------- 3. 凸性（离散年复利） ----------
    # 凸性 = Σ [ t*(t+1)*PV ] / [ P * (1+y)^2 ]
    conv_numerator = np.sum(t * (t + 1) * pv)
    convexity = conv_numerator / (price * (1 + ytm)**2)

    # ---------- 4. 估算收益率上升 80 个基点的价格变化 ----------
    # 使用二阶近似：ΔP/P ≈ -D_mod * Δy + 0.5 * Conv * (Δy)^2
    price_change_ratio = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)
    price_drop_pct = price_change_ratio * 100   # 转为百分比形式（例如 -4.51 表示下跌 4.51%）

    # ---------- 输出结果 ----------
    result = {
        'price_drop_pct': price_drop_pct
    }
    print(result)

if __name__ == '__main__':
    main()
