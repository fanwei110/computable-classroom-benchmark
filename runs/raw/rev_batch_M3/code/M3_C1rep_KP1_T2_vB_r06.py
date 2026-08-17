import numpy as np
import matplotlib.pyplot as plt

# 基础参数设定
r1, r2 = 0.071, 0.124       # 收益率 7.1% 和 12.4%
s1, s2 = 0.163, 0.289       # 波动率 16.3% 和 28.9%
rhos = [0.15, 0.45, 0.75]   # 相关系数
target_ret = 0.10            # 目标收益 10%

# 生成资产1的权重（包含做空情况以便画出完整的双曲线前沿）
w1 = np.linspace(-0.5, 1.5, 500)
w2 = 1 - w1

# 初始化需要计算的特定变量
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

plt.figure(figsize=(10, 7))

for rho in rhos:
    # 计算组合的收益与波动率
    ret = w1 * r1 + w2 * r2
    vol = np.sqrt(w1**2 * s1**2 + w2**2 * s2**2 + 2 * w1 * w2 * rho * s1 * s2)
    
    # 解析计算最小方差组合 (MVP) 的权重
    w1_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    w2_mvp = 1 - w1_mvp
    
    # 计算 MVP 的收益与波动率
    mvp_ret = w1_mvp * r1 + w2_mvp * r2
    mvp_vol = np.sqrt(w1_mvp**2 * s1**2 + w2_mvp**2 * s2**2 + 2 * w1_mvp * w2_mvp * rho * s1 * s2)
    
    # 绘制前沿曲线
    plt.plot(vol * 100, ret * 100, label=f'ρ = {rho}', linewidth=2)
    
    # 标出最小方差点
    plt.scatter(mvp_vol * 100, mvp_ret * 100, marker='o', s=60, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\n({mvp_vol*100:.2f}%, {mvp_ret*100:.2f}%)',
                 xy=(mvp_vol * 100, mvp_ret * 100),
                 xytext=(mvp_vol * 100 + 3, mvp_ret * 100 - 1.2),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

    # 针对相关系数 0.45 的特定计算
    if rho == 0.45:
        mvp_vol_at_rho45 = mvp_vol * 100
        
        # 计算目标收益 10% 时的权重及最小波动率
        w1_target = (r2 - target_ret) / (r2 - r1)
        w2_target = 1 - w1_target
        target_vol = np.sqrt(w1_target**2 * s1**2 + w2_target**2 * s2**2 + 2 * w1_target * w2_target * rho * s1 * s2)
        frontier_vol_at_target = target_vol * 100
        
        # 标出目标收益10%的点
        plt.scatter(target_vol * 100, target_ret * 100, marker='*', s=120, color='red', zorder=5)
        plt.annotate(f'Target 10% (ρ=0.45)\n({target_vol*100:.2f}%, 10.00%)',
                     xy=(target_vol * 100, target_ret * 100),
                     xytext=(target_vol * 100 + 3, target_ret * 100 + 0.8),
                     arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=5))

# 图表格式设置
plt.title('Two-Asset Efficient Frontier (Different Correlations)')
plt.xlabel('Volatility (%)')
plt.ylabel('Return (%)')
plt.xlim(10, 50)
plt.ylim(4, 16)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图表
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 按照输出契约构建结果字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_at_rho45, 2),
    'frontier_vol_at_target': round(frontier_vol_at_target, 2),
    'figure_path': fig_path
}

print(result)
