import matplotlib
matplotlib.use('Agg')  # 非交互式后端，便于无图形界面环境保存图片
import matplotlib.pyplot as plt
import numpy as np

# ========== 可调参数 ==========
R_F = 0.023        # 无风险利率 (2.3%)
E_R_M = 0.094      # 市场期望收益 (9.4%)
# ============================

# 三只股票的数据：名称，beta，实际收益
stocks = [
    ("X", 0.62, 0.081),
    ("Y", 1.18, 0.131),
    ("Z", 1.51, 0.099),
]

# ---------- 计算 SML ----------
market_risk_premium = E_R_M - R_F          # 市场风险溢价，即 SML 斜率
sml_slope = market_risk_premium            # SML 的斜率

# 生成 beta 取值（0 到 2）
beta_vals = np.linspace(0, 2, 100)
sml_vals = R_F + sml_slope * beta_vals     # SML 收益率

# beta = 1.27 处的 CAPM 期望收益
target_beta = 1.27
er_at_beta_127 = R_F + sml_slope * target_beta

# ---------- 绘图 ----------
fig, ax = plt.subplots(figsize=(8, 5))

# 绘制 SML
ax.plot(beta_vals, sml_vals, 'b-', label='SML (CAMP)', linewidth=2)

# 标出无风险利率与市场组合
ax.scatter(0, R_F, color='black', zorder=5)
ax.text(0.05, R_F, f'Risk-free\n({R_F:.3f})', fontsize=9, verticalalignment='bottom')
ax.scatter(1, E_R_M, color='black', zorder=5)
ax.text(1.05, E_R_M, f'Market\n({E_R_M:.3f})', fontsize=9, verticalalignment='bottom')

# 标出三只股票
colors = ['red', 'green', 'orange']
for (name, beta, ret), color in zip(stocks, colors):
    ax.scatter(beta, ret, color=color, s=80, zorder=5)
    ax.annotate(f'{name}\n(β={beta}, r={ret:.3f})',
                (beta, ret),
                textcoords="offset points",
                xytext=(10, 10),
                fontsize=9,
                color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# 图形修饰
ax.set_xlabel('β (Beta)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title(f'Security Market Line (R_f = {R_F:.3f}, E[R_m] = {E_R_M:.3f})', fontsize=13)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right')
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.22)  # 留出上方空间显示标注

plt.tight_layout()

# 保存图片
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)  # 释放内存

# ---------- 输出结果 ----------
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path,
}

# 打印结果供教师查看
print("=== CAPM / SML 分析结果 ===")
print(f"SML 斜率 (市场风险溢价) : {sml_slope:.4f} ({sml_slope*100:.2f}%)")
print(f"β = 1.27 处的CAPM期望收益: {er_at_beta_127:.4f} ({er_at_beta_127*100:.2f}%)")
print(f"图形已保存至: {figure_path}")
print("\nresult 字典内容:")
print(result)
