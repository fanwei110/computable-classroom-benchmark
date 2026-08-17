import numpy as np

# ==================== 债券参数设定 ====================
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率 4.6%
ytm = 0.053               # 当前收益率 5.3%
n = 7                     # 期限 7 年（假设每年付息一次）
delta_y = 0.008           # 收益率上升 80 个基点 (0.80%)

# ==================== 1. 计算债券价格及利率敏感性 ====================
# 构建现金流与时间数组
t = np.arange(1, n + 1)
cf = np.full(n, face_value * coupon_rate)
cf[-1] += face_value      # 最后一期加入面值

# 计算贴现因子与现值
discount_factors = (1 + ytm) ** t
pv = cf / discount_factors

# 债券当前价格
price = np.sum(pv)

# 麦考利久期
mac_duration = np.sum(t * pv) / price

# 修正久期：衡量价格对收益率变动的线性敏感性
mod_duration = mac_duration / (1 + ytm)

# 凸性：衡量价格-收益率曲线的弯曲程度，提供二阶修正
# 公式：C = [1/(P*(1+y)^2)] * Σ [t*(t+1)*CF_t / (1+y)^t]
# 等价于 C = Σ [t*(t+1)*PV_t / (P*(1+y)^2)]
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm)**2)

# ==================== 2. 估算收益率上升 80bp 的价格影响 ====================
# 使用泰勒展开式（久期 + 凸性）估算价格变动百分比
# ΔP/P ≈ -D_mod * Δy + (1/2) * C * (Δy)^2
price_change_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# 跌幅（取价格变动百分比的相反数，以正数表示跌幅）
price_drop_pct = -price_change_pct

# ==================== 3. 把跌幅存入 result ====================
result = {
    'price_drop_pct': price_drop_pct
}

# （以下为课堂投屏友好打印，非必须但有助于展示）
print(f"债券当前价格: {price:.4f}")
print(f"修正久期: {mod_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"收益率上升80bp估算跌幅: {price_drop_pct:.4%}")
print(f"\n结果字典 result: {result}")
