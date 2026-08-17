import numpy as np
import matplotlib.pyplot as plt

# 已知参数
E1, E2 = 0.071, 0.124
vol1, vol2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 生成权重序列（包含卖空情况以展示完整前沿）
w1 = np.linspace(-0.5, 1.5, 500)
w2 = 1 - w1

mvp_vol_45 = 0
vol_target_10 = 0

plt.figure(figsize=(10, 7))

for rho in rhos:
    # 计算组合收益与波动率
    rets = w1 * E1 + w2 * E2
    cov12 = rho * vol1 * vol2
    vols = np.sqrt((w1**2) * (vol1**2) + (w2**2) * (vol2**2) + 2 * w1 * w2 * cov12)
    
    # 绘制有效前沿
    plt.plot(vols, rets, label=f'$\\rho$ = {rho}')
    
    # 计算最小方差组合(MVP)权重
    w1_mvp = (vol2**2 - cov12) / (vol1**2 + vol2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    
    # 计算MVP的收益与波动率
    ret_mvp = w1_mvp * E1 + w2_mvp * E2
    vol_mvp = np.sqrt((w1_mvp**2) * (vol1**2) + (w2_mvp**2) * (vol2**2) + 2 * w1_mvp * w2_mvp * cov12)
    
    # 标出MVP点
    plt.scatter(vol_mvp, ret_mvp, marker='o', s=60, zorder=5)
    plt.annotate(f'MVP ({vol_mvp:.2%}, {ret_mvp:.2%})', 
                 xy=(vol_mvp, ret_mvp), 
                 xytext=(10, 5), 
                 textcoords='offset points',
                 fontsize=9)
                 
    # 针对 rho = 0.45 计算特定指标
    if rho == 0.45:
        mvp_vol_45 = vol_mvp
        
        # 目标收益 10% 的最小波动率组合
        target_ret = 0.10
        w1_target = (target_ret - E2) / (E1 - E2)
        w2_target = 1 - w1_target
        vol_target_10 = np.sqrt((w1_target**2) * (vol1**2) + (w2_target**2) * (vol2**2) + 2 * w1_target * w2_target * cov12)

# 绘制单独的资产点
plt.scatter([vol1, vol2], [E1, E2], color='black', marker='*', s=150, zorder=6, label='Assets')

plt.title('Two-Asset Efficient Frontier')
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path)
plt.close()

# 按照输出契约要求，构建结果字典
result = {
    'mvp_vol_at_rho45': round(float(mvp_vol_45), 4),      # 0.45相关系数下的MVP波动率 (16.17%)
    'frontier_vol_at_target': round(float(vol_target_10), 4), # 目标收益10%时的最小波动率 (20.24%)
    'figure_path': fig_path
}

print(result)
