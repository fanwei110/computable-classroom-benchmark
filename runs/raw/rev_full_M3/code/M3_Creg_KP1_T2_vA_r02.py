import numpy as np
import matplotlib.pyplot as plt

# ==================== 资产参数 ====================
mu1 = 0.071      # 资产1期望年收益
mu2 = 0.124      # 资产2期望年收益
sig1 = 0.163     # 资产1年化波动率
sig2 = 0.289     # 资产2年化波动率

rhos = [0.15, 0.45, 0.75] # 相关系数

# ==================== 核心计算函数 ====================
def calc_w_for_target_mu(mu_target, mu1, mu2):
    """计算目标期望收益下的资产1权重"""
    return (mu_target - mu2) / (mu1 - mu2)

def calc_portfolio_sigma(w, sig1, sig2, rho):
    """计算给定权重和相关系数下的组合波动率"""
    var = w**2 * sig1**2 + (1-w)**2 * sig2**2 + 2 * w * (1-w) * rho * sig1 * sig2
    return np.sqrt(var)

def calc_w_mvp(sig1, sig2, rho):
    """计算最小方差组合(MVP)中资产1的权重"""
    denominator = sig1**2 + sig2**2 - 2 * rho * sig1 * sig2
    return (sig2**2 - rho * sig1 * sig2) / denominator

# ==================== 特定任务计算 (rho = 0.45) ====================
rho45 = 0.45
# 1. 计算rho=0.45时最小方差组合的权重、收益和波动率
w_mvp_45 = calc_w_mvp(sig1, sig2, rho45)
mu_mvp_45 = w_mvp_45 * mu1 + (1 - w_mvp_45) * mu2
mvp_vol_45 = calc_portfolio_sigma(w_mvp_45, sig1, sig2, rho45)

# 2. 计算rho=0.45、目标收益10%时的权重和最小波动率
target_mu = 0.10
w_target_10 = calc_w_for_target_mu(target_mu, mu1, mu2)
frontier_vol_at_target = calc_portfolio_sigma(w_target_10, sig1, sig2, rho45)

# ==================== 绘图 ====================
fig, ax = plt.subplots(figsize=(10, 7))

# 权重范围（允许卖空，故向0-1区间两端延伸）
w_range = np.linspace(-1.0, 2.0, 1000)

# 遍历相关系数绘制均值-方差前沿
colors = ['blue', 'green', 'red']

for rho, color in zip(rhos, colors):
    # 计算当前rho下的MVP
    w_mvp = calc_w_mvp(sig1, sig2, rho)
    mu_mvp = w_mvp * mu1 + (1 - w_mvp) * mu2
    sig_mvp = calc_portfolio_sigma(w_mvp, sig1, sig2, rho)
    
    # 计算前沿曲线
    mus = w_range * mu1 + (1 - w_range) * mu2
    sigs = calc_portfolio_sigma(w_range, sig1, sig2, rho)
    
    # 绘制前沿曲线
    ax.plot(sigs, mus, label=f'ρ = {rho:.2f}', color=color, linewidth=2)
    
    # 标出最小方差组合
    ax.scatter(sig_mvp, mu_mvp, color=color, zorder=5, marker='o', s=80)
    
    # 动态调整注释位置以避免重叠
    offsets = {
        0.15: (0.02, 0.012),
        0.45: (0.02, -0.012),
        0.75: (-0.14, -0.025)
    }
    ax.annotate(f'MVP (ρ={rho})\nσ={sig_mvp:.2%}, μ={mu_mvp:.2%}',
                xy=(sig_mvp, mu_mvp), 
                xytext=(sig_mvp + offsets[rho][0], mu_mvp + offsets[rho][1]),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 标出原始的两个风险资产点
ax.scatter([sig1, sig2], [mu1, mu2], color='black', zorder=5, marker='D', s=80, label='Individual Assets')
ax.annotate('Asset 1', xy=(sig1, mu1), xytext=(sig1 - 0.06, mu1 + 0.01), fontsize=10)
ax.annotate('Asset 2', xy=(sig2, mu2), xytext=(sig2 + 0.01, mu2 + 0.01), fontsize=10)

# 格式化坐标轴为百分比形式
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))

ax.set_xlabel('Volatility (Annualized)', fontsize=12)
ax.set_ylabel('Expected Return (Annualized)', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Two Risky Assets', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图像
figure_path = 'mean_variance_frontier.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# ==================== 输出结果封装 ====================
result = {
    'mvp_vol_at_rho45': float(mvp_vol_45),
    'frontier_vol_at_target': float(frontier_vol_at_target),
    'figure_path': figure_path
}

# 打印字典以供验证（可选）
# print(result)
