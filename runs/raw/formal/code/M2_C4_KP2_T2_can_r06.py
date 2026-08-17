import numpy as np
import matplotlib.pyplot as plt
import os

# ========================================================
# 可调参数：无风险利率与市场期望收益（均以小数表示）
# 教师可在以下两行直接修改数值，再运行即可更新全图及结果
rf = 0.023    # 无风险利率 (2.3%)
rm = 0.094    # 市场期望收益 (9.4%)
# ========================================================

# ---------- 计算 SML 斜率（市场风险溢价）----------
slope = rm - rf         # CAPM 的斜率 = E(Rm) - Rf

# ---------- 三只股票的数据 ----------
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ---------- 生成 SML 线 ----------
betas = np.linspace(0, 2, 200)
er_sml = rf + slope * betas

# ---------- 绘制证券市场线 ----------
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(betas, er_sml, 'b-', linewidth=2, label='Security Market Line (SML)')
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (CAPM)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.6)

# 辅助线：无风险利率水平线 & 市场组合的 beta=1 竖线
ax.axhline(y=rf, color='gray', linestyle=':', linewidth=1)
ax.axvline(x=1.0, color='gray', linestyle=':', linewidth=1)

# 标注市场组合 (β=1, E(Rm))
ax.scatter(1.0, rm, color='green', s=100, zorder=5, label='Market Portfolio')
ax.text(1.0, rm + 0.003, f'Market\n(β=1.00, E(Rm)={rm:.3f})',
        ha='center', fontsize=9)

# 标注三只股票
colors = ['darkred', 'darkorange', 'purple']
for (name, data), color in zip(stocks.items(), colors):
    b = data['beta']
    r = data['return']
    ax.scatter(b, r, color=color, s=80, zorder=5)
    # 在点旁边显示名称、beta 值和实现收益
    ax.text(b + 0.03, r + 0.001, f'{name} (β={b}, r={r:.3f})',
            fontsize=9, color=color, weight='bold')

ax.legend(loc='lower right')

# 保存图形（绝对路径，确保可复现）
figure_path = os.path.abspath('sml.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()   # 释放内存，避免在交互环境中重复显示

# ---------- 计算 beta = 1.27 处的 CAPM 期望收益 ----------
beta_target = 1.27
er_target = rf + slope * beta_target

# ---------- 输出结果字典（严格按照契约要求的键名）----------
result = {
    'sml_slope': slope,                # 市场风险溢价
    'er_at_beta_127': er_target,       # β=1.27 对应的期望收益
    'figure_path': figure_path         # 图形文件的绝对路径
}

# 可选：打印结果供课堂查看
print("===== CAPM SML 分析结果 =====")
print(f"SML 斜率 (市场风险溢价): {slope:.5f}  ({slope*100:.2f}%)")
print(f"β=1.27 处的 CAPM 期望收益: {er_target:.5f}  ({er_target*100:.2f}%)")
print(f"图形已保存至: {figure_path}")
print("\n结果字典:", result)
