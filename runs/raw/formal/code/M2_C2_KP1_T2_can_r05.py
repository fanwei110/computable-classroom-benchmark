import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. 参数设定
# ------------------------------
r1 = 0.071          # 资产1的年期望收益
r2 = 0.124          # 资产2的年期望收益
sigma1 = 0.163      # 资产1的年化波动率
sigma2 = 0.289      # 资产2的年化波动率
rhos = [0.15, 0.45, 0.75]               # 需要考察的相关系数
target_return = 0.10                    # 目标期望收益
w1_scan = np.linspace(-3.0, 4.0, 800)   # 足够覆盖卖空范围的权重扫描

# ------------------------------
# 2. 辅助函数：给定权重 w1 计算组合收益与波动率
# ------------------------------
def portfolio_metrics(w1, r1, r2, s1, s2, rho):
    """返回 (组合期望收益, 组合波动率)"""
    w2 = 1.0 - w1
    ret = w1 * r1 + w2 * r2
    var = (w1**2 * s1**2 +
           w2**2 * s2**2 +
           2 * w1 * w2 * rho * s1 * s2)
    return ret, np.sqrt(var)

# ------------------------------
# 3. 绘图：均值-方差前沿 & 最小方差组合标记
# ------------------------------
plt.figure(figsize=(10, 6))

for rho in rhos:
    # 扫描曲线
    rets, vols = portfolio_metrics(w1_scan, r1, r2, sigma1, sigma2, rho)
    plt.plot(vols, rets, label=f'ρ = {rho}')

    # 计算最小方差组合 (MVP) 的权重（解析解）
    cov12 = rho * sigma1 * sigma2
    w1_mvp = (sigma2**2 - cov12) / (sigma1**2 + sigma2**2 - 2 * cov12)
    ret_mvp, vol_mvp = portfolio_metrics(w1_mvp, r1, r2, sigma1, sigma2, rho)

    # 在曲线上标出 MVP 点（使用与曲线相同的颜色）
    color = plt.gca().lines[-1].get_color()
    plt.scatter(vol_mvp, ret_mvp, color=color, zorder=5)
    plt.annotate('MVP', (vol_mvp, ret_mvp),
                 textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8, color=color)

plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Mean-Variance Frontier: Two Risky Assets')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ------------------------------
# 4. 针对 ρ = 0.45 的特殊计算
# ------------------------------
rho_fixed = 0.45

# 4.1 最小方差组合的波动率
cov12_fixed = rho_fixed * sigma1 * sigma2
w1_mvp_fixed = (sigma2**2 - cov12_fixed) / (sigma1**2 + sigma2**2 - 2 * cov12_fixed)
_, mvp_vol = portfolio_metrics(w1_mvp_fixed, r1, r2, sigma1, sigma2, rho_fixed)

# 4.2 目标收益 10% 下的最小波动率
# 两资产满仓下目标收益唯一确定权重
w1_target = (target_return - r2) / (r1 - r2)
_, target_vol = portfolio_metrics(w1_target, r1, r2, sigma1, sigma2, rho_fixed)

# ------------------------------
# 5. 整理最终输出
# ------------------------------
result = {
    'mvp_vol_at_rho45': mvp_vol,
    'frontier_vol_at_target': target_vol,
    'figure_path': figure_path
}

# 控制台打印，方便课堂查看
print(result)
