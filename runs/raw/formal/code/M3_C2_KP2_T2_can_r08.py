import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==========================================
# 1. 参数化无风险利率与市场期望收益
# ==========================================
rf = 0.023      # 无风险利率 2.3%
rm = 0.094      # 市场期望收益 9.4%

# ==========================================
# 2. 计算 SML 斜率及 beta=1.27 处的期望收益
# ==========================================
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 画出 beta 从 0 到 2 的 SML 并标出股票点
# ==========================================
# SML 线数据
betas = np.linspace(0, 2, 100)
er_sml = rf + betas * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 SML 线
ax.plot(betas, er_sml, label=f'SML (Slope={sml_slope:.3f})', color='blue', linewidth=2)

# 绘制无风险利率和市场组合点作为参考
ax.scatter(0, rf, color='black', zorder=5)
ax.annotate('Risk-Free Rate', xy=(0, rf), xytext=(15, -15), 
            textcoords='offset points', fontsize=9)
ax.scatter(1, rm, color='black', zorder=5)
ax.annotate('Market Portfolio', xy=(1, rm), xytext=(15, 10), 
            textcoords='offset points', fontsize=9)

# 绘制三只股票并标注
for name, data in stocks.items():
    beta_val = data['beta']
    ret_val = data['return']
    ax.scatter(beta_val, ret_val, color='red', zorder=5)
    # 标注内容：股票名、Beta、实际收益
    ax.annotate(f"Stock {name}\n(β={beta_val}, r={ret_val*100:.1f}%)", 
                xy=(beta_val, ret_val), 
                xytext=(20, 10 if ret_val > rf + beta_val * sml_slope else -25), 
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.6),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# 格式化图表
ax.set_title('Security Market Line (SML) & Stock Positions', fontsize=14)
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.xaxis.set_major_locator(mticker.MultipleLocator(0.2))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=1))
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=11)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.18)

# ==========================================
# 4. 保存图形并填充 result 字典
# ==========================================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印结果以供验证
print("Result Dictionary:")
print(result)
