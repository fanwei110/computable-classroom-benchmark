import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数化无风险利率与市场期望收益
# ==========================================
rf = 0.023      # 无风险利率 2.3%
rm = 0.094      # 市场期望收益 9.4%

# ==========================================
# 2. 计算 SML 斜率与 beta=1.27 处的期望收益
# ==========================================
# CAPM 公式: E(Ri) = rf + beta * (rm - rf)
# SML 斜率即为市场风险溢价
sml_slope = rm - rf

# 计算 beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 准备绘图数据
# ==========================================
# beta 范围 0 到 2
betas = np.linspace(0, 2, 100)
# SML 线上的期望收益
er_sml = rf + betas * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 4. 绘制证券市场线与股票点
# ==========================================
# 为确保在任意系统下中文及负号正常显示，使用英文标注及标准字体设置
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 画出 SML
ax.plot(betas, er_sml * 100, color='blue', linewidth=2, label='Security Market Line (SML)')

# 画出无风险利率点和市场组合点作为参考
ax.scatter(0, rf * 100, color='black', zorder=5)
ax.annotate(f'Rf = {rf*100:.1f}%', (0, rf * 100), textcoords="offset points", xytext=(10, -10))

ax.scatter(1, rm * 100, color='green', zorder=5)
ax.annotate(f'Market (β=1, E[R]={rm*100:.1f}%)', (1, rm * 100), textcoords="offset points", xytext=(10, -15))

# 画出股票 X, Y, Z 并标注
colors = {'X': 'red', 'Y': 'orange', 'Z': 'purple'}
offsets = {'X': (10, 10), 'Y': (10, 5), 'Z': (10, -15)} # 调整标注位置防重叠

for name, data in stocks.items():
    beta_i = data['beta']
    ret_i = data['return']
    ret_sml_i = rf + beta_i * sml_slope # 该 beta 下的 CAPM 期望收益
    
    # 画股票点
    ax.scatter(beta_i, ret_i * 100, color=colors[name], zorder=5, s=60)
    
    # 画偏离 SML 的虚线（直观展示 Alpha）
    ax.vlines(beta_i, min(ret_i, ret_sml_i) * 100, max(ret_i, ret_sml_i) * 100, 
              color=colors[name], linestyles='dashed', linewidth=1)
    
    # 标注股票名称和收益
    ax.annotate(f'Stock {name}\n(β={beta_i}, R={ret_i*100:.1f}%)', 
                (beta_i, ret_i * 100), 
                textcoords="offset points", 
                xytext=offsets[name],
                arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.5))

# 图表格式设置
ax.set_title('CAPM & Security Market Line (SML)', fontsize=14)
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return (%)', fontsize=12)
ax.set_xlim(-0.05, 2.1)
ax.set_ylim(0, 16)
ax.axhline(0, color='grey', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left', fontsize=11)

# ==========================================
# 5. 保存图形并填充 result 字典
# ==========================================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 将结果存入字典，键名严格按要求指定
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 控制台输出验证（教师投屏可见）
print(f"--- Calculation Results ---")
print(f"SML Slope (Market Risk Premium): {result['sml_slope']:.4f} ({result['sml_slope']*100:.2f}%)")
print(f"Expected Return at β=1.27       : {result['er_at_beta_127']:.4f} ({result['er_at_beta_127']*100:.2f}%)")
print(f"Figure saved to                 : {result['figure_path']}")
print(f"--- Result Dictionary ---")
print(result)
