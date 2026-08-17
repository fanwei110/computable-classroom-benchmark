import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数定义
# ==========================================
# 资产1的期望收益与波动率
e1 = 0.071
s1 = 0.163

# 资产2的期望收益与波动率
e2 = 0.124
s2 = 0.289

# 给定的三种相关系数
rhos = [0.15, 0.45, 0.75]

# 目标期望收益
target_ret = 0.10

# ==========================================
# 2. 核心计算函数
# ==========================================
def get_mvp_weight(s1, s2, rho):
    """
    计算最小方差组合(MVP)中资产1的权重。
    推导：对组合方差求一阶导数并令其为0。
    """
    numerator = s2**2 - rho * s1 * s2
    denominator = s1**2 + s2**2 - 2 * rho * s1 * s2
    return numerator / denominator

def get_portfolio_metrics(w1, e1, e2, s1, s2, rho):
    """
    根据资产1的权重，计算组合的期望收益与波动率。
    允许卖空（w1可为负），满仓（w2 = 1 - w1）。
    """
    ret = w1 * e1 + (1 - w1) * e2
    var = (w1**2) * (s1**2) + ((1 - w1)**2) * (s2**2) + 2 * w1 * (1 - w1) * rho * s1 * s2
    vol = np.sqrt(var)
    return ret, vol

# ==========================================
# 3. 针对 rho=0.45 的特定计算与报告
# ==========================================
rho_45 = 0.45

# 计算 rho=0.45 时的最小方差组合
w1_mvp_45 = get_mvp_weight(s1, s2, rho_45)
_, mvp_vol_45 = get_portfolio_metrics(w1_mvp_45, e1, e2, s1, s2, rho_45)

# 计算目标期望收益 10% 下的权重与可达到的最小波动率
# 两资产满仓条件下，同一期望收益仅对应唯一权重组合，因此该组合的波动率即为可达最小波动率
w1_target_45 = (target_ret - e2) / (e1 - e2)
_, target_vol_45 = get_portfolio_metrics(w1_target_45, e1, e2, s1, s2, rho_45)

# ==========================================
# 4. 绘制均值-方差前沿图
# ==========================================
fig, ax = plt.subplots(figsize=(10, 7))

# 设定权重范围，涵盖无卖空到允许卖空的区域
w1_range = np.linspace(-0.5, 2.5, 1000)

colors = ['blue', 'orange', 'green']

for i, rho in enumerate(rhos):
    # 计算当前相关系数下的最小方差组合
    w1_mvp = get_mvp_weight(s1, s2, rho)
    ret_mvp, vol_mvp = get_portfolio_metrics(w1_mvp, e1, e2, s1, s2, rho)
    
    # 生成整条前沿曲线的收益与波动率
    rets = w1_range * e1 + (1 - w1_range) * e2
    vols = np.sqrt(w1_range**2 * s1**2 + (1 - w1_range)**2 * s2**2 + 2 * w1_range * (1 - w1_range) * rho * s1 * s2)
    
    # 绘制前沿曲线
    ax.plot(vols, rets, color=colors[i], label=f'Frontier ($\\rho = {rho:.2f}$)', linewidth=2)
    
    # 绘制最小方差组合点并标出
    ax.scatter(vol_mvp, ret_mvp, marker='*', s=250, color=colors[i], zorder=5, edgecolor='black', linewidth=0.5)
    ax.text(vol_mvp + 0.005, ret_mvp - 0.005, f'MVP ($\\rho={rho:.2f}$)\nVol={vol_mvp:.2%}', 
            fontsize=9, color=colors[i], verticalalignment='top')

# 图表装饰
ax.set_xlabel('Annualized Volatility', fontsize=12)
ax.set_ylabel('Expected Annual Return', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Two Risky Assets', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)

# 限制坐标轴范围，使视觉集中在核心区域
ax.set_xlim(0.10, 0.55)
ax.set_ylim(-0.05, 0.25)

# 保存图表
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 结果封装输出
# ==========================================
result = {
    'mvp_vol_at_rho45': float(mvp_vol_45),
    'frontier_vol_at_target': float(target_vol_45),
    'figure_path': figure_path
}

# 打印验证（可选）
if __name__ == '__main__':
    print(f"最小方差组合年化波动率 (rho=0.45): {result['mvp_vol_at_rho45']:.4%}")
    print(f"目标10%收益下的最小年化波动率 (rho=0.45): {result['frontier_vol_at_target']:.4%}")
    print(f"图表已保存至: {result['figure_path']}")
