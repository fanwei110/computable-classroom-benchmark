import numpy as np
import matplotlib.pyplot as plt

# 债券基本参数
F = 100               # 面值
c = 0.046             # 票息率
C = F * c             # 票息
T = 7                 # 期限（年）
y0 = 0.053            # 初始YTM
y_range = (0.02, 0.09) # 收益率绘图范围

# 变动幅度设定 (可调参数，修改此值即可调整变动幅度)
delta_y_bp = 100
delta_y = delta_y_bp / 10000

# 计算精确价格的函数
def bond_price(y, C, F, T):
    return sum([C / (1+y)**t for t in range(1, T+1)]) + F / (1+y)**T

# 计算麦考利久期的函数
def mac_duration(y, C, F, T):
    p = bond_price(y, C, F, T)
    return (sum([t * C / (1+y)**t for t in range(1, T+1)]) + T * F / (1+y)**T) / p

# 初始状态计算
P0 = bond_price(y0, C, F, T)
MacD0 = mac_duration(y0, C, F, T)
ModD0 = MacD0 / (1 + y0)  # 修正久期

# 目标要求计算
y_up = y0 + delta_y
price_at_up100bp = bond_price(y_up, C, F, T)
dur_approx_change_up100bp = -ModD0 * delta_y  # 久期法估计的相对变化率

# 生成绘图数据
yields = np.linspace(y_range[0], y_range[1], 500)
exact_prices = [bond_price(y, C, F, T) for y in yields]
# 久期近似价格：P_approx = P0 * (1 - ModD0 * (y - y0))
approx_prices = [P0 * (1 - ModD0 * (y - y0)) for y in yields]

# 绘图
plt.figure(figsize=(10, 6))
line1, = plt.plot(yields * 100, exact_prices, label='精确价格曲线', color='blue', linewidth=2)
line2, = plt.plot(yields * 100, approx_prices, label='久期近似价格 (切线)', color='red', linestyle='--', linewidth=2)

# 标记初始点和变动后的精确点
plt.scatter([y0 * 100, y_up * 100], [P0, price_at_up100bp], color='black', zorder=5)
plt.axvline(x=y0 * 100, color='gray', linestyle=':', alpha=0.7)
plt.axvline(x=y_up * 100, color='gray', linestyle=':', alpha=0.7)

# 标注文字
plt.annotate(f'初始 YTM = {y0*100}%\n精确价格 = {P0:.4f}', 
             xy=(y0*100, P0), xytext=(y0*100-1.5, P0+5),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate(f'上升{delta_y_bp}bp后 YTM = {y_up*100}%\n精确价格 = {price_at_up100bp:.4f}\n久期法相对变化 = {dur_approx_change_up100bp*100:.4f}%', 
             xy=(y_up*100, price_at_up100bp), xytext=(y_up*100+0.5, price_at_up100bp+5),
             arrowprops=dict(facecolor='black', shrink=0.05))

# 图例分开（放置在不同位置）
leg1 = plt.legend(handles=[line1], loc='upper right', frameon=True)
plt.gca().add_artist(leg1)
plt.legend(handles=[line2], loc='center right', frameon=True)

# 图表装饰
plt.title(f'价格-收益率曲线与久期近似 (变动幅度: {delta_y_bp}bp可调)')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图片
fig_path = 'price_yield_curve.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约存入字典
result = {
    'price_at_up100bp': round(price_at_up100bp, 4),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 4),
    'figure_path': fig_path
}

# 打印结果供验证
print(result)
