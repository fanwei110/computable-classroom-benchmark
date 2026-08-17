import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 存储结果
result = {}

# 计算 MVP 和有效前沿的函数
def portfolio_stats(w1, mu, sigma, rho):
    w2 = 1 - w1
    ret = w1 * mu[0] + w2 * mu[1]
    var = (w1 * sigma[0])**2 + (w2 * sigma[1])**2 + 2 * w1 * w2 * rho * sigma[0] * sigma[1]
    return ret, np.sqrt(var)

# 准备画图
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['b', 'g', 'r']
for i, rho in enumerate(rhos):
    # 生成所有权重组合的收益和风险
    w1_range = np.linspace(0, 1, 500)
    rets = []
    vols = []
    for w1 in w1_range:
        ret, vol = portfolio_stats(w1, mu, sigma, rho)
        rets.append(ret)
        vols.append(vol)
    rets = np.array(rets)
    vols = np.array(vols)

    # 计算最小方差组合
    cov12 = rho * sigma[0] * sigma[1]
    var1 = sigma[0]**2
    var2 = sigma[1]**2
    w1_mvp = (var2 - cov12) / (var1 + var2 - 2 * cov12)
    w1_mvp = np.clip(w1_mvp, 0, 1)   # MVP 权重可能超出[0,1]？在此题不会
    ret_mvp, vol_mvp = portfolio_stats(w1_mvp, mu, sigma, rho)

    # 分离有效前沿（收益高于MVP的部分）
    idx_mvp = np.argmin(vols)
    frontier_ret = rets[idx_mvp:]
    frontier_vol = vols[idx_mvp:]

    # 画有效前沿
    ax.plot(frontier_vol, frontier_ret, color=colors[i], label=f'ρ = {rho}')
    # 标出 MVP
    ax.scatter(vol_mvp, ret_mvp, color=colors[i], marker='o', s=50, zorder=5)
    ax.annotate(f'MVP ρ={rho}', (vol_mvp, ret_mvp),
                textcoords="offset points", xytext=(10, -10), fontsize=8)

    # 对 ρ=0.45 保存要求的数据
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = round(vol_mvp, 4)   # 0.1617
        # 目标收益 10% 的组合
        w1_target = (mu[1] - target_return) / (mu[1] - mu[0])
        w1_target = np.clip(w1_target, 0, 1)
        ret_target, vol_target = portfolio_stats(w1_target, mu, sigma, rho)
        result['frontier_vol_at_target'] = round(vol_target, 4)  # 0.2024

ax.set_xlabel('年化波动率')
ax.set_ylabel('期望年收益')
ax.set_title('两种风险资产的有效前沿')
ax.legend()
ax.grid(True)

# 保存图片
figure_path = './efficient_frontier.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)
result['figure_path'] = figure_path

print(result)
