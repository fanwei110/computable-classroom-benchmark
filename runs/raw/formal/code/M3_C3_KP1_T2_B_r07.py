import numpy as np
import matplotlib.pyplot as plt

# 基础参数
r1, r2 = 0.071, 0.124
v1, v2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

def portfolio_stats(w1, r1, r2, v1, v2, rho):
    w2 = 1 - w1
    ret = w1 * r1 + w2 * r2
    vol = np.sqrt(w1**2 * v1**2 + w2**2 * v2**2 + 2 * w1 * w2 * rho * v1 * v2)
    return ret, vol

def mvp_weight(v1, v2, rho):
    num = v2**2 - rho * v1 * v2
    den = v1**2 + v2**2 - 2 * rho * v1 * v2
    return num / den

# 目标收益 10% 对应的权重
target_ret = 0.10
w1_target = (target_ret - r2) / (r1 - r2)

mvp_vol_at_rho45 = None
frontier_vol_at_target = None

plt.figure(figsize=(10, 6))

for rho in rhos:
    # 权重范围扫描
    w1s = np.linspace(-0.5, 1.5, 500)
    rets, vols = portfolio_stats(w1s, r1, r2, v1, v2, rho)
    
    # 计算 MVP
    w1_mvp = mvp_weight(v1, v2, rho)
    ret_mvp, vol_mvp = portfolio_stats(w1_mvp, r1, r2, v1, v2, rho)
    
    # 绘制前沿：有效前沿实线，非有效部分虚线
    efficient_mask = rets >= ret_mvp
    inefficient_mask = rets < ret_mvp
    
    plt.plot(np.array(vols)[efficient_mask], np.array(rets)[efficient_mask], linestyle='-', label=f'ρ = {rho:.2f} (Efficient)')
    plt.plot(np.array(vols)[inefficient_mask], np.array(rets)[inefficient_mask], linestyle='--', alpha=0.5)
    
    # 标注 MVP
    plt.scatter(vol_mvp, ret_mvp, marker='D', zorder=5)
    plt.annotate(f'MVP (ρ={rho:.2f})\nVol: {vol_mvp:.2%}\nRet: {ret_mvp:.2%}', 
                 xy=(vol_mvp, ret_mvp), xytext=(10, 10), textcoords='offset points',
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # 提取 rho = 0.45 的特定数值
    if abs(rho - 0.45) < 1e-6:
        mvp_vol_at_rho45 = vol_mvp
        ret_target, vol_target = portfolio_stats(w1_target, r1, r2, v1, v2, rho)
        frontier_vol_at_target = vol_target
        
        # 标注目标收益10%的点
        plt.scatter(vol_target, ret_target, marker='*', color='red', zorder=5, s=100)
        plt.annotate(f'Target 10% (ρ=0.45)\nVol: {vol_target:.2%}', 
                     xy=(vol_target, ret_target), xytext=(-80, -30), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='red'),
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Two-Asset Efficient Frontier with Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# 按输出契约封装结果
result = {
    'mvp_vol_at_rho45': float(mvp_vol_at_rho45),
    'frontier_vol_at_target': float(frontier_vol_at_target),
    'figure_path': figure_path
}

print(result)
