import numpy as np

# ================== 债券参数设置 ==================
F = 100          # 面值
c = 0.046        # 票息率 (4.6%)
n = 7            # 期限 (年)
y = 0.053        # 到期收益率 (5.3%)

# 假设：每年付息一次，到期一次还本付息

# ================== 步骤1：计算价格 ==================
# 生成时间序列 t = [1, 2, ..., 7]
t = np.arange(1, n + 1)

# 生成现金流：前 6 期为票息，第 7 期为票息 + 面值
cf = np.full(n, F * c)
cf[-1] += F

# 计算贴现因子与现值
discount_factors = (1 + y) ** -t
pv = cf * discount_factors

# 价格为现金流现值之和
price = np.sum(pv)

# ================== 步骤2：计算麦考利久期与修正久期 ==================
# 麦考利久期 = (t * PV) 之和 / 价格
macaulay_duration_years = np.sum(t * pv) / price

# 修正久期 = 麦考利久期 / (1 + y)
modified_duration_years = macaulay_duration_years / (1 + y)

# ================== 步骤3：计算凸性 ==================
# 凸性 = 1/P * d^2P/dy^2 = 1/(P*(1+y)^2) * sum(t*(t+1)*CF_t / (1+y)^t)
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + y) ** 2)

# ================== 步骤4：填充 result ==================
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

# 投屏展示结果
print("债券定价与久期、凸性计算结果：")
for key, value in result.items():
    print(f"{key:30s}: {value}")
