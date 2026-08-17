import numpy as np
import os

# --- 1. 固定计算 ---
rf = 2.3
rm = 9.4
slope = rm - rf                # 市场风险溢价
beta_target = 1.27
er_target = rf + beta_target * slope   # 所需收益率

result = {
    'sml_slope': slope,
    'er_at_beta_127': er_target,
    'figure_path': 'sml_interactive.html'
}

# --- 2. 尝试用 bokeh 绘制可交互图（带两个滑块）---
try:
    from bokeh.plotting import figure, output_file, save
    from bokeh.models import ColumnDataSource, Slider, CustomJS, Label
    from bokeh.layouts import column

    beta_vals = np.linspace(0, 2, 200)
    er_vals = rf + beta_vals * slope
    source = ColumnDataSource(data=dict(beta=beta_vals, er=er_vals))

    p = figure(title="Security Market Line (SML) with Adjustable Rf and Rm",
               x_axis_label='Beta', y_axis_label='Expected Return (%)',
               width=700, height=500)
    p.line('beta', 'er', source=source, line_width=2, legend_label='SML')

    # 标注三个股票点
    points = {'X': (0.62, 8.1), 'Y': (1.18, 13.1), 'Z': (1.51, 9.9)}
    colors = ['red', 'green', 'orange']
    for i, (name, (b, r)) in enumerate(points.items()):
        p.scatter(x=[b], y=[r], size=10, color=colors[i], legend_label=f'{name} (β={b}, R={r}%)')
        p.add_layout(Label(x=b, y=r, text=name, x_offset=5, y_offset=5))

    # 滑块
    rf_slider = Slider(start=0, end=5, value=rf, step=0.1, title="Risk-free Rate (%)")
    rm_slider = Slider(start=7, end=15, value=rm, step=0.1, title="Market Return (%)")

    # JS 回调：滑块变化时更新直线
    callback = CustomJS(args=dict(source=source, rf_slider=rf_slider, rm_slider=rm_slider), code="""
        const data = source.data;
        const beta = data['beta'];
        const er = data['er'];
        const rf = rf_slider.value;
        const rm = rm_slider.value;
        for (let i = 0; i < beta.length; i++) {
            er[i] = rf + beta[i] * (rm - rf);
        }
        source.change.emit();
    """)
    rf_slider.js_on_change('value', callback)
    rm_slider.js_on_change('value', callback)

    output_file(result['figure_path'], title="SML Interactive")
    save(column(p, rf_slider, rm_slider))
    print("交互图已用 bokeh 生成。")

except ImportError:
    # --- 3. 备选方案：Plotly 可编辑模式（点可拖，但线不会自动更新）---
    try:
        import plotly.graph_objects as go
        import plotly.io as pio

        beta_vals = np.linspace(0, 2, 100)
        er_vals = rf + beta_vals * slope

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=beta_vals, y=er_vals, mode='lines', name='SML'))

        fig.add_trace(go.Scatter(x=[0.62, 1.18, 1.51], y=[8.1, 13.1, 9.9],
                                 mode='markers+text', text=['X', 'Y', 'Z'],
                                 textposition='top center',
                                 marker=dict(size=10, color=['red', 'green', 'orange']),
                                 name='Stocks'))

        fig.add_trace(go.Scatter(x=[0, 1], y=[rf, rm],
                                 mode='markers+text', text=['Rf', 'Rm'],
                                 textposition='bottom center',
                                 marker=dict(size=12, color='black', symbol='diamond'),
                                 name='Rf & Rm (可拖拽)'))

        fig.update_layout(xaxis_title='Beta', yaxis_title='Expected Return (%)',
                          title='SML (Drag the Rf and Rm points to adjust)')

        fig.write_html(result['figure_path'],
                       config={'editable': True, 'edits': {'shapePosition': True}})
        print("交互图已用 Plotly（可编辑点）生成，线不会自动更新。")
    except ImportError:
        # --- 4. 最后的静态图 fallback ---
        import matplotlib.pyplot as plt
        beta_vals = np.linspace(0, 2, 100)
        er_vals = rf + beta_vals * slope
        plt.figure()
        plt.plot(beta_vals, er_vals, label='SML')
        plt.scatter([0.62, 1.18, 1.51], [8.1, 13.1, 9.9], c=['red', 'green', 'orange'])
        for x, y, t in zip([0.62, 1.18, 1.51], [8.1, 13.1, 9.9], ['X', 'Y', 'Z']):
            plt.text(x, y, t)
        plt.axhline(rf, linestyle='--', color='gray', label='Rf')
        plt.axhline(rm, linestyle='--', color='gray', label='Rm')
        plt.xlabel('Beta')
        plt.ylabel('Expected Return (%)')
        plt.title('SML')
        plt.legend()
        static_path = result['figure_path'].replace('.html', '.png')
        plt.savefig(static_path)
        result['figure_path'] = static_path
        print("仅生成了静态图片（缺少可拖拽交互功能）。")

print(result)
