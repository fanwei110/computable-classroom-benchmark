import numpy as np

# ==========================================
// 假设处理说明：
// 1. 债券按年付息，现金流在每年年末发生
// 2. 收益率变动 80 个基点 = 0.008
// 3. 凸性采用连续复利/标准泰勒展开定义：Convexity = (1/P) * Σ [t(t+1)CF / (1+y)^(t+2)]
// 4. 价格变动百分比采用二阶泰勒展开近似：ΔP/P ≈ -D_mod * Δy + 0.5 * Convexity * (Δy)^2
// 5. 输出 price_drop_pct 为跌幅的小数形式（如 0.045 表示下跌 4.5%），与金融工程中 pd.pct_change() 习惯一致
# ==========================================

def calculate_bond_price_drop():
    # 债券基本参数
    face_value = 100.0
    coupon_rate = 0.046
    ytm = 0.053
    maturity = 7
    delta_y = 0.008  # 收益率上升80个基点
    
    # 构造现金流与时间序列
    coupon = face_value * coupon_rate
    cash_flows = np.array([coupon] * (maturity - 1) + [coupon + face_value])
    times = np.arange(1, maturity + 1)
    
    # 1. 计算该债券在当前收益率下的利率敏感性
    # 贴现因子与现值
    discount_factors = (1 + ytm) ** times
    pv_of_cfs = cash_flows / discount_factors
    price = np.sum(pv_of_cfs)
    
    # 麦考利久期
    mac_duration = np.sum(times * pv_of_cfs) / price
    # 修正久期
    mod_duration = mac_duration / (1 + ytm)
    
    # 凸性
    convexity = np.sum(times * (times + 1) * cash_flows / (1 + ytm)**(times + 2)) / price
    
    # 2. 估算收益率上升 80 个基点的价格影响
    # 价格变动百分比近似 (二阶泰勒展开)
    pct_change = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)
    
    # 3. 把跌幅存入 result
    # "跌幅"取变动绝对值，以小数形式表现（如 0.045 表示下跌 4.5%）
    price_drop_pct = -pct_change
    
    result = {'price_drop_pct': price_drop_pct}
    return result

# 执行计算并存入result
result = calculate_bond_price_drop()

# 用于课堂投屏展示的结果打印
print(f"估算结果: {result}")
print(f"即债券价格大约下跌 {result['price_drop_pct']*100:.2f}%")
