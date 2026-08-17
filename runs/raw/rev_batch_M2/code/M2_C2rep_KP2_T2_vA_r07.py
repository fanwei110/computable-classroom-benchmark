import matplotlib
matplotlib.use('Agg')          # 非交互式后端，确保在服务器或无显示器环境正常保存图片
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 可调参数 (Adjustable parameters)
# ============================================================
RISK_FREE_RATE = 0.023          # 无风险利率
MARKET_RETURN  = 0.094          # 市场期望收益

# ============================================================
# 计算证券市场线 (SML) 的斜率 & CAPM 函数
# ============================================================
sml_slope = MARKET_RETURN - RISK_FREE_RATE          # 市场风险溢价

def capm_er(beta, rf=RISK_FREE_RATE, rm=MARKET_RETURN):
    """返回给定 beta 的 CAPM 期望收益"""
    return rf + beta * (rm - rf)

# ============================================================
# 数据准备
# ============================================================
# 生成 beta 从 0 到 2 的点，用于画 SML 直线
beta_vals = np.linspace(0, 2, 100)
sml_vals  = capm_er(beta_vals)

# 三只股票的数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099},
}

# ============================================================
# 绘制 SML 并标注股票
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

# SML 直线
ax.plot(beta_vals, sml_vals, color='black', linewidth=2, label='SML')

# 标出股票点
for name, s in stocks.items():
    ax.scatter(s['beta'], s['return'], color='red', s=60, zorder=5)
    ax.annotate(name,
                xy=(s['beta'], s['return']),
                xytext=(0, 12),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold',
                color='darkred')

# 坐标轴与标题
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)

# 保存图形
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================================================
# 报告要求的指标
# ============================================================
er_at_beta_127 = capm_er(1.27)   # beta=1.27 处的 CAPM 期望收益

result = {
    'sml_slope': sml_slope,               # 斜率 = 0.071
    'er_at_beta_127': er_at_beta_127,     # 0.11317
    'figure_path': figure_path            # 'sml_plot.png'
}

# 如需在控制台查看结果，可取消下面一行的注释
# print(result)
