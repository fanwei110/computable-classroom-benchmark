import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rhos = [0.15, 0.45, 0.75]

# 准备绘图
fig, ax = plt.subplots(figsize=(8, 5))

# 结果存储
result = {}

for rho in rhos:
    cov = np.array([[sigma[0]**2, rho * sigma[0] * sigma[1]],
                    [rho * sigma[0] * sigma[1], sigma[1]**2]])
    # 生成组合权重
    ws = np.linspace(0, 1, 200)
    rets = ws * r[0] + (1 - ws) * r[1]
    vols = np.sqrt(ws**2 * sigma[0]**2 + (1 - ws)**2 * sigma[1]**2 +
                   2 * ws * (1 - ws) * cov[0, 1])
    
    # 绘制有效前沿
    ax.plot(vols, rets, label=f'ρ={rho}')
    
    # 找到最小方差组合 (MVP)
    mvp_w1 = (sigma[1]**2 - cov[0, 1]) / (sigma[0]**2 + sigma[1]**2 - 2 * cov[0, 1])
    mvp_w2 = 1 - mvp_w1
    mvp_ret = mvp_w1 * r[0] + mvp_w2 * r[1]
    mvp_vol = np.sqrt(mvp_w1**2 * sigma[0]**2 + mvp_w2**2 * sigma[1]**2 +
                      2 * mvp_w1 * mvp_w2 * cov[0, 1])
    
    # 标注 MVP 点
    ax.scatter(mvp_vol, mvp_ret, marker='*', s=100, zorder=5)
    ax.annotate(f'ρ={rho}\nMVP', (mvp_vol, mvp_ret),
                textcoords="offset points", xytext=(10, -10), fontsize=8)
    
    # 记录 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = round(mvp_vol, 4)
        
        # 目标收益 10% 时的最小波动率（有效前沿上分支）
        target_ret = 0.10
        # w1 * r1 + (1-w1) * r2 = target_ret  -> w1 = (target_ret - r2) / (r1 - r2)
        w1_target = (target_ret - r[1]) / (r[0] - r[1])
        if 0 <= w1_target <= 1:
            w2_target = 1 - w1_target
            vol_target = np.sqrt(w1_target**2 * sigma[0]**2 + w2_target**2 * sigma[1]**2 +
                                 2 * w1_target * w2_target * cov[0, 1])
            result['frontier_vol_at_target'] = round(vol_target, 4)
            # 在图上标出目标收益点
            ax.scatter(vol_target, target_ret, marker='o', s=80, color='red', zorder=5)
            ax.annotate(f'Target 10%\nρ=0.45', (vol_target, target_ret),
                        textcoords="offset points", xytext=(10, 10), fontsize=8, color='red')

# 图形修饰
ax.set_xlabel('Volatility (σ)')
ax.set_ylabel('Expected Return')
ax.set_title('Efficient Frontiers for Two Assets')
ax.legend()
ax.grid(True)
fig.tight_layout()

# 保存图片
fig_path = 'frontier.png'
fig.savefig(fig_path)
result['figure_path'] = fig_path

print(result)
