import numpy as np

def main():
    # ----- 债券参数 -----
    face_value = 100.0        # 面值
    coupon_rate = 0.046       # 票面利率 4.6%
    ytm = 0.053               # 当前到期收益率 5.3%
    maturity = 7              # 期限 7 年
    delta_y = 0.008           # 收益率上升 80 bp = 0.80%
    
    # 假设每年付息一次（题目未指定频率，采用最常见的按年付息）
    freq = 1
    
    # ----- 现金流时间与金额 -----
    # 时间点：1, 2, ..., maturity
    times = np.arange(1, maturity + 1, dtype=float)
    coupon = face_value * coupon_rate
    cashflows = np.full(maturity, coupon)
    cashflows[-1] += face_value   # 最后一年包含本金
    
    # ----- 贴现因子与现值 -----
    discount = (1 + ytm) ** (-times)
    pv_cf = cashflows * discount
    price = np.sum(pv_cf)
    
    # ----- 麦考利久期 -----
    weighted_times = times * pv_cf
    macaulay_duration = np.sum(weighted_times) / price
    
    # ----- 修正久期 -----
    modified_duration = macaulay_duration / (1 + ytm)
    
    # ----- 凸性 -----
    # 凸性公式：Σ [ t*(t+1)*CF_t / (1+y)^(t+2) ] / P
    # 等价于 Σ [ t*(t+1)*pv_cf ] / (P * (1+y)^2)
    weighted_convexity = times * (times + 1) * pv_cf
    convexity = np.sum(weighted_convexity) / (price * (1 + ytm)**2)
    
    # ----- 利用久期与凸性估算价格变化百分比 -----
    # dP/P ≈ - ModD * Δy + 0.5 * Conv * (Δy)^2
    dp_pct_estimate = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)
    
    # 跌幅百分比（正数表示下跌）
    price_drop_pct_estimate = -dp_pct_estimate * 100.0
    
    # （可选验证）直接用新收益率计算价格，得到精确跌幅
    ytm_new = ytm + delta_y
    discount_new = (1 + ytm_new) ** (-times)
    price_new = np.sum(cashflows * discount_new)
    price_drop_pct_exact = (price - price_new) / price * 100.0
    
    # ----- 结果字典 -----
    result = {
        'price_drop_pct': price_drop_pct_estimate  # 基于久期+凸性估算的跌幅百分比
    }
    
    # 打印结果（供投屏展示）
    print("债券基本信息：面值100，票面利率4.6%，当前收益率5.3%，期限7年，按年付息")
    print(f"当前价格：{price:.4f}")
    print(f"麦考利久期：{macaulay_duration:.4f} 年")
    print(f"修正久期：{modified_duration:.4f}")
    print(f"凸性：{convexity:.4f}")
    print(f"收益率上升 {delta_y*100:.0f} bp 后的估算跌幅：{price_drop_pct_estimate:.4f}%")
    print(f"（精确跌幅验证：{price_drop_pct_exact:.4f}%）")
    print("\n结果字典：", result)
    
    return result

if __name__ == "__main__":
    result = main()
