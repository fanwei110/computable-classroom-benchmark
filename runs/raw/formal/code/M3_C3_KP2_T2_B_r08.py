import matplotlib.pyplot as plt
import numpy as np

# --- 1. 初始参数与计算 ---
rf = 0.023      # 无风险利率 2.3%
rm = 0.094      # 市场收益率 9.4%

# SML斜率 (市场风险溢价)
sml_slope = rm - rf

# Beta为1.27时的预期收益率
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 资产X, Y, Z的数据
assets = {
    'X': {'beta': 0.62, 'er': 0.081},
    'Y': {'beta': 1.18, 'er': 0.131},
    'Z': {'beta': 1.51, 'er': 0.099}
}

# --- 2. 绘图 ---
fig, ax = plt.subplots(figsize=(10, 8))

# 画SML线 (beta 0 到 2)
betas = np.linspace(0, 2, 100)
sml_returns = rf + betas * sml_slope
sml_line, = ax.plot(betas, sml_returns, label='SML', color='blue', linewidth=2)

# 标出X, Y, Z三个点
for name, data in assets.items():
    ax.scatter(data['beta'], data['er'], color='red', zorder=5)
    ax.annotate(f"{name} ({data['beta']:.2f}, {data['er']:.1%})", 
                xy=(data['beta'], data['er']), 
                xytext=(10, 10), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                fontsize=11)

# 标出可拖动的rf和rm点
rf_point, = ax.plot(0, rf, 'go', markersize=10, zorder=6, label='Rf (Drag me)')
rm_point, = ax.plot(1, rm, 'mo', markersize=10, zorder=6, label='Market (Drag me)')

ax.annotate(f'Rf (0, {rf:.1%})', xy=(0, rf), xytext=(-15, 10), textcoords='offset points', color='green', fontsize=10)
ax.annotate(f'Market (1, {rm:.1%})', xy=(1, rm), xytext=(10, -15), textcoords='offset points', color='purple', fontsize=10)

# 图表格式设置
ax.set_xlim(-0.1, 2.1)
ax.set_ylim(0, 0.18)
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left')

# --- 3. 实现拖拽功能 ---
class DraggablePoint:
    def __init__(self, point, is_rf_point):
        self.point = point
        self.is_rf_point = is_rf_point
        self.press = None
        
    def connect(self):
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = self.point.get_ydata()[0], event.y

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.point.axes: return
        yorig, ypress = self.press
        dy = event.y - ypress
        new_y = max(0, yorig + dy)  # 收益率不能为负数（逻辑限制）
        self.point.set_ydata([new_y])
        
        # 获取当前rf和rm
        current_rf = rf_point.get_ydata()[0]
        current_rm = rm_point.get_ydata()[0]
        
        # 更新SML线
        new_sml_returns = current_rf + betas * (current_rm - current_rf)
        sml_line.set_ydata(new_sml_returns)
        
        self.point.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.point.figure.canvas.draw()

# 绑定拖拽
draggable_rf = DraggablePoint(rf_point, is_rf_point=True)
draggable_rf.connect()
draggable_rm = DraggablePoint(rm_point, is_rf_point=False)
draggable_rm.connect()

# --- 4. 保存图像与输出结果 ---
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
# plt.show() # 在脚本环境中可取消注释以查看交互界面

# 按照契约存入字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print(result)
