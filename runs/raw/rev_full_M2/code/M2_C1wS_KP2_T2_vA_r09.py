import numpy as np
import matplotlib.pyplot as plt

# ==================== 可调参数区 ====================
RISK_FREE_RATE = 0.023      # 无风险利率，例如 2.3%
MARKET_RETURN  = 0.094      # 市场期望收益，例如 9.4%
# ===================================================

# -------------------- SML 参数计算 --------------------
slope = MARKET_RETURN - RISK_FREE_RATE   # 市场风险溢价，亦即 SML 斜率

# -------------------- 生成 SML 数据 --------------------
beta_vals = np.linspace(0, 2, 200)
sml_vals = RISK_FREE_RATE + slope * beta_vals

# -------------------- 三个股票点 --------------------
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# -------------------- 绘制 SML 图 --------------------
plt.figure(figsize=(9, 6))
plt.plot(beta_vals, sml_vals, 'b-', linewidth=2, label='SML')
plt.axhline(y=RISK_FREE_RATE, color='gray', linestyle='--', alpha=0.7,
            label=f'Risk‑free rate = {RISK_FREE_RATE:.1%}')
plt.axvline(x=1, color='gray', linestyle='--', alpha=0.4)

# 标注三个点
for name, (b, er) in stocks.items():
    plt.scatter(b, er, s=120, zorder=5, label=f'{name} (β={b}, E(r)={er:.1%})')
    plt.annotate(name, (b, er), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=10, fontweight='bold')

# 装饰
plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.title('Security Market Line (SML)', fontsize=14)
plt.legend(fontsize=9, loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
figure_path = 'sml.png'
plt.savefig(figure_path, dpi=200)
plt.close()   # 避免在交互式环境重复显示

# -------------------- 计算 beta=1.27 的期望收益 --------------------
beta_target = 1.27
er_at_beta_127 = RISK_FREE_RATE + slope * beta_target

# -------------------- 按要求构造输出字典 --------------------
result = {
    'sml_slope': slope,              # SML 斜率（市场风险溢价）
    'er_at_beta_127': er_at_beta_127, # beta=1.27 对应的期望收益
    'figure_path': figure_path       # 保存的图片路径
}

# 打印结果供课堂查看
print("SML 斜率 (市场风险溢价): {:.4f} ({:.2f}%)".format(result['sml_slope'], result['sml_slope']*100))
print("beta = 1.27 的期望收益: {:.4f} ({:.2f}%)".format(result['er_at_beta_127'], result['er_at_beta_127']*100))
print("图形已保存至:", result['figure_path'])
