import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu1, mu2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
# 相关系数列表
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 结果字典
result = {}

# 权重扫描
w = np.linspace(0, 1, 200)

plt.figure(figsize=(8, 6))

for rho in rhos:
    # 组合期望收益和标准差
    mu_p = w * mu1 + (1 - w) * mu2
    cov = rho * sigma1 * sigma2
    var_p = w**2 * sigma1**2 + (1 - w)**2 * sigma2**2 + 2 * w * (1 - w) * cov
    sigma_p = np.sqrt(var_p)

    # 最小方差组合权重
    w_mvp = (sigma2**2 - rho * sigma1 * sigma2) / (sigma1**2 + sigma2**2 - 2 * rho * sigma1 * sigma2)
    mu_mvp = w_mvp * mu1 + (1 - w_mvp) * mu2
    sigma_mvp = np.sqrt(w_mvp**2 * sigma1**2 + (1 - w_mvp)**2 * sigma2**2 + 2 * w_mvp * (1 - w_mvp) * cov)

    # 绘图
    plt.plot(sigma_p * 100, mu_p * 100, label=f'ρ = {rho}')
    plt.scatter(sigma_mvp * 100, mu_mvp * 100, marker='o', s=50)

    # 保存结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = sigma_mvp

        # 目标收益 10% 对应的最小波动率
        if target_return < mu_mvp:
            # 若目标收益低于 MVP，有效前沿最小波动率仍是 MVP
            target_vol = sigma_mvp
        else:
            w_target = (target_return - mu2) / (mu1 - mu2)
            target_vol = np.sqrt(w_target**2 * sigma1**2 + (1 - w_target)**2 * sigma2**2 +
                                 2 * w_target * (1 - w_target) * cov)
        result['frontier_vol_at_target'] = target_vol

# 图表修饰
plt.xlabel('波动率 (%)')
plt.ylabel('期望收益 (%)')
plt.title('两资产有效前沿（不同相关系数）')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图表
fig_path = 'effective_frontier.png'
plt.savefig(fig_path)
result['figure_path'] = fig_path

# 输出结果
print(result)
