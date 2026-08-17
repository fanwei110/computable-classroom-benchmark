import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ==========================================
# 1. 参数化无风险利率与市场期望收益
# ==========================================
rf = 0.023   # 无风险利率 2.3%
rm = 0.094   # 市场期望收益 9.4%

# ==========================================
# 2. 计算 SML 斜率与 beta=1.27 处的期望收益
# ==========================================
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 定义股票数据
# ==========================================
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 4. 绘制证券市场线 (SML) 与股票点
# ==========================================
# 生成 beta 数组
betas = np.linspace(0, 2, 100)
# 计算 SML 对应的期望收益
er_sml = rf + betas * sml_slope

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制 SML
plt.plot(betas, er_sml, label='Security Market Line (SML)', color='blue', linewidth=2)

# 标出市场组合和无风险利率点作为参考
plt.scatter(1, rm, color='green', marker='*', s=200, zorder=5, label='Market Portfolio (M)')
plt.scatter(0, rf, color='orange', marker='D', s=100, zorder=5, label='Risk-Free Rate (Rf)')

# 绘制股票点并带标注
for name, data in stocks.items():
    beta_val = data['beta']
    ret_val = data['return']
    
    # 计算该 beta 下的 CAPM 期望收益，用于判断标注偏移方向
    er_sml_val = rf + beta_val * sml_slope
    
    plt.scatter(beta_val, ret_val, color='red', zorder=5)
    
    # Alpha 为正(收益高于SML)标注向上偏移，Alpha 为负标注向下偏移
    if ret_val >= er_sml_val:
        xytext = (beta_val + 0.05, ret_val + 0.008)
    else:
        xytext = (beta_val + 0.05, ret_val - 0.015)
        
    plt.annotate(f"Stock {name}\n(β={beta_val}, E={ret_val*100:.1f}%)",
                 xy=(beta_val, ret_val),
                 xytext=xytext,
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                 fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 设置图形属性
plt.title('CAPM: Security Market Line (SML) and Stock Valuation', fontsize=14)
plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.xlim(0, 2)
plt.ylim(0, 0.20)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=11, loc='upper left')

# Y 轴刻度显示为百分比
plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))

# ==========================================
# 5. 保存图形
# ==========================================
figure_path = 'sml_capm_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 6. 填充 result 字典
# ==========================================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 课堂演示时打印结果
print(result)
