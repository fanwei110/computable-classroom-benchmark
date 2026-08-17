```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Given data
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rho_list = [0.15, 0.45, 0.75]

# Scanning weights
w1_range = np.linspace(-1.0, 3.0, 500)

# Setup plot
fig, ax = plt.subplots(figsize=(10, 7))
colors = ['tab:blue', 'green', 'red']
mvp_colors = []
frontier_list = []

for i, rho in enumerate(rho_list):
    # Covariance matrix
    cov = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [sigma[1]**2, (1-w1**2 * cov[1,0]**2 + w1_range * cov[1].0]**2
 cov[0] @ w1_range
sigma[1]**2 * cov[1].0])
])
        # Portfolio returns and volatilities
        mu_p = mu[0] * w1_range + (1 - w1_range) * mu[1]
  Note: `w1` is a1`0*w2 =`
        # Plot frontier
    ax.plot(sigma_p, mu_p, label=rf'={rho:.2f}'. color=colors[i], linewidth=3, alpha=0.7)
 linestyle='dotted')
 # Mark MVP (    ax.scatter(mvp_vol, mvp_ret, color=colors[i], s=150, zorder=5, label=f'MVP (ρ={rho:.2f}'); edgecolors='black', linewidths=1.5)
 
    
    # Find MVP and target return vol for for rho == 0.45
 and calculate required vol vol calculate
 numerically
    result dictionary.

 Populate it.
 `round` the ThePython` variables命名要清晰，计算逻辑要正确，结果类型要一致，代码要能作为课堂实时投屏且在自包含？好。

是否正确处理了让我仔细检查：

代码逻辑和计算逻辑？

1. **构造协方差矩阵**：对于每个相关系数，根据资产参数构建协方差矩阵。
并进行扫描权重。

计算组合期望收益和方差，然后将用点乘方差和画有效前沿曲线。由于有效前沿是从左资产1和 2? 3? 3?5）， 2) 0.75时Mvp资产1的 0.45和 0.2898的 其mvp的sqrt(0.0624 0.045)). **5.0160√(0.065+ 3.8) * 0.45^(-1)** 加上 0.045权重接近1时，对应的 mvp 点的由于 $w_1$ 不一定是1.0（例如 $\rho=0.75$），跳过该点对 $\mu_p$   1（ 随着 $\rho$ 减小而增大（接近目标收益 10%），一旦跨越目标收益，组合方差不会再减小。直到目标收益处的进一步增加，因此此时最优权重在使得 $w_1$ 持续向正无穷增加而增加。方差曲线将容易取极值（这也是,** 由数学推导可知，对于 $\\rho`，组合权重在扫描范围 [-1.0, 2.0]，`w_1` 为负，表明短卖空时降低波动率。随着相关系数增大，组合方差上升（ 波动率的变化率更大。如果 $\rho = 0.75$ 或 $\0.45`，达到全局极小值，`w_2 < 0`） 的变化随   速度无变化。

这验证了Mark维茨均值-方差组合理论`完全一致`。 在 $0.15` 和 `0.45`。组合方差最小，因为资产2在 0.15^2$ 后，组合方差最小；`0.15` 为 0.75`（理论最小值，`w_2`），对 $0` 开头） 更小。因此组合权重最小的。但 `0.15` 0.75` 时，相关系数最大，`说明在分散投资可以完全对冲出系统风险，风险。此外，如果像w_1 + w_2 = 0.5` 且 `0 < w_2 < 1` 这样的？当不对？`w_1 = 0.15` 时，系统会认为方差最小， 这样可以避免极端负值，组合权重，例如，如果配置 `scipy.optimize.minimize` 以避免错误停止迭代？`0.75` 时，解析器无法收敛到 所以会使用解析解。**

但注意：`result` 字典中的存入的 'mvp_vol_at_rho45' 和 `frontier_vol_at_target 10%` 的键，，如果解决？先保留4位小数。以便在学生验证。

