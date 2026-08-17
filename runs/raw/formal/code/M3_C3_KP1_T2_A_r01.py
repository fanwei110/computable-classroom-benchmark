import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu1, mu2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289

# 定义计算组合收益与波动率的函数
def portfolio_stats(w, rho):
    ret = w * mu1 + (1 - w) * mu2
    var = w**2 * sig1**2 + (1 - w)**2 * sig2**2 + 2 * w * (1 - w) * rho * sig1 * sig2
    vol = np.sqrt(var)
    return ret, vol

# 定义计算最小方差组合权重的函数
def mvp_weight(rho):
    numerator = sig2**2 - rho * sig1 * sig2
    denominator = sig1**2 + sig2**2 - 2 * rho * sig1 * sig2
    return numerator / denominator

# --- 计算 rho=0.45 时的特定指标 ---
rho_45 = 0.45

# 1. rho=0.45 时的最小方差组合
w_mvp_45 = mvp_weight(rho_45)
ret_mvp_45, vol_mvp_45 = portfolio_stats(w_mvp_45, rho_45)

# 2. 目标收益 10% 时的最小波动率
target_ret = 0.10
w_target = (target_ret - mu2) / (mu1 - mu2)
ret_target_45, vol_target_45 = portfolio_stats(w_target, rho_45)

# --- 绘图 ---
plt.figure(figsize=(10, 6), dpi=150)
weights = np.linspace(-0.5, 1.5, 500) # 扩展权重范围以画出完整双曲线

rhos = [0.15, 0.45, 0.75]
colors = ['blue', 'green', 'red']

for rho, color in zip(rhos, colors):
    rets, vols = [], []
    for w in weights:
        r, v = portfolio_stats(w, rho)
        rets.append(r)
        vols.append(v)
    
    # 画前沿线
    plt.plot(vols, rets, label=f'ρ = {rho}', color=color)
    
    # 计算并标出最小方差组合(MVP)
    w_mvp = mvp_weight(rho)
    r_mvp, v_mvp = portfolio_stats(w_mvp, rho)
    plt.scatter(v_mvp, r_mvp, color=color, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\nσ={v_mvp:.2%}, R={r_mvp:.2%}', 
                 xy=(v_mvp, r_mvp), xytext=(10, 10),
                 textcoords='offset points', ha='left', fontsize=9,
                 arrowprops=dict(arrowstyle='->', ls='--', color=color))

plt.xlabel('Volatility (Annualized)')
plt.ylabel('Expected Return (Annualized)')
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.close()

# --- 输出结果 ---
result = {
    'mvp_vol_at_rho45': vol_mvp_45,
    'frontier_vol_at_target': vol_target_45,
    'figure_path': figure_path
}

print(result)
