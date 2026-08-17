import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r1, r2 = 0.071, 0.124
s1, s2 = 0.163, 0.289

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 权重范围（允许卖空，以便画出完整的前沿曲线）
weights = np.linspace(-0.5, 1.5, 500)

def portfolio_metrics(w, rho):
    """计算组合的期望收益和波动率"""
    ret = w * r1 + (1 - w) * r2
    var = (w * s1)**2 + ((1 - w) * s2)**2 + 2 * w * (1 - w) * rho * s1 * s2
    vol = np.sqrt(var)
    return ret, vol

def mvp_weight(rho):
    """计算最小方差组合的权重"""
    w_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    return w_mvp

# 计算 rho=0.45 时的最小方差组合波动率
rho_45 = 0.45
w_mvp_45 = mvp_weight(rho_45)
_, vol_mvp_45 = portfolio_metrics(w_mvp_45, rho_45)

# 计算目标收益10%时的最小波动率（rho=0.45）
target_ret = 0.10
# 对于两资产，达到目标收益的权重是唯一的（无风险资产时才有切点）
w_target = (r2 - target_ret) / (r2 - r1)
_, vol_target_45 = portfolio_metrics(w_target, rho_45)

# 绘图
plt.figure(figsize=(10, 7))
colors = ['blue', 'green', 'red']

for rho, color in zip(rhos, colors):
    rets, vols = portfolio_metrics(weights, rho)
    plt.plot(vols * 100, rets * 100, label=f'ρ = {rho}', color=color)
    
    # 计算并标出最小方差组合 (MVP)
    w_mvp = mvp_weight(rho)
    ret_mvp, vol_mvp = portfolio_metrics(w_mvp, rho)
    plt.scatter(vol_mvp * 100, ret_mvp * 100, marker='*', s=200, color=color, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\nVol={vol_mvp*100:.2f}%', 
                 xy=(vol_mvp * 100, ret_mvp * 100),
                 xytext=(vol_mvp * 100 + 2, ret_mvp * 100 - 0.8),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                 fontsize=9)

# 标出目标收益10%的点 (rho=0.45)
ret_target_10, vol_target_10 = portfolio_metrics(w_target, rho_45)
plt.scatter(vol_target_10 * 100, ret_target_10 * 100, marker='D', color='purple', s=100, zorder=5, label='Target 10% (ρ=0.45)')
plt.annotate(f'Target 10% (ρ=0.45)\nVol={vol_target_10*100:.2f}%', 
             xy=(vol_target_10 * 100, ret_target_10 * 100),
             xytext=(vol_target_10 * 100 + 2, ret_target_10 * 100 + 0.8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
             fontsize=9)

plt.title('Efficient Frontier for Two Assets under Different Correlations')
plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path)
plt.close()

# 存入结果字典
result = {
    'mvp_vol_at_rho45': vol_mvp_45,
    'frontier_vol_at_target': vol_target_45,
    'figure_path': fig_path
}

print(f"ρ=0.45时最小方差组合的波动率: {result['mvp_vol_at_rho45']:.4f} ({result['mvp_vol_at_rho45']*100:.2f}%)")
print(f"目标收益10%时最小波动率: {result['frontier_vol_at_target']:.4f} ({result['frontier_vol_at_target']*100:.2f}%)")
print(f"图片已保存至: {result['figure_path']}")
