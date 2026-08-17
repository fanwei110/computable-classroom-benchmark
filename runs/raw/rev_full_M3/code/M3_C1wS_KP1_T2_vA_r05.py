import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 资产参数设定 ====================
mu1 = 0.071      # 资产1期望年收益
sigma1 = 0.163   # 资产1年化波动率
mu2 = 0.124      # 资产2期望年收益
sigma2 = 0.289   # 资产2年化波动率

var1 = sigma1 ** 2
var2 = sigma2 ** 2

# 相关系数列表
rhos = [0.15, 0.45, 0.75]
target_mu = 0.10 # 目标收益 10%

# 扫描权重：允许一定程度的卖空以画出完整的双曲线边界
w1_arr = np.linspace(-0.5, 1.5, 1000)
mu_p = w1_arr * mu1 + (1 - w1_arr) * mu2

# ==================== 2. 计算并绘图 ====================
plt.figure(figsize=(10, 7))

# 颜色映射
colors = {0.15: 'blue', 0.45: 'green', 0.75: 'red'}

mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 构造协方差
    cov12 = rho * sigma1 * sigma2
    
    # 组合方差与标准差
    var_p = (w1_arr**2 * var1 + 
             (1 - w1_arr)**2 * var2 + 
             2 * w1_arr * (1 - w1_arr) * cov12)
    vol_p = np.sqrt(var_p)
    
    # ---------------- 计算最小方差组合(MVP) ----------------
    # 利用一阶导数求极值点：d(w'Σw)/dw1 = 0
    w1_mvp = (var2 - cov12) / (var1 + var2 - 2 * cov12)
    mu_mvp = w1_mvp * mu1 + (1 - w1_mvp) * mu2
    var_mvp = (w1_mvp**2 * var1 + 
               (1 - w1_mvp)**2 * var2 + 
               2 * w1_mvp * (1 - w1_mvp) * cov12)
    vol_mvp = np.sqrt(var_mvp)
    
    # 画出前沿曲线
    plt.plot(vol_p, mu_p, color=colors[rho], label=f'Frontier (ρ = {rho})', linewidth=2)
    
    # 标出最小方差组合
    plt.scatter(vol_mvp, mu_mvp, marker='*', s=200, color=colors[rho], 
                edgecolor='black', zorder=5, label=f'MVP (ρ = {rho})')
    
    # ---------------- 针对 rho = 0.45 的特定计算 ----------------
    if np.isclose(rho, 0.45):
        # 1. 保存 rho=0.45 的 MVP 波动率
        mvp_vol_at_rho45 = vol_mvp
        
        # 2. 计算目标收益 10% 下的最小波动率
        # 满仓约束下：w1 * mu1 + (1-w1) * mu2 = target_mu
        w1_target = (target_mu - mu2) / (mu1 - mu2)
        var_target = (w1_target**2 * var1 + 
                      (1 - w1_target)**2 * var2 + 
                      2 * w1_target * (1 - w1_target) * cov12)
        vol_target = np.sqrt(var_target)
        frontier_vol_at_target = vol_target
        
        # 在图上标出目标收益10%的点
        plt.scatter(vol_target, target_mu, marker='D', s=100, color=colors[rho], 
                    edgecolor='black', zorder=5, label=f'Target 10% (ρ = {rho})')

# ==================== 3. 图表美化 ====================
plt.title('Markowitz Mean-Variance Efficient Frontier', fontsize=14)
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Annualized Expected Return', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)

# 将刻度格式化为百分比
plt.xticks(ticks=plt.xticks()[0], labels=[f'{xtick:.1%}' for xtick in plt.xticks()[0]])
plt.yticks(ticks=plt.yticks()[0], labels=[f'{ytick:.1%}' for ytick in plt.yticks()[0]])

# ==================== 4. 保存图形及输出结果 ====================
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')

# 封装结果到字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 打印输出供课堂展示核对
print("="*50)
print("计算结果:")
print(f"ρ=0.45 时, 最小方差组合(MVP)的波动率: {result['mvp_vol_at_rho45']:.4%}")
print(f"ρ=0.45 时, 目标收益10%的最小波动率: {result['frontier_vol_at_target']:.4%}")
print(f"图表已保存至: {result['figure_path']}")
print("="*50)
