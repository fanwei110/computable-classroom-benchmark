import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 资产参数
mu = np.array([0.071, 0.124])          # 期望收益
sigma = np.array([0.163, 0.289])       # 波动率
correlations = [0.15, 0.45, 0.75]      # 相关系数列表

# 存储结果的字典
result = {}

# 1. 构造协方差矩阵并绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    # 构造协方差矩阵
    cov_matrix = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])

    # 生成权重向量（w1从-1到2，步长0.001，确保覆盖所有可能组合）
    w1 = np.linspace(-1, 2, 1000)
    w2 = 1 - w1
    weights = np.column_stack((w1, w2))

    # 计算组合收益和波动率
    portfolio_returns = weights @ mu
    portfolio_vols = np.sqrt(np.einsum('...i,ij,...j->...', weights, cov_matrix, weights))

    # 绘制有效前沿（只绘制波动率最小的部分）
    valid = (portfolio_returns >= mu[0]) & (portfolio_returns <= mu[1])
    plt.plot(portfolio_vols[valid], portfolio_returns[valid],
             label=f'ρ={rho}', linewidth=1.5)

    # 2. 找到最小方差组合
    def portfolio_variance(w, cov):
        return w @ cov @ w.T

    # 约束：权重之和为1
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = ((None, None), (None, None))  # 允许卖空

    # 初始猜测
    w0 = np.array([0.5, 0.5])

    # 优化
    res = minimize(portfolio_variance, w0, args=(cov_matrix,),
                   constraints=constraints, bounds=bounds)
    w_mvp = res.x
    vol_mvp = np.sqrt(portfolio_variance(w_mvp, cov_matrix))
    ret_mvp = w_mvp @ mu

    # 标记最小方差组合
    plt.scatter(vol_mvp, ret_mvp, color='red', zorder=5)
    plt.text(vol_mvp, ret_mvp, 'MVP', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

    # 存储ρ=0.45时的MVP波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp

# 3. 对ρ=0.45计算目标收益10%时的最小波动率
rho_45 = 0.45
cov_matrix_45 = np.array([
    [sigma[0]**2, rho_45 * sigma[0] * sigma[1]],
    [rho_45 * sigma[0] * sigma[1], sigma[1]**2]
])

# 优化问题：最小化波动率，约束收益=10%，权重之和=1
def portfolio_vol(w, cov):
    return np.sqrt(w @ cov @ w.T)

constraints_target = (
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
    {'type': 'eq', 'fun': lambda w: w @ mu - 0.10}
)
bounds_target = ((None, None), (None, None))

res_target = minimize(portfolio_vol, w0, args=(cov_matrix_45,),
                      constraints=constraints_target, bounds=bounds_target)
vol_target = res_target.fun
result['frontier_vol_at_target'] = vol_target

# 图形设置
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
result['figure_path'] = figure_path

# 显示图形（可选，在课堂演示时可能需要）
plt.show()

# 输出结果
print(result)
