import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 债券参数设定 ====================
face_value = 100.0         # 面值
coupon_rate = 0.046        # 票息率 (小数表示 4.6%)
years = 7                  # 期限 (年)
current_yield = 0.053      # 当前收益率 (小数表示 5.3%)
dy_100bp = 0.01            # 收益率上升100基点 (小数表示 1%)

# ==================== 2. 核心计算函数 ====================
def bond_price_scalar(y, F, c, T):
    """计算给定单一收益率下的债券精确价格（年复利）"""
    t = np.arange(1, T + 1)
    cf = np.full(T, F * c)
    cf[-1] += F  # 最后一期加入面值
    return np.sum(cf / (1 + y)**t)

def bond_price_vectorized(y_arr, F, c, T):
    """计算给定收益率数组下的债券精确价格（向量化运算）"""
    t = np.arange(1, T + 1)[:, None]  # 形状 (T, 1)
    cf = np.full(T, F * c)
    cf[-1] += F
    # 利用广播机制: cf形状(T,), y_arr形状(1,N), 计算结果形状(T,N)
    pv = cf[:, None] / (1 + y_arr[None, :])**t
    return np.sum(pv, axis=0)

def bond_metrics(y, F, c, T):
    """计算当前收益率下的价格、麦考利久期、修正久期与凸性"""
    t = np.arange(1, T + 1)
    cf = np.full(T, F * c)
    cf[-1] += F
    
    P = bond_price_scalar(y, F, c, T)
    
    # 麦考利久期 = Σ[t*CF_t/(1+y)^t] / P
    MacD = np.sum(t * cf / (1 + y)**t) / P
    
    # 修正久期 = 麦考利久期 / (1+y)
    ModD = MacD / (1 + y)
    
    # 凸性 = Σ[t(t+1)CF_t/(1+y)^(t+2)] / P (单位：年的平方)
    Conv = np.sum(t * (t + 1) * cf / (1 + y)**(t + 2)) / P
    
    return P, MacD, ModD, Conv

# ==================== 3. 计算基准指标与网格 ====================
P0, MacD, ModD, Conv = bond_metrics(current_yield, face_value, coupon_rate, years)

# 收益率变动幅度做成可调：设定偏离当前收益率的最小与最大幅度
# 对应于收益率从 2% 到 9% (0.02 - 0.053 = -0.033, 0.09 - 0.053 = 0.037)
dy_min = -0.033
dy_max = 0.037
dy_grid = np.linspace(dy_min, dy_max, 700)
y_grid = current_yield + dy_grid

# 精确价格-收益率曲线
P_exact_grid = bond_price_vectorized(y_grid, face_value, coupon_rate, years)

# 一阶久期近似直线 (dP/P = -ModD * dy)
P_dur_grid = P0 * (1 - ModD * dy_grid)

# 久期+凸性近似曲线 (dP/P = -ModD*dy + 0.5*Conv*dy^2)
P_dur_conv_grid = P0 * (1 - ModD * dy_grid + 0.5 * Conv * dy_grid**2)

# ==================== 4. 特定情景 (+100bp) 计算 ====================
# 收益率上升100bp后的精确价格
price_at_up100bp = bond_price_scalar(current_yield + dy_100bp, face_value, coupon_rate, years)

# 久期法估计的一阶相对价格变化 (小数，下跌为负)
dur_approx_change_up100bp = -ModD * dy_100bp

# ==================== 5. 绘图与保存 ====================
# 设置中文字体与负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9, 6))

# 绘制三条曲线
ax.plot(y_grid * 100, P_exact_grid, label='精确价格-收益率曲线', color='blue', linewidth=2.5)
ax.plot(y_grid * 100, P_dur_grid, label='一阶久期近似 (直线)', color='red', linestyle='--', linewidth=1.5)
ax.plot(y_grid * 100, P_dur_conv_grid, label='久期+凸性近似 (曲线)', color='green', linestyle='-.', linewidth=1.5)

# 标注当前收益率点
ax.axvline(current_yield * 100, color='gray', linestyle=':', alpha=0.7, 
           label=f'当前收益率 ({current_yield*100:.1f}%)')
ax.scatter([current_yield * 100], [P0], color='black', zorder=5, s=30)

# 图形格式调整
ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.set_title('债券价格-收益率曲线及久期/凸性近似', fontsize=14)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 6. 输出契约填充 ====================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 课堂演示打印输出
print(f"当前收益率下精确价格 P0: {P0:.4f}")
print(f"修正久期 ModD: {ModD:.4f}")
print(f"凸性 Conv: {Conv:.4f}")
print(f"+100bp 后精确价格: {result['price_at_up100bp']:.4f}")
print(f"+100bp 久期法估计相对变化: {result['dur_approx_change_up100bp']:.4f}")
print(f"图形已保存至: {result['figure_path']}")
