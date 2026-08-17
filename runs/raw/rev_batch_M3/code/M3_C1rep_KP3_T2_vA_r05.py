import numpy as np
import plotly.graph_objects as go

# 债券参数
F = 100       # 面值
C = 4.6       # 票息
n = 7         # 期限
y0 = 0.053    # 初始收益率 5.3%

# 债券精确价格计算函数
def bond_price(y):
    return sum(C / (1+y)**t for t in range(1, n+1)) + F / (1+y)**n

# 修正久期计算函数
def mod_duration(y):
    p = bond_price(y)
    mac_d = sum(t * C / (1+y)**t for t in range(1, n+1)) + n * F / (1+y)**n
    return (mac_d / p) / (1 + y)

# 1. 计算收益率上升100个基点后的精确价格
y_up_100bp = y0 + 0.01
price_at_up100bp = round(bond_price(y_up_100bp), 4)

# 2. 计算用久期估计的相对价格变化
md0 = mod_duration(y0)
dur_approx_change_up100bp = round(-md0 * 0.01, 6)

# 3. 生成价格-收益率曲线数据
yields = np.linspace(0.02, 0.09, 300)
exact_prices = [bond_price(y) for y in yields]

# 基于初始收益率 y0 的久期近似线
p0 = bond_price(y0)
approx_prices_base = [p0 * (1 - md0 * (y - y0)) for y in yields]

# 4. 绘制交互式图表（含收益率变动幅度滑块）
fig = go.Figure()

# 添加精确价格曲线
fig.add_trace(go.Scatter(
    x=yields*100, y=exact_prices, mode='lines', 
    name='精确价格', line=dict(color='blue', width=3)
))

# 添加久期近似曲线
fig.add_trace(go.Scatter(
    x=yields*100, y=approx_prices_base, mode='lines', 
    name='久期近似', line=dict(color='red', dash='dash', width=2)
))

# 添加初始基准点标记
fig.add_trace(go.Scatter(
    x=[y0*100], y=[p0], mode='markers',
    name='初始基准点 (5.3%)', marker=dict(size=10, color='black', symbol='circle')
))

# 初始变动点标记（变动幅度为0时重合）
delta_y_init = 0
y_target_init = y0 + delta_y_init
p_exact_init = bond_price(y_target_init)
p_approx_init = p0 * (1 - md0 * delta_y_init)

fig.add_trace(go.Scatter(
    x=[y_target_init*100], y=[p_exact_init], mode='markers',
    name='变动后精确价格', marker=dict(size=12, color='blue', symbol='x')
))
fig.add_trace(go.Scatter(
    x=[y_target_init*100], y=[p_approx_init], mode='markers',
    name='变动后近似价格', marker=dict(size=12, color='red', symbol='diamond')
))

# 创建“收益率变动幅度”可调滑块
steps = []
for delta_y in np.linspace(-0.05, 0.05, 101):
    y_target = y0 + delta_y
    p_exact_target = bond_price(y_target)
    p_approx_target = p0 * (1 - md0 * delta_y)
    
    step = dict(
        method="update",
        args=[
            {"x": [yields*100, yields*100, [y0*100], [y_target*100], [y_target*100]],
             "y": [exact_prices, approx_prices_base, [p0], [p_exact_target], [p_approx_target]]},
            {"title": f"债券价格-收益率曲线 (收益率变动: {delta_y*100:+.1f}%)",
             "annotations": [
                 dict(x=y_target*100, y=p_exact_target, text=f"精确: {p_exact_target:.2f}", showarrow=True, arrowhead=1, ax=40, ay=-40),
                 dict(x=y_target*100, y=p_approx_target, text=f"近似: {p_approx_target:.2f}", showarrow=True, arrowhead=1, ax=-40, ay=40)
             ]}
        ],
        label=f"{delta_y*100:+.1f}%"
    )
    steps.append(step)

sliders = [dict(
    active=50, # 对应变动幅度 0.0%
    currentvalue={"prefix": "收益率变动幅度 (Δy): ", "font": {"size": 16}},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders,
    title="债券价格-收益率曲线 (收益率变动: +0.0%)",
    xaxis_title="收益率 (%)",
    yaxis_title="价格",
    legend_title="图例",
    font=dict(size=14),
    template="plotly_white"
)

# 保存为交互式HTML文件
figure_path = 'bond_price_yield_curve.html'
fig.write_html(figure_path)

# 5. 按照输出契约存入字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

print(result)
