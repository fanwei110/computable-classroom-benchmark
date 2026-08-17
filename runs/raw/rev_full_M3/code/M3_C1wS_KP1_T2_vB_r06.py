import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ==========================================
# 1. 基础参数设定
# ==========================================
mu1 = 0.071      # 资产1期望收益率
mu2 = 0.124      # 资产2期望收益率
vol1 = 0.163     # 资产1波动率
vol2 = 0.289     # 资产2波动率
var1 = vol1 ** 2 # 资产1方差
var2 = vol2 ** 2 # 资产2方差

rhos = [0.15, 0.45, 0.75] # 三种相关系数
target_mu = 0.10          # 目标收益

# ==========================================
# 2. 绘图准备与遍历计算
# ==========================================
fig, ax = plt.subplots(figsize=(10, 7))

# 设置百分比坐标轴格式
pct_formatter = FuncFormatter(lambda y, _: f'{y:.0%}')
ax.xaxis.set_major_formatter(pct_formatter)
ax.yaxis.set_major_formatter(pct_formatter)

# 权重扫描范围：允许一定卖空以展现完整前沿形状
w1_range = np.linspace(-0.5, 1.5, 1000)

# 预先在图例中声明最小方差点的标记
ax.plot([], [], marker='*', color='black', linestyle='None', 
        markersize=12, label='MVP (Minimum Variance Portfolio)')

for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * vol1 * vol2
    cov_matrix = np.array([[var1, cov12], 
                           [cov12, var2]])
    
    # 组合权重矩阵 (2 x N)
    w_mat = np.vstack((w1_range, 1 - w1_range))
    
    # 组合期望收益 (N, )
    mu_arr = w1_range * mu1 + (1 - w1_range) * mu2
    
    # 组合方差与波动率: w'Σw 向量化计算
    var_arr = np.sum(w_mat * (cov_matrix @ w_mat), axis=0)
    vol_arr = np.sqrt(var_arr)
    
    # 绘制前沿曲线
    ax.plot(vol_arr, mu_arr, label=f'ρ = {rho}', linewidth=2)
    
    # 解析法求最小方差组合 (MVP)
    # 对 w'Σw 关于 w1 求导并令其为0，可得 w1_mvp = (var2 - cov12) / (var1 + var2 - 2*cov12)
    w1_mvp = (var2 - cov12) / (var1 + var2 - 2 * cov12)
    w_mvp = np.array([w1_mvp, 1 - w1_mvp])
    
    # MVP的收益与波动率
    mvp_mu = w_mvp @ np.array([mu1, mu2])
    mvp_vol = np.sqrt(w_mvp @ cov_matrix @ w_mvp)
    
    # 在图上标出最小方差点
    ax.scatter(mvp_vol, mvp_mu, marker='*', color='black', s=200, zorder=5)

# ==========================================
# 3. 针对 rho = 0.45 的特定计算
# ==========================================
rho_45 = 0.45
cov12_45 = rho_45 * vol1 * vol2
cov_matrix_45 = np.array([[var1, cov12_45], 
                          [cov12_45, var2]])

# (1) 0.45对应的最小方差组合波动率
w1_mvp_45 = (var2 - cov12_45) / (var1 + var2 - 2 * cov12_45)
w_mvp_45 = np.array([w1_mvp_45, 1 - w1_mvp_45])
mvp_vol_45 = np.sqrt(w_mvp_45 @ cov_matrix_45 @ w_mvp_45)

# (2) 目标收益10%下的最小波动率
# 两资产下，满足目标收益的权重是唯一的：w1 = (mu_target - mu2) / (mu1 - mu2)
w1_target = (target_mu - mu2) / (mu1 - mu2)
w_target = np.array([w1_target, 1 - w1_target])
frontier_vol_at_target = np.sqrt(w_target @ cov_matrix_45 @ w_target)

# ==========================================
# 4. 图形修饰与保存
# ==========================================
ax.set_xlabel('Volatility (Standard Deviation)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Markowitz Mean-Variance Efficient Frontier (Two Assets)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)

# 限制坐标轴范围让有效前沿核心区域更清晰
ax.set_xlim(0.10, 0.40)
ax.set_ylim(0.04, 0.16)

fig.savefig('efficient_frontier.png', dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 结果字典填充
# ==========================================
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': 'efficient_frontier.png'
}

# 供课堂投屏或验证打印
print(f" rho=0.45 最小方差组合波动率: {mvp_vol_45:.4%}")
print(f" rho=0.45 目标收益10%最小波动率: {frontier_vol_at_target:.4%}")
print(f" 图形已保存至: {result['figure_path']}")
