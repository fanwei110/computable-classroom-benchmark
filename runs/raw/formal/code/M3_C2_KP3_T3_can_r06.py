import numpy as np

# ==================== 债券参数设置 ====================
F = 100.0         # 面值
T = 7             # 期限（年）
c = 0.046         # 票息率
y = 0.053         # 当前收益率
delta_y = 0.008   # 收益率上升幅度（80个基点）

# 假设：每年付息1次（国内《证券投资学》未指明时的默认惯例）
# 构造现金流时间与金额
t = np.arange(1, T + 1)
cf = np.full(T, F * c)
cf[-1] += F  # 最后一期加上面值

# ==================== 1. 计算当前收益率下的利率敏感性 ====================
# 贴现因子
df = (1 + y) ** -t

# 当前债券价格
P0 = np.sum(cf * df)

# 麦考利久期
mac_duration = np.sum(t * cf * df) / P0

# 修正久期
mod_duration = mac_duration / (1 + y)

# 凸性 (Convexity)
# 根据定义：C = (1/P) * d^2P/dy^2 = sum[ t(t+1) * CF / (1+y)^(t+2) ] / P
convexity = np.sum(t * (t + 1) * cf * df) / (P0 * (1 + y)**2)

# ==================== 2. 估算收益率上升80个基点的价格影响 ====================
# 使用久期与凸性进行二阶近似估算价格变动百分比
# ΔP/P ≈ -D_mod * Δy + 0.5 * Convexity * (Δy)^2
price_drop_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# （附加：计算精确跌幅供课堂对比演示）
df_new = (1 + y + delta_y) ** -t
P_new = np.sum(cf * df_new)
exact_drop_pct = (P_new - P0) / P0

# ==================== 打印结果供投屏展示 ====================
print("="*50)
print("【债券定价与久期、凸性 - 课堂计算结果】")
print("="*50)
print(f"当前债券价格 (P0):          \t{P0:.4f}")
print(f"麦考利久期 (MacDuration):   \t{mac_duration:.4f} 年")
print(f"修正久期 (ModDuration):     \t{mod_duration:.4f}")
print(f"凸性 (Convexity):           \t{convexity:.4f}")
print("-"*50)
print(f"收益率上升 80bp 后估算跌幅: \t{price_drop_pct:.4%}")
print(f"收益率上升 80bp 后精确跌幅: \t{exact_drop_pct:.4%}")
print(f"(估算误差: \t\t\t{abs(price_drop_pct - exact_drop_pct):.4%})")
print("="*50)

# ==================== 3. 把跌幅存入 result ====================
result = {
    'price_drop_pct': price_drop_pct
}
