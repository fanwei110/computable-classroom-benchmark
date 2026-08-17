import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    # 资产参数（小数形式）
    r = np.array([0.071, 0.124])          # 期望年收益
    sigma = np.array([0.163, 0.289])      # 年化波动率
    rhos = [0.15, 0.45, 0.75]            # 相关系数
    target_return = 0.10                  # 目标期望收益 10%

    # 存储结果
    mvp_vol_at_rho45 = None
    frontier_vol_at_target = None

    # 准备绘图
    plt.figure(figsize=(10, 6))

    # 对每个相关系数进行扫描和计算
    for rho in rhos:
        # 构造协方差矩阵（仅用于清晰性，实际上直接代入公式）
        cov_12 = rho * sigma[0] * sigma[1]
        
        # 扫描组合权重 w1，允许卖空（满仓 w1 + w2 = 1）
        w1_range = np.linspace(-2.5, 3.5, 2000)
        w2_range = 1.0 - w1_range
        
        # 组合收益
        port_ret = w1_range * r[0] + w2_range * r[1]
        # 组合方差
        port_var = (w1_range**2 * sigma[0]**2 +
                    w2_range**2 * sigma[1]**2 +
                    2 * w1_range * w2_range * cov_12)
        port_std = np.sqrt(port_var)
        
        # 绘制前沿曲线（用百分比显示更直观）
        plt.plot(port_std * 100, port_ret * 100,
                 label=f'ρ = {rho}', linewidth=2)
        
        # ---- 计算并标记最小方差组合（MVP）----
        # 解析解
        w1_mvp = (sigma[1]**2 - cov_12) / (sigma[0]**2 + sigma[1]**2 - 2 * cov_12)
        w2_mvp = 1.0 - w1_mvp
        mvp_ret = w1_mvp * r[0] + w2_mvp * r[1]
        mvp_var = (w1_mvp**2 * sigma[0]**2 +
                   w2_mvp**2 * sigma[1]**2 +
                   2 * w1_mvp * w2_mvp * cov_12)
        mvp_std = np.sqrt(mvp_var)
        
        # 在曲线上标出 MVP（用大号散点）
        plt.scatter(mvp_std * 100, mvp_ret * 100,
                    s=80, zorder=5, marker='o',
                    edgecolors='black', linewidth=0.8,
                    label=f'MVP ρ={rho}' if rho == rhos[0] else "")
        
        # 如果当前是目标相关系数 0.45，则记录结果
        if rho == 0.45:
            mvp_vol_at_rho45 = mvp_std  # 小数形式
            # 目标收益 10% 的波动率（唯一可行组合）
            w1_target = (target_return - r[1]) / (r[0] - r[1])
            w2_target = 1.0 - w1_target
            target_var = (w1_target**2 * sigma[0]**2 +
                          w2_target**2 * sigma[1]**2 +
                          2 * w1_target * w2_target * cov_12)
            frontier_vol_at_target = np.sqrt(target_var)

    # 图形标注与美化
    plt.xlabel('Annualized Volatility (%)')
    plt.ylabel('Expected Annual Return (%)')
    plt.title('Mean-Variance Frontiers for Different Correlations')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # 保存图形
    figure_filename = 'mean_variance_frontier.png'
    figure_path = os.path.abspath(figure_filename)
    plt.savefig(figure_path, dpi=150)
    plt.show()
    plt.close()

    # 按要求的键名填写 result 字典
    result = {
        'mvp_vol_at_rho45': mvp_vol_at_rho45,
        'frontier_vol_at_target': frontier_vol_at_target,
        'figure_path': figure_path
    }

    # 输出到控制台，方便教师查看
    print("=== 计算结果 ===")
    print(f"相关系数 0.45 下最小方差组合的年化波动率: {mvp_vol_at_rho45:.6f} ({mvp_vol_at_rho45*100:.4f}%)")
    print(f"目标收益 10% 下可达到的最小年化波动率: {frontier_vol_at_target:.6f} ({frontier_vol_at_target*100:.4f}%)")
    print(f"图形保存路径: {figure_path}")
    print("result =", result)

    return result

if __name__ == "__main__":
    result = main()
