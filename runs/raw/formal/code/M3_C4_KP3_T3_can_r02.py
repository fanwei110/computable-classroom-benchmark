import numpy as np

# ================= 债券基本参数 =================
face_value = 100           # 面值
coupon_rate = 0.046        # 票息率 4.6%
ytm = 0.053                # 到期收益率 5.3%
maturity = 7               # 期限 7年
delta_y = 0.008             # 收益率上升 80 个基点

# ================= 1. 计算当前收益率下的修正久期 =================
# 时间序列 t = [1, 2, ..., 7]
t = np.arange(1, maturity + 1)

# 构建现金流：前 6 期为票息，第 7 期为票息 + 面值
cash_flows = np.full(maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# 按年复利计算贴现因子与现值
discount_factors = (1 + ytm) ** t
pv_cash_flows = cash_flows / discount_factors

# 计算债券当前价格 P
P = np.sum(pv_cash_flows)

# 计算麦考利久期: D_mac = Σ[t * PV(CF_t)] / P
mac_duration = np.sum(t * pv_cash_flows) / P

# 计算修正久期: D_mod = D_mac / (1 + y)
mod_duration = mac_duration / (1 + ytm)

# ================= 2. 套用经验法则估算跌幅 =================
# 课程约定一阶近似: dP/P = -D_mod × dy
# 题目要求输出跌幅大小（正的小数），因此取绝对值
price_drop_pct = abs(mod_duration * delta_y)

# ================= 3. 存入结果字典 =================
result = {'price_drop_pct': price_drop_pct}

# -------------------- 投屏辅助打印 --------------------
print(f"【计算过程】")
print(f"债券价格 P          = {P:.4f}")
print(f"麦考利久期 D_mac    = {mac_duration:.4f} 年")
print(f"修正久期 D_mod      = {mod_duration:.4f} 年")
print(f"收益率变动 dy       = {delta_y:.4f}")
print(f"一阶近似跌幅 dP/P   = {price_drop_pct:.6f} (即 {price_drop_pct*100:.4f}%)")
print(f"\n【输出结果】\nresult = {result}")
