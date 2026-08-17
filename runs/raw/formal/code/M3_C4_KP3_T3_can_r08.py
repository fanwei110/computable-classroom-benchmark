import numpy as np

# ==================== 债券参数设置 ====================
T = 7                      # 期限（年）
F = 100                    # 面值
coupon_rate = 0.046        # 票息率 (小数表示)
y = 0.053                  # 收益率 (小数表示)
dy = 0.008                 # 收益率变动量 (80个基点，小数表示)

# ==================== 计算现金流与贴现因子 ====================
# 构建每期现金流，前 T-1 年为票息，第 T 年为票息+面值
CF = np.full(T, coupon_rate * F)
CF[-1] += F

# 构建时间序列 t = 1, 2, ..., T
t = np.arange(1, T + 1)

# 贴现因子 (1+y)^t
discount_factors = (1 + y) ** t

# ==================== 计算债券价格与久期 ====================
# 1. 计算当前收益率下的债券价格 P
P = np.sum(CF / discount_factors)

# 2. 计算麦考利久期 MacDur = Σ[t * CF_t / (1+y)^t] / P
MacDur = np.sum(t * CF / discount_factors) / P

# 3. 计算修正久期 ModDur = MacDur / (1+y)
ModDur = MacDur / (1 + y)

# ==================== 估算价格跌幅 ====================
# 套用课程一阶近似经验法则：dP/P = -D_mod × dy
# 题目要求跌幅大小作为正的小数，因此取绝对值
price_drop_pct = ModDur * dy

# ==================== 输出结果 ====================
result = {
    'price_drop_pct': price_drop_pct
}

# 课堂投屏展示辅助信息（方便教师讲解验证）
print(f"债券价格 P = {P:.4f}")
print(f"麦考利久期 MacDur = {MacDur:.4f} 年")
print(f"修正久期 ModDur = {ModDur:.4f}")
print(f"收益率变动 dy = {dy} ({dy*100:.1f} bps)")
print(f"预计价格跌幅 dP/P = {price_drop_pct:.6f} ({price_drop_pct*100:.4f}%)")
print("-" * 30)
print(f"result = {result}")
