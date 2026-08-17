import numpy as np
import matplotlib.pyplot as plt

# ====================
# 1. 基础参数设置
# ====================
mu1 = 0.071       # 资产1期望年收益
mu2 = 0.124       # 资产2期望年收益
sig1 = 0.163      # 资产1年化波动率
sig2 = 0.289      # 资产2年化波动率

# 相关系数列表
rhos = [0.15, 0.45, 0.75]

# 扫描权重：允许卖空，w1范围适当放大以完整展现前沿
w1_scan = np.linspace(-0.5, 1.5, 500)
w2_scan = 1 - w1_scan

# ====================
# 2. 绘图与计算
# ====================
plt.figure(figsize=(10, 7))

# 用于存储最终要求的结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# 目标期望收益
target_return = 0.10

for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * sig1 * sig2
    Sigma = np.array([[sig1**2, cov12], 
                      [cov12, sig2**2]])
    
    # ------------------
    # 扫描权重计算前沿
    # ------------------
    port_ret = w1_scan * mu1 + w2_scan * mu2
    port_var = w1_scan**2 * sig1**2 + w2_scan**2 * sig2**2 + 2 * w1_scan * w2_scan * cov12
    # 防止因数值精度导致极小的负数无法开方
    port_vol = np.sqrt(np.maximum(port_var, 0))
    
    # 绘制前沿曲线
    plt.plot(port_vol, port_ret, label=f'$\\rho = {rho}$', lw=2)
    
    # ------------------
    # 计算并标出最小方差组合(MVP)
    # ------------------
    # 两资产MVP解析解权重公式
    w1_mvp = (sig2**2 - cov12) / (sig1**2 + sig2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    
    mvp_ret = w1_mvp * mu1 + w2_mvp * mu2
    mvp_var = w1_mvp**2 * sig1**2 + w2_mvp**2 * sig2**2 + 2 * w1_mvp * w2_mvp * cov12
    mvp_vol = np.sqrt(mvp_var)
    
    # 在图上标出MVP点
    plt.scatter(mvp_vol, mvp_ret, marker='D', s=50, zorder=5)
    
    # ------------------
    # 针对rho=0.45的特殊计算
    # ------------------
    if rho == 0.45:
        # 记录MVP的波动率
        mvp_vol_at_rho45 = mvp_vol
        
        # 计算目标期望收益下的最小波动率（满仓约束下两资产唯一确定组合权重）
        w1_target = (target_return - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        
        target_var = w1_target**2 * sig1**2 + w2_target**2 * sig2**2 + 2 * w1_target * w2_target * cov12
        frontier_vol_at_target = np.sqrt(target_var)
        
        # （可选）在图上也标出目标收益点，方便课堂演示
        plt.scatter(frontier_vol_at_target, target_return, marker='*', s=150, color='red', zorder=6, label='Target at 10% ($\\rho=0.45$)')

# ====================
# 3. 图表修饰与保存
# ====================
plt.title('Mean-Variance Frontier under Different Correlations', fontsize=14)
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Expected Annual Return', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

figure_path = 'markowitz_frontier.png'
plt.savefig(figure_path, dpi=300)
plt.close()

# ====================
# 4. 封装输出结果
# ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 打印结果以供检查（课堂演示时可以注释掉）
print(f"rho=0.45 时最小方差组合的年化波动率: {mvp_vol_at_rho45:.4f}")
print(f"rho=0.45 时期望收益10%对应的最小年化波动率: {frontier_vol_at_target:.4f}")
print(f"图片已保存至: {figure_path}")
