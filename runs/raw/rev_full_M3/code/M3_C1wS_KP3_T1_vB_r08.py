import numpy as np

# ==================== 债券参数设定 ====================
face_value = 100          # 面值
coupon_rate = 0.046       # 票息率 4.6%
years_to_maturity = 7     # 期限 7年
ytm = 0.053              # 到期收益率 5.3%

# 假设：题目未指明付息频率，按市场惯例采用【每年付息一次】进行计算

# ==================== 现金流构造 ====================
# 生成各期时间节点 t = [1, 2, 3, 4, 5, 6, 7]
t = np.arange(1, years_to_maturity + 1)

# 各期现金流：1-6期为票息，第7期为票息+面值
cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# 各期贴现因子
discount_factors = (1 + ytm) ** t

# 各期现金流现值
pv_cash_flows = cash_flows / discount_factors

# ==================== 1. 计算债券价格 ====================
# 价格为现金流现值之和
price = np.sum(pv_cash_flows)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 麦考利久期 = 现金流回流时间的加权平均
macaulay_duration = np.sum(t * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1 + ytm)，衡量价格对收益率的线性敏感性
modified_duration = macaulay_duration / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性公式: (1/P) * Σ [ t*(t+1) * CF_t / (1+y)^(t+2) ]
# 在数学上等价于: (1/P) * Σ [ t*(t+1) * PV_t / (1+y)^2 ]
convexity = np.sum(t * (t + 1) * pv_cash_flows) / (price * (1 + ytm)**2)

# ==================== 4. 填充 result 字典 ====================
# 保留4位小数以保持课堂投屏展示的整洁与精确度
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration, 4),
    'modified_duration_years': round(modified_duration, 4),
    'convexity': round(convexity, 4)
}

# 课堂投屏打印展示
print("="*45)
print("《证券投资学》- 债券定价与久期、凸性计算")
print("="*45)
print(f"债券假设: 面值{face_value}, 票息{coupon_rate*100}%, {years_to_maturity}年, YTM={ytm*100}% (年付息)")
print("-"*45)
for key, value in result.items():
    if 'duration' in key:
        print(f"{key:<30}: {value:.4f} 年")
    elif key == 'convexity':
        print(f"{key:<30}: {value:.4f}")
    else:
        print(f"{key:<30}: {value:.4f}")
print("="*45)
