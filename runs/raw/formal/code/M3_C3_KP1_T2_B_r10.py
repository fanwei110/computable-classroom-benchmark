import numpy as np
import matplotlib.pyplot as plt

# --- 输入参数 ---
R1, R2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_ret = 0.10

# --- 辅助计算函数 ---
def calc_mvp(R1, R2, sig1, sig2, rho):
    """计算最小方差组合的权重、收益率和波动率"""
    V1, V2 = sig1**2, sig2**2
    cov = rho * sig1 * sig2
    # 最小方差组合权重
    w1 = (V2 - cov) / (V1 + V2 - 2 * cov)
    w2 = 1 - w1
    # 最小方差组合收益率
    ret = w1 * R1 + w2 * R2
    # 最小方差组合波动率 (使用代数等价公式以减少浮点误差)
    vol = np.sqrt((V1 * V2 - cov**2) / (V1 + V2 - 2 * cov))
    return w1, w2, ret, vol

def calc_frontier_vol(R1, R2, sig1, sig2, rho, target_ret):
    """计算给定目标收益率下的最小波动率"""
    w1 = (target_ret - R2) / (R1 - R2)
    w2 = 1 - w1
    cov = rho * sig1 * sig2
    vol = np.sqrt(w1**2 * sig1**2 + w2**2 * sig2**2 + 2 * w1 * w2 * cov)
    return vol, w1, w2

# --- 计算题目要求的特定数值 ---
_, _, mvp_ret_45, mvp_vol_45 = calc_mvp(R1, R2, sig1, sig2, 0.45)
frontier_vol_target, w1_target, w2_target = calc_frontier_vol(R1, R2, sig1, sig2, 0.45, target_ret)

# --- 绘制有效前沿图 ---
w1_arr = np.linspace(-0.5, 1.5, 500)
w2_arr = 1 - w1_arr

plt.figure(figsize=(10, 7))
colors = ['blue', 'green', 'red']

for i, rho in enumerate(rhos):
    cov = rho * sig1 * sig2
    # 计算全组合的收益与波动率
    Rp = w1_arr * R1 + w2_arr * R2
    sigp2 = w1_arr**2 * sig1**2 + w2_arr**2 * sig2**2 + 2 * w1_arr * w2_arr * cov
    sigp = np.sqrt(sigp2)
    
    # 画出双曲线
    plt.plot(sigp, Rp, label=f'$\\rho = {rho}$', color=colors[i], alpha=0.8)
    
    # 标出最小方差点 MVP
    _, _, mvp_ret, mvp_vol = calc_mvp(R1, R2, sig1, sig2, rho)
    plt.scatter(mvp_vol, mvp_ret, marker='*', s=200, color=colors[i], zorder=5)
    plt.annotate(f'MVP ($\\rho={rho}$)\nVol={mvp_vol:.2%}, Ret={mvp_ret:.2%}',
                 xy=(mvp_vol, mvp_ret), xytext=(10, 10 + i*15), textcoords='offset points',
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

# 标出 rho=0.45 时目标收益 10% 的最优点
plt.scatter(frontier_vol_target, target_ret, color='darkgreen', marker='D', s=100, zorder=6, 
            label=f'Target 10% ($\\rho=0.45$)')
plt.annotate(f'Target ($\\rho=0.45$)\nVol={frontier_vol_target:.2%}',
             xy=(frontier_vol_target, target_ret), xytext=(-100, 20), textcoords='offset points',
             arrowprops=dict(facecolor='darkgreen', shrink=0.05, width=1, headwidth=5))

plt.xlabel('Volatility ($\\sigma$)')
plt.ylabel('Expected Return ($\\mu$)')
plt.title('Two-Asset Efficient Frontiers for Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图表
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# --- 封装输出结果 ---
result = {
    'mvp_vol_at_rho45': round(mvp_vol_45, 5),
    'frontier_vol_at_target': round(frontier_vol_target, 5),
    'figure_path': fig_path
}

print(result)
