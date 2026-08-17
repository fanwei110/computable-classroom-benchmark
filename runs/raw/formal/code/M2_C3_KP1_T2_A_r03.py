import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数（小数）
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rho_list = [0.15, 0.45, 0.75]

# 生成权重序列（涵盖卖空情况，展示完整可行集曲线）
w1_range = np.linspace(-2, 3, 1000)

# 初始化结果字典
result = {}

# 准备绘图
plt.figure(figsize=(10, 6))

for rho in rho_list:
    # 计算组合方差与收益
    cov = rho * sigma[0] * sigma[1]
    var_p = (w1_range**2 * sigma[0]**2 +
             (1 - w1_range)**2 * sigma[1]**2 +
             2 * w1_range * (1 - w1_range) * cov)
    std_p = np.sqrt(var_p)
    ret_p = w1_range * mu[0] + (1 - w1_range) * mu[1]

    # 最小方差组合（MVP）解析解
    w1_mvp = (sigma[1]**2 - rho * sigma[0] * sigma[1]) / (
        sigma[0]**2 + sigma[1]**2 - 2 * rho * sigma[0] * sigma[1])
    w2_mvp = 1 - w1_mvp
    ret_mvp = w1_mvp * mu[0] + w2_mvp * mu[1]
    std_mvp = np.sqrt(w1_mvp**2 * sigma[0]**2 +
                      w2_mvp**2 * sigma[1]**2 +
                      2 * w1_mvp * w2_mvp * rho * sigma[0] * sigma[1])

    # 绘制整条可行集（权重全范围）
    plt.plot(std_p, ret_p, label=f'ρ = {rho}')
    # 标出MVP点
    plt.scatter(std_mvp, ret_mvp, marker='o', s=60,
                edgecolors='k', linewidth=0.8, zorder=5)

    # 存储 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = std_mvp

# 计算 ρ=0.45，目标收益 10% 的最小波动率
rho45 = 0.45
target_ret = 0.10
# 由收益反推权重 (mu1 != mu2)
w1_target = (target_ret - mu[1]) / (mu[0] - mu[1])
w2_target = 1 - w1_target
cov_target = rho45 * sigma[0] * sigma[1]
var_target = (w1_target**2 * sigma[0]**2 +
              w2_target**2 * sigma[1]**2 +
              2 * w1_target * w2_target * cov_target)
std_target = np.sqrt(var_target)
result['frontier_vol_at_target'] = std_target

# 图上标出目标收益组合点（可选）
plt.scatter(std_target, target_ret, marker='*', s=120,
            color='red', edgecolors='k', linewidth=0.8,
            label=f'Target 10% (ρ=0.45)', zorder=6)

plt.xlabel('Annualized Volatility')
plt.ylabel('Annualized Expected Return')
plt.title('Efficient Frontier for Two Assets')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# 保存图片
fig_path = os.path.join(os.getcwd(), 'efficient_frontier.png')
plt.savefig(fig_path, dpi=150)
plt.close()
result['figure_path'] = fig_path

print(result)
