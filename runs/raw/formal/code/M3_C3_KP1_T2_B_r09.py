import numpy as np
import matplotlib.pyplot as plt

# --- 1. 参数设定 ---
r1, r2 = 0.071, 0.124
s1, s2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# --- 2. 绘图准备 ---
plt.figure(figsize=(10, 7))

# 权重扫描范围 (包含卖空情况以展示完整的双曲线)
w1_arr = np.linspace(-0.5, 1.5, 1000)
w2_arr = 1 - w1_arr
ret_arr = w1_arr * r1 + w2_arr * r2

for rho in rhos:
    # 计算组合波动率
    var_arr = (w1_arr**2 * s1**2 + w2_arr**2 * s2**2 + 2 * w1_arr * w2_arr * rho * s1 * s2)
    vol_arr = np.sqrt(var_arr)
    
    # 计算最小方差点 (MVP)
    w1_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    w2_mvp = 1 - w1_mvp
    r_mvp = w1_mvp * r1 + w2_mvp * r2
    var_mvp = (w1_mvp**2 * s1**2 + w2_mvp**2 * s2**2 + 2 * w1_mvp * w2_mvp * rho * s1 * s2)
    s_mvp = np.sqrt(var_mvp)
    
    # 绘制无效前沿(下半支，虚线)与有效前沿(上半支，实线)
    ineff_mask = ret_arr < r_mvp
    eff_mask = ret_arr >= r_mvp
    plt.plot(vol_arr[ineff_mask], ret_arr[ineff_mask], linestyle='--', alpha=0.4, color='gray')
    plt.plot(vol_arr[eff_mask], ret_arr[eff_mask], label=f'Efficient Frontier (ρ={rho:.2f})', linewidth=2)
    
    # 标出最小方差点
    plt.scatter(s_mvp, r_mvp, marker='o', s=60, zorder=5, edgecolor='black', facecolor='red')
    plt.annotate(f'MVP (ρ={rho:.2f})\nσ={s_mvp:.2%}, r={r_mvp:.2%}',
                 xy=(s_mvp, r_mvp), xytext=(s_mvp + 0.02, r_mvp - 0.008),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                 fontsize=9)

# 添加目标收益参考线
plt.axhline(y=target_return, color='blue', linestyle=':', label='Target Return = 10%')

plt.title('Two-Asset Efficient Frontier (Varying Correlations)')
plt.xlabel('Portfolio Volatility (σ)')
plt.ylabel('Portfolio Expected Return (r)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.50)
plt.ylim(0.0, 0.20)

# 保存图像
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# --- 3. 题目要求的数值计算 ---

# (1) rho = 0.45 时的最小方差组合波动率
rho_45 = 0.45
w1_mvp_45 = (s2**2 - rho_45 * s1 * s2) / (s1**2 + s2**2 - 2 * rho_45 * s1 * s2)
w2_mvp_45 = 1 - w1_mvp_45
var_mvp_45 = (w1_mvp_45**2 * s1**2 + w2_mvp_45**2 * s2**2 + 2 * w1_mvp_45 * w2_mvp_45 * rho_45 * s1 * s2)
mvp_vol_at_rho45 = np.sqrt(var_mvp_45)

# (2) rho = 0.45 且目标收益为 10% 时的最小波动率
w1_target = (target_return - r2) / (r1 - r2)
w2_target = 1 - w1_target
var_target_45 = (w1_target**2 * s1**2 + w2_target**2 * s2**2 + 2 * w1_target * w2_target * rho_45 * s1 * s2)
frontier_vol_at_target = np.sqrt(var_target_45)

# --- 4. 按照输出契约封装结果 ---
result = {
    'mvp_vol_at_rho45': float(mvp_vol_at_rho45),
    'frontier_vol_at_target': float(frontier_vol_at_target),
    'figure_path': fig_path
}

print(result)
