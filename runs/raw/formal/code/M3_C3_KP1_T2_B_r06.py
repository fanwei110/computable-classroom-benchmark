import numpy as np
import matplotlib.pyplot as plt

# --- 1. 参数设定 ---
mu1, mu2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_ret = 0.10

# --- 2. 核心计算函数 ---
def calc_portfolio(w1, mu1, mu2, sig1, sig2, rho):
    """计算给定权重下的收益与波动率"""
    w2 = 1 - w1
    ret = w1 * mu1 + w2 * mu2
    vol = np.sqrt((w1 * sig1)**2 + (w2 * sig2)**2 + 2 * w1 * w2 * rho * sig1 * sig2)
    return ret, vol

def calc_mvp(mu1, mu2, sig1, sig2, rho):
    """计算最小方差组合(MVP)的权重、收益与波动率"""
    w1_mvp = (sig2**2 - rho * sig1 * sig2) / (sig1**2 + sig2**2 - 2 * rho * sig1 * sig2)
    ret_mvp, vol_mvp = calc_portfolio(w1_mvp, mu1, mu2, sig1, sig2, rho)
    return w1_mvp, ret_mvp, vol_mvp

def calc_vol_at_target(target, mu1, mu2, sig1, sig2, rho):
    """计算目标收益率下的最小波动率（两资产情况下权重唯一）"""
    w1_target = (target - mu2) / (mu1 - mu2)
    _, vol_target = calc_portfolio(w1_target, mu1, mu2, sig1, sig2, rho)
    return vol_target

# --- 3. 计算所需结果 ---
# 相关系数 0.45 的 MVP 波动率
_, _, mvp_vol_45 = calc_mvp(mu1, mu2, sig1, sig2, 0.45)

# 相关系数 0.45 时，目标收益 10% 的最小波动率
frontier_vol_target = calc_vol_at_target(target_ret, mu1, mu2, sig1, sig2, 0.45)

# --- 4. 绘图 ---
plt.figure(figsize=(10, 7), dpi=150)
w1_array = np.linspace(-0.3, 1.3, 500) # 扩展权重以展现完整双曲线

for rho in rhos:
    rets, vols = calc_portfolio(w1_array, mu1, mu2, sig1, sig2, rho)
    plt.plot(vols, rets, label=f'ρ = {rho}', linewidth=2)
    
    # 标出最小方差点 MVP
    _, ret_mvp, vol_mvp = calc_mvp(mu1, mu2, sig1, sig2, rho)
    plt.scatter(vol_mvp, ret_mvp, marker='*', s=250, zorder=5, edgecolors='black', linewidths=0.8)
    plt.annotate(f'MVP (ρ={rho})\nVol={vol_mvp:.2%}', 
                 xy=(vol_mvp, ret_mvp), 
                 xytext=(vol_mvp + 0.015, ret_mvp - 0.005),
                 fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='gray', lw=1.2))

# 标出目标收益10%的点 (针对rho=0.45)
plt.scatter(frontier_vol_target, target_ret, marker='D', color='red', s=100, zorder=5, edgecolors='black')
plt.annotate(f'Target 10% (ρ=0.45)\nVol={frontier_vol_target:.2%}', 
             xy=(frontier_vol_target, target_ret), 
             xytext=(frontier_vol_target + 0.02, target_ret + 0.005),
             fontsize=9,
             arrowprops=dict(arrowstyle='->', color='red', lw=1.2))

# 图表装饰
plt.title('Two-Asset Efficient Frontier (Different Correlations)', fontsize=14)
plt.xlabel('Volatility (Standard Deviation)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.xlim(0.10, 0.45)
plt.ylim(0.04, 0.16)
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图表
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.close()

# --- 5. 封装输出结果 ---
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': frontier_vol_target,
    'figure_path': figure_path
}

# 打印结果以供检查
print(result)
