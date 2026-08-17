import numpy as np

# 债券基本参数
T = 7              # 期限（年）
F = 100            # 面值
c = 0.046          # 票息率（小数表示）
y = 0.053          # 收益率（小数表示）
dy = 0.008         # 收益率变动（80个基点，小数表示）

# 生成现金流时间点与现金流
t = np.arange(1, T + 1)
coupons = np.full(T, c * F)
coupons[-1] += F   # 最后一期加上面值本金

# 计算贴现因子与贴现现金流
discount_factors = (1 + y) ** t
dcf = coupons / discount_factors

# 1. 计算当前收益率下的债券价格
P = np.sum(dcf)

# 计算麦考利久期 (Macaulay Duration)
mac_duration = np.sum(t * dcf) / P

# 计算修正久期 (Modified Duration)，按年复利约定：D_mod = D_mac / (1+y)
mod_duration = mac_duration / (1 + y)

# 2. 套用课程经验法则 dP/P = -D_mod * dy，计算价格变动百分比
dp_pct = -mod_duration * dy

# 3. 提取跌幅大小，作为正的小数存入结果
price_drop_pct = abs(dp_pct)

# 按输出契约存入字典
result = {'price_drop_pct': price_drop_pct}

# (可选：便于课堂投屏展示计算过程与结果)
print(f"债券价格 P = {P:.4f}")
print(f"麦考利久期 D_mac = {mac_duration:.4f} 年")
print(f"修正久期 D_mod = {mod_duration:.4f} 年")
print(f"收益率上升 {dy*100:.0f} 个基点，价格大约跌幅 = {price_drop_pct:.4f} (即 {price_drop_pct*100:.2f}%)")
print(f"result = {result}")
