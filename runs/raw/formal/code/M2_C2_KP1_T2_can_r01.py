import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 给定的资产参数
mu = np.array([0.071, 0.124])  # 期望年收益
sigma = np.array([0.163, 0.289])  # 年化波动率
correlations = [0.15, 0.45, 0.75]  # 相关系数列表

# 创建结果字典
result = {}

def portfolio_stats(w, mu, cov):
    """计算组合的期望收益和波动率"""
    port_return = np.dot(w, mu)
    port_vol = np.sqrt(np.dot(w.T, np.dot(cov, w)))
    return port_return, port_vol

def min_variance_portfolio(mu, cov):
    """计算最小方差组合（允许卖空，满仓约束）"""
    n = len(mu)
    # 满仓约束: sum(w) = 1
    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    
    # 初始猜测
    w0 = np.ones(n) / n
    
    # 目标函数：最小化组合方差
    def objective(w):
        return np.dot(w.T, np.dot(cov, w))
    
    # 优化
    result = minimize(objective, w0, method='SLSQP', constraints=cons,
                     bounds=None, options={'disp': False})
    
    return result.x

def efficient_frontier(mu, cov, num_points=200):
    """生成有效前沿的权重和统计量"""
    n = len(mu)
    mvp_w = min_variance_portfolio(mu, cov)
    mvp_return, mvp_vol = portfolio_stats(mvp_w, mu, cov)
    
    # 扫描目标收益范围（包含最小方差组合的收益）
    target_returns = np.linspace(mu.min() - 0.05, mu.max() + 0.05, num_points)
    frontier_vols = []
    frontier_rets = []
    frontier_weights = []
    
    cons_base = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    
    for target_return in target_returns:
        # 目标收益约束
        cons = cons_base + ({'type': 'eq', 'fun': lambda w, r=target_return: 
                            np.dot(w, mu) - r},)
        
        # 目标函数：最小化组合方差
        def objective(w):
            return np.dot(w.T, np.dot(cov, w))
        
        # 初始猜测
        w0 = np.ones(n) / n
        
        # 优化
        opt_result = minimize(objective, w0, method='SLSQP', constraints=cons,
                             bounds=None, options={'disp': False})
        
        if opt_result.success:
            port_return, port_vol = portfolio_stats(opt_result.x, mu, cov)
            frontier_vols.append(port_vol)
            frontier_rets.append(port_return)
            frontier_weights.append(opt_result.x)
    
    return np.array(frontier_rets), np.array(frontier_vols), np.array(frontier_weights), mvp_w, mvp_return, mvp_vol

def target_return_portfolio(mu, cov, target_return):
    """计算给定目标收益下的最小方差组合"""
    n = len(mu)
    
    # 约束：满仓和目标收益
    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: np.dot(w, mu) - target_return})
    
    # 目标函数：最小化方差
    def objective(w):
        return np.dot(w.T, np.dot(cov, w))
    
    # 初始猜测
    w0 = np.ones(n) / n
    
    # 优化
    opt_result = minimize(objective, w0, method='SLSQP', constraints=cons,
                         bounds=None, options={'disp': False})
    
    if opt_result.success:
        _, port_vol = portfolio_stats(opt_result.x, mu, cov)
        return port_vol
    else:
        return None

# 创建图形
fig, ax = plt.subplots(figsize=(12, 8))

# 存储每种相关系数的最小方差组合信息
mvp_info = {}

# 对每个相关系数进行分析
for rho in correlations:
    # 构造协方差矩阵
    cov_matrix = np.array([[sigma[0]**2, rho * sigma[0] * sigma[1]],
                          [rho * sigma[0] * sigma[1], sigma[1]**2]])
    
    # 生成有效前沿
    frontier_rets, frontier_vols, frontier_weights, mvp_w, mvp_return, mvp_vol = \
        efficient_frontier(mu, cov_matrix)
    
    # 存储最小方差组合信息
    mvp_info[rho] = {'weights': mvp_w, 'return': mvp_return, 'vol': mvp_vol}
    
    # 绘制有效前沿
    ax.plot(frontier_vols, frontier_rets, linewidth=2, 
            label=f'相关系数 ρ = {rho}', alpha=0.8)
    
    # 标记最小方差组合
    ax.scatter(mvp_vol, mvp_return, s=100, marker='*', 
              edgecolors='black', linewidth=1.5, zorder=10)
    
    # 添加最小方差组合注释
    ax.annotate(f'ρ={rho}\n({mvp_vol:.3f}, {mvp_return:.3f})', 
               xy=(mvp_vol, mvp_return), xytext=(10, 10),
               textcoords='offset points', fontsize=8,
               bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7))

# 标注散点资产
for i in range(len(mu)):
    ax.scatter(sigma[i], mu[i], s=150, marker='^', 
              edgecolors='black', linewidth=1.5, zorder=10)
    ax.annotate(f'资产{i+1}\n({sigma[i]:.3f}, {mu[i]:.3f})', 
               xy=(sigma[i], mu[i]), xytext=(15, 15),
               textcoords='offset points', fontsize=9,
               bbox=dict(boxstyle='round,pad=0.3', fc='lightblue', alpha=0.7))

# 计算ρ=0.45时的特定指标
cov_045 = np.array([[sigma[0]**2, 0.45 * sigma[0] * sigma[1]],
                   [0.45 * sigma[0] * sigma[1], sigma[1]**2]])

# 最小方差组合的波动率
mvp_w_045 = mvp_info[0.45]['weights']
mvp_vol_045 = mvp_info[0.45]['vol']

# 目标期望收益10%下的最小波动率
target_return = 0.10
target_vol_045 = target_return_portfolio(mu, cov_045, target_return)

# 在图上标记目标收益点
if target_vol_045:
    ax.scatter(target_vol_045, target_return, s=150, marker='D', 
              edgecolors='black', linewidth=2, zorder=10, color='red')
    ax.annotate(f'目标收益{target_return:.1%}\n波动率={target_vol_045:.4f}', 
               xy=(target_vol_045, target_return), xytext=(20, -20),
               textcoords='offset points', fontsize=9,
               bbox=dict(boxstyle='round,pad=0.3', fc='lightcoral', alpha=0.7))

# 设置图形属性
ax.set_xlabel('年化波动率 (标准差)', fontsize=12)
ax.set_ylabel('期望年化收益', fontsize=12)
ax.set_title('马科维茨均值-方差前沿 (不同相关系数)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='best', fontsize=10)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0.05)

# 添加注释
ax.text(0.02, 0.98, '★ = 最小方差组合\n▲ = 单个资产\n◆ = 目标收益10%', 
        transform=ax.transAxes, fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))

# 保存图形
figure_path = 'markowitz_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.show()

# 存储结果
result['mvp_vol_at_rho45'] = mvp_vol_045
result['frontier_vol_at_target'] = target_vol_045
result['figure_path'] = figure_path

# 打印结果
print(f"相关系数 0.45 时的最小方差组合年化波动率: {mvp_vol_045:.4f} ({mvp_vol_045:.2%})")
print(f"目标期望收益 10% 下可达到的最小年化波动率: {target_vol_045:.4f} ({target_vol_045:.2%})")
print(f"\n最小方差组合详细信息 (ρ=0.45):")
print(f"  权重: 资产1 = {mvp_w_045[0]:.4f}, 资产2 = {mvp_w_045[1]:.4f}")
print(f"  期望收益: {mvp_info[0.45]['return']:.4f}")
print(f"  波动率: {mvp_info[0.45]['vol']:.4f}")

print(f"\n结果字典:")
for key, value in result.items():
    print(f"  {key}: {value}")

# 验证结果不为None
assert result['mvp_vol_at_rho45'] is not None, "MVP volatility calculation failed"
assert result['frontier_vol_at_target'] is not None, "Target return volatility calculation failed"
assert result['figure_path'] is not None, "Figure path is None"

print("\n✓ 所有计算完成，结果已保存到 result 字典")
