import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])

# 相关系数列表
rhos = [0.15, 0.45, 0.75]

# 目标期望收益
target_return = 0.10

# 存储结果的字典
result = {}

# 计算辅助函数
def portfolio_stats(w1, mu, sigma, rho):
    """根据权重 w1 (w2 = 1 - w1) 计算组合期望收益和标准差"""
    w2 = 1 - w1
    ret = w1 * mu[0] + w2 * mu[1]
    var = (w1**2 * sigma[0]**2 +
           w2**2 * sigma[1]**2 +
           2 * w1 * w2 * rho * sigma[0] * sigma[1])
    return ret, np.sqrt(np.maximum(var, 0))  # 防止微小的负值

# 解析计算最小方差组合
def min_var_portfolio(mu, sigma, rho):
    """返回最小方差组合的收益率和波动率"""
    s1, s2 = sigma[0], sigma[1]
    r = rho
    # 最优权重 (允许卖空, 满仓)
    w1_opt = (s2**2 - r * s1 * s2) / (s1**2 + s2**2 - 2 * r * s1 * s2)
    ret, vol = portfolio_stats(w1_opt, mu, sigma, r)
    return ret, vol, w1_opt

# 解析计算给定收益下的波动率
def vol_at_return(target, mu, sigma, rho):
    """给定目标期望收益，返回满仓组合的波动率(唯一解)。"""
    # 解线性方程
    # w1*mu1 + (1-w1)*mu2 = target => w1*(mu1 - mu2) = target - mu2
    w1 = (target - mu[1]) / (mu[0] - mu[1])
    w2 = 1 - w1
    var = (w1**2 * sigma[0]**2 +
           w2**2 * sigma[1]**2 +
           2 * w1 * w2 * rho * sigma[0] * sigma[1])
    return np.sqrt(np.maximum(var, 0))

# 计算 rho=0.45 下的要求数据
rho_specific = 0.45
mvp_ret_45, mvp_vol_45, _ = min_var_portfolio(mu, sigma, rho_specific)
target_vol_45 = vol_at_return(target_return, mu, sigma, rho_specific)

result['mvp_vol_at_rho45'] = mvp_vol_45
result['frontier_vol_at_target'] = target_vol_45

# 画图
plt.figure(figsize=(8, 6))

# 扫描权重的范围，确保前沿完整（卖空前沿向两端延伸）
w1_range = np.linspace(-2, 3, 1000)

for rho in rhos:
    rets, vols = portfolio_stats(w1_range, mu, sigma, rho)
    plt.plot(vols, rets, label=f'ρ = {rho}')

    # 最小方差组合点
    mvp_ret, mvp_vol, _ = min_var_portfolio(mu, sigma, rho)
    plt.scatter(mvp_vol, mvp_ret, marker='o', s=80,
                edgecolors='k', linewidth=0.8, zorder=5)
    # 标注 MVP
    plt.annotate(f'MVP ρ={rho}',
                 (mvp_vol, mvp_ret),
                 textcoords="offset points",
                 xytext=(10, -10),
                 ha='left', fontsize=8,
                 arrowprops=dict(arrowstyle='->', lw=0.8))

# 额外标注 rho=0.45 时目标收益点（可选）
target_vol = target_vol_45
plt.scatter(target_vol, target_return, marker='s', color='red', s=80,
            edgecolors='k', linewidth=0.8, zorder=6)
plt.annotate(f'10% return\nσ={target_vol:.4f}',
             (target_vol, target_return),
             textcoords="offset points",
             xytext=(-10, -20),
             ha='right', fontsize=8,
             arrowprops=dict(arrowstyle='->', lw=0.8),
             color='red')

plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return (μ)')
plt.title('Mean-Variance Frontier for Two Risky Assets')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
fig_path = 'frontier.png'
plt.savefig(fig_path, dpi=150)
plt.close()
result['figure_path'] = fig_path

# 输出结果（供教师查看）
print("结果字典:")
for k, v in result.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.6f}")
    else:
        print(f"  {k}: {v}")
