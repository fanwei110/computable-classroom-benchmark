import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
mu = np.array([0.071, 0.124])                    # 期望年收益
sigma = np.array([0.163, 0.289])                 # 年化波动率
rhos = [0.15, 0.45, 0.75]                        # 相关系数列表
target_return = 0.10                             # 目标期望收益 10%

# 存放结果
result = {}

# 创建图形
plt.figure(figsize=(10, 6))

for rho in rhos:
    # 协方差矩阵元素
    cov_11 = sigma[0] ** 2
    cov_22 = sigma[1] ** 2
    cov_12 = rho * sigma[0] * sigma[1]

    # 最小方差组合权重 w1 (资产1权重)
    # w1 = (σ2^2 - ρ σ1 σ2) / (σ1^2 + σ2^2 - 2 ρ σ1 σ2)
    w1_mvp = (cov_22 - cov_12) / (cov_11 + cov_22 - 2 * cov_12)
    w2_mvp = 1.0 - w1_mvp

    # 最小方差组合的期望收益与波动率
    ret_mvp = w1_mvp * mu[0] + w2_mvp * mu[1]
    vol_mvp = np.sqrt(w1_mvp**2 * cov_11 + w2_mvp**2 * cov_22 + 2 * w1_mvp * w2_mvp * cov_12)

    # 如果是 0.45 相关系数，记录最小方差组合波动率
    if abs(rho - 0.45) < 1e-12:
        result['mvp_vol_at_rho45'] = vol_mvp

    # 扫描组合权重，生成均值-方差前沿
    w1_range = np.linspace(-1.5, 2.5, 2000)   # 允许卖空，足够覆盖
    w2_range = 1.0 - w1_range
    ret_range = w1_range * mu[0] + w2_range * mu[1]
    vol_range = np.sqrt(
        w1_range**2 * cov_11 +
        w2_range**2 * cov_22 +
        2 * w1_range * w2_range * cov_12
    )

    # 绘制前沿曲线
    plt.plot(vol_range, ret_range, lw=2, label=f'$\\rho$ = {rho}')
    # 标记最小方差组合
    plt.scatter(vol_mvp, ret_mvp, s=80, zorder=5, marker='o', color=plt.gca().lines[-1].get_color())

# 对相关系数 0.45 计算目标收益 10% 的最小波动率
rho_target = 0.45
cov_12_target = rho_target * sigma[0] * sigma[1]
# 由满仓约束解权重： w1*mu1 + (1-w1)*mu2 = target_return
w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
w2_target = 1.0 - w1_target
vol_target = np.sqrt(
    w1_target**2 * cov_11 +
    w2_target**2 * cov_22 +
    2 * w1_target * w2_target * cov_12_target
)
result['frontier_vol_at_target'] = vol_target

# 图表修饰
plt.xlabel('Volatility (Std Dev)', fontsize=13)
plt.ylabel('Expected Return', fontsize=13)
plt.title('Mean-Variance Frontiers for Different Correlation Coefficients', fontsize=14)
plt.grid(alpha=0.3)
plt.legend(title='Correlation', fontsize=11)
plt.tight_layout()

# 保存图形
figure_filename = 'mean_variance_frontiers.png'
plt.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close()

# 写入 figure_path (使用绝对路径增强可复现性)
result['figure_path'] = os.path.abspath(figure_filename)

# 输出结果字典
print(result)
