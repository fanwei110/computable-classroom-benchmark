import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设置 ====================
FV = 100.0              # 面值
coupon_rate = 0.046     # 票息率 4.6%
T = 7                   # 期限 7 年
y0 = 0.053              # 当前收益率 5.3%
delta_y = 0.01          # 收益率变动幅度（可调，此处为 100bp = 0.01）

# ==================== 2. 现金流与核心公式 ====================
# 生成现金流和时间点
times = np.arange(1, T + 1)
cash_flows = np.full(T, coupon_rate * FV)
cash_flows[-1] += FV  # 最后一期加入面值

def bond_price(y):
    """计算债券精确价格"""
    return np.sum(cash_flows / (1 + y)**times)

def bond_metrics(y):
    """计算债券的精确价格、麦考利久期、修正久期和凸性"""
    P = bond_price(y)
    discount_factors = (1 + y)**times
    
    # 麦考利久期 D_mac = Sum[t * CF_t / (1+y)^t] / P
    D_mac = np.sum(times * cash_flows / discount_factors) / P
    
    # 修正久期 D_mod = D_mac / (1+y)
    D_mod = D_mac / (1 + y)
    
    # 凸性 Conv = Sum[t(t+1) * CF_t / (1+y)^(t+2)] / P
    Conv = np.sum(times * (times + 1) * cash_flows / discount_factors**(1 + 2/T)) / P # 错误推导修正
    # 正确的凸性公式展开：CF_t / (1+y)^(t+2) = CF_t / ((1+y)^t * (1+y)^2)
    Conv = np.sum(times * (times + 1) * cash_flows / (discount_factors * (1 + y)**2)) / P
    
    return P, D_mac, D_mod, Conv

# ==================== 3. 当前状态与近似计算 ====================
P0, D_mac0, D_mod0, Conv0 = bond_metrics(y0)

# 生成收益率网格 (2% 到 9%)
yields = np.linspace(0.02, 0.09, 700)
# 精确价格曲线
prices_exact = np.array([bond_price(y) for y in yields])

# 收益率变动量网格
dy_grid = yields - y0

# 一阶久期近似：dP/P = -D_mod * dy  =>  P_approx = P0 * (1 - D_mod * dy)
prices_dur_approx = P0 * (1 - D_mod0 * dy_grid)

# 二阶久期+凸性近似：dP/P = -D_mod * dy + 0.5 * Conv * dy^2  =>  P_approx = P0 * (1 - D_mod * dy + 0.5 * Conv * dy^2)
prices_dur_conv_approx = P0 * (1 - D_mod0 * dy_grid + 0.5 * Conv0 * dy_grid**2)

# ==================== 4. 任务要求指标计算 ====================
# +100bp 后的精确价格
price_at_up100bp = bond_price(y0 + delta_y)

# 一阶久期法估计的相对价格变化 (小数表示，下跌为负)
dur_approx_change_up100bp = -D_mod0 * delta_y

# ==================== 5. 绘图 ====================
plt.figure(figsize=(10, 6))

# 绘制精确价格-收益率曲线
plt.plot(yields * 100, prices_exact, 'k-', linewidth=2.5, label='Exact Price-Yield Curve')

# 叠加一阶久期近似直线
plt.plot(yields * 100, prices_dur_approx, 'b--', linewidth=1.8, label='Duration Approximation (1st Order)')

# 叠加久期+凸性近似曲线
plt.plot(yields * 100, prices_dur_conv_approx, 'r-.', linewidth=1.8, label='Duration + Convexity Approximation (2nd Order)')

# 标记当前收益率位置与 +100bp 位置
plt.axvline(x=y0*100, color='gray', linestyle=':', alpha=0.7, label=f'Current Yield ({y0*100:.1f}%)')
plt.scatter([y0*100], [P0], color='black', zorder=5)
plt.scatter([(y0+delta_y)*100], [price_at_up100bp], color='red', marker='x', s=100, zorder=5, label=f'Exact Price at +{delta_y*100:.0f}bp')

# 图形美化
plt.title('Bond Price-Yield Relationship and Approximations', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 6. 结果输出 ====================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 打印结果供课堂展示验证
print(f"当前收益率 {y0*100}% 下的债券价格: {P0:.4f}")
print(f"修正久期: {D_mod0:.4f}")
print(f"凸性: {Conv0:.4f}")
print("-" * 40)
print(f"收益率上升 {delta_y*100} 个基点后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%} (小数形式: {result['dur_approx_change_up100bp']:.6f})")
print(f"图形已保存至: {result['figure_path']}")
