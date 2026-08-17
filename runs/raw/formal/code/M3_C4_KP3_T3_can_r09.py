import numpy as np

# 债券基本参数
face_value = 100        # 面值
coupon_rate = 0.046    # 票息率 4.6%
n_years = 7            # 期限 7年
ytm = 0.053            # 收益率 5.3%
dy = 0.008             # 收益率变动 80个基点 (0.8%)

# 1. 计算现金流与现值
times = np.arange(1, n_years + 1)
cash_flows = np.full(n_years, face_value * coupon_rate)
cash_flows[-1] += face_value  # 最后一期还本

# 贴现因子与现值
discount_factors = (1 + ytm) ** times
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# 2. 计算麦考利久期与修正久期
# 麦考利久期 D_mac = Σ[t * PV(CF_t)] / P
mac_duration = np.sum(times * pv_cash_flows) / price

# 修正久期 D_mod = D_mac / (1 + y)
mod_duration = mac_duration / (1 + ytm)

# 3. 套用课程经验法则 dP/P = -D_mod * dy，计算跌幅大小（取正的小数）
price_drop_pct = mod_duration * dy

# 按输出契约存入字典
result = {
    'price_drop_pct': price_drop_pct
}

# 输出结果以便投屏展示
print(result)
