import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数设定
# ==========================================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity = 7                # 期限 7 年
current_yield = 0.053       # 当前收益率 5.3%
payment_freq = 1            # 付息频率（1代表每年付息一次）

# 可调参数：收益率变动幅度（画图的收益率范围）
yield_plot_range = (0.02, 0.09)  # 2% 到 9%，可按需调整

# ==========================================
# 现金流构造
# ==========================================
periods = maturity * payment_freq
times = np.arange(1, periods + 1)
coupon_payment = (face_value * coupon_rate) / payment_freq

# 构建现金流数组：前 n-1 期为票息，最后一期为票息+面值
cash_flows = np.full(periods, coupon_payment)
cash_flows[-1] += face_value

# ==========================================
# 核心计算函数
# ==========================================
def calculate_bond_price(y, times, cash_flows, freq):
    """计算给定收益率下的债券精确价格"""
    period_y = y / freq
    pv_cash_flows = cash_flows / (1 + period_y)**times
    return np.sum(pv_cash_flows)

def calculate_duration(y, times, cash_flows, freq, price):
    """计算麦考利久期和修正久期"""
    period_y = y / freq
    pv_cash_flows = cash_flows / (1 + period_y)**times
    
    # 麦考利久期 (以期为单位)
    mac_period_duration = np.sum(times * pv_cash_flows) / price
    # 转换为以年为单位
    mac_year_duration = mac_period_duration / freq
    # 修正久期
    mod_duration = mac_year_duration / (1 + period_y)
    
    return mac_year_duration, mod_duration

# ==========================================
# 计算当前收益率下的价格与久期
# ==========================================
P0 = calculate_bond_price(current_yield, times, cash_flows, payment_freq)
mac_dur, mod_dur = calculate_duration(current_yield, times, cash_flows, payment_freq, P0)

# ==========================================
# 生成价格-收益率曲线数据
# ==========================================
yields = np.linspace(yield_plot_range[0], yield_plot_range[1], 1000)
exact_prices = np.array([calculate_bond_price(y, times, cash_flows, payment_freq) for y in yields])

# 基于久期的近似价格曲线：P(y) ≈ P0 * (1 - ModD * (y - y0))
approx_prices = P0 * (1 - mod_dur * (yields - current_yield))

# ==========================================
# 绘图
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(yields * 100, exact_prices, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(yields * 100, approx_prices, label='Duration-Based Approximation', color='red', linestyle='--', linewidth=2)
plt.axvline(x=current_yield * 100, color='gray', linestyle=':', label=f'Current Yield ({current_yield*100:.1f}%)')

plt.title('Bond Price-Yield Curve and Duration Approximation')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 保存图表
fig_path = 'price_yield_curve.png'
plt.savefig(fig_path)
plt.close()

# ==========================================
# 计算特定要求：收益率上升 100 个基点 (1%)
# ==========================================
up100bp_yield = current_yield + 0.01

# 1. 精确价格
price_at_up100bp = calculate_bond_price(up100bp_yield, times, cash_flows, payment_freq)

# 2. 久期法估计的相对价格变化 (ΔP/P0 ≈ -ModD * Δy)
dur_approx_change_up100bp = -mod_dur * 0.01

# ==========================================
# 封装输出结果
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# 打印结果以便查看
print(result)
