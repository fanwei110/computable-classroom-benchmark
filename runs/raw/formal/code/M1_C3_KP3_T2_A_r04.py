import numpy as np
import matplotlib.pyplot as plt
import os

def bond_price(FV, C, T, y):
    """计算债券精确价格（年复利）"""
    price = 0.0
    for t in range(1, T + 1):
        price += C * FV / ((1 + y) ** t)
    price += FV / ((1 + y) ** T)
    return price

def macaulay_duration(FV, C, T, y):
    """计算Macaulay久期"""
    dur = 0.0
    P = bond_price(FV, C, T, y)
    for t in range(1, T + 1):
        dur += t * C * FV / ((1 + y) ** t)
    dur += T * FV / ((1 + y) ** T)
    dur /= P
    return dur

def modified_duration(FV, C, T, y):
    """计算修正久期"""
    dur = macaulay_duration(FV, C, T, y)
    return dur / (1 + y)

# 参数
FV = 100
C = 0.046
T = 7
y_initial = 0.053
delta_y = 0.01  # 100个基点

# 计算初始价格和久期
P_initial = bond_price(FV, C, T, y_initial)
mod_dur = modified_duration(FV, C, T, y_initial)

# 收益率上升100bp后的精确价格
y_new = y_initial + delta_y
P_new = bond_price(FV, C, T, y_new)

# 久期近似价格变化
dur_approx_change = -mod_dur * delta_y

# 绘制价格随收益率变化的曲线
y_range = np.linspace(0.02, 0.09, 100)
prices_exact = [bond_price(FV, C, T, y) for y in y_range]
prices_approx = [P_initial * (1 - mod_dur * (y - y_initial)) for y in y_range]

plt.figure(figsize=(10, 6))
plt.plot(y_range, prices_exact, label='Exact Price', color='blue')
plt.plot(y_range, prices_approx, label='Duration Approximation', color='red', linestyle='--')
plt.xlabel('Yield')
plt.ylabel('Price')
plt.title('Bond Price vs Yield')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'bond_price_vs_yield.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'price_at_up100bp': P_new,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
