import numpy as np
import matplotlib.pyplot as plt

# 参数设置
r1 = 0.071
r2 = 0.124
vol1 = 0.163
vol2 = 0.289
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 存储结果的字典
result = {}

# 扫描权重的范围（资产1的权重）
w1_range = np.linspace(-1.5, 2.5, 2000)  # 足够覆盖卖空范围

# 绘图设置
plt.figure(figsize=(10, 7))

for rho in rhos:
    # 协方差矩阵元素（此处直接使用解析式）
    cov12 = rho * vol1 * vol2
    var1 = vol1 ** 2
    var2 = vol2 ** 2

    # 组合收益率与方差
    w2_range = 1 - w1_range
    port_ret = w1_range * r1 + w2_range * r2
    port_var = (w1_range ** 2) * var1 + (w2_range ** 2) * var2 + 2 * w1_range * w2_range * cov12
    port_vol = np.sqrt(port_var)

    # 绘制前沿曲线
    plt.plot(port_vol, port_ret, label=f'ρ = {rho}')

    # 最小方差组合 (MVP) 解析解
    w1_mvp = (var2 - cov12) / (var1 + var2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    ret_mvp = w1_mvp * r1 + w2_mvp * r2
    var_mvp = (w1_mvp ** 2) * var1 + (w2_mvp ** 2) * var2 + 2 * w1_mvp * w2_mvp * cov12
    vol_mvp = np.sqrt(var_mvp)

    # 标记MVP点
    plt.scatter(vol_mvp, ret_mvp, marker='*', s=150, 
                label=f'MVP ρ={rho}' if rho == rhos[1] else "", zorder=5)

    # 存储rho=0.45时的MVP波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp

        # 目标收益10%下的组合
        w1_target = (target_return - r2) / (r1 - r2)
        w2_target = 1 - w1_target
        var_target = (w1_target ** 2) * var1 + (w2_target ** 2) * var2 + 2 * w1_target * w2_target * cov12
        vol_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = vol_target

        # 标记目标收益点（可选，便于课堂展示）
        plt.scatter(vol_target, target_return, marker='o', s=80, 
                    color='red', label=f'Target 10% ρ=0.45', zorder=5)

# 图形修饰
plt.xlabel('Annualized Volatility (Std Dev)')
plt.ylabel('Annualized Expected Return')
plt.title('Mean-Variance Frontier for Two Risky Assets')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 保存图形
figure_filename = 'frontier.png'
plt.savefig(figure_filename, dpi=150)
result['figure_path'] = figure_filename

# 输出结果字典（课堂展示用）
print(result)
