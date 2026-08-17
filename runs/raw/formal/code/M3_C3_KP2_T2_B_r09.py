import plotly.graph_objects as go
import os

# 1. 初始参数设定 (小数表示)
rf = 0.023
rm = 0.094

# 2. 计算 SML 斜率和 Beta=1.27 对应的收益率
sml_slope = rm - rf
er_at_beta_127 = rf + 1.27 * sml_slope

# 3. 定义 SML 线上的点 (Beta 从 0 到 2)
beta_line = [0, 2]
er_line = [rf, rf + 2 * sml_slope]

# 4. 定义资产 X, Y, Z 的坐标
points_beta = [0.62, 1.18, 1.51]
points_er = [0.081, 0.131, 0.099]
points_name = ['X', 'Y', 'Z']

# 5. 创建 Plotly 交互图表
fig = go.Figure()

# 添加 SML 线
fig.add_trace(go.Scatter(
    x=beta_line, 
    y=er_line,
    mode='lines',
    name='SML',
    line=dict(color='blue', width=2)
))

# 添加资产点 X, Y, Z
fig.add_trace(go.Scatter(
    x=points_beta, 
    y=points_er,
    mode='markers+text',
    name='资产点',
    text=points_name,
    textposition='top center',
    marker=dict(size=10, color='red')
))

# 添加可拖动的无风险利率(rf)点和市场收益(Market)点
# 将它们单独放在一个 trace 中，方便识别与拖动
fig.add_trace(go.Scatter(
    x=[0, 1], 
    y=[rf, rm],
    mode='markers+text',
    name='关键点 (可拖动)',
    text=['rf', 'Market'],
    textposition='top center',
    marker=dict(size=12, color='green', symbol='diamond')
))

# 6. 设置图表格式
fig.update_layout(
    title='Security Market Line (SML) - 拖动绿色菱形点可改变rf与Market',
    xaxis_title='Beta',
    yaxis_title='Expected Return (E[R])',
    xaxis=dict(range=[-0.1, 2.2], dtick=0.5),
    yaxis=dict(range=[0, 0.20], tickformat='.1%'),
    showlegend=True
)

# 7. 保存图表为 HTML 文件（保留交互拖动功能）
# 在 Plotly 的 HTML 输出中，设置 editable=True 可以让用户在浏览器中拖动数据点
figure_path = 'sml_interactive_plot.html'
fig.write_html(figure_path, config={'editable': True, 'scrollZoom': True})

# 8. 将结果存入字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印结果验证
print(result)
