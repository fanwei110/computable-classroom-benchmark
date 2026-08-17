import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
FACE_VALUE = 100.0          # 面值
COUPON_RATE = 0.046         # 票息率（年化）
MATURITY_YEARS = 7          # 期限（年）
CURRENT_YIELD = 0.053       # 当前收益率
YIELD_CHANGE_BPS = 100      # 收益率变动幅度（基点），可调
YIELD_RANGE = (0.02, 0.09)  # 绘图收益率范围

# ==================== 债券定价函数 ====================
def bond_price(face_value, coupon_rate, maturity_years, yield_rate):
    """
    计算债券的精确价格（全价），假设每年付息一次，面值100。
    """
    coupon = face_value * coupon_rate
    periods = int(maturity_years)
    
    # 现金流现值之和
    cashflow_pv = sum([coupon / (1 + yield_rate)**t for t in range(1, periods + 1)])
    principal_pv = face_value / (1 + yield_rate)**periods
    
    return cashflow_pv + principal_pv

# ==================== 久期计算（修正久期） ====================
def modified_duration(face_value, coupon_rate, maturity_years, yield_rate):
    """
    计算修正久期（Modified Duration），用于价格对收益率的线性近似。
    修正久期 = Macaulay久期 / (1 + yield)
    """
    coupon = face_value * coupon_rate
    periods = int(maturity_years)
    
    # 计算各期现金流的现值
    pv_cashflows = np.array([coupon / (1 + yield_rate)**t for t in range(1, periods + 1)])
    pv_principal = face_value / (1 + yield_rate)**periods
    
    # 所有现金流的现值总和 = 债券价格
    total_pv = np.sum(pv_cashflows) + pv_principal
    
    # Macaulay久期 = Σ(t * PV_t) / total_pv
    weighted_times = np.sum(np.arange(1, periods + 1) * pv_cashflows) + periods * pv_principal
    macaulay_duration = weighted_times / total_pv
    
    # 修正久期
    mod_duration = macaulay_duration / (1 + yield_rate)
    
    return mod_duration, total_pv

# ==================== 核心计算 ====================
# 1. 计算当前收益率下的精确价格和修正久期
current_mod_dur, current_price = modified_duration(FACE_VALUE, COUPON_RATE, MATURITY_YEARS, CURRENT_YIELD)

# 2. 收益率上升100个基点后的新收益率
yield_up100bp = CURRENT_YIELD + YIELD_CHANGE_BPS / 10000.0

# 3. 精确价格（收益率上升100bp后）
price_up100bp = bond_price(FACE_VALUE, COUPON_RATE, MATURITY_YEARS, yield_up100bp)

# 4. 久期法估计的相对价格变化
# ΔP/P ≈ -修正久期 × Δy
delta_yield = YIELD_CHANGE_BPS / 10000.0
dur_approx_relative_change = -current_mod_dur * delta_yield

# 5. 久期法估计的绝对价格变化百分比
dur_approx_change_up100bp = dur_approx_relative_change * 100  # 转换为百分比

# ==================== 生成绘图数据 ====================
yield_grid = np.linspace(YIELD_RANGE[0], YIELD_RANGE[1], 500)

# 精确价格曲线
exact_prices = np.array([bond_price(FACE_VALUE, COUPON_RATE, MATURITY_YEARS, y) 
                         for y in yield_grid])

# 久期近似价格曲线
# P_approx(y) = P_current * (1 - 修正久期 * (y - y_current))
approx_prices = current_price * (1 - current_mod_dur * (yield_grid - CURRENT_YIELD))

# ==================== 绘图 ====================
fig, ax = plt.subplots(figsize=(10, 6))

# 精确价格-收益率曲线
ax.plot(yield_grid * 100, exact_prices, 'b-', linewidth=2, label='精确价格-收益率曲线 (Exact)')

# 久期近似（在当前收益率附近叠加，这里是全范围展示）
ax.plot(yield_grid * 100, approx_prices, 'r--', linewidth=1.8, label='久期近似 (Duration Approximation)')

# 标记当前收益率点
ax.plot(CURRENT_YIELD * 100, current_price, 'go', markersize=8, 
        label=f'当前收益率点 ({CURRENT_YIELD*100:.1f}%)')

# 标记收益率上升100bp后的精确价格点
ax.plot(yield_up100bp * 100, price_up100bp, 'rs', markersize=8, 
        label=f'收益率+{YIELD_CHANGE_BPS}bp精确价格')

# 久期近似预测的+100bp价格
approx_price_up100bp = current_price * (1 - current_mod_dur * delta_yield)
ax.plot(yield_up100bp * 100, approx_price_up100bp, 'm^', markersize=8, 
        label=f'久期近似预测的+{YIELD_CHANGE_BPS}bp价格')

# 图例、标签和标题
ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.set_title(f'债券价格-收益率曲线 (面值{FACE_VALUE}, 票息{COUPON_RATE*100}%, {MATURITY_YEARS}年期)', 
             fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3, linestyle='--')

# 调整收益率变动幅度（通过标题下方文字显示可调参数）
ax.text(0.5, 0.98, f'收益率变动幅度: {YIELD_CHANGE_BPS}基点 (可调参数)', 
        transform=ax.transAxes, fontsize=10, ha='center', va='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# 保存图形
figure_filename = 'bond_price_yield_curve.png'
plt.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 组装结果字典 ====================
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_filename
}

# ==================== 输出结果 ====================
print("=" * 60)
print("债券分析结果")
print("=" * 60)
print(f"债券参数: 面值={FACE_VALUE}, 票息率={COUPON_RATE*100}%, 期限={MATURITY_YEARS}年")
print(f"当前收益率: {CURRENT_YIELD*100}%")
print(f"收益率变动幅度: {YIELD_CHANGE_BPS}基点")
print("-" * 40)
print(f"收益率上升100bp后的精确价格: {price_up100bp:.6f}")
print(f"久期法估计的相对价格变化: {dur_approx_change_up100bp:.4f}%")
print(f"修正久期 (当前收益率下): {current_mod_dur:.4f}")
print("-" * 40)
print(f"图表已保存至: {figure_filename}")
print("=" * 60)

# 验证结果字典
print("\n结果字典内容:")
for key, value in result.items():
    if key == 'figure_path':
        print(f"  '{key}': '{value}'")
    else:
        print(f"  '{key}': {value}")
