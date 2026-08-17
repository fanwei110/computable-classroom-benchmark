import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

# 1. 参数设置
K = 97.5
r = 0.043
T = 0.58
S_range = np.linspace(70, 140, 700)
vols = [0.15, 0.276, 0.40]

# 2. 定义Black-Scholes Delta计算函数 (看涨期权)
def calc_call_delta(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 3. 计算标的等于110、波动率27.6%时的Delta
delta_s110 = calc_call_delta(110, K, T, r, 0.276)

# 4. 绘制交互式图表
fig = go.Figure()

# 画出给定的三条波动率曲线
for vol in vols:
    deltas = calc_call_delta(S_range, K, T, r, vol)
    fig.add_trace(go.Scatter(
        x=S_range, 
        y=deltas, 
        mode='lines', 
        name=f'Vol = {vol*100:.1f}%'
    ))

# 添加一条可调的自定义波动率曲线 (初始设为27.6%)
custom_vol_init = 0.276
fig.add_trace(go.Scatter(
    x=S_range, 
    y=calc_call_delta(S_range, K, T, r, custom_vol_init),
    mode='lines', 
    name='Custom Vol (Adjustable)', 
    line=dict(dash='dash', width=4)
))

# 制作滑动条，实现波动率可调
steps = []
for vol in np.arange(0.10, 0.51, 0.01):
    step = dict(
        method="restyle",
        args=[{"y": [calc_call_delta(S_range, K, T, r, vol)]}, [3]], # 更新第4条trace
        label=f"{vol*100:.0f}%"
    )
    steps.append(step)

sliders = [dict(
    active=17, # 初始位置对应 0.27 (最接近0.276)
    currentvalue={"prefix": "Custom Vol: "},
    steps=steps
)]

fig.update_layout(
    title="Call Option Delta vs Underlying Price",
    xaxis_title="Underlying Price (S)",
    yaxis_title="Delta",
    legend_title="Volatility",
    sliders=sliders
)

# 5. 保存图表并输出结果
figure_path = "delta_vs_S_interactive.html"
fig.write_html(figure_path)

# 按照输出契约存入字典
result = {
    'delta_at_s110': round(delta_s110, 4),
    'figure_path': figure_path
}

print(result)
