import numpy as np
import matplotlib.pyplot as plt

# 资产数据
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rho_list = [0.15, 0.45, 0.75]

# 目标收益 10%
target_return = 0.10

# 结果字典
result = {}

# 准备绘图
fig, ax = plt.subplots(figsize=(8, 5))

for rho in rho_list:
    cov = np.array([[sigma[0]**2, rho*sigma[0]*sigma[1]],
                    [rho*sigma[0]*sigma[1], sigma[1]**2]])
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(2)
    # 最小方差组合权重
    w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)
    mu_mvp = mu @ w_mvp
    vol_mvp = np.sqrt(w_mvp @ cov @ w_mvp)
    
    # 记录 rho=0.45 的 MVP 波动率
    if abs(rho - 0.45) < 1e-10:
        result['mvp_vol_at_rho45'] = float(vol_mvp)
    
    # 生成有效前沿曲线（组合权重遍历）
    ws = np.linspace(0, 1, 200)
    # 也可只画有效部分：收益高于MVP的部分，但这里画全部边界
    rets = ws*mu[0] + (1-ws)*mu[1]
    vols = np.sqrt(ws**2 * sigma[0]**2 + (1-ws)**2 * sigma[1]**2 +
                   2*ws*(1-ws)*rho*sigma[0]*sigma[1])
    # 分割有效前沿（只取收益 >= MVP收益）
    valid = rets >= mu_mvp
    ax.plot(vols[valid], rets[valid], label=f'ρ = {rho}')
    ax.scatter(vol_mvp, mu_mvp, color='red', zorder=5)

# 目标收益10% 在 rho=0.45 下的最小波动率
rho_target = 0.45
cov_target = np.array([[sigma[0]**2, rho_target*sigma[0]*sigma[1]],
                       [rho_target*sigma[0]*sigma[1], sigma[1]**2]])
# 利用线性约束直接计算权重
# 权重由期望收益唯一确定（两资产情况下）
w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
w_target = np.array([w1_target, 1 - w1_target])
vol_target = np.sqrt(w_target @ cov_target @ w_target)
result['frontier_vol_at_target'] = float(vol_target)

# 图中标注目标收益点
ax.scatter(vol_target, target_return, color='green', marker='*', s=100,
           label=f'Target 10% (ρ=0.45)')

ax.set_xlabel('Volatility (σ)')
ax.set_ylabel('Expected Return (μ)')
ax.set_title('Efficient Frontiers with different correlations')
ax.legend()
ax.grid(True)

# 保存图片
fig_path = 'frontier.png'
plt.savefig(fig_path, dpi=150)
result['figure_path'] = fig_path
plt.show()

print("result字典内容：")
print(result)
