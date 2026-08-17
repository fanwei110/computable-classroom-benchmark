import numpy as np

# ==================== 债券参数设定 ====================
F = 100          # 面值 (Face Value)
c = 0.046        # 票息率 (Coupon Rate)，4.6%
y = 0.053        # 当前收益率 (Yield to Maturity)，5.3%
T = 7            # 期限 (Maturity)，7年 (假设按年付息)
dy = 0.008       # 收益率变动 (Delta Yield)，上升80个基点 = 0.80%

# ==================== 1. 计算当前收益率下的利率敏感性 ====================
# 生成现金流时间序列与现金流
t = np.arange(1, T + 1)
cf = np.full(T, F * c)  # 票息现金流
cf[-1] += F             # 最后一期加入面值

# 贴现因子与现值
discount_factors = (1 + y) ** t
pv = cf / discount_factors

# 债券当前价格
P = np.sum(pv)

# 麦考利久期
# MacD = sum(t * PV(CF_t)) / P
mac_duration = np.sum(t * pv) / P

# 修正久期
# ModD = MacD / (1 + y)
mod_duration = mac_duration / (1 + y)

# 凸性
# Conv = sum(t * (t+1) * PV(CF_t)) / (P * (1+y)^2)
convexity = np.sum(t * (t + 1) * pv) / (P * (1 + y)**2)

# ==================== 2. 估算收益率上升80个基点的价格影响 ====================
# 使用久期和凸性估算价格变动百分比 (泰勒展开式)
# ΔP/P ≈ -ModD * Δy + 0.5 * Conv * (Δy)^2
price_change_pct = -mod_duration * dy + 0.5 * convexity * (dy ** 2)

# "跌幅"通常以正数表示下降的幅度，因此取估算结果的相反数
price_drop_pct = -price_change_pct

# ==================== 3. 存入结果 ====================
result = {
    'price_drop_pct': price_drop_pct
}

# -------------------- 课堂投屏展示区 --------------------
print("="*50)
print(f"债券当前价格 (Price)          : {P:.4f}")
print(f"麦考利久期    : {mac_duration:.4f} 年")
print(f"修正久期      : {mod_duration:.4f}")
print(f"凸性          : {convexity:.4f}")
print("="*50)
print(f"收益率上升 (基点)             : {dy * 10000:.0f} bp")
print(f"久期效应导致的价格变动        : {-mod_duration * dy:.4%}")
print(f"凸性效应导致的价格变动        : {0.5 * convexity * (dy ** 2):.4%}")
print(f"综合价格变动估算              : {price_change_pct:.4%}")
print(f"预计跌幅幅度                  : {price_drop_pct:.4%}")
print("="*50)
print(f"最终结果 result: {result}")
