import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r1, r2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 组合计算函数
def portfolio_stats(w, r1, r2, s1, s2, rho):
    rp = w * r1 + (1 - w) * r2
    var = w**2 * s1**2 + (1 - w)**2 * s2**2 + 2 * w * (1 - w) * rho * s1 * s2
    return rp, np.sqrt(var)

# MVP 权重与波动率
def mvp(rho, s1, s2):
    cov = rho * s1 * s2
    w = (s2**2 - cov) / (s1**2 + s2**2 - 2 * cov)
    return w

# 网格点
w_vals = np.linspace(0, 1, 500)

plt.figure(figsize=(10, 6))

for rho in rhos:
    rp, sigp = portfolio_stats(w_vals, r1, r2, sigma1, sigma2, rho)
    plt.plot(sigp * 100, rp * 100, label=f'ρ = {rho}')
    # 最小方差点
    w_mvp = mvp(rho, sigma1, sigma2)
    r_mvp, sig_mvp = portfolio_stats(w_mvp, r1, r2, sigma1, sigma2, rho)
    plt.scatter(sig_mvp * 100, r_mvp * 100, marker='o', s=60, zorder=5)
    plt.annotate(f'MVP\n({sig_mvp*100:.2f}%, {r_mvp*100:.2f}%)',
                 (sig_mvp*100, r_mvp*100), textcoords="offset points",
                 xytext=(10, -10), fontsize=8)

plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Efficient Frontier for Two Assets')
plt.legend()
plt.grid(True)
plt.tight_layout()
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# ---- 计算所需指标 ----
# rho = 0.45 时的 MVP 波动率
rho45 = 0.45
w_mvp45 = mvp(rho45, sigma1, sigma2)
_, mvp_vol_45 = portfolio_stats(w_mvp45, r1, r2, sigma1, sigma2, rho45)

# 目标收益 10% 的最小波动率（在有效前沿上）
target = 0.10
# 权重由目标收益确定
w_target = (target - r2) / (r1 - r2)
_, frontier_vol_target = portfolio_stats(w_target, r1, r2, sigma1, sigma2, rho45)

# 结果字典
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': frontier_vol_target,
    'figure_path': figure_path
}

print(result)
