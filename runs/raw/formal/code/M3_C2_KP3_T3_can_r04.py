import numpy as np

# ==========================================
# 债券基本参数
# ==========================================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
n_years = 7                 # 期限 7年
y_current = 0.053           # 当前收益率 5.3%
delta_y = 0.008             # 收益率上升 80 个基点

# ==========================================
# 1. 计算债券在当前收益率下的利率敏感性
# ==========================================
# 构造现金流与对应期数
periods = np.arange(1, n_years + 1)
cash_flows = np.full(n_years, face_value * coupon_rate)
cash_flows[-1] += face_value  # 最后一期加入面值

# 贴现因子
discount_factors = (1 + y_current) ** periods

# 各期现金流现值
pv_cf = cash_flows / discount_factors

# 当前债券价格
price = np.sum(pv_cf)

# 麦考利久期
macaulay_duration = np.sum(periods * pv_cf) / price

# 修正久期
modified_duration = macaulay_duration / (1 + y_current)

# 凸性
convexity = np.sum(periods * (periods + 1) * cash_flows / (1 + y_current) ** (periods + 2)) / price

# ==========================================
# 2. 估算收益率上升 80 个基点的价格影响
# ==========================================
# 根据泰勒展开式估算价格变动百分比:
# dP/P ≈ -Modified_Duration * dy + 0.5 * Convexity * dy^2
price_change_pct = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# ==========================================
# 3. 输出结果
# ==========================================
# price_drop_pct 为价格变动百分比，负数代表价格下跌
result = {
    'price_drop_pct': price_change_pct
}

# 用于课堂投屏展示的计算过程打印（可选，方便教师讲解）
print(f"当前债券价格: {price:.4f}")
print(f"修正久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"估算价格变动百分比: {price_change_pct:.4%}")
print(f"结果字典: {result}")
