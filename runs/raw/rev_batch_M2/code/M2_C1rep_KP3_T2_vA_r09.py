import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ------------------------------
# 债券参数
face_value = 100.0
coupon_rate = 0.046
years = 7
ytm = 0.053
dy = 0.01  # 100个基点（可调参数）
ytm_up = ytm + dy

# ------------------------------
# 现金流时间
t = np.arange(1, years + 1)
cashflows = np.full(years, coupon_rate * face_value)
cashflows[-1] += face_value  # 最后一期还本

# 精确价格函数
def bond_price(y):
    return np.sum(cashflows / (1 + y) ** t)

P0 = bond_price(ytm)
P_up = bond_price(ytm_up)

# 精确相对价格变化（上行100bp）
price_at_up100bp = P_up
exact_relative_change = (P_up - P0) / P0

# ------------------------------
# 久期近似
# 麦考利久期
pv = cashflows / (1 + ytm) ** t
mac_duration = np.sum(t * pv) / P0
modified_duration = mac_duration / (1 + ytm)
dur_approx_change_up100bp = -modified_duration * dy  # 相对变化

# ------------------------------
# 绘图
y_range = np.linspace(0.02, 0.09, 200)
prices = bond_price(y_range)

# 切线（久期近似直线）
# P ≈ P0 + dP/dy * (y - ytm)，其中 dP/dy = - P0 * modified_duration
dPdy = -P0 * modified_duration
tangent_line = P0 + dPdy * (y_range - ytm)

# 使用 plotly 制作可交互图表，添加滑块控制收益率变动幅度（dy）
fig = go.Figure()

fig.add_trace(go.Scatter(x=y_range, y=prices,
                         mode='lines',
                         name='精确价格',
                         line=dict(color='blue')))

# 初始切线（固定显示）
fig.add_trace(go.Scatter(x=y_range, y=tangent_line,
                         mode='lines',
                         name='久期近似（切线）',
                         line=dict(color='red', dash='dash')))

# 当前收益率点
fig.add_trace(go.Scatter(x=[ytm], y=[P0],
                         mode='markers',
                         marker=dict(color='black', size=8),
                         name='当前收益率点'))

# 添加滑块，调整收益率变动区间高亮
# 这里用两个垂直线表示 Δy 范围，并标注价格变化
# 初始 dy = 0.01
def add_dy_lines(dy_val):
    """返回 y_low, y_high 的两条竖线"""
    y_low = ytm - dy_val
    y_high = ytm + dy_val
    P_low = bond_price(y_low)
    P_high = bond_price(y_high)
    return y_low, y_high, P_low, P_high

# 创建滑块的帧？为了简洁，可以用一个滑块控制一个填色区域，但 Plotly 滑块控制需要较多代码。
# 这里采用简单方式：在图上添加滑块，通过更新形状来更改变动幅度。
# 为了可保存为 HTML 并保留交互，我们使用 Plotly 的滑块和 updatemenus 太复杂，
# 可以使用 plotly 的 'sliders' 调节参数。
# 简易方法：预生成多条不同 dy 的垂直线，用滑块控制可见性？
# 我们采用一个可行方案：用滑块修改图形中垂直区间的 x 范围。
# 为了完全“可调”，我将在图中加入滑块，控制一个填充区域。

# 创建一个填充区域表示收益率变动范围
dy_init = 0.01
y_low_init = ytm - dy_init
y_high_init = ytm + dy_init
P_low_init = bond_price(y_low_init)
P_high_init = bond_price(y_high_init)

# 添加填充区域（初始）
fig.add_vrect(x0=y_low_init, x1=y_high_init,
              fillcolor="green", opacity=0.1,
              line_width=0, name='变动区间')

# 添加滑块步骤
steps = []
for delta in np.arange(0.005, 0.051, 0.005):
    y_l = ytm - delta
    y_h = ytm + delta
    step = dict(
        method="relayout",
        args=[{"shapes[0].x0": y_l,
               "shapes[0].x1": y_h}],
        label=f"{delta*100:.0f} bp"
    )
    steps.append(step)

# 注意：fig.add_vrect 会创建一个 shape，索引为 0
# 需要将形状列表控制起来。
fig.update_layout(
    sliders=[dict(
        active=1,  # 初始 dy=0.01 对应索引 1? delta 0.005,0.01,... 0.01是第二个
        currentvalue={"prefix": "收益率变动: "},
        pad={"t": 50},
        steps=steps
    )]
)

# 更新布局
fig.update_layout(
    title="债券价格—收益率曲线及久期近似",
    xaxis_title="收益率",
    yaxis_title="价格",
    legend_title="图例"
)

# 保存为 HTML 文件
figure_path = "bond_price_duration.html"
fig.write_html(figure_path)

# ------------------------------
# 结果字典
result = {
    'price_at_up100bp': round(price_at_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': os.path.abspath(figure_path)
}

print(result)
