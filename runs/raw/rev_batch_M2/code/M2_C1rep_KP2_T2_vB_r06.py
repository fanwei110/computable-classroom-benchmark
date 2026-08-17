import os
import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.models import Slider, CustomJS, ColumnDataSource, Div, LabelSet
from bokeh.layouts import column

# ---------- 初始参数 ----------
rf_init = 0.023      # 无风险利率 2.3%
rm_init = 0.094      # 市场收益率 9.4%
beta_range = np.linspace(0, 2, 100)

# ---------- 计算静态结果 ----------
market_premium = rm_init - rf_init                # SML 斜率
sml_slope = market_premium                       # 0.071
er_at_beta_127 = rf_init + 1.27 * market_premium # β=1.27 对应的预期收益

# ---------- 数据源 ----------
source_sml = ColumnDataSource(data=dict(
    beta=beta_range,
    er=rf_init + beta_range * market_premium
))
source_rf = ColumnDataSource(data=dict(beta=[0], er=[rf_init]))
source_mkt = ColumnDataSource(data=dict(beta=[1], er=[rm_init]))
source_xyz = ColumnDataSource(data=dict(
    beta=[0.62, 1.18, 1.51],
    er=[0.081, 0.131, 0.099],
    label=['X', 'Y', 'Z']
))

# ---------- 文字提示 ----------
slope_div = Div(text=f"SML 斜率：{market_premium:.4f} （{market_premium*100:.2f}%）")
er_beta127_div = Div(text=f"β=1.27 预期收益：{er_at_beta_127:.4f} （{er_at_beta_127*100:.2f}%）")

# ---------- 绘图 ----------
p = figure(title="证券市场线 (SML) - 可拖动 rf 与市场收益",
           x_range=(-0.1, 2.2), y_range=(0, 0.2),
           x_axis_label="贝塔 (β)", y_axis_label="预期收益率",
           tools="pan,wheel_zoom,box_zoom,reset,save")

p.line('beta', 'er', source=source_sml, line_width=2, legend_label='SML')
p.scatter('beta', 'er', source=source_rf, size=12, color='red', legend_label='无风险利率 (β=0)')
p.scatter('beta', 'er', source=source_mkt, size=12, color='green', marker='s', legend_label='市场组合 (β=1)')
p.scatter('beta', 'er', source=source_xyz, size=12, color='blue', marker='d', legend_label='股票 X, Y, Z')

# 为股票添加标签
labels = LabelSet(x='beta', y='er', text='label', source=source_xyz, x_offset=6, y_offset=6)
p.add_layout(labels)

# ---------- 滑块 ----------
slider_rf = Slider(start=0, end=0.05, value=rf_init, step=0.001, title="无风险利率 (rf)")
slider_rm = Slider(start=0.05, end=0.15, value=rm_init, step=0.001, title="市场收益率 (rm)")

# ---------- 交互回调 ----------
callback = CustomJS(args=dict(
    source_sml=source_sml,
    source_rf=source_rf,
    source_mkt=source_mkt,
    slope_div=slope_div,
    er_beta127_div=er_beta127_div,
    slider_rf=slider_rf,
    slider_rm=slider_rm
), code="""
    const rf = slider_rf.value;
    const rm = slider_rm.value;
    const prem = rm - rf;

    // 更新 SML 线
    const betas = source_sml.data['beta'];
    const ers = source_sml.data['er'];
    for (let i = 0; i < betas.length; i++) {
        ers[i] = rf + betas[i] * prem;
    }
    source_sml.data['er'] = ers;
    source_sml.change.emit();

    // 更新无风险点
    source_rf.data['er'] = [rf];
    source_rf.change.emit();

    // 更新市场点
    source_mkt.data['er'] = [rm];
    source_mkt.change.emit();

    // 更新文字
    slope_div.text = "SML 斜率：" + prem.toFixed(4) + " （" + (prem*100).toFixed(2) + "%）";
    const er127 = rf + 1.27 * prem;
    er_beta127_div.text = "β=1.27 预期收益：" + er127.toFixed(4) + " （" + (er127*100).toFixed(2) + "%）";
""")
slider_rf.js_on_change('value', callback)
slider_rm.js_on_change('value', callback)

# ---------- 布局与保存 ----------
layout = column(slider_rf, slider_rm, slope_div, er_beta127_div, p)
output_path = os.path.abspath("sml_interactive.html")
output_file(output_path)
save(layout)

# ---------- 结果契约 ----------
result = {
    'sml_slope': sml_slope,            # 0.071 即 7.1%
    'er_at_beta_127': er_at_beta_127,  # 0.11317 即 11.317%
    'figure_path': output_path
}

print(result)
