import numpy as np
import matplotlib.pyplot as plt

def main():
    # 资产参数
    r = np.array([0.071, 0.124])          # 期望年化收益
    s = np.array([0.163, 0.289])          # 年化波动率
    var1, var2 = s[0]**2, s[1]**2         # 方差
    rhos = [0.15, 0.45, 0.75]            # 相关系数
    colors = ['steelblue', 'darkgreen', 'crimson']
    
    # ------ 计算 rho=0.45 时所需的两个结果 ------
    rho_target = 0.45
    cov12_target = rho_target * s[0] * s[1]
    
    # 最小方差组合 (MVP)
    w1_mvp = (var2 - cov12_target) / (var1 + var2 - 2*cov12_target)
    w2_mvp = 1.0 - w1_mvp
    var_mvp = (w1_mvp**2 * var1 + w2_mvp**2 * var2 + 2 * w1_mvp * w2_mvp * cov12_target)
    mvp_vol_at_rho45 = np.sqrt(var_mvp)
    
    # 目标收益 10% 下的组合 (满仓、允许卖空，唯一解)
    mu_target = 0.10
    w1_target = (mu_target - r[1]) / (r[0] - r[1])
    w2_target = 1.0 - w1_target
    var_target = (w1_target**2 * var1 + w2_target**2 * var2 +
                  2 * w1_target * w2_target * cov12_target)
    frontier_vol_at_target = np.sqrt(var_target)
    
    # ------ 绘制均值-方差前沿 ------
    fig, ax = plt.subplots(figsize=(9, 6))
    w_range = np.linspace(-1.5, 2.5, 2000)   # 足够展示卖空情况
    
    for i, rho in enumerate(rhos):
        cov12 = rho * s[0] * s[1]
        # 组合权重
        w1 = w_range
        w2 = 1.0 - w1
        
        # 组合收益与方差
        mu_p = w1 * r[0] + w2 * r[1]
        var_p = (w1**2 * var1 + w2**2 * var2 + 2 * w1 * w2 * cov12)
        var_p = np.maximum(var_p, 0)          # 防止数值误差产生极小负数
        sigma_p = np.sqrt(var_p)
        
        ax.plot(sigma_p * 100, mu_p * 100, color=colors[i],
                label=f'ρ = {rho}', linewidth=1.8)
        
        # 该相关系数下的最小方差组合
        w1_mvp_i = (var2 - cov12) / (var1 + var2 - 2*cov12)
        w2_mvp_i = 1.0 - w1_mvp_i
        mu_mvp_i = w1_mvp_i * r[0] + w2_mvp_i * r[1]
        var_mvp_i = (w1_mvp_i**2 * var1 + w2_mvp_i**2 * var2 +
                     2 * w1_mvp_i * w2_mvp_i * cov12)
        sigma_mvp_i = np.sqrt(var_mvp_i)
        
        ax.scatter(sigma_mvp_i * 100, mu_mvp_i * 100,
                   color=colors[i], marker='*', s=180, zorder=5)
    
    # 为图例添加统一的 MVP 标记
    ax.scatter([], [], color='black', marker='*', s=100, label='MVP')
    
    # 标出 rho=0.45 时 10% 目标收益的组合
    ax.scatter(frontier_vol_at_target * 100, mu_target * 100,
               color='darkgreen', marker='o', s=100, zorder=5,
               label='Target 10% (ρ=0.45)')
    
    # 图面装饰
    ax.set_xlabel('Annualized Volatility (%)', fontsize=12)
    ax.set_ylabel('Expected Annual Return (%)', fontsize=12)
    ax.set_title('Mean‑Variance Frontier: Two Risky Assets', fontsize=14)
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    figure_path = 'frontier.png'
    plt.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------ 组织输出结果 ------
    result = {
        'mvp_vol_at_rho45': mvp_vol_at_rho45,
        'frontier_vol_at_target': frontier_vol_at_target,
        'figure_path': figure_path
    }
    
    # 实时投屏时便于查看
    print("=" * 55)
    print("Results for ρ = 0.45")
    print("Minimum Variance Portfolio volatility: {:.4f} ({:.2f}%)".format(
        mvp_vol_at_rho45, mvp_vol_at_rho45 * 100))
    print("Frontier vol at target return 10%:    {:.4f} ({:.2f}%)".format(
        frontier_vol_at_target, frontier_vol_at_target * 100))
    print("=" * 55)
    
    return result


if __name__ == '__main__':
    result = main()
