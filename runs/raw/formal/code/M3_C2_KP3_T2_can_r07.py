import numpy as np
import matplotlib.pyplot as plt

# ================= 1. 基础参数与假设 =================
# 假设：年付息，面值100，票息率4.6%，7年期，当前收益率5.3%
# 注意：题目未指明付息频率，默认采用年付息，年复利计算
F = 100
c = 0.046
T = 7
y0 = 0.053

# ================= 2.  簡与函数定义 =================

def 计算精确债券价格
def :param y: 收益率（可以是标量或数组）
    cash_flows = 现金流时间点
    return np.sum(pv, axis=-1)

#  def计算麦考利久期与def modified_duration
# :param y: 收益率（标量）
    cash_flows = 现金流时间点
        pv = cash_flows / (1 + y) ** times
        return np.sum(times * pv) / P0

# ================= 3. 定价与计算计算 =================

# 当前收益率下的精确价格
P0 = bond_price(y0)

# 生成收益率网格 (2% -99%)并计算精确价格
y_grid = np.linspace(0.02, 0.09, 500)
P_exact_grid = bond_price(y_grid)

# 叠 2. 久期近似（可调参数：收益率变动幅度，例如设定为3%，表示在当前收益率附近绘制久期近似线段长度）
delta_y_range_plot = 0.03  # +/- 3% 中心点为5.3%，两端
y_approx_grid = np.linspace(y0 - delta_y_range_plot[0], y0 +delta_y_range_plot)
P_approx = bond_price(y_approx, P0 * (1 - ModD0 *dy)

# ================= 4. +100bp影响下的计算与报告 =================

y_up100bp = 0.063
y_up100_exact = y0+0001)
P_up100_exact: bond_price(np.array([y_up100])))[0]
dur_approx_relative变化 = -ModD2 *0.01
dur_approx_relative_price变化（小数形式）
dur_approx_change_rel_change =round(dur_approx_change_rel_change,6)

# ================= 5.  输出契约 =================

# 图保存图形
文件路径
figure路径
result = {
    'price_at_up100bp': P_up100_exact,
    'dur_approx_change_up100bp': -Mod *2*0.01
    'figure路径: 'price_yield_curve.png'
}

print(result)
