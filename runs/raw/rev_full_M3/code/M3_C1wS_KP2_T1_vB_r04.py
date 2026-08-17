import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设定
# ==========================================
rf = 0.023          # 无风险利率 rf = 2.3%
rm = 0.094          # 市场期望收益 E[Rm] = 9.4%
beta_x = 0.62       # 股票 X 的 Beta
beta_y = 1.18       # 股票 Y 的 Beta
beta_z = 1.51       # 股票 Z 的 Beta
actual_ry = 0.131   # 股票 Y 的实际收益 = 13.1%

# 市场风险溢价
market_premium = rm - rf

# ==========================================
# 2. 套用 CAPM 公式：E[Ri] = rf + beta * (E[Rm] - rf)
# ==========================================
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ==========================================
# 3. 计算 Y 的 Alpha：实际收益 - CAPM 预测收益
# ==========================================
alpha_y = actual_ry - er_y

# ==========================================
# 4. 填充 result 字典
# ==========================================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==========================================
# 5. 控制台输出（辅助课堂投屏讲解）
# ==========================================
print("="*45)
print("       CAPM 与证券市场线 (SML) 计算结果       ")
print("="*45)
print(f"无风险利率 (rf):       {rf:.1%}")
print(f"市场期望收益 (E[Rm]): {rm:.1%}")
print(f"市场风险溢价 (MRP):   {market_premium:.1%}")
print("-" * 45)
print(f"股票 X (β={beta_x}): E[Rx] = {er_x:.4%}")
print(f"股票 Y (β={beta_y}): E[Ry] = {er_y:.4%}")
print(f"股票 Z (β={beta_z}): E[Rz] = {er_z:.4%}")
print("-" * 45)
print(f"股票 Y 实际收益:      {actual_ry:.1%}")
print(f"股票 Y 的 Alpha (α):  {alpha_y:.4%}")
print("="*45)
print(f"\nresult 字典内容: \n{result}\n")

# ==========================================
# 6. 可视化：绘制证券市场线 (SML) 与 Alpha 偏离
# ==========================================
# 生成 SML 线的数据
betas_line = np.linspace(0, 1.8, 100)
sml_line = rf + betas_line * market_premium

fig, ax = plt.subplots(figsize=(9, 6))

# 绘制 SML
ax.plot(betas_line, sml_line, label='SML: $E[R_i] = r_f + \\beta_i (E[R_m] - r_f)$', 
        color='blue', linewidth=2)

# 绘制 X, Y, Z 在 SML 上的定价点
ax.scatter([beta_x, beta_y, beta_z], [er_x, er_y, er_z], 
           color='black', s=60, zorder=5, label='CAPM Fair Return (on SML)')

# 标注 SML 上的点
ax.annotate(f'X (β={beta_x})\nE[R]={er_x:.2%}', xy=(beta_x, er_x), 
            xytext=(beta_x-0.15, er_x-0.012), fontsize=10)
ax.annotate(f'Z (β={beta_z})\nE[R]={er_z:.2%}', xy=(beta_z, er_z), 
            xytext=(beta_z+0.05, er_z-0.012), fontsize=10)

# 绘制 Y 的实际收益点
ax.scatter([beta_y], [actual_ry], color='red', s=80, zorder=5, marker='*', 
           label='Actual Return of Y')
ax.annotate(f'Y Actual\n{actual_ry:.1%}', xy=(beta_y, actual_ry), 
            xytext=(beta_y+0.1, actual_ry), fontsize=10, color='red')

# 绘制 Alpha 线段 (垂直距离)
ax.vlines(beta_y, er_y, actual_ry, colors='red', linestyles='dashed', linewidth=1.5)
ax.text(beta_y + 0.05, (er_y + actual_ry)/2, f'α = {alpha_y:.2%}', 
        color='red', fontsize=12, fontweight='bold',
        bbox=dict(facecolor='white', edgecolor='red', alpha=0.8))

# 图表装饰
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return $E[R_i]$', fontsize=12)
ax.set_title('Capital Asset Pricing Model (CAPM) & Alpha', fontsize=14)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlim(0, 1.8)
ax.set_ylim(0, 0.16)

# 展示图像
plt.tight_layout()
plt.show()
