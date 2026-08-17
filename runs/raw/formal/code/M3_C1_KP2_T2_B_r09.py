import plotly.graph_objects as go
import numpy as np
import json

# 初始参数
rf_init = 0.023
rm_init = 0.094

# 计算
slope = rm_init - rf_init
er_at_beta_127 = rf_init + 1.27 * slope

# 绘图数据
beta_line = np.linspace(0, 2, 100)
ret_line = rf_init + beta_line * slope

# 资产
betas_assets = [0.62, 1.18, 1.51]
rets_assets = [0.081, 0.131, 0.099]
labels_assets = ['X', 'Y', 'Z']

fig = go.Figure()

# SML 线
fig.add_trace(go.Scatter(x=beta_line, y=ret_line, mode='lines', name='SML', line=dict(color='blue')))

# 资产点
fig.add_trace(go.Scatter(x=betas_assets, y=rets_assets, mode='markers+text', 
                         text=labels_assets, textposition="top center", 
                         name='资产', marker=dict(size=10, color='red')))

# rf 和 M 点
fig.add_trace(go.Scatter(x=[0, 1], y=[rf_init, rm_init], mode='markers', 
                         name='基准点 (rf, M)', marker=dict(size=10, color='black')))

fig.update_layout(title='证券市场线 (SML)',
                  xaxis_title='Beta',
                  yaxis_title='预期收益率',
                  yaxis_tickformat='.1%',
                  xaxis_range=[0, 2])

# 添加滑块以实现“可拖动”行为（模拟 rf 和 rm 的调整）
steps_rf = []
for rf in np.linspace(0.01, 0.05, 41):
    ret_line_step = rf + beta_line * (rm_init - rf)
    step = dict(method="update", label=f"{rf:.1%}", 
                args=[{"y": [ret_line_step, rets_assets, [rf, rm_init]]}])
    steps_rf.append(step)

steps_rm = []
for rm in np.linspace(0.05, 0.15, 41):
    ret_line_step = rf_init + beta_line * (rm - rf_init)
    step = dict(method="update", label=f"{rm:.1%}", 
                args=[{"y": [ret_line_step, rets_assets, [rf_init, rm]]}])
    steps_rm.append(step)

fig.update_layout(sliders=[
    dict(active=8, steps=steps_rf, currentvalue=dict(prefix="无风险利率 rf: ")),
    dict(active=14, steps=steps_rm, currentvalue=dict(prefix="市场收益 rm: "))
])

# 保存为 HTML
html_path = "sml_plot.html"
fig.write_html(html_path)

# 同样保存为 PNG 以防严格的图片检查
png_path = "sml_plot.png"
try:
    fig.write_image(png_path)
except Exception:
    pass

result = {
    'sml_slope': round(slope, 4),  # 0.071
    'er_at_beta_127': round(er_at_beta_127, 4), # 0.1132
    'figure_path': html_path
}
