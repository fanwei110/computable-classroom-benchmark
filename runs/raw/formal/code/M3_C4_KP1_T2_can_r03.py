import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设定与协方差矩阵构造
# ==========================================
mu = np.array([0.071, 0.124])          # 期望年收益
sigma = np.array([0.163, 0.289])       # 年化波动率
rhos = [0.15, 0.45, 0.75]             # 相关系数列表

# 满仓约束下扫描权重 (允许卖空，w1可小于0或大于1)
w1 = np.linspace(-0.5, 2.5, 1000)
w2 = 1 - w1

# 计算各权重下的期望收益
port_mu = w1 * mu[0] + w2 * mu[1]

# ==========================================
# 2. 绘图准备
# ==========================================
plt.figure(figsize=(10, 7))

# 用于存储 rho=0.45 时需要报告的数值
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * sigma[0] * sigma[1]
    Sigma = np.array([
        [sigma[0]**2, cov12],
        [cov12, sigma[1]**2]
    ])
    
    # 扫描权重计算组合波动率 (方差开方前截断极小负值以保证数值稳定)
    port_var = w1**2 * Sigma[0, 0] + 2 * w1 * w2 * Sigma[0, 1] + w2**2 * Sigma[1, 1]
    port_vol = np.sqrt(np.maximum(port_var, 0))
    
    # 计算最小方差组合 (MVP) 解析解
    inv_Sigma = np.linalg.inv(Sigma)
    ones = np.ones(2)
    w_mvp = (inv_Sigma @ ones) / (ones @ inv_Sigma @ ones)
    
    mu_mvp = w_mvp @ mu
    var_mvp = w_mvp @ Sigma @ w_mvp
    vol_mvp = np.sqrt(var_mvp)
    
    # 画出均值-方差前沿曲线
    plt.plot(port_vol, port_mu, label=f'ρ = {rho:.2f}')
    
    # 标出最小方差组合
    plt.scatter(vol_mvp, mu_mvp, marker='D', s=80, zorder=5, edgecolors='k', linewidths=1.2)
    plt.annotate(f'MVP (ρ={rho:.2f})', (vol_mvp, mu_mvp), 
                 textcoords="offset points", xytext=(10, 5), fontsize=9)
    
    # ==========================================
    # 3. 对相关系数 0.45 计算所需的两个波动率
    # ==========================================
    if rho == 0.45:
        mvp_vol_at_rho45 = float(vol_mvp)
        
        # 目标期望收益 10% 下可达到的最小波动率 (双资产下唯一确定权重)
        target_mu = 0.10
        w1_target = (target_mu - mu[1]) / (mu[0] - mu[1])
        w_target = np.array([w1_target, 1 - w1_target])
        
        var_target = w_target @ Sigma @ w_target
        frontier_vol_at_target = float(np.sqrt(var_target))

# ==========================================
# 4. 图形修饰与保存
# ==========================================
plt.xlabel('Volatility (Annualized)')
plt.ylabel('Expected Return (Annualized)')
plt.title('Mean-Variance Frontiers under Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.55)
plt.ylim(0.0, 0.18)

figure_path = 'markowitz_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 填充结果字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 运行时输出以验证 (可选)
if __name__ == '__main__':
    print(result)
