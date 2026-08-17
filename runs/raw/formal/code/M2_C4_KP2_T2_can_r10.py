import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 可调参数（在此修改即可全局生效） ====================
Rf = 0.023          # 无风险利率，小数表示（2.3%）
E_Rm = 0.094        # 市场期望收益，小数表示（9.4%）
# =====================================================================

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'ret': 0.081},
    'Y': {'beta': 1.18, 'ret': 0.131},
    'Z': {'beta': 1.51, 'ret': 0.099}
}

# 计算市场风险溢价（SML斜率）
market_risk_premium = E_Rm - Rf

# SML直线：beta 0 到 2
beta_line = np.linspace(0, 2, 200)
expected_return_line = Rf + beta_line * market_risk_premium

# 单点计算：beta = 1.27 处的CAPM期望收益
beta_target = 1.27
er_at_target = Rf + beta_target * market_risk_premium

# -------------------- 绘制 SML --------------------
plt.figure(figsize=(8, 5))
plt.plot(beta_line, expected_return_line, 'b-', linewidth=2, label='SML')
plt.scatter(0, Rf, color='black', zorder=5, label='无风险利率')
plt.scatter(1, E_Rm, color='green', zorder=5, label='市场组合')

# 标注三只股票
colors = {'X': 'red', 'Y': 'orange', 'Z': 'purple'}
for name, data in stocks.items():
    b = data['beta']
    r = data['ret']
    plt.scatter(b, r, color=colors[name], zorder=6, edgecolor='black', s=60)
    plt.annotate(name, (b, r), textcoords="offset points",
                 xytext=(5, 5), ha='left', fontsize=11, fontweight='bold',
                 color=colors[name])

# 图形修饰
plt.title(f'证券市场线 ( $R_f={Rf:.3f},\ E(R_m)={E_Rm:.3f}$ )', fontsize=14)
plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('期望收益', fontsize=12)
plt.xlim(0, 2)
plt.ylim(0, 0.16)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

# 保存图形
figure_filename = 'sml_plot.png'
plt.savefig(figure_filename, dpi=150)
plt.close()  # 释放内存，防止在某些环境中多余显示

# -------------------- 组织输出 --------------------
result = {
    'sml_slope': round(market_risk_premium, 6),       # 斜率（市场风险溢价）
    'er_at_beta_127': round(er_at_target, 6),          # beta=1.27处的期望收益
    'figure_path': os.path.abspath(figure_filename)    # 图的绝对路径
}

# 打印结果，便于教师在投屏时查看
print("====== CAPM 结果 ======")
print(f"SML 斜率（市场风险溢价）: {result['sml_slope']:.6f}")
print(f"beta = {beta_target} 处的CAPM期望收益: {result['er_at_beta_127']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
print("=======================")
