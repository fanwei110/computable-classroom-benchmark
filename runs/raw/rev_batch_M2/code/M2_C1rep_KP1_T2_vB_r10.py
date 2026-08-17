import numpy as np
import matplotlib.pyplot as plt

# 给定参数
r = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rho_list = [0.15, 0.45, 0.75]
target_return = 0.10

# 存储结果
result = {}

# 计算函数：给定权重w1, 返回组合收益和波动率
def portfolio(w1, r, sigma, rho):
    w2 = 1 - w1
    ret = w1 * r[0] + w2 * r[1]
    vol = np.sqrt(w1**2 * sigma[0]**2 + w2**2 * sigma[1]**2 + 2*w1*w2*sigma[0]*sigma[1]*rho)
    return ret, vol

# 生成绘图
plt.figure(figsize=(10, 6))
colors = ['blue', 'green', 'red']

for i, rho in enumerate(rho_list):
    # 生成有效前沿（不允许卖空 w1 在 0 到 1 之间）
    ws = np.linspace(0, 1, 500)
    rets, vols = portfolio(ws, r, sigma, rho)
    
    # 只取有效前沿部分（收益大于MVP的收益部分）
    # 先计算MVP
    var1 = sigma[0]**2
    var2 = sigma[1]**2
    cov = sigma[0]*sigma[1]*rho
    w1_mvp = (var2 - cov) / (var1 + var2 - 2*cov)
    w1_mvp = np.clip(w1_mvp, 0, 1)  # 不允许卖空限制
    mvp_ret, mvp_vol = portfolio(w1_mvp, r, sigma, rho)
    
    # 存储当 rho=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol
    
    # 计算目标收益10%下的最小波动率
    if target_return <= r[1] and target_return >= r[0]:
        # 解方程求权重: w1*r0 + (1-w1)*r1 = target
        w1_target = (target_return - r[1]) / (r[0] - r[1])
        w1_target = np.clip(w1_target, 0, 1)
        target_ret, target_vol = portfolio(w1_target, r, sigma, rho)
        if rho == 0.45:
            result['frontier_vol_at_target'] = target_vol
    else:
        if rho == 0.45:
            result['frontier_vol_at_target'] = None
    
    # 绘制有效前沿（只画收益 >= mvp_ret 的部分）
    mask = rets >= mvp_ret
    plt.plot(vols[mask], rets[mask], color=colors[i], label=f'ρ = {rho}')
    
    # 标记最小方差点
    plt.scatter(mvp_vol, mvp_ret, color=colors[i], marker='o', s=80, zorder=5)
    plt.annotate(f'MVP ρ={rho}\n(σ={mvp_vol:.3f}, r={mvp_ret:.3f})', 
                 (mvp_vol, mvp_ret), textcoords="offset points", xytext=(5, -15), fontsize=8)
    
    # 如果存在10%目标收益点，标记
    if target_return <= r[1] and target_return >= r[0]:
        plt.scatter(target_vol, target_ret, color=colors[i], marker='s', s=60, zorder=5)
        if rho == 0.45:
            plt.annotate(f'Target 10%\nσ={target_vol:.4f}', 
                         (target_vol, target_ret), textcoords="offset points", xytext=(10, 0), fontsize=8)

# 标记单个资产点
plt.scatter(sigma[0], r[0], color='black', marker='*', s=150, zorder=6, label='Asset 1')
plt.annotate('Asset 1', (sigma[0], r[0]), textcoords="offset points", xytext=(5, 5))
plt.scatter(sigma[1], r[1], color='black', marker='*', s=150, zorder=6, label='Asset 2')
plt.annotate('Asset 2', (sigma[1], r[1]), textcoords="offset points", xytext=(5, 5))

plt.xlabel('Volatility (σ)')
plt.ylabel('Return (r)')
plt.title('Two-Asset Efficient Frontier with Different Correlations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=150)
plt.close()

result['figure_path'] = fig_path

print(result)