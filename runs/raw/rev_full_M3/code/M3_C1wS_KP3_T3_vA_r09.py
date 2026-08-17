import numpy as np

# ================= 1. 基础参数设定 =================
# 题目给定参数
face_value = 100          # 面值
coupon_rate = 0.046       # 票息率 4.6%
y = 0.053                 # 当前收益率 5.3%
T = 7                     # 期限 7年
delta_y = 0.008           # 收益率上升 80 个基点 (0.8%)

# 假设：每年付息一次（符合未指明时的默认学术惯例）
# ================= 2. 计算现金流 =================
times = np.arange(1, T + 1)
cash_flows = np.full(T, face_value * coupon_rate)
cash_flows[-1] += face_value  # 最后一期偿还本金

# ================= 3. 计算利率敏感性 (久期与凸性) =================
# 贴现因子
discount_factors = (1 + y) ** times

# 现金流现值
pv_cash_flows = cash_flows / discount_factors

# 当前债券价格
P = np.sum(pv_cash_flows)

# 麦考利久期
mac_duration = np.sum(times * pv_cash_flows) / P

# 修正久期 = 麦考利久期 / (1 + y)
mod_duration = mac_duration / (1 + y)

# 凸性 = (1/P) * Σ [ CF_t * t * (t+1) / (1+y)^(t+2) ]
convexity = np.sum(cash_flows * times * (times + 1) / ((1 + y) ** (times + 2))) / P

# ================= 4. 估算价格影响 =================
# 价格变动百分比近似公式: ΔP/P ≈ -D* × Δy + (1/2) × C × (Δy)^2
# 跌幅即价格变动的百分比（预期为一个负数）
price_drop_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# ================= 5. 输出结果 =================
result = {
    'price_drop_pct': price_drop_pct
}

# 课堂投屏辅助打印（直观展示计算过程与对比）
print(f"【当前状态】")
print(f"债券当前价格 (P0): {P:.4f} 元")
print(f"修正久期: {mod_duration:.4f}")
print(f"凸性: {convexity:.4f}\n")

print(f"【估算：收益率上升 80bp】")
print(f"久期效应 (-D* × Δy): {-mod_duration * delta_y:.4%}")
print(f"凸性效应 (0.5 × C × Δy²): {0.5 * convexity * (delta_y ** 2):.4%}")
print(f"估算跌幅 (price_drop_pct): {price_drop_pct:.4%}\n")

# 验证：精确价格计算对比
P_new = np.sum(cash_flows / ((1 + y + delta_y) ** times))
exact_drop_pct = (P_new - P) / P
print(f"【验证：精确价格重估】")
print(f"新价格 (P1): {P_new:.4f} 元")
print(f"精确跌幅: {exact_drop_pct:.4%}")
print(f"久期-凸性估算误差: {abs(price_drop_pct - exact_drop_pct):.4%}")
