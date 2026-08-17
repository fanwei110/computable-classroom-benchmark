import numpy as np

# ==================== 债券参数设置 ====================
face_value = 100        # 面值
coupon_rate = 0.046     # 票息率 4.6%
ytm = 0.053             # 当前收益率 5.3%
n_years = 7             # 期限 7 年
delta_y = 0.008         # 收益率上升 80 个基点 (0.8%)

# ==================== 1. 计算债券在当前收益率下的利率敏感性 ====================
# 构建现金流：前 6 年为票息，第 7 年为票息 + 面值
cash_flows = np.array([face_value * coupon_rate] * (n_years - 1) + 
                       [face_value * (1 + coupon_rate)])
times = np.arange(1, n_years + 1)

# 计算贴现因子与现值
discount_factors = (1 + ytm) ** times
pv_cash_flows = cash_flows / discount_factors

# 债券当前价格
price = np.sum(pv_cash_flows)

# 麦考利久期 (Macaulay Duration)
mac_duration = np.sum(times * pv_cash_flows) / price

# 修正久期 (Modified Duration) - 衡量价格对收益率的一阶敏感性
mod_duration = mac_duration / (1 + ytm)

# 凸性 (Convexity) - 衡量价格对收益率的二阶敏感性
# 凸性公式: (1/P) * sum[ t*(t+1)*CF / (1+y)^(t+2) ]
convexity = np.sum(times * (times + 1) * cash_flows / ((1 + ytm) ** (times + 2))) / price

# ==================== 2. 估算收益率上升 80 个基点的价格影响 ====================
# 价格变动百分比的二阶近似：dP/P ≈ -ModD * dy + 0.5 * Conv * dy^2
price_change_pct = (-mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)) * 100

# 跌幅（以价格变动百分比表示，负号代表下跌）
price_drop_pct = price_change_pct

# ==================== 3. 把跌幅存入 result ====================
result = {
    'price_drop_pct': price_drop_pct
}

# 打印结果以便课堂展示
print(f"债券当前价格: {price:.4f}")
print(f"修正久期: {mod_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"收益率上升80bps后的预估跌幅: {price_drop_pct:.4f}%")
print(f"result字典: {result}")

