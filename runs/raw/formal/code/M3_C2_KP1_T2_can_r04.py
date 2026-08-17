import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
mu1, mu2 = 0.071, 0.124       # 期望年收益
sig1, sig2 = 0.163, 0.289     # 年化波动率
rhos = [0.15, 0.45, 0.75]     # 给定的相关系数
target_return = 0.10           # 目标期望收益

# ==================== 权重扫描 ====================
# 允许卖空，满仓约束下 w1 + w2 = 1，仅扫描 w1 即可
w1_arr = np.linspace(-1.0, 2.0, 1000)
w2_arr = 1.0 - w1_arr

# 各权重下的组合期望收益
port_ret_arr = w1_arr * mu1 + w2_arr * mu2

# ==================== 绘图与计算 ====================
plt.figure(figsize=(10, 7))

# 用于存储特定计算结果
mvp_vol_rho45 = None
frontier_vol_target_rho45 = None

for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * sig1 * sig2
    # 组合方差：w1^2*sig1^2 + w2^2*sig2^2 + 2*w1*w2*cov12
    port_var_arr = (w1_arr**2) * (sig1**2) + (w2_arr**2) * (sig2**2) + 2 * w1_arr * w2_arr * cov12
    port_vol_arr = np.sqrt(port_var_arr)
    
    # 寻找最小方差组合 (MVP)
    mvp_idx = np.argmin(port_var_arr)
    mvp_w1 = w1_arr[mvp_idx]
    mvp_ret = port_ret_arr[mvp_idx]
    mvp_vol = port_vol_arr[mvp_idx]
    
    # 绘制有效前沿曲线
    plt.plot(port_vol_arr, port_ret_arr, label=f'ρ = {rho:.2f}')
    # 标出最小方差组合
    plt.scatter(mvp_vol, mvp_ret, marker='*', s=200, zorder=5)
    
    # rho = 0.45 时的特定计算
    if rho == 0.45:
        mvp_vol_rho45 = mvp_vol
        
        # 解析求解目标期望收益下的最优权重
        # 由 E[Rp] = w1*mu1 + (1-w1)*mu2 = target_return
        w1_target = (target_return - mu2) / (mu1 - mu2)
        w2_target = 1.0 - w1_target
        
        # 计算该权重下的波动率
        target_var = (w1_target**2) * (sig1**2) + (w2_target**2) * (sig2**2) + 2 * w1_target * w2_target * cov12
        frontier_vol_target_rho45 = np.sqrt(target_var)

# ==================== 图表美化 ====================
plt.xlabel('Volatility (σ)', fontsize=12)
plt.ylabel('Expected Return (μ)', fontsize=12)
plt.title('Mean-Variance Frontier for Different Correlations', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, max(sig2, np.max(port_vol_arr)) * 1.1)
plt.ylim(min(mu1, mu2) - 0.02, max(mu1, mu2) + 0.02)

# 标出单一资产点
plt.scatter([sig1, sig2], [mu1, mu2], c='black', marker='o', s=60, zorder=5, label='Individual Assets')
plt.text(sig1, mu1, ' Asset 1', verticalalignment='bottom')
plt.text(sig2, mu2, ' Asset 2', verticalalignment='bottom')

figure_path = 'markowitz_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 结果封装 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_rho45,
    'frontier_vol_at_target': frontier_vol_target_rho45,
    'figure_path': figure_path
}

# 课堂展示打印（可选，方便投屏观看输出）
print(f"相关系数为0.45时的最小方差组合年化波动率: {mvp_vol_rho45:.4%}")
print(f"相关系数为0.45时目标收益10%下的最小年化波动率: {frontier_vol_target_rho45:.4%}")
print(f"图表已保存至: {figure_path}")
