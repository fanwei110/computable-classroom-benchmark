import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r = np.array([0.071, 0.124])
vol = np.array([0.163, 0.289])
rhos = [0.15, 0.45, 0.75]

# 目标
target_return = 0.10

def portfolio_stats(w, r, vol, rho):
    """返回给定权重的组合收益和波动率"""
    w = np.asarray(w)
    ret = np.dot(w, r)
    cov = np.array([[vol[0]**2, rho*vol[0]*vol[1]],
                    [rho*vol[0]*vol[1], vol[1]**2]])
    var = np.dot(w, np.dot(cov, w))
    return ret, np.sqrt(var)

# 生成前沿点
weights = np.linspace(0, 1, 100)
frontiers = {}
for rho in rhos:
    rets, vols = [], []
    for w1 in weights:
        w = np.array([w1, 1-w1])
        ret, vol_ = portfolio_stats(w, r, vol, rho)
        rets.append(ret)
        vols.append(vol_)
    frontiers[rho] = (rets, vols)

# 计算 MVP（最小方差组合）
def mvp(r, vol, rho):
    cov = np.array([[vol[0]**2, rho*vol[0]*vol[1]],
                    [rho*vol[0]*vol[1], vol[1]**2]])
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(2)
    w = inv_cov @ ones / (ones @ inv_cov @ ones)
    ret, vol_ = portfolio_stats(w, r, vol, rho)
    return w, ret, vol_

# 绘制前沿
plt.figure(figsize=(8,6))
colors = ['blue', 'orange', 'green']
for i, rho in enumerate(rhos):
    rets, vols = frontiers[rho]
    plt.plot(vols, rets, color=colors[i], label=f'ρ={rho}')
    # 标注 MVP
    w, mvp_ret, mvp_vol = mvp(r, vol, rho)
    plt.scatter(mvp_vol, mvp_ret, color=colors[i], marker='*', s=100, zorder=5)
    if rho == 0.45:
        mvp_vol_rho45 = mvp_vol

# 目标收益 10% 的点（rho=0.45）
w_target = np.array([(target_return - r[1])/(r[0]-r[1]), 
                     (target_return - r[0])/(r[1]-r[0])])
target_ret, target_vol = portfolio_stats(w_target, r, vol, 0.45)
frontier_vol_at_target = target_vol
plt.scatter(target_vol, target_ret, color='red', marker='o', s=80, label=f'Target {target_return:.0%}')

plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return')
plt.title('Two-Asset Efficient Frontier')
plt.legend()
plt.grid(True)

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=150)
plt.show()

# 结果字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_rho45, 6),       # 0.161681 左右
    'frontier_vol_at_target': round(frontier_vol_at_target, 6),  # 0.202387 左右
    'figure_path': fig_path
}

print(result)
