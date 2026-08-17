import numpy as np
import matplotlib
matplotlib.use('Agg')   # 在无图形显示的环境中安全运行
import matplotlib.pyplot as plt

def main():
    # ---------- 给定的资产数据 ----------
    mu = np.array([0.071, 0.124])          # 年化期望收益
    sigma = np.array([0.163, 0.289])       # 年化波动率
    rhos = [0.15, 0.45, 0.75]              # 需要考察的相关系数

    # ---------- 扫描组合权重（满仓，允许卖空） ----------
    w1 = np.linspace(-1.5, 2.5, 4000)      # 资产1的权重扫描范围
    w2 = 1.0 - w1                          # 满仓约束
    weights = np.column_stack((w1, w2))    # 形状 (N, 2)

    # ---------- 准备绘图 ----------
    plt.figure(figsize=(8, 6))

    # 预先声明结果字典
    result = {}

    # ---------- 对每个相关系数画前沿 ----------
    for rho in rhos:
        # 构造协方差矩阵
        cov12 = rho * sigma[0] * sigma[1]
        cov_mat = np.array([[sigma[0]**2, cov12],
                            [cov12,        sigma[1]**2]])

        # 组合收益与风险
        port_mu = weights @ mu
        port_var = np.sum(weights * (weights @ cov_mat), axis=1)  # 组合方差
        port_vol = np.sqrt(port_var)                              # 标准差

        # 画出整条曲线（所有扫描点连成的边界）
        plt.plot(port_vol, port_mu, label=f'$\\rho$ = {rho}')

        # 在曲线上标出最小方差组合（MVP）
        mvp_idx = np.argmin(port_var)
        plt.scatter(port_vol[mvp_idx], port_mu[mvp_idx],
                    s=60, zorder=5, edgecolors='black')

        # ---------- 对 ρ = 0.45 进行精确计算 ----------
        if rho == 0.45:
            # ---- MVP 解析解 ----
            s1, s2 = sigma[0], sigma[1]
            r = rho
            num_mvp = s2**2 - r * s1 * s2
            den_mvp = s1**2 + s2**2 - 2 * r * s1 * s2
            w1_mvp = num_mvp / den_mvp
            w_mvp = np.array([w1_mvp, 1.0 - w1_mvp])
            var_mvp = w_mvp @ cov_mat @ w_mvp
            result['mvp_vol_at_rho45'] = float(np.sqrt(var_mvp))

            # ---- 目标期望收益 10% 的最小波动率 ----
            mu_target = 0.10
            w1_target = (mu_target - mu[1]) / (mu[0] - mu[1])
            w_target = np.array([w1_target, 1.0 - w1_target])
            var_target = w_target @ cov_mat @ w_target
            vol_target = float(np.sqrt(var_target))
            result['frontier_vol_at_target'] = vol_target

            # 在图上高亮目标点
            plt.scatter(vol_target, mu_target, marker='*', s=150,
                        color='red', zorder=6, label='Target return 10%')

    # ---------- 图形修饰与保存 ----------
    plt.xlabel('Annualized Volatility')
    plt.ylabel('Expected Annual Return')
    plt.title('Mean–Variance Frontier with Different Correlations')
    plt.legend()
    plt.grid(True, alpha=0.3)

    fig_path = 'frontier.png'
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()

    result['figure_path'] = fig_path

    # 输出所有要求的结果
    print(result)

if __name__ == '__main__':
    main()
