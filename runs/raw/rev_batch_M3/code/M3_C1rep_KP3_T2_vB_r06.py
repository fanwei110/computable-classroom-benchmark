import numpy as np
import matplotlib.pyplot as plt

# 债券参数
F = 100                # 面值
coupon_rate = 0.046    # 票息率 4.6%
T = 7                  # 期限 7年
y0 = 0.053             # 当前到期收益率 5.3%
c = F * coupon_rate    # 每期票息额

# 精确价格计算函数
def bond_price(y, c, F, T):
    if y == 0:
        return c * T + F
    return c * (1 - (1 + y)**-T) / y + F * (1 + y)**-T

# 计算当前YTM下的精确价格
P0 = bond_price(y0, c, F, T)

# 计算麦考利久期和修正久期
t_arr = np.arange(1, T + 1)
cf_arr = np.full(T, c)
cf_arr[-1] += F  # 最后一期加入面值

pv_cf_arr = cf_arr / (1 + y0)**t_arr
MacD = np.sum(t_arr * pv_cf_arr) / P0
MD = MacD / (1 + y0)

# 久期近似价格计算函数（一阶线性近似，随变动幅度可调）
def dur_approx_price(y, P0, MD, y0):
    delta_y = y - y0
    return P0 * (1 - MD * delta_y)

# 变动幅度设定（此处设为+100bp，该参数可按需调节）
delta_y = 0.01 
y_new = y0 + delta_y

# 计算收益率+100bp后的精确价格
price_at_up100bp = bond_price(y_new, c, F, T)

# 计算久期法估计的相对变化（ΔP/P ≈ -MD * Δy）
dur_approx_change_up100bp = -MD * delta_y

# 画图：精确价格曲线 vs 久期近似曲线
y_range = np.linspace(0.02, 0.09, 500)
P_exact = [bond_price(y, c, F, T) for y in y_range]
P_approx = [dur_approx_price(y, P0, MD, y0) for y in y_range]

plt.figure(figsize=(10, 6))
plt.plot(y_range * 100, P_exact, label='Exact Price', color='blue', linewidth=2)
plt.plot(y_range * 100, P_approx, label='Duration Approximation', color='red', linestyle='--', linewidth=2)

# 标出当前YTM与价格的点
plt.scatter(y0 * 100, P0, color='black', zorder=5)
plt.annotate(f'Current YTM = {y0*100:.1f}%\nPrice = {P0:.2f}', 
             xy=(y0 * 100, P0), xytext=(y0 * 100 + 1.5, P0 + 5),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.title('Price-Yield Curve & Duration Approximation')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图表
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 将所有要求的输出存入字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

print(result)
