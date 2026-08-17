import numpy as np

# =====================
# 1. 债券参数设置
# =====================
FV = 100               # 面值
coupon_rate = 0.046     # 票息率 (4.6%)
n = 7                  # 期限 (7年)
y = 0.053              # 当前收益率 (5.3%)
dy = 0.008             # 收益率上升幅度 (80个基点)

# 假设：按年付息，现金流在每年年末发生
t = np.arange(1, n + 1)
C = FV * coupon_rate   # 每年票息

# 构造现金流序列：前6年仅有票息，第7年包含票息和面值
cf = np.full(n, C)
cf[-1] += FV

# =====================
# 2. 计算债券价格与利率敏感性指标
# =====================
# 计算贴现现金流
discount_factors = (1 + y) ** t
dcf = cf / discount_factors

# 债券当前价格
P = np.sum(dcf)

# 麦考利久期 (Macaulay Duration)
D_mac = np.sum(t * dcf) / P

# 修正久期 (Modified Duration)
D_mod = D_mac / (1 + y)

# 凸性 (Convexity)
Conv = np.sum(t * (t + 1) * dcf) / (P * (1 + y) ** 2)

# =====================
# 3. 估算收益率上升 80 个基点的价格影响
# =====================
# 价格变动百分比近似公式: dP/P ≈ -D_mod * dy + 0.5 * Conv * dy^2
pct_change = -D_mod * dy + 0.5 * Conv * dy ** 2

# 题目要求计算“跌多少”，以绝对值形式表示下降的幅度
price_drop_pct = abs(pct_change)

# 课堂投屏打印展示（辅助理解）
print(f"=== 债券定价与久期、凸性分析 ===")
print(f"当前债券价格 P:\t{P:.4f}")
print(f"麦考利久期 D_mac:\t{D_mac:.4f} 年")
print(f"修正久期 D_mod:\t{D_mod:.4f}")
print(f"凸性 Conv:\t\t{Conv:.4f}")
print(f"------------------------------------")
print(f"收益率上升 (基点):\t{dy * 10000:.0f} bp")
print(f"久期影响 (一阶):\t{-D_mod * dy:.4%}")
print(f"凸性影响 (二阶):\t{0.5 * Conv * dy ** 2:.4%}")
print(f"预计价格变动百分比:\t{pct_change:.4%}")
print(f"预计价格跌幅:\t\t{price_drop_pct:.4%}")

# =====================
# 4. 存入结果
# =====================
result = {
    'price_drop_pct': price_drop_pct
}
