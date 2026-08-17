import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 可调参数：无风险利率与市场期望收益
# ============================================================
RF = 0.023            # 无风险利率 2.3%
MARKET_RETURN = 0.094 # 市场期望收益 9.4%

# ---------- 计算 SML 参数 ----------
sml_slope = MARKET_RETURN - RF                # 市场风险溢价（斜率）
beta_target = 1.27
er_at_target = RF + beta_target * sml_slope    # beta=1.27 处的 CAPM 期望收益

# ---------- 绘制 SML ----------
beta_vals = np.linspace(0, 2, 200)
sml_vals = RF + beta_vals * sml_slope

plt.figure(figsize=(8, 6))
plt.plot(
    beta_vals, sml_vals,
    color='#2c3e50', linewidth=2.5,
    label='Security Market Line (SML)'
)

# ---------- 股票 X, Y, Z ----------
stocks = {
    'X': {'beta': 0.62, 'return': 0.081, 'color': '#e74c3c'},
    'Y': {'beta': 1.18, 'return': 0.131, 'color': '#27ae60'},
    'Z': {'beta': 1.51, 'return': 0.099, 'color': '#8e44ad'},
}

for name, s in stocks.items():
    plt.scatter(
        s['beta'], s['return'],
        color=s['color'], s=80, zorder=5,
        edgecolors='white', linewidths=0.8,
        label=f'Stock {name}'
    )
    plt.annotate(
        f'{name} (β={s["beta"]}, {s["return"]:.1%})',
        xy=(s['beta'], s['return']),
        xytext=(12 if name != 'Z' else -12, 10),  # 避免重叠
        textcoords='offset points',
        ha='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8)
    )

# ---------- 图形美化 ----------
plt.xlim(0, 2)
plt.ylim(0, 0.20)
plt.xticks(np.arange(0, 2.1, 0.2))
plt.yticks(np.arange(0, 0.21, 0.02))
plt.xlabel('Beta (Systematic Risk)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.title('Capital Asset Pricing Model (CAPM) - Security Market Line', fontsize=14, weight='bold')

# 在图中显示可调参数与计算结果
param_text = (
    f'Risk-Free Rate (Rf) = {RF:.1%}\n'
    f'Market Expected Return (E(Rm)) = {MARKET_RETURN:.1%}\n'
    f'SML Slope (Market Risk Premium) = {sml_slope:.3%}\n'
    f'Expected Return at β={beta_target} = {er_at_target:.4%}'
)
plt.gca().text(
    1.5, 0.02, param_text,
    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
    fontsize=9, verticalalignment='bottom'
)

plt.legend(loc='lower right', fontsize=9)
plt.grid(alpha=0.3)
plt.tight_layout()

# ---------- 保存图形 ----------
figure_path = 'sml_capm.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ---------- 按要求输出 result 字典 ----------
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_target,
    'figure_path': figure_path,
}

# 可打印供教师检查（保留在变量中即可）
print("SML Slope: {:.4f}".format(result['sml_slope']))
print("Expected Return at beta=1.27: {:.4f}".format(result['er_at_beta_127']))
print("Figure saved to:", result['figure_path'])
