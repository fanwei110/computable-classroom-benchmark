import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==================== 1. 定义资产参数 ====================
e1 = 0.071    # 资产1期望年收益
e2 = 0.124    # 资产2期望年收益
s1 = 0.163    # 资产1年化波动率
s2 = 0.289    # 资产2年化波动率

rhos = [0.15, 0.45, 0.75]  # 相关系数列表
target_return = 0.10       # 目标期望收益

# ==================== 2. 核心计算函数 ====================
def portfolio_metrics(w, e1, e2, s1, s2, rho):
    """计算给定权重下的投资组合期望收益与波动率"""
    e_p = w * e1 + (1 - w) * e2
    s_p_sq = w**2 * s1**2 + (1 - w)**2 * s2**2 + 2 * w * (1 - w) * rho * s1 * s2
    s_p = np.sqrt(np.maximum(s_p_sq, 0))  # 防止浮点误差导致负数
    return e_p, s_p

def calc_mvp(e1, e2, s1, s2, rho):
    """计算最小方差组合(MVP)的权重、期望收益与波动率"""
    w_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    e_mvp, s_mvp = portfolio_metrics(w_mvp, e1, e2, s1, s2, rho)
    return w_mvp, e_mvp, s_mvp

def calc_target_portfolio(e1, e2, s1, s2, rho, target):
    """计算达到目标收益率的组合权重与最小波动率"""
    w_target = (target - e2) / (e1 - e2)
    e_p, s_p = portfolio_metrics(w_target, e1, e2, s1, s2, rho)
    return w_target, e_p, s_p

# ==================== 3. 绘图与计算 ====================
# 生成权重网格（允许卖空，范围适当放大以展现双曲线全貌）
ws = np.linspace(-1.5, 2.5, 1000)

fig, ax = plt.subplots(figsize=(10, 7))
colors = ['#1f77b4', '#2ca02c', '#d62728']  # 蓝、绿、红

# 存储特定条件的计算结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for i, rho in enumerate(rhos):
    e_ps = []
    s_ps = []
    
    # 计算前沿曲线
    for w in ws:
        e_p, s_p = portfolio_metrics(w, e1, e2, s1, s2, rho)
        e_ps.append(e_p)
        s_ps.append(s_p)
        
    e_ps = np.array(e_ps)
    s_ps = np.array(s_ps)
    
    # 绘制前沿曲线
    ax.plot(s_ps, e_ps, label=f'ρ = {rho:.2f}', color=colors[i], linewidth=2)
    
    # 计算并标记最小方差组合(MVP)
    w_mvp, e_mvp, s_mvp = calc_mvp(e1, e2, s1, s2, rho)
    ax.scatter(s_mvp, e_mvp, marker='o', color=colors[i], s=60, zorder=5)
    ax.annotate(f'MVP (ρ={rho:.2f})\nσ={s_mvp:.2%}', 
                xy=(s_mvp, e_mvp), 
                xytext=(15, -20), 
                textcoords='offset points',
                fontsize=9,
                arrowprops=dict(arrowstyle='->', color=colors[i]))
    
    # 提取 rho = 0.45 时的特定数值
    if rho == 0.45:
        mvp_vol_at_rho45 = s_mvp
        
        _, _, s_target = calc_target_portfolio(e1, e2, s1, s2, rho, target_return)
        frontier_vol_at_target = s_target
        
        # 在图中标记目标收益点
        ax.scatter(s_target, target_return, marker='*', color=colors[i], s=150, zorder=5, edgecolors='k')
        ax.annotate(f'Target 10%\nσ={s_target:.2%}', 
                    xy=(s_target, target_return), 
                    xytext=(20, 10), 
                    textcoords='offset points',
                    fontsize=9,
                    arrowprops=dict(arrowstyle='->', color=colors[i]))

# ==================== 4. 图表美化 ====================
ax.set_xlabel('Volatility (Annualized)', fontsize=12)
ax.set_ylabel('Expected Return (Annualized)', fontsize=12)
ax.set_title('Mean-Variance Frontier of Two Risky Assets', fontsize=14)
ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=1))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=1))
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图片
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 5. 输出结果封装 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 打印结果以便核对
print(result)
