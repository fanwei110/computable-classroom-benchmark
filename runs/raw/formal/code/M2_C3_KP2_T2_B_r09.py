import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

# ---------- 输入参数（小数形式） ----------
rf = 0.0230          # 无风险利率
mkt = 0.0940         # 市场组合收益率
beta_range = np.linspace(0, 2, 100)

# 三个股票点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ---------- 计算要求指标 ----------
slope = mkt - rf                              # SML 斜率
beta_target = 1.27
er_target = rf + beta_target * slope          # beta=1.27 的预期收益

result = {
    'sml_slope': round(slope, 6),
    'er_at_beta_127': round(er_target, 6),
    'figure_path': './sml_interactive.html'
}

# ---------- 构建交互式图表 ----------
# 创建基础 SML 线（初始参数 rf, mkt）
sml_y = rf + slope * beta_range

fig = make_subplots()

# SML 线
fig.add_trace(go.Scatter(
    x=beta_range, y=sml_y,
    mode='lines', name='SML',
    line=dict(color='blue', width=2)
))

# 市场组合点 (Beta=1, 市场收益)
fig.add_trace(go.Scatter(
    x=[1], y=[mkt],
    mode='markers', name='市场组合',
    marker=dict(color='red', size=10, symbol='star')
))

# X, Y, Z 点
for name, (b, er) in points.items():
    fig.add_trace(go.Scatter(
        x=[b], y=[er],
        mode='markers+text',
        name=name,
        text=[name],
        textposition='top center',
        marker=dict(size=8)
    ))

# 滑块：rf 和 mkt 两个参数
steps = []
rf_vals = [0.01, 0.02, 0.023, 0.03, 0.04]
mkt_vals = [0.08, 0.09, 0.094, 0.10, 0.12]

for rf_val in rf_vals:
    for mkt_val in mkt_vals:
        s = (mkt_val - rf_val)
        y_line = rf_val + s * beta_range
        # SML 线更新
        line_trace = go.Scatter(
            x=beta_range, y=y_line,
            mode='lines', line=dict(color='blue', width=2),
            name='SML'
        )
        # 市场组合点更新
        mkt_trace = go.Scatter(
            x=[1], y=[mkt_val],
            mode='markers', marker=dict(color='red', size=10, symbol='star'),
            name='市场组合'
        )
        step = dict(
            method='update',
            args=[{'y': [y_line, mkt_trace.y]},
                  {'xaxis.title': 'Beta', 'yaxis.title': '预期收益率'}],
            label=f'rf={rf_val:.3f}, mkt={mkt_val:.3f}'
        )
        steps.append(step)

# 简化：使用两个独立滑块（更直观）
fig = go.Figure()

# SML 线（初始）
fig.add_trace(go.Scatter(
    x=beta_range, y=rf + slope * beta_range,
    mode='lines', name='SML', line=dict(color='blue')
))
# 市场组合
fig.add_trace(go.Scatter(
    x=[1], y=[mkt], mode='markers', name='市场组合',
    marker=dict(color='red', size=10, symbol='star')
))
# 三个股票
for name, (b, er) in points.items():
    fig.add_trace(go.Scatter(
        x=[b], y=[er], mode='markers+text', name=name,
        text=[name], textposition='top center', marker=dict(size=8)
    ))

# 添加滑块
fig.update_layout(
    sliders=[{
        'active': 0,
        'currentvalue': {'prefix': '无风险利率 rf: '},
        'steps': [{
            'label': f'{v:.3f}',
            'method': 'update',
            'args': [
                {'y': [v + (mkt - v) * beta_range, None, None, None, None]},
                {'yaxis.range': [0, 0.2]}
            ]
        } for v in rf_vals]
    }, {
        'active': 0,
        'currentvalue': {'prefix': '市场收益率 mkt: '},
        'steps': [{
            'label': f'{v:.3f}',
            'method': 'update',
            'args': [
                {'y': [rf + (v - rf) * beta_range, None, None, None, None]},
                {'yaxis.range': [0, 0.2]}
            ]
        } for v in mkt_vals]
    }],
    xaxis=dict(title='Beta', range=[0, 2]),
    yaxis=dict(title='预期收益率', range=[0, 0.2]),
    title='证券市场线 (SML) - 可拖动 rf 与市场收益率'
)

# 保存交互式图表为 HTML 文件
pio.write_html(fig, file=result['figure_path'], auto_open=False)

print(result)
