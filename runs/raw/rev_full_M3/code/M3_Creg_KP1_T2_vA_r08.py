import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==================== 1. 定义资产参数 ====================
E1 = 0.071       # 资产1期望年收益
E2 = 0.124       # 资产2期望年收益
sigma1 = 0.163   # 资产1年化波动率
sigma2 = 0.289   # 资产2年化波动率

# 给定的三种相关系数
rhos = [0.15, 0.45, 0.75]

# 允许卖空，设定权重范围以展示完整的双曲线前沿
w1_arr = np.linspace(-0.5, 1.5, 1000)
w2_arr = 1 - w1_arr

# ==================== 2. 绘制均值-方差前沿 ====================
plt.figure(figsize=(10, 7))

# 用于存储所需报告的特定值
mvp_vol_45 = None
frontier_vol_10_45 = None

for rho in rhos:
    # 协方差
    cov12 = rho * sigma1 * sigma2
    
    # 计算投资组合的期望收益和波动率
    mu_p = w1_arr * E1 + w2_arr * E2
    var_p = (w1_arr**2 * sigma1**2 + 
             w2_arr**2 * sigma2**2 + 
             2 * w1_arr * w2_arr * cov12)
    std_p = np.sqrt(var_p)
    
    # 计算最小方差组合 (MVP)
    w1_mvp = (sigma2**2 - cov12) / (sigma1**2 + sigma2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    mu_mvp = w1_mvp * E1 + w2_mvp * E2
    var_mvp = (w1_mvp**2 * sigma1**2 + 
               w2_mvp**2 * sigma2**2 + 
               2 * w1_mvp * w2_mvp * cov12)
    std_mvp = np.sqrt(var_mvp)
    
    # 绘制前沿曲线
    plt.plot(std_p, mu_p, label=f'相关系数 ρ = {rho}', linewidth=2)
    
    # 标出最小方差组合点
    plt.scatter(std_mvp, mu_mvp, marker='*', s=200, zorder=5, edgecolors='black', linewidths=0.5)
    plt.annotate(f'MVP (ρ={rho})\nσ={std_mvp:.2%}', 
                 xy=(std_mvp, mu_mvp), 
                 xytext=(15, -25 if rho == 0.75 else 15), 
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                 fontsize=9,
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # 针对相关系数 0.45 的特定计算需求
    if rho == 0.45:
        # 记录 0.45 下的 MVP 波动率
        mvp_vol_45 = std_mvp
        
        # 计算目标期望收益 10% 下的最小波动率
        target_mu = 0.10
        # 由 w1*E1 + w2*E2 = target_mu 且 w1+w2=1 解得:
        w1_target = (target_mu - E2) / (E1 - E2)
        w2_target = 1 - w1_target
        var_target = (w1_target**2 * sigma1**2 + 
                     w2_target**2 * sigma2**2 + 
                     2 * w1_target * w2_target * cov12)
        std_target = np.sqrt(var_target)
        frontier_vol_10_45 = std_target

# 图表修饰
plt.title('两只风险资产的均值-方差前沿', fontsize=14)
plt.xlabel('年化波动率', fontsize=12)
plt.ylabel('期望年收益', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.50)
plt.ylim(0.02, 0.18)

# 保存图表
fig_path = 'mean_variance_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 3. 构建输出字典 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': frontier_vol_10_45,
    'figure_path': fig_path
}

# 打印结果以供验证
print("任务输出结果：")
for k, v in result.items():
    if isinstance(v, float):
        print(f"{k}: {v:.6f} ({v*100:.4f}%)")
    else:
        print(f"{k}: {v}")
