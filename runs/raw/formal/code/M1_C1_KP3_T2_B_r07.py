import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
face_value = 100
coupon_rate = 0.046
ytm_base = 0.053
n_years = 7
y_range = np.linspace(0.02, 0.09, 100)

# 计算精确价格
def bond_price(y, coupon, face_value, n):
    cash_flows = np.array([coupon * face_value] * n + [face_value * (1 + coupon)])
    periods = np.arange(1, n + 2)
    pv = np.sum(cash_flows / (1 + y) ** periods)
    return pv

# 计算久期
def macaulay_duration(y, coupon, face_value, n):
    cash_flows = np.array([coupon * face_value] * n + [face_value * (1 + coupon)])
    periods = np.arange(1, n + 2)
    pv_cash_flows = cash_flows / (1 + y) ** periods
    duration = np.sum(periods * pv_cash_flows) / np.sum(pv_cash_flows)
    return duration

# 基准价格和久期
P0 = bond_price(ytm_base, coupon_rate, face_value, n_years)
D = macaulay_duration(ytm_base, coupon_rate, face_value, n_years)
ModD = D / (1 + ytm_base)

# 精确价格和久期近似价格
prices_exact = [bond_price(y, coupon_rate, face_value, n_years) for y in y_range]
prices_approx = [P0 * (1 - ModD * (y - ytm_base)) for y in y_range]

# 收益率+100bp后的结果
ytm_up100bp = ytm_base + 0.01
price_up100bp = bond_price(ytm_up100bp, coupon_rate, face_value, n_years)
dur_approx_change = -ModD * 0.01 * 100  # 百分比变化

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(y_range * 100, prices_exact, label='精确价格', color='blue')
plt.plot(y_range * 100, prices_approx, label='久期近似', color='red', linestyle='--')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.title('价格收益率曲线')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
