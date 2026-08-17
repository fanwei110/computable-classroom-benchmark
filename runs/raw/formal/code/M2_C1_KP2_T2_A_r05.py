import matplotlib.pyplot as plt

# ========== 可调参数 ==========
rf = 0.023           # 无风险利率
market_return = 0.094  # 市场期望收益
# ============================

# 计算 SML 斜率
sml_slope = market_return - rf

# 计算 Beta=1.27 时的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 生成 Beta 序列
beta = [0, 2]
er = [rf + b * sml_slope for b in beta]

# 三个给定点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 绘图
plt.figure(figsize=(8, 5))
plt.plot(beta, er, 'b-', linewidth=2, label='SML')
plt.axhline(y=rf, color='gray', linestyle='--', linewidth=0.8, label=f'$R_f$ = {rf*100:.1f}%')
plt.axvline(x=1, color='gray', linestyle='--', linewidth=0.8)

# 市场组合点
plt.scatter([1], [market_return], color='blue', s=60, zorder=5)
plt.text(1, market_return, f'  Market (β=1, {market_return*100:.1f}%)',
         verticalalignment='bottom', fontsize=9, color='blue')

# 标出 X, Y, Z
colors = ['red', 'green', 'orange']
for (name, (bx, erx)), c in zip(points.items(), colors):
    plt.scatter(bx, erx, color=c, s=60, zorder=5)
    plt.text(bx, erx, f'  {name} (β={bx}, {erx*100:.1f}%)',
             verticalalignment='bottom', fontsize=9, color=c)

# 标注 Beta=1.27 点
plt.scatter([beta_target], [er_at_beta_127], color='purple', s=60, zorder=5)
plt.text(beta_target, er_at_beta_127 - 0.008, 
         f'β=1.27\n{er_at_beta_127*100:.2f}%', 
         ha='center', fontsize=9, color='purple')

plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.title('Security Market Line (SML)', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 2)
plt.ylim(0, 0.20)
plt.xticks([0, 0.5, 1.0, 1.27, 1.5, 2.0])
plt.tight_layout()

# 保存图片
figure_path = 'sml.png'
plt.savefig(figure_path, dpi=150)
plt.show()

# ========== 输出结果字典 ==========
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print(result)
