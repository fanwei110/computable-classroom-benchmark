import numpy as np
import matplotlib.pyplot as plt

# ==================== 债券参数与课程约定 ====================
F = 100.0               # 面值
c = 0.046               # 票息率 (4.6%)
T = 7                   # 期限 (7年)
y0 = 0.053              # 当前收益率 (5.3%)

# 可调的收益率变动幅度 (当前设为100个基点，可按需修改)
delta_y = 0.01          # 100 bp = 0.01

# ==================== 现金流构建 ====================
times = np.arange(1, T + 1)
CFs = np.full(T, c * F)
CFs[-1] += F            # 最后一期加入面值

# ==================== 核心计算函数 ====================
def bond_price(y, times, CFs):
    """精确债券定价：现金流贴现求和"""
    return np.sum(CFs / (1 + y)**times)

def bond_metrics(y, times, CFs):
    """计算债券在收益率y下的价格、修正久期、凸性"""
    P = bond_price(y, times, CFs)
    pv_cfs = CFs / (1 + y)**times
    
    # 麦考利久期
    mac_duration = np.sum(times * pv_cfs) / P
    # 修正久期 = 麦考利久期 / (1+y)
    mod_duration = mac_duration / (1 + y)
    
    # 凸性 = Σ[t(t+1)CF_t/(1+y)^(t+2)] / P
    convexity = np.sum(times * (times + 1) * CFs / (1 + y)**(times + 2)) / P
    
    return P, mod_duration, convexity

# ==================== 1. 精确价格-收益率曲线 ====================
y_grid = np.linspace(0.02, 0.09, 300)  # 2% 到 9% 的收益率网格
P_exact_grid = np.array([bond_price(y, times, CFs) for y in y_grid])

# ==================== 2. 当前收益率处的久期与凸性近似 ====================
P0, D_mod, C0 = bond_metrics(y0, times, CFs)

# 收益率变动网格 (相对于 y0)
dy_grid = y_grid - y0

# 一阶久期近似: dP/P = -D_mod * dy  =>  P_approx = P0 * (1 - D_mod * dy)
P_dur_approx = P0 * (1 - D_mod * dy_grid)

# 久期+凸性近似: dP/P = -D_mod * dy + 0.5 * C * dy^2  =>  P_approx = P0 * (1 - D_mod * dy + 0.5 * C * dy^2)
P_dur_conv_approx = P0 * (1 - D_mod * dy_grid + 0.5 * C0 * dy_grid**2)

# ==================== 3. 报告 +100bp 的精确价格与一阶相对变化 ====================
y_up = y0 + delta_y
price_at_up100bp = bond_price(y_up, times, CFs)
# 久期法估计的相对价格变化 (小数表示，下跌为负)
dur_approx_change_up100bp = -D_mod * delta_y

# ==================== 4. 绘图与保存 ====================
plt.figure(figsize=(10, 6))

# 绘制三条曲线
plt.plot(y_grid * 100, P_exact_grid, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_grid * 100, P_dur_approx, label='Duration Approximation (1st Order)', color='red', linestyle='--')
plt.plot(y_grid * 100, P_dur_conv_approx, label='Duration + Convexity Approximation', color='green', linestyle='-.')

# 标注当前收益率点
plt.scatter([y0 * 100], [P0], color='black', zorder=5)
plt.axvline(x=y0 * 100, color='gray', linestyle=':', alpha=0.7, label=f'Current Yield = {y0*100:.1f}%')

# 设置图表格式
plt.title('Bond Price-Yield Curve and Approximations', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 输出契约 ====================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 打印结果供课堂投屏参考
print(f"当前收益率 (y0): {y0*100:.1f}%")
print(f"当前精确价格 (P0): {P0:.4f}")
print(f"修正久期 (D_mod): {D_mod:.4f}")
print(f"凸性 (C): {C0:.4f}")
print("-" * 40)
print(f"收益率上升 {delta_y*100:.0f}bp 后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"收益率上升 {delta_y*100:.0f}bp 后的久期法估计相对变化: {result['dur_approx_change_up100bp']:.4f} ({result['dur_approx_change_up100bp']*100:.2f}%)")
print(f"图形已保存至: {result['figure_path']}")
