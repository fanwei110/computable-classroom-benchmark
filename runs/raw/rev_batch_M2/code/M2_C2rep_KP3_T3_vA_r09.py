import numpy as np

def bond_price(face, coupon_rate, ytm, maturity, freq=1):
    """
    计算债券价格（每年付息 freq=1 次）。
    
    参数:
        face: 面值
        coupon_rate: 票息率（年化）
        ytm: 到期收益率（年化）
        maturity: 剩余年限（年）
        freq: 年付息次数，默认为1（每年付息）
    
    返回:
        债券价格
    """
    periods = int(maturity * freq)
    coupon = face * coupon_rate / freq
    discount_factors = (1 + ytm / freq) ** -np.arange(1, periods + 1)
    cashflows = np.full(periods, coupon)
    cashflows[-1] += face  # 最后一期支付本金
    price = np.sum(cashflows * discount_factors)
    return price

def main():
    # 债券参数
    face = 100.0          # 面值
    coupon_rate = 0.046   # 票息率 4.6%
    ytm = 0.053           # 初始收益率 5.3%
    maturity = 7.0        # 7年期
    delta_y = 0.0080      # 收益率上升 80 个基点

    # 1. 计算当前收益率下的债券价格
    price_old = bond_price(face, coupon_rate, ytm, maturity)
    
    # 计算收益率变动后的债券价格
    ytm_new = ytm + delta_y
    price_new = bond_price(face, coupon_rate, ytm_new, maturity)
    
    # 2. 计算价格变动百分比（负值表示下跌）
    price_change_pct = (price_new - price_old) / price_old * 100
    
    # 3. 跌幅定义为价格下跌幅度的正百分比
    price_drop_pct = -price_change_pct  # 收益率上升时价格下跌，所以取正数

    # 将结果存入字典
    result = {'price_drop_pct': price_drop_pct}
    
    # 输出结果以便投屏展示
    print("债券定价与利率敏感性分析")
    print("=" * 40)
    print(f"面值: {face}, 票息率: {coupon_rate*100}%, 初始收益率: {ytm*100}%")
    print(f"当前价格: {price_old:.4f}")
    print(f"收益率上升 {delta_y*100:.0f} 个基点后新收益率: {ytm_new*100}%")
    print(f"新价格: {price_new:.4f}")
    print(f"价格变动百分比: {price_change_pct:.4f}%")
    print(f"价格跌幅: {price_drop_pct:.4f}%")
    print("=" * 40)
    print("result =", result)

if __name__ == "__main__":
    main()
