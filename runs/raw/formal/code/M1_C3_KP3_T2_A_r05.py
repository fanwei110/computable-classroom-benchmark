import numpy as np
import matplotlib.pyplot as plt
import os

def bond_price(y, C, F, T):
    """计算债券价格（年复利）"""
    price = sum([C / (1 + y) ** t for t in range(1, T + 1)]) + F / (1 + y) ** T
    return price

def macaulay_duration(y, C, F, T):
    """计算麦考利久期"""
    weighted_cashflows = sum([t * C / (1 + y) ** t for t in range(1, T + 1)]) + T * F / (1 + y) ** T
    price = bond_price(y, C, F, T)
    return weighted_cashflows / price

def modified_duration(y, C, F, T):
    """计算修正久期"""
    mac_dur = macaulay_duration(y, C, F, T)
    return mac_dur / (1 + y)

# 参数
C = 4.6  # 年票息
F = 100  # 面值
T = 7    # 年限
y0 = 0.053  # 初始收益率

# 收益率范围
y_range = np.linspace(0.02, 0.09, 100)
prices_exact = [bond_price(y, C, F, T) for y in y_range]

# 久期近似（在y0处线性近似）
mod_dur = modified_duration(y0, C, F, T)
price0 = bond_price(y0, C, F, T)
prices_approx = [price0 * (1 - mod_dur * (y - y0)) for y in y_range]

# 收益率上升100bp后的精确价格
y_up100bp = y0 + 0.01
price_up100bp = bond_price(y_up100bp, C, F, T)

# 久期近似的相对价格变化
dur_approx_change = -mod_dur * 0.01

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(y_range, prices_exact, label='Exact', color='blue')
plt.plot(y_range, prices_approx, label='Duration Approximation', color='red', linestyle='--')
plt.xlabel('Yield')
plt.ylabel('Bond Price')
plt.title('Bond Price vs Yield (Exact vs Duration Approximation)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'bond_price_vs_yield.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
