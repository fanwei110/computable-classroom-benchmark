import numpy as np
import matplotlib.pyplot as plt

# ==================== 可调参数 ====================
risk_free_rate = 0.023      # 无风险利率 (2.3%)
market_return = 0.094       # 市场期望收益 (9.4%)
# =================================================

# 股票数据：名称, beta, 实际期望收益
stocks = [
    ('X', 0.62, 0.081),
    ('Y', 1.18, 0.131),
    ('Z', 1.51, 0.099)
]

# 计算市场风险溢价 (SML 斜率)
market_premium = market_return - risk_free_rate

# 计算 beta=1.27 处的 CAPM 期望收益
beta_target = 1.27
er_target = risk_free_rate + beta_target * market_premium

# 准备 SML 的 beta 网格
beta_grid = np.linspace(0, 2, 100)
sml_line = risk_free_rate + beta_grid * market_premium

# ========== 绘图 ==========
fig, ax = plt.subplots(figsize=(8, 5))

# 绘制 SML
ax.plot(beta_grid, sml_line, 'b-', linewidth=2, label='Security Market Line (SML)')

# 标出无风险资产和市场组合
ax.scatter([0], [risk_free_rate], color='black', zorder=5)
ax.text(0, risk_free_rate, '  $R_f$', verticalalignment='bottom', fontsize=10)
ax.scatter([1], [market_return], color='black', zorder=5)
ax.text(1, market_return, '  Market', verticalalignment='bottom', fontsize=10)

# 标出三只股票
colors = ['red', 'green', 'orange']
for (name, beta, ret), color in zip(stocks, colors):
    ax.scatter([beta], [ret], color=color, zorder=5, edgecolors='k', s=60)
    ax.text(beta, ret, f'  {name}', verticalalignment='bottom', fontsize=11, fontweight='bold')

# 坐标轴标签与标题
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (CAPM)', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left')

# 保存图形
figure_path = 'sml.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ========== 结果字典 ==========
result = {
    'sml_slope': round(market_premium, 6),          # 斜率 = 市场风险溢价
    'er_at_beta_127': round(er_target, 6),          # beta=1.27 处的 CAPM 期望收益
    'figure_path': figure_path                      # 图形文件路径
}

# 课堂实时运行时可查看结果
if __name__ == '__main__':
    print("结果字典：")
    for k, v in result.items():
        print(f"  {k}: {v}")
