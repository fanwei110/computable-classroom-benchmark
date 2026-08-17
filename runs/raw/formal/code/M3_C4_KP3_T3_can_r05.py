import numpy as np

# ==================== 债券参数设置 ====================
F = 100           # 面值
c = 0.046         # 票息率 4.6%
y = 0.053         # 收益率 5.3%
T = 7             # 期限 7年
dy = 0.008        # 收益率变动 80个基点

# ==================== 现金流与贴现 ====================
# 构建各期现金流：第1到第6年为票息，第7年为票息+面值
t_array = np.arange(1, T + 1)
cf_array = np.full(T, F * c)
cf_array[-1] += F

# 计算各期贴现因子
discount_factors = (1 + y) ** t_array

# 计算债券当前价格 P
pv_array = cf_array / discount_factors
P = np.sum(pv_array)

# ==================== 麦考利久期与修正久期 ====================
# 麦考利久期 D_mac = Σ [ t * CF_t / (1+y)^t ] / P
D_mac = np.sum(t_array * pv_array) / P

# 修正久期 D_mod = D_mac / (1+y) （课程约定：年复利）
D_mod = D_mac / (1 + y)

# ==================== 估算价格跌幅 ====================
# 课程经验法则（一阶近似）：dP/P = -D_mod × dy
price_drop_ratio = -D_mod * dy

# 取跌幅大小为正的小数
price_drop_pct = abs(price_drop_ratio)

# ==================== 结果输出 ====================
result = {
    'price_drop_pct': price_drop_pct
}

# 课堂投屏展示辅助打印（可选，便于教师讲解）
print(f"债券当前价格 P = {P:.4f}")
print(f"麦考利久期 D_mac = {D_mac:.4f} 年")
print(f"修正久期 D_mod = {D_mod:.4f} 年")
print(f"收益率上升 {dy*100:.1f} 个基点，一阶近似估算价格跌幅: {price_drop_pct:.4f} (即 {price_drop_pct*100:.2f}%)")
print(f"result = {result}")
