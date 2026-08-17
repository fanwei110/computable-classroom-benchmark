import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数化设定 ====================
# 采用百分比数值进行计算，以保证直观性和内部一致性
rf = 2.3      # 无风险利率 (%)
rm = 9.4      # 市场期望收益 (%)

# 三只股票的数据 (beta, 实际收益 %)
stocks = {
    'X': {'beta': 0.62, 'return': 8.1},
    'Y': {'beta': 1.18, 'return': 13.1},
    'Z': {'beta': 1.51, 'return': 9.9}
}

# ==================== 2. 计算 SML 斜率与指定 Beta 的期望收益 ====================
# SML 斜率即市场风险溢价
sml_slope = rm - rf

# Beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==================== 3. 绘制图形 ====================
# 生成 Beta 从 0 到 2 的数据
betas = np.linspace(0, 2, 100)
sml_returns = rf + betas * sml_slope

# 设置图形尺寸与风格
plt.figure(figsize=(10, 7))
plt.style.use('seaborn-v0_8-whitegrid')

# 画出 SML 线
plt.plot(betas, sml_returns, label='Securities Market Line (SML)', 
         color='darkblue', linewidth=2.5)

# 画出无风险利率点与市场组合点
plt.scatter(0, rf, color='black', s=60, zorder=5)
plt.annotate('Risk-free Rate\n(0, 2.3%)', xy=(0, rf), xytext=(15, -15),
             textcoords='offset points', fontsize=10, 
             arrowprops=dict(arrowstyle='->', color='black'))

plt.scatter(1, rm, color='darkblue', s=60, zorder=5)
plt.annotate('Market Portfolio\n(1, 9.4%)', xy=(1, rm), xytext=(15, 10),
             textcoords='offset points', fontsize=10,
             arrowprops=dict(arrowstyle='->', color='darkblue'))

# 画出股票 X, Y, Z 的点，并标注 Alpha（偏离 SML 的部分）
colors = {'X': 'red', 'Y': 'green', 'Z': 'orange'}
for name, data in stocks.items():
    beta_i = data['beta']
    ret_i = data['return']
    sml_ret_i = rf + beta_i * sml_slope  # SML 上的均衡收益
    alpha_i = ret_i - sml_ret_i           # Alpha
    
    # 画股票点
    plt.scatter(beta_i, ret_i, color=colors[name], s=80, zorder=5)
    
    # 画垂直虚线标出 Alpha 偏离
    plt.plot([beta_i, beta_i], [sml_ret_i, ret_i], 
             color=colors[name], linestyle='--', linewidth=1.5)
    
    # 标注文字
    y_offset = 15 if alpha_i >= 0 else -25
    plt.annotate(f"Stock {name}\nβ={beta_i}, E(R)={ret_i}%\nα={alpha_i:.2f}%", 
                 xy=(beta_i, ret_i), 
                 xytext=(20, y_offset),
                 textcoords='offset points',
                 fontsize=10,
                 color=colors[name],
                 arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.2))

# 添加标签与标题
plt.title('CAPM & Securities Market Line (SML)', fontsize=16, fontweight='bold')
plt.xlabel('Beta (Systematic Risk)', fontsize=13)
plt.ylabel('Expected Return (%)', fontsize=13)
plt.xlim(0, 2)
plt.ylim(0, 20)
plt.legend(fontsize=12, loc='upper left')

# ==================== 4. 保存图形并填充 result ====================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 将所有要求的输出存入字典
result = {
    'sml_slope': sml_slope,            # 7.1 (%)
    'er_at_beta_127': er_at_beta_127,  # 11.317 (%)
    'figure_path': figure_path
}

# 课堂展示打印验证
print(f"SML Slope (Market Risk Premium): {result['sml_slope']}%")
print(f"Expected Return at Beta=1.27: {result['er_at_beta_127']}%")
print(f"Figure saved at: {result['figure_path']}")
