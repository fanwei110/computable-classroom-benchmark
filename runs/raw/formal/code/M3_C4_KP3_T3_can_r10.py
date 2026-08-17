import numpy as np

# ========== 债券参数 ==========
face_value = 100        # 面值
coupon_rate = 0.046     # 票息率 4.6%
y = 0.053               # 收益率 5.3%
T = 7                   # 期限 7 年
dy = 0.008              # 收益率上升 80 个基点

# ========== 现金流与时间 ==========
# 前 T-1 期现金流为票息，第 T 期现金流为票息+面值
cash_flows = np.array([face_value * coupon_rate] * (T - 1) + [face_value * (1 + coupon_rate)])
times = np.arange(1, T + 1)

# ========== 贴现因子 ==========
discount_factors = (1 + y) ** times

# ========== 债券定价 ==========
P = np.sum(cash_flows / discount_factors)

# ========== 麦考利久期 ==========
# MacD = Σ [t * CF_t / (1+y)^t] / P
mac_dur = np.sum(times * cash_flows / discount_factors) / P

# ========== 修正久期 ==========
# ModD = MacD / (1+y)
mod_dur = mac_dur / (1 + y)

# ========== 估算价格跌幅 ==========
# 课程经验法则：dP/P = -D_mod × dy
# 跌幅大小为正的小数
price_drop_pct = mod_dur * dy

# ========== 输出结果 ==========
result = {'price_drop_pct': price_drop_pct}

# （如果需要当堂打印验证，可取消下面注释）
# print(f"当前债券价格 P = {P:.4f}")
# print(f"麦考利久期 MacD = {mac_dur:.4f} 年")
# print(f"修正久期 ModD = {mod_dur:.4f} 年")
# print(f"收益率上升 80bps 后的价格跌幅估算 = {price_drop_pct:.4%}")
# print(result)
