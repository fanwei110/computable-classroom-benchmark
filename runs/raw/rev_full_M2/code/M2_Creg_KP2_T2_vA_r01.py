import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 可调参数：无风险利率与市场期望收益（以小数表示）
# 修改这两个值即可调整图形与计算结果
rf = 0.023      # 无风险利率
rm = 0.094      # 市场期望收益
# ============================================================

# 计算 SML 斜率 (市场风险溢价)
sml_slope = rm - rf

# 生成 beta 序列用于绘制 SML 直线
beta_range = np.linspace(0, 2, 100)
sml_line = rf + beta_range * sml_slope

# 股票数据：{名称: (beta, 期望收益)}
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ------------------------------
# 绘图
fig, ax = plt.subplots(figsize=(9, 6))

# 证券市场线
ax.plot(beta_range, sml_line, linewidth=2, color='black',
        label=f'SML (r$_f$={rf:.1%}, E(r$_m$)={rm:.1%})')

# 绘制每一只股票并添加标注
for name, (b, ret) in stocks.items():
    ax.scatter(b, ret, s=80, zorder=5)
    ax.annotate(f'{name}\n(β={b:.2f}, E={ret:.2%})',
                (b, ret), textcoords="offset points",
                xytext=(10, 10), fontsize=10,
                arrowprops=dict(arrowstyle='->', lw=1.2))

# 坐标轴与标题
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', alpha=0.6)

# 保存图像
figure_path = os.path.abspath('sml.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()   # 避免在非交互环境中弹出窗口

# ------------------------------
# 计算 beta = 1.27 时的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ------------------------------
# 输出结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印结果以供查看（脚本运行后可直接看到）
print("Result dictionary:")
for k, v in result.items():
    print(f"  {k}: {v}")

# 此时 result 已按要求准备好，可直接被其他模块导入使用
