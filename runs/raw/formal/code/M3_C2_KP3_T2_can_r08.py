import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
Face_Value = 100           # 面值
Coupon_Rate = 0.046        # 票息率 4.6%
Maturity = 7               # 期限 7 年
Current_Yield = 0.053      # 当前收益率 5.3%
Yield_Shift_bps = 100      # 可调：收益率变动幅度（基点），1 bp = 0.01%

# 收益率网格范围
Yield_Min = 0.02           # 2%
Yield_Max = 0.09           # 9%

# ==================== 现金流构建 ====================
times = np.arange(1, Maturity + 1)
cashflows = np.full(Maturity, Face_Value * Coupon_Rate)
cashflows[-1] += Face_Value  # 最后一期加入面值

# ==================== 精确价格计算函数 ====================
def calculate_bond_price(yields, cf, t):
    """
    向量化计算债券精确价格
    yields: 收益率标量或数组
    cf: 现金流数组
    t: 对应时间数组
    """
    yields = np.atleast_1d(yields)
    # 广播机制：yields 为 (N, 1), t 为 (1, T)，折现因子为 (N, T)
    discount_factors = (1 + yields[:, np.newaxis]) ** t
    prices = np.sum(cf / discount_factors, axis=1)
    return prices if prices.size > 1 else prices.item()

# ==================== 久期与近似计算 ====================
# 1. 计算当前收益率下的精确价格
P0 = calculate_bond_price(Current_Yield, cashflows, times)

# 2. 计算麦考利久期
pv_cashflows = cashflows / (1 + Current_Yield) ** times
Macaulay_Duration = np.sum(times * pv_cashflows) / P0

# 3. 计算修正久期
Modified_Duration = Macaulay_Duration / (1 + Current_Yield)

# ==================== 绘图数据生成 ====================
# 生成收益率网格
yield_grid = np.linspace(Yield_Min, Yield_Max, 500)

# 精确价格曲线
exact_prices = calculate_bond_price(yield_grid, cashflows, times)

# 基于久期的近似价格曲线：P_approx = P0 * (1 - ModD * (y - y0))
# 收益率变动幅度可调由 Yield_Shift_bps 控制，但曲线绘制是连续的，反映局部线性近似
approx_prices = P0 * (1 - Modified_Duration * (yield_grid - Current_Yield))

# ==================== +100bp 专项计算 ====================
delta_y = Yield_Shift_bps / 10000.0  # 100个基点转为绝对值 0.01

# 收益率上升 100bp 后的精确价格
price_at_up100bp = calculate_bond_price(Current_Yield + delta_y, cashflows, times)

# 久期法估计的相对价格变化 (%形式转为小数形式，即 dP/P)
dur_approx_change_up100bp = -Modified_Duration * delta_y

# ==================== 绘图 ====================
plt.figure(figsize=(10, 6), dpi=150)

# 绘制精确价格曲线
plt.plot(yield_grid * 100, exact_prices, 
         label='Exact Price-Yield Curve', color='blue', linewidth=2)

# 绘制基于久期的近似曲线
plt.plot(yield_grid * 100, approx_prices, 
         label='Duration-Based Approximation', color='orange', linestyle='--', linewidth=2)

# 标注当前收益率位置
plt.axvline(x=Current_Yield * 100, color='red', linestyle=':', linewidth=1.2, 
            label=f'Current Yield ({Current_Yield*100:.1f}%)')
plt.scatter([Current_Yield * 100], [P0], color='red', zorder=5)

# 图形美化
plt.title('Bond Price-Yield Relationship and Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# 限制X轴在设定的范围内更清晰
plt.xlim(Yield_Min * 100, Yield_Max * 100)

# 保存图形
figure_path = 'bond_price_yield_duration.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.close()

# ==================== 输出契约 ====================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 为方便课堂投屏展示，打印结果核对
if __name__ == '__main__':
    print(f"当前价格 (P0): {P0:.4f}")
    print(f"修正久期: {Modified_Duration:.4f}")
    print(f"收益率上升100bp后精确价格: {result['price_at_up100bp']:.4f}")
    print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
    print(f"图形已保存至: {result['figure_path']}")
