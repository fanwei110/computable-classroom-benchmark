import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
mu1 = 0.071         # 资产1 期望年收益
mu2 = 0.124         # 资产2 期望年收益
sigma1 = 0.163      # 资产1 年化波动率
sigma2 = 0.289      # 资产2 年化波动率

rhos = [0.15, 0.45, 0.75]               # 三种相关系数
target_return = 0.10                    # 目标期望收益 10%

# ==================== 辅助函数 ====================
def portfolio_stats(w1, mu1, mu2, sigma1, sigma2, rho):
    """返回组合期望收益和标准差"""
    w2 = 1.0 - w1
    mu_p = w1 * mu1 + w2 * mu2
    var_p = w1**2 * sigma1**2 + w2**2 * sigma2**2 + 2 * w1 * w2 * rho * sigma1 * sigma2
    sigma_p = np.sqrt(var_p)
    return mu_p, sigma_p

def min_variance_weight(sigma1, sigma2, rho):
    """最小方差组合中资产1的权重"""
    cov12 = rho * sigma1 * sigma2
    numerator = sigma2**2 - cov12
    denominator = sigma1**2 + sigma2**2 - 2 * cov12
    return numerator / denominator

# ==================== 计算要求的结果 ====================
# 1) 相关系数 0.45 时，最小方差组合的年化波动率
w1_mvp_045 = min_variance_weight(sigma1, sigma2, 0.45)
_, sigma_mvp_045 = portfolio_stats(w1_mvp_045, mu1, mu2, sigma1, sigma2, 0.45)

# 2) 相关系数 0.45 时，目标期望收益 10% 下的最小年化波动率
# 由线性方程解出资产1权重
w1_target = (target_return - mu2) / (mu1 - mu2)
_, sigma_target = portfolio_stats(w1_target, mu1, mu2, sigma1, sigma2, 0.45)

# ==================== 画图 ====================
# 生成一系列资产1权重，涵盖足够范围以展示曲线形态
w1_vals = np.linspace(-3, 4, 1400)  # 从-300%到400%，足够覆盖

plt.figure(figsize=(8, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 三条曲线的颜色

for rho, color in zip(rhos, colors):
    mu_vals, sigma_vals = portfolio_stats(w1_vals, mu1, mu2, sigma1, sigma2, rho)

    # 绘制前沿曲线（百分比显示，乘以100）
    plt.plot(sigma_vals * 100, mu_vals * 100,
             color=color, linewidth=1.5, label=f'ρ = {rho:.2f}')

    # 计算并标记最小方差组合
    w1_mvp = min_variance_weight(sigma1, sigma2, rho)
    mu_mvp, sigma_mvp = portfolio_stats(w1_mvp, mu1, mu2, sigma1, sigma2, rho)
    plt.scatter(sigma_mvp * 100, mu_mvp * 100,
                color=color, marker='o', s=60, edgecolors='k', linewidth=0.8,
                zorder=5, label=f'MVP (ρ={rho:.2f})' if rho == rhos[0] else "")

# 图表装饰
plt.xlabel('Annualized Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Mean-Variance Frontier for Two Risky Assets')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

# 保存图片
figure_path = 'mean_variance_frontiers.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ==================== 输出字典 ====================
result = {
    'mvp_vol_at_rho45': sigma_mvp_045,
    'frontier_vol_at_target': sigma_target,
    'figure_path': figure_path
}

print("结果字典：", result)
