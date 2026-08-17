import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r1, r2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 生成组合权重范围（包含卖空部分）
w = np.linspace(-0.5, 1.5, 500)

plt.figure(figsize=(9, 6))

# 存储最小方差组合点
mvp_points = {}

for rho in rhos:
    # 组合收益与波动率
    ret = w * r1 + (1 - w) * r2
    var = w**2 * sig1**2 + (1 - w)**2 * sig2**2 + 2 * w * (1 - w) * rho * sig1 * sig2
    std = np.sqrt(var)
    plt.plot(std, ret, label=f'ρ = {rho}')
    
    # 最小方差组合权重、收益、波动率
    w_mvp = (sig2**2 - rho * sig1 * sig2) / (sig1**2 + sig2**2 - 2 * rho * sig1 * sig2)
    ret_mvp = w_mvp * r1 + (1 - w_mvp) * r2
    var_mvp = (w_mvp**2 * sig1**2 + (1 - w_mvp)**2 * sig2**2 +
               2 * w_mvp * (1 - w_mvp) * rho * sig1 * sig2)
    std_mvp = np.sqrt(var_mvp)
    mvp_points[rho] = (std_mvp, ret_mvp)
    plt.scatter(std_mvp, ret_mvp, color='red', zorder=5)
    plt.annotate(f'MVP(ρ={rho})', (std_mvp, ret_mvp),
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

# 标出原资产
plt.scatter(sig1, r1, marker='s', color='black', label='Asset 1 (7.1%, 16.3%)')
plt.scatter(sig2, r2, marker='^', color='black', label='Asset 2 (12.4%, 28.9%)')

plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Two-Asset Efficient Frontier')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('frontier.png')
plt.close()

# ---------- 计算要求的数值 ----------
rho45 = 0.45

# 1) ρ=0.45 时最小方差组合的波动率
w_mvp_45 = (sig2**2 - rho45 * sig1 * sig2) / (sig1**2 + sig2**2 - 2 * rho45 * sig1 * sig2)
var_mvp_45 = (w_mvp_45**2 * sig1**2 + (1 - w_mvp_45)**2 * sig2**2 +
              2 * w_mvp_45 * (1 - w_mvp_45) * rho45 * sig1 * sig2)
mvp_vol_at_rho45 = np.sqrt(var_mvp_45)

# 2) 目标收益 10% 时的最小波动率（ρ=0.45）
r_target = 0.10
w_target = (r_target - r2) / (r1 - r2)   # 线性方程直接解出唯一权重
var_target = (w_target**2 * sig1**2 + (1 - w_target)**2 * sig2**2 +
              2 * w_target * (1 - w_target) * rho45 * sig1 * sig2)
frontier_vol_at_target = np.sqrt(var_target)

# 结果字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,        # 约 0.1617 (16.17%)
    'frontier_vol_at_target': frontier_vol_at_target,  # 约 0.2024 (20.24%)
    'figure_path': 'frontier.png'
}

print(result)
