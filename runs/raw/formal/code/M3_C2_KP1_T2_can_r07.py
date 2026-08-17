import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设定
# ==========================================
mu1, mu2 = 0.071, 0.124        # 期望年收益
sig1, sig2 = 0.163, 0.289      # 年化波动率
rhos = [0.15, 0.45, 0.75]      # 给定的相关系数
mu_target = 0.10               # 目标期望收益

# ==========================================
# 2. 组合权重扫描与前沿计算
# ==========================================
# 允许卖空，权重可以超出[0,1]区间，选取[-0.5, 2.0]以展示完整的双曲线前沿
w1_vals = np.linspace(-0.5, 2.0, 1000)
w2_vals = 1 - w1_vals
w_arr = np.vstack([w1_vals, w2_vals]).T  # shape: (1000, 2)

mu_vec = np.array([mu1, mu2])

plt.figure(figsize=(10, 7))

mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * sig1 * sig2
    Sigma = np.array([[sig1**2, cov12], 
                      [cov12, sig2**2]])
    
    # 扫描权重计算组合的期望收益与方差
    mu_p = w_arr @ mu_vec
    var_p = (w_arr @ Sigma * w_arr).sum(axis=1)
    var_p = np.maximum(var_p, 0)  # 防止浮点误差导致极小的负数
    sig_p = np.sqrt(var_p)
    
    # 绘制前沿曲线，并获取当前线条颜色以便MVP点配色
    line, = plt.plot(sig_p, mu_p, label=f'$\\rho = {rho}$', linewidth=1.5)
    line_color = line.get_color()
    
    # 解析求解最小方差组合 (MVP)
    # 对 var = w^2*sig1^2 + (1-w)^2*sig2^2 + 2*w*(1-w)*cov12 求导令其等于0
    w1_mvp = (sig2**2 - cov12) / (sig1**2 + sig2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    w_mvp = np.array([w1_mvp, w2_mvp])
    
    mu_mvp = w_mvp @ mu_vec
    var_mvp = w_mvp @ Sigma @ w_mvp
    sig_mvp = np.sqrt(max(var_mvp, 0))
    
    # 在图上标出最小方差组合，颜色与对应曲线一致
    plt.scatter(sig_mvp, mu_mvp, s=60, zorder=5, color=line_color, edgecolors='black')
    
    # 针对相关系数 0.45 计算所需的两个指标
    if rho == 0.45:
        mvp_vol_at_rho45 = sig_mvp
        
        # 目标期望收益 10% 的组合权重 (两资产满仓约束下，权重被唯一确定)
        w1_target = (mu2 - mu_target) / (mu2 - mu1)
        w2_target = 1 - w1_target
        w_target = np.array([w1_target, w2_target])
        
        var_target = w_target @ Sigma @ w_target
        frontier_vol_at_target = np.sqrt(max(var_target, 0))
        
        # 额外标记目标收益点，辅助课堂展示
        plt.scatter(frontier_vol_at_target, mu_target, marker='*', s=200, color='red', zorder=5, 
                    label='Target 10% ($\\rho=0.45$)')

# ==========================================
# 3. 图表格式设置与保存
# ==========================================
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Expected Annual Return', fontsize=12)
plt.title('Markowitz Mean-Variance Frontier', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

fig_path = 'markowitz_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 4. 填充结果字典与输出
# ==========================================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': fig_path
}

# 终端打印结果以便课堂投屏实时查看
print("--- 计算结果 ---")
print(f"1. 相关系数 0.45 时的最小方差组合年化波动率: {result['mvp_vol_at_rho45']:.4%}")
print(f"2. 相关系数 0.45 时目标期望收益 10% 下的最小年化波动率: {result['frontier_vol_at_target']:.4%}")
print(f"3. 图像已保存至: {result['figure_path']}")
