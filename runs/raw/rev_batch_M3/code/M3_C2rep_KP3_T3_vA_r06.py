import numpy as np

# ==================== 债券参数 ====================
F = 100          # 面值
c = 0.046        # 票息率 (4.6%)
y = 0.053        # 当前收益率 (5.3%)
n = 7            # 期限 (年)
delta_y = 0.008  # 收益率上升 80 个基点 (0.80%)

# 假设：债券按年付息
C = F * c        # 年票息金额

# ==================== 1. 计算当前价格与利率敏感性 ====================
# 生成现金流时间与金额
t_arr = np.arange(1, n + 1)
cf_arr = np.full(n, C)
cf_arr[-1] += F  # 最后一期还本付息

# 贴现因子与当前价格
discount = (1 + y) ** t_arr
P0 = np.sum(cf_arr / discount)

# Macaulay 久期
pv_cf = cf_arr / discount
MacD = np.sum(t_arr * pv_cf) / P0

# 修正久期 (Modified Duration)
ModD = MacD / (1 + y)

# 凸性 (Convexity)
# 二阶导数项：t*(t+1)*CF / (1+y)^(t+2)
Conv = np.sum(t_arr * (t_arr + 1) * cf_arr / (1 + y)**(t_arr + 2)) / P0

# ==================== 2. 估算收益率上升 80 个基点的价格影响 ====================
# 使用泰勒展开二阶近似估算价格变动百分比：
# ΔP/P ≈ -ModD * Δy + 0.5 * Conv * (Δy)^2
price_drop_pct = -ModD * delta_y + 0.5 * Conv * (delta_y ** 2)

# ==================== 3. 存储结果 ====================
# price_drop_pct 存储的是价格变动百分比（以小数表示，负号代表下跌）
result = {'price_drop_pct': price_drop_pct}

# 为了课堂展示方便，可打印核心结果（非强制，不改变 result）
print(f"当前债券价格: {P0:.4f}")
print(f"修正久期: {ModD:.4f}")
print(f"凸性: {Conv:.4f}")
print(f"估算跌幅(price_drop_pct): {price_drop_pct:.4%}")
