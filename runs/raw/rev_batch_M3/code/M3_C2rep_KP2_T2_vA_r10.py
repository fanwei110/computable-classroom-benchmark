import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ==========================================
# 1. 参数化设置 (无风险利率与市场期望收益)
# ==========================================
rf = 0.023      # 无风险利率 2.3%
rm = 0.094      # 市场期望收益 9.4%

# ==========================================
# 2. 计算 SML 斜率与特定 Beta 的期望收益
# ==========================================
# SML 方程: E(Ri) = Rf + βi * (Rm - Rf)
# SML 斜率即为市场风险溢价
sml_slope = rm - rf

# 计算 beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 股票数据准备
# ==========================================
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 4. 绘图：证券市场线 (SML) 与股票点
# ==========================================
# 生成 beta 从 0 到 2 的序列
betas = np.linspace(0, 2, 100)
# 计算 SML 对应的期望收益
er_sml = rf + betas * sml_slope

# 创建画布
fig, ax = plt.subplots(figsize=(10, 7))

# 绘制 SML 直线
ax.plot(betas, er_sml, color='blue', linewidth=2, label=f'SML (Slope = {sml_slope:.2%})')

# 标出无风险资产点 (beta=0)
ax.scatter(0, rf, color='blue', marker='o', s=80, zorder=5)
ax.annotate(f'Risk-Free (0, {rf:.1%})', (0, rf), textcoords="offset points", xytext=(10, 5), color='blue')

# 标出市场组合点 (beta=1)
ax.scatter(1, rm, color='blue', marker='o', s=80, zorder=5)
ax.annotate(f'Market (1.0, {rm:.1%})', (1, rm), textcoords="offset points", xytext=(10, -15), color='blue')

# 绘制股票 X, Y, Z 的点并标注
# 为防止标签与线重叠，设置不同的偏移量
colors = {'X': 'red', 'Y': 'green', 'Z': 'purple'}
offsets = {'X': (10, 5), 'Y': (10, 5), 'Z': (10, -15)}

for name, data in stocks.items():
    beta_val = data['beta']
    ret_val = data['return']
    
    # 画点
    ax.scatter(beta_val, ret_val, color=colors[name], s=100, zorder=5, label=f'Stock {name}')
    
    # 计算该 beta 下的 CAPM 理论收益 (用于标示 Alpha 的偏离)
    capm_ret = rf + beta_val * sml_slope
    alpha = ret_val - capm_ret
    
    # 标注内容：名称, 实际收益, Alpha
    label_text = f'{name} (β={beta_val}, E={ret_val:.1%}, α={alpha:.2%})'
    ax.annotate(label_text,
                (beta_val, ret_val),
                textcoords="offset points",
                xytext=offsets[name],
                color=colors[name],
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.2))

# 格式化图表
ax.set_title('Capital Asset Pricing Model (CAPM) - Security Market Line', fontsize=14, fontweight='bold')
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return (E[R])', fontsize=12)
ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=10)

# 限制坐标轴范围使图形美观
ax.set_xlim(-0.05, 2.05)
ax.set_ylim(0.0, 0.18)

# ==========================================
# 5. 保存图形并填充 result 字典
# ==========================================
figure_path = 'sml_capm_plot.png'
fig.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# 严格按要求构建输出字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# (可选) 打印结果以供课堂演示查看
if __name__ == '__main__':
    print("计算结果：")
    print(f"SML 斜率 (市场风险溢价): {result['sml_slope']:.4f} ({result['sml_slope']:.2%})")
    print(f"Beta=1.27 处的 CAPM 期望收益: {result['er_at_beta_127']:.4f} ({result['er_at_beta_127']:.2%})")
    print(f"图形已保存至: {result['figure_path']}")
