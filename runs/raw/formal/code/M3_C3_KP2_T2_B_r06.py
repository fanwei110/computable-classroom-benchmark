import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

# --- 1. 初始参数与计算 ---
rf = 0.023
erm = 0.094

sml_slope = erm - rf
er_at_beta_127 = rf + 1.27 * sml_slope

# --- 2. 绘制SML图 ---
fig, ax = plt.subplots(figsize=(10, 6))

# SML线数据
betas = np.linspace(0, 2, 100)
sml_y = rf + betas * sml_slope
sml_line, = ax.plot(betas, sml_y, 'b-', label='SML', linewidth=2)

# 绘制无风险利率和市场组合点（可拖拽）
pt_rf, = ax.plot(0, rf, 'ko', markersize=10, label='Risk-free rate (Drag me)', zorder=5)
pt_m, = ax.plot(1, erm, 'ro', markersize=10, label='Market return (Drag me)', zorder=5)

# 绘制X, Y, Z三点
assets = {'X': (0.62, 0.081), 'Y': (1.18, 0.131), 'Z': (1.51, 0.099)}
markers = {'X': 'g^', 'Y': 'ms', 'Z': 'cD'}
for name, (beta, er) in assets.items():
    ax.plot(beta, er, markers[name], markersize=9, label=f'{name} ({beta}, {er:.1%})', zorder=5)

# 动态文本：斜率和Beta=1.27的收益
txt_slope = ax.text(0.02, 0.95, f'SML Slope: {sml_slope:.2%}', transform=ax.transAxes, va='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=11)
txt_er127 = ax.text(0.02, 0.88, f'E[R] at beta 1.27: {er_at_beta_127:.2%}', transform=ax.transAxes, va='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=11)

# 格式化图表
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_xlim(0, 2)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=1))
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='lower right')

# --- 3. 拖拽交互逻辑 ---
class DraggablePoint:
    def __init__(self, point, x_constraint=None):
        self.point = point
        self.press = None
        self.x_constraint = x_constraint

    def connect(self):
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = (self.point.get_xdata()[0], self.point.get_ydata()[0]), (event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.point.axes: return
        x0, y0 = self.press[0]
        xpress, ypress = self.press[1]
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        
        new_x = x0 + dx
        new_y = y0 + dy
        
        # 约束X轴：rf点只能在beta=0移动，市场点只能在beta=1移动
        if self.x_constraint is not None:
            new_x = self.x_constraint
            
        self.point.set_xdata([new_x])
        self.point.set_ydata([new_y])
        
        update_sml()
        self.point.figure.canvas.draw()

    def on_release(self, event):
        self.press = None

def update_sml():
    new_rf = pt_rf.get_ydata()[0]
    new_erm = pt_m.get_ydata()[0]
    new_slope = new_erm - new_rf
    sml_line.set_ydata(new_rf + betas * new_slope)
    new_er127 = new_rf + 1.27 * new_slope
    txt_slope.set_text(f'SML Slope: {new_slope:.2%}')
    txt_er127.set_text(f'E[R] at beta 1.27: {new_er127:.2%}')

dp_rf = DraggablePoint(pt_rf, x_constraint=0)
dp_m = DraggablePoint(pt_m, x_constraint=1)
dp_rf.connect()
dp_m.connect()

# --- 4. 保存与输出 ---
fig_path = 'sml_plot.png'
plt.savefig(fig_path, bbox_inches='tight')

# 按要求把所有输出存入result字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': fig_path
}

# 打印结果以供验证
print(result)
