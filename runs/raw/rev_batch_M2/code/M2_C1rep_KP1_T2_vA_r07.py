import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rho_list = [0.15, 0.45, 0.75]

# 生成组合权重（允许卖空，覆盖整条双曲线）
w1 = np.linspace(-0.5, 1.5, 500)
w2 = 1 - w1

results = {}
fig, ax = plt.subplots(figsize=(10, 6))

for rho in rho_list:
    cov = rho * sigma[0] * sigma[1]
    cov_matrix = np.array([[sigma[0]**2, cov],
                           [cov, sigma[1]**2]])

    # 组合方差与收益
    port_var = w1**2 * sigma[0]**2 + w2**2 * sigma[1]**2 + 2*w1*w2*cov
    port_std = np.sqrt(port_var)
    port_ret = w1 * r[0] + w2 * r[1]

    # 最小方差组合 (MVP)
    # 解析解
    w1_mvp = (sigma[1]**2 - cov) / (sigma[0]**2 + sigma[1]**2 - 2*cov)
    w2_mvp = 1 - w1_mvp
    mvp_ret = w1_mvp * r[0] + w2_mvp * r[1]
    mvp_std = np.sqrt(w1_mvp**2 * sigma[0]**2 + w2_mvp**2 * sigma[1]**2 + 2*w1_mvp*w2_mvp*cov)

    # 画前沿
    ax.plot(port_std, port_ret, label=f'ρ = {rho}')
    # 标出 MVP
    ax.scatter(mvp_std, mvp_ret, marker='*', s=150, zorder=5)

    # 保存 ρ=0.45 的结果
    if rho == 0.45:
        # MVP 波动率
        mvp_vol_45 = mvp_std
        # 目标收益 10% 时最小波动率
        # 解权重：w1*r1 + (1-w1)*r2 = 0.10
        w1_target = (0.10 - r[1]) / (r[0] - r[1])
        w2_target = 1 - w1_target
        target_var = w1_target**2 * sigma[0]**2 + w2_target**2 * sigma[1]**2 + 2*w1_target*w2_target*cov
        target_std = np.sqrt(target_var)
        results['mvp_vol_at_rho45'] = round(mvp_vol_45, 4)
        results['frontier_vol_at_target'] = round(target_std, 4)

ax.set_xlabel('年化波动率')
ax.set_ylabel('年化期望收益')
ax.set_title('两种资产的有效前沿')
ax.legend()
ax.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

results['figure_path'] = figure_path
print(results)
