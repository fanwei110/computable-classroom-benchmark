import numpy as np
import matplotlib.pyplot as plt

# 给定参数（小数形式）
r1, r2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_return = 0.10  # 目标收益

# 协方差矩阵元素
var1 = sigma1 ** 2
var2 = sigma2 ** 2

# 存储计算结果
result = {}

# 创建图形
plt.figure(figsize=(10, 6))

for rho in rhos:
    cov = rho * sigma1 * sigma2

    # 生成资产1的权重范围，用于画有效前沿
    w1_range = np.linspace(-0.5, 1.5, 300)
    w2_range = 1 - w1_range
    ret_range = w1_range * r1 + w2_range * r2
    vol_range = np.sqrt(
        w1_range**2 * var1 + w2_range**2 * var2 + 2 * w1_range * w2_range * cov
    )

    # 画有效前沿曲线
    plt.plot(vol_range, ret_range, label=f'ρ = {rho}')

    # 最小方差组合 (MVP)
    w1_mvp = (var2 - cov) / (var1 + var2 - 2 * cov)
    w2_mvp = 1 - w1_mvp
    ret_mvp = w1_mvp * r1 + w2_mvp * r2
    vol_mvp = np.sqrt(
        w1_mvp**2 * var1 + w2_mvp**2 * var2 + 2 * w1_mvp * w2_mvp * cov
    )

    # 标注最小方差点
    plt.scatter(vol_mvp, ret_mvp, marker='o', s=50,
                label=f'MVP ρ={rho}: ({vol_mvp:.4f}, {ret_mvp:.4f})' if rho == rhos[0] else "")

    # 单独记录 rho=0.45 的结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp
        # 目标收益10%的最小波动率组合（即该收益在有效前沿上的唯一点）
        w1_target = (target_return - r2) / (r1 - r2)
        w2_target = 1 - w1_target
        vol_target = np.sqrt(
            w1_target**2 * var1 + w2_target**2 * var2 + 2 * w1_target * w2_target * cov
        )
        result['frontier_vol_at_target'] = vol_target

        # 在图上标注目标收益点
        plt.scatter(vol_target, target_return, marker='*', s=100, color='red',
                    label=f'Target 10% ρ=0.45: ({vol_target:.4f}, {target_return:.2f})')

# 图形设置
plt.xlabel('波动率 (Volatility)')
plt.ylabel('收益率 (Return)')
plt.title('两资产有效前沿 (不同相关系数)')
plt.legend()
plt.grid(True)

# 保存图形
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path)
plt.close()

result['figure_path'] = fig_path

# 输出结果
print(result)
