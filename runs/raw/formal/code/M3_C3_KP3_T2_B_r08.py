import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体，防止图例和标题乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ================= 债券参数与计算约定 =================
F = 100                  # 面值
c_rate = 0.046           # 票息率 4.6%
T = 7                    # 期限 7年
y0 = 0.053               # 初始到期收益率 YTM 5.3%

# 变动幅度可调：此处设定为 +100bp (0.01)
delta_y = 0.01           # 若需调整变动幅度，修改此变量即可

# 构造现金流（年复利，按年付息）
times = np.arange(1, T + 1)
cash_flows = np.full(T, F * c_rate)
cash_flows[-1] += F      # 最后一期加入本金

# ================= 核心计算函数 =================
def bond_price(ytm, cash_flows, times):
    """精确价格计算：基于年复利贴现"""
    return np.sum(cash_flows / (1 + ytm)**times)

def mac_duration(ytm, cash_flows, times):
    """Macaulay久期计算"""
    P = bond_price(ytm, cash_flows, times)
    return np.sum(times * (cash_flows / (1 + ytm)**times)) / P

# 初始状态计算
P0 = bond_price(y0, cash_flows, times)
D_mac = mac_duration(y0, cash_flows, times)
D_mod = D_mac / (1 + y0)  # 修正久期

# 1. 收益率+100bp后的精确价格
y_up = y0 + delta_y
P_up = bond_price(y_up, cash_flows, times)

# 2. 久期法估的相对变化 (ΔP/P ≈ -D_mod * Δy)
dur_approx_rel_change = -D_mod * delta_y

# ================= 绘图：精确价格 vs 久期近似 =================
yields_plot = np.linspace(0.02, 0.09, 500)
exact_prices_plot = [bond_price(y, cash_flows, times) for y in yields_plot]

# 久期近似线：P(y) ≈ P0 - P0 * D_mod * (y - y0)
approx_prices_plot = [P0 - P0 * D_mod * (y - y0) for y in yields_plot]

plt.figure(figsize=(10, 6))
# 曲线1：精确价格-收益率曲线
plt.plot(yields_plot * 100, exact_prices_plot, label='精确价格', color='blue', linewidth=2)
# 曲线2：久期近似价格曲线（切线）
plt.plot(yields_plot * 100, approx_prices_plot, label='久期近似价格', color='red', linestyle='--', linewidth=2)

# 标注初始点
plt.scatter([y0*100], [P0], color='black', zorder=5)
plt.annotate(f'初始 (YTM={y0*100}%, P={P0:.2f})', xy=(y0*100, P0), xytext=(y0*100+0.5, P0+2))

# 标注 +100bp 变动后的点
P_approx_up = P0 * (1 + dur_approx_rel_change)
plt.scatter([y_up*100], [P_up], color='green', zorder=5, label=f'+100bp 精确价格 ({P_up:.2f})')
plt.scatter([y_up*100], [P_approx_up], color='orange', marker='x', s=100, zorder=5, label=f'+100bp 久期近似 ({P_approx_up:.2f})')

# 绘制变动幅度的辅助线
plt.vlines(y0*100, min(P_up, P_approx_up)-2, P0, colors='grey', linestyles='dotted')
plt.vlines(y_up*100, min(P_up, P_approx_up)-2, P0, colors='grey', linestyles='dotted')
plt.hlines(P0, y0*100, y_up*100, colors='grey', linestyles='dotted')
plt.hlines(P_up, y0*100, y_up*100, colors='grey', linestyles='dotted')
plt.annotate(f'Δy = +{delta_y*100:.0f}bp', xy=((y0*100 + y_up*100)/2, P0+0.5), ha='center', color='grey')

plt.title('债券价格-收益率曲线及久期近似 (面值100, 票息4.6%, 7年)')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.legend(loc='upper right')
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图像
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 存入结果字典 =================
result = {
    'price_at_up100bp': round(P_up, 6),
    'dur_approx_change_up100bp': round(dur_approx_rel_change, 6),
    'figure_path': figure_path
}

# 打印结果供查看
print(result)
