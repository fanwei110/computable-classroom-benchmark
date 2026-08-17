import numpy as np
import matplotlib.pyplot as plt

# 资产参数（小数形式）
mu1, mu2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
var1, var2 = sigma1**2, sigma2**2

# 三个相关系数
rhos = [0.15, 0.45, 0.75]
colors = ['blue', 'green', 'red']

# 用于存放目标值的字典
result = {}

# 生成一个较宽范围的权重以覆盖全局最小方差组合
w1_range = np.linspace(-1.5, 2.5, 1000)

plt.figure(figsize=(8, 5))

for rho, color in zip(rhos, colors):
    cov = rho * sigma1 * sigma2
    
    # 组合收益与波动率
    w2_range = 1 - w1_range
    port_mu = w1_range * mu1 + w2_range * mu2
    port_var = (w1_range**2 * var1 + w2_range**2 * var2 +
                2 * w1_range * w2_range * cov)
    port_sigma = np.sqrt(port_var)
    
    # 全局最小方差组合（MVP）
    # 解析解权重
    w1_mvp = (var2 - cov) / (var1 + var2 - 2*cov)
    w2_mvp = 1 - w1_mvp
    mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
    sigma_mvp = np.sqrt(w1_mvp**2 * var1 + w2_mvp**2 * var2 +
                        2 * w1_mvp * w2_mvp * cov)
    
    # 找出有效前沿部分（mu >= mu_mvp 的上半支）
    eff_mask = port_mu >= mu_mvp
    eff_mu = port_mu[eff_mask]
    eff_sigma = port_sigma[eff_mask]
    
    # 绘制有效前沿曲线
    label = f'ρ = {rho}'
    plt.plot(eff_sigma, eff_mu, color=color, label=label)
    
    # 标出最小方差组合
    plt.scatter(sigma_mvp, mu_mvp, color=color, marker='o', s=50, zorder=5,
                edgecolors='black')
    # 可选：在旁边标注
    # plt.annotate(f'MVP\n({sigma_mvp:.3f}, {mu_mvp:.3f})', 
    #              (sigma_mvp, mu_mvp), textcoords="offset points",
    #              xytext=(10, -10), fontsize=8, color=color)
    
    # 若为 rho=0.45，记录所需数值
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = round(sigma_mvp, 6)
        # 目标收益 10% 时的最小波动率
        w1_target = (0.10 - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        sigma_target = np.sqrt(w1_target**2 * var1 + w2_target**2 * var2 +
                               2 * w1_target * w2_target * cov)
        result['frontier_vol_at_target'] = round(sigma_target, 6)

# 图和轴标签
plt.xlabel('年化波动率')
plt.ylabel('期望年收益')
plt.title('不同相关系数下的有效前沿')
plt.legend()
plt.grid(True)

# 保存图像
figure_file = 'efficient_frontier.png'
plt.savefig(figure_file, dpi=150, bbox_inches='tight')
plt.close()

result['figure_path'] = figure_file

# 输出结果
print(result)
