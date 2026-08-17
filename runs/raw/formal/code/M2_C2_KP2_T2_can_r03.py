import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 可调参数（教师可在课堂上实时修改这两行并重新运行）
Rf = 0.023          # 无风险利率
Rm = 0.094          # 市场期望收益
# ============================================================

# 股票数据：名称，beta，实际收益
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ---------- 计算 SML ----------
slope = Rm - Rf                          # 市场风险溢价，即 SML 斜率
beta_range = np.linspace(0, 2, 200)      # beta 0 ~ 2
er_sml = Rf + beta_range * slope         # 证券市场线上的期望收益

# beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_target = Rf + beta_target * slope

# ---------- 绘图 ----------
plt.figure(figsize=(10, 6))

# 绘制证券市场线
plt.plot(beta_range, er_sml * 100, 'k-', linewidth=2, label='Security Market Line (SML)')

# 标出无风险资产 (β=0) 和市场组合 (β=1)
plt.scatter(0, Rf * 100, c='blue', s=80, zorder=5, label='Risk‑free asset')
plt.annotate(f'Rf = {Rf*100:.1f}%', (0, Rf * 100),
             textcoords="offset points", xytext=(-10, -15), fontsize=9)
plt.scatter(1, Rm * 100, c='green', s=80, zorder=5, label='Market portfolio')
plt.annotate(f'Market\n(β=1, {Rm*100:.1f}%)', (1, Rm * 100),
             textcoords="offset points", xytext=(10, -5), fontsize=9)

# 标出三只股票
for name, (beta, ret) in stocks.items():
    plt.scatter(beta, ret * 100, c='red', marker='X', s=100, zorder=6)
    plt.annotate(f'{name}  (β={beta:.2f}, {ret*100:.1f}%)',
                 (beta, ret * 100),
                 textcoords="offset points", xytext=(8, 8),
                 fontsize=9, color='darkred')

# 修饰图形
plt.xlabel('Beta', fontsize=12)
plt.ylabel('Expected Return (%)', fontsize=12)
plt.title('Capital Asset Pricing Model – Security Market Line', fontsize=14)
plt.xlim(0, 2)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# 保存图形
figure_filename = 'sml_capm.png'
plt.savefig(figure_filename, dpi=150)
plt.close()
figure_path = os.path.abspath(figure_filename)

# ---------- 输出结果 ----------
result = {
    'sml_slope': slope,                # 市场风险溢价
    'er_at_beta_127': er_target,       # β=1.27 的期望收益
    'figure_path': figure_path         # 图形绝对路径
}

# 直接在屏幕上打印，方便教师查看
if __name__ == '__main__':
    print("=== CAPM & SML 计算结果 ===")
    print(f"SML 斜率（市场风险溢价）：{result['sml_slope']:.4f}  ({result['sml_slope']*100:.2f}%)")
    print(f"β = 1.27 处的 CAPM 期望收益：{result['er_at_beta_127']:.4f}  ({result['er_at_beta_127']*100:.2f}%)")
    print(f"图形已保存至：{result['figure_path']}")
    print("\nresult 字典内容：", result)
