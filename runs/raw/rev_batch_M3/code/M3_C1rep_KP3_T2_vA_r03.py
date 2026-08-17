import numpy as np
import matplotlib.pyplot as plt
import json

# 设置中文字体与负号显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ================= 1. 债券基础参数 =================
F = 100            # 面值
c = 0.046          # 票息率
n = 7              # 期限（年）
y0 = 0.053         # 当前收益率

# ================= 2. 核心计算函数 =================
def bond_price(y):
    """计算债券精确价格"""
    t = np.arange(1, n + 1)
    cf = np.full(n, F * c)
    cf[-1] += F  # 最后一期加入本金
    return np.sum(cf / (1 + y)**t)

def modified_duration(y):
    """计算修正久期"""
    P = bond_price(y)
    t = np.arange(1, n + 1)
    cf = np.full(n, F * c)
    cf[-1] += F
    mac_duration = np.sum(t * cf / (1 + y)**t) / P
    return mac_duration / (1 + y)

# 当前状态
P0 = bond_price(y0)
D0 = modified_duration(y0)

# ================= 3. 目标指标计算 =================
# 收益率上升100个基点 (1%)
delta_y_100bp = 0.01
y_up100 = y0 + delta_y_100bp

# 精确价格
price_at_up100bp = bond_price(y_up100)

# 久期估计的相对价格变化 (ΔP/P ≈ -D_mod * Δy)
dur_approx_change_up100bp = -D0 * delta_y_100bp

# ================= 4. 绘图 =================
y_plot = np.linspace(0.02, 0.09, 500)
p_exact_plot = [bond_price(y) for y in y_plot]

# 【可调参数】收益率变动幅度（控制近似直线的绘制范围）
# 默认设为3.5%，即以y0为中心左右各画3.5%，几乎覆盖2%-9%全区间
# 修改此值可以调整近似直线的展示幅度
DELTA_Y_AMP = 0.035 

y_approx_plot = np.linspace(max(0.02, y0 - DELTA_Y_AMP), min(0.09, y0 + DELTA_Y_AMP), 200)
p_approx_plot = [P0 * (1 - D0 * (y - y0)) for y in y_approx_plot]

plt.figure(figsize=(10, 6))
# 绘制精确曲线
plt.plot(y_plot * 100, p_exact_plot, label='精确价格曲线', color='blue', linewidth=2)
# 绘制久期近似直线
plt.plot(y_approx_plot * 100, p_approx_plot, label=f'久期近似曲线 (幅度±{DELTA_Y_AMP*100:.1f}%)', 
         color='red', linestyle='--', linewidth=2)

# 标注初始点
plt.scatter([y0 * 100], [P0], color='black', zorder=5)
plt.annotate(f'初始点 (Y={y0*100:.1f}%, P={P0:.2f})', 
             xy=(y0 * 100, P0), xytext=(y0 * 100 + 1.5, P0 + 3),
             arrowprops=dict(facecolor='black', shrink=0.05))

# 标注上升100bp点
plt.scatter([y_up100 * 100], [price_at_up100bp], color='green', zorder=5)
plt.annotate(f'上升100bp (Y={y_up100*100:.1f}%, P={price_at_up100bp:.2f})', 
             xy=(y_up100 * 100, price_at_up100bp), xytext=(y_up100 * 100 + 1, price_at_up100bp + 3),
             arrowprops=dict(facecolor='green', shrink=0.05))

plt.title('债券价格随收益率变化曲线（含久期近似）')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图片
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 5. 输出契约封装 =================
result = {
    'price_at_up100bp': round(price_at_up100bp, 4),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': figure_path
}

# 打印结果
print(json.dumps(result, ensure_ascii=False, indent=4))
