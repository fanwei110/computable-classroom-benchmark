import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# 可调参数（教师可在此修改）
R_f = 2.3        # 无风险利率，单位：%
E_R_m = 9.4      # 市场期望收益，单位：%
# ==============================================

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 8.1},
    'Y': {'beta': 1.18, 'return': 13.1},
    'Z': {'beta': 1.51, 'return': 9.9}
}

# ---------- 计算 ----------
sml_slope = E_R_m - R_f          # 市场风险溢价（SML斜率）
beta_target = 1.27
er_at_beta_127 = R_f + sml_slope * beta_target

# ---------- 绘图 ----------
beta_range = np.linspace(0, 2, 100)
sml_line = R_f + sml_slope * beta_range

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(beta_range, sml_line, 'b-', linewidth=2, label='Security Market Line')

# 市场组合
ax.scatter(1, E_R_m, color='black', s=80, zorder=5, label='Market Portfolio')
ax.annotate(f'Market\n(β=1, E(R)={E_R_m:.1f}%)', (1, E_R_m),
            textcoords="offset points", xytext=(10, 0), fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=1.0))

# 无风险资产
ax.scatter(0, R_f, color='black', s=80, zorder=5, label='Risk‑free Asset')
ax.annotate(f'Rf = {R_f}%', (0, R_f),
            textcoords="offset points", xytext=(-50, 5), fontsize=9)

# 三只股票
for name, s in stocks.items():
    ax.scatter(s['beta'], s['return'], marker='X', s=100, zorder=5,
               label=f'Stock {name}')
    ax.annotate(f'{name}  (β={s["beta"]:.2f}, r={s["return"]:.1f}%)',
                (s['beta'], s['return']),
                textcoords="offset points", xytext=(15, 10), fontsize=9,
                arrowprops=dict(arrowstyle='->', lw=1.0))

# 格式
ax.set_xlabel('Beta (β)')
ax.set_ylabel('Expected Return (%)')
ax.set_title('Security Market Line (SML)')
ax.set_xlim(0, 2)
ax.set_ylim(0, max(sml_line.max(), max(s['return'] for s in stocks.values())) + 3)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right')

plt.tight_layout()

# ---------- 保存图形 ----------
figure_path = 'sml_chart.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)   # 若在交互环境中运行可替换为 plt.show()

# ---------- 输出结果 ----------
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print(result)
