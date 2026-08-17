import numpy as np
import matplotlib.pyplot as plt

# ---------------- 基础参数设定 ----------------
r1, r2 = 0.071, 0.124       # 期望年收益
s1, s2 = 0.163, 0.289       # 年化波动率
rhos = [0.15, 0.45, 0.75]   # 相关系数
target_ret = 0.10            # 目标收益率

# 目标收益率对应的资产1权重 w
# E[Rp] = w * r1 + (1 - w) * r2 => w = (target_ret - r2) / (r1 - r2)
w_target = (target_ret - r2) / (r1 - r2)

# 初始化结果字典
result = {}

# ---------------- 画图与计算 ----------------
plt.figure(figsize=(10, 7))
colors = ['b', 'g', 'r']

for i, rho in enumerate(rhos):
    # 允许一定程度的卖空以展示完整的双曲线前沿，权重范围设为 [-0.5, 1.5]
    w = np.linspace(-0.5, 1.5, 1000)
    
    # 组合期望收益与波动率
    port_ret = w * r1 + (1 - w) * r2
    port_vol = np.sqrt(w**2 * s1**2 + (1 - w)**2 * s2**2 + 2 * w * (1 - w) * rho * s1 * s2)
    
    # 计算 Minimum Variance Portfolio (MVP) 的权重
    # 对方差求导令其等于0：d(Vol^2)/dw = 0
    w_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    
    # 计算 MVP 的收益与波动率
    ret_mvp = w_mvp * r1 + (1 - w_mvp) * r2
    vol_mvp = np.sqrt(w_mvp**2 * s1**2 + (1 - w_mvp)**2 * s2**2 + 2 * w_mvp * (1 - w_mvp) * rho * s1 * s2)
    
    # 绘制前沿曲线
    plt.plot(port_vol, port_ret, label=f'ρ = {rho}', color=colors[i], lw=2)
    
    # 标记最小方差组合 (MVP)
    plt.scatter(vol_mvp, ret_mvp, color=colors[i], marker='*', s=250, zorder=5)
    plt.text(vol_mvp + 0.005, ret_mvp - 0.002, f'MVP (ρ={rho})\nVol={vol_mvp:.2%}', fontsize=9)
    
    # 单独记录 rho=0.45 时的需求指标
    if rho == 0.45:
        # 1. rho=0.45时最小方差组合的波动率
        result['mvp_vol_at_rho45'] = vol_mvp
        
        # 2. 目标收益10%时的最小波动率
        vol_target = np.sqrt(w_target**2 * s1**2 + (1 - w_target)**2 * s2**2 + 
                             2 * w_target * (1 - w_target) * rho * s1 * s2)
        result['frontier_vol_at_target'] = vol_target

# ---------------- 图表美化 ----------------
plt.title('Efficient Frontier with Different Correlations', fontsize=14)
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Annualized Expected Return', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.10, 0.45)
plt.ylim(0.04, 0.16)

# 保存图表
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
result['figure_path'] = fig_path

# 打印最终结果
print(result)
