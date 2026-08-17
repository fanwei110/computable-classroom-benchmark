import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years = 7
ytm = 0.053

# 现金流
cashflows = np.full(years, face_value * coupon_rate)
cashflows[-1] += face_value  # 最后一年加回本金

# 时间数组（从1到7）
t = np.arange(1, years + 1)

# 贴现因子
discount = (1 + ytm) ** (-t)

# 1. 价格：现金流贴现之和
price = np.sum(cashflows * discount)

# 2. 麦考利久期（年）
macaulay_duration = np.sum(t * cashflows * discount) / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 3. 凸性（年平方）
convexity = np.sum(t * (t + 1) * cashflows * (1 + ytm) ** (-t - 2)) / price

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 打印结果
print("债券价格:", round(result['price'], 4))
print("麦考利久期（年）:", round(result['macaulay_duration_years'], 4))
print("修正久期（年）:", round(result['modified_duration_years'], 4))
print("凸性（年平方）:", round(result['convexity'], 4))
