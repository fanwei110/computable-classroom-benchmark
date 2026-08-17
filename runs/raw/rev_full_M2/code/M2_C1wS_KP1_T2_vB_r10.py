import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 给定参数
asset_returns = np.array([0.071, 0.124])   # 两资产收益率
asset_vols    = np.array([0.163, 0.289])   # 两资产波动率
correlations  = [0.15, 0.45, 0.75]         # 三种相关系数
target_return = 0.10                       # 目标收益率 10%
risk_free     = None                       # 无风险利率未指定，仅画有效前沿

# 组合约束：满仓(权重之和=1)，允许卖空？通常马科维茨基础模型不允许卖空更有教学意义。
# 这里假设不允许卖空: 0 <= w_i <= 1，这样有效前沿更真实，且最小方差组合有封闭解但用优化更稳健。
# 同时为了展示理论形状，也保留卖空情况？题目没有说明，通常教学中最简单情形允许卖空能画出完整双曲线。
# 但"满仓约束下使其最小"仅指 sum(w)=1。根据常见《证券投资学》课堂演示，先使用允许卖空(无边界)画理论有效前沿。
# 然而为了包含更实际情形，我选择画出两种：但题目只要求画三条相关系数的有效前沿。我使用无边界约束以呈现完整抛物线。
# 注意：若不允许卖空，有效前沿可能截断，但教学通常展示完整曲线。采用权重无限制，仅需满足 sum(w)=1。

# 扫描权重范围足够宽，以完整覆盖曲线
w1_range = np.linspace(-0.5, 1.5, 500)  # 卖空允许，足够覆盖
w2_range = 1 - w1_range

# 准备绘图
fig, ax = plt.subplots(figsize=(10, 7))
colors = ['blue', 'green', 'red']   # 对应三条相关系数
mvp_points = []  # 存储最小方差组合 (vol, ret, rho)

# 存储结果
result = {}

# =========================================
# 1. 构造协方差矩阵并计算组合收益/方差
# =========================================
for idx, rho in enumerate(correlations):
    # 协方差矩阵
    cov12 = rho * asset_vols[0] * asset_vols[1]
    cov_matrix = np.array([[asset_vols[0]**2, cov12],
                           [cov12, asset_vols[1]**2]])
    
    # 组合权重向量 (w1, w2)
    weights = np.column_stack((w1_range, w2_range))
    # 组合收益
    port_return = weights @ asset_returns
    # 组合方差: w'Σw
    port_var = np.sum(weights * (weights @ cov_matrix), axis=1)
    port_vol = np.sqrt(port_var)
    
    # 画有效前沿：由于是两资产且允许卖空，所有点构成双曲线。有效前沿是上方部分(收益大于MVP收益的曲线)
    # 通常我们只画有效前沿部分，但为了完整展示，画整个可行集然后突出有效前沿。
    # 题目要求"画有效前沿"，我将画出全局最小方差以上的部分，并在图上标出最小方差点。
    # 先找到最小方差组合 (通过解析或扫描)
    min_var_idx = np.argmin(port_var)
    mvp_vol = port_vol[min_var_idx]
    mvp_ret = port_return[min_var_idx]
    mvp_points.append((mvp_vol, mvp_ret, rho))
    
    # 分离有效前沿：收益 >= MVP收益 的部分
    valid_idx = port_return >= mvp_ret
    ef_vol = port_vol[valid_idx]
    ef_ret = port_return[valid_idx]
    # 按波动率排序以便画线
    sort_idx = np.argsort(ef_vol)
    ef_vol_sorted = ef_vol[sort_idx]
    ef_ret_sorted = ef_ret[sort_idx]
    
    # 绘制有效前沿
    ax.plot(ef_vol_sorted, ef_ret_sorted, color=colors[idx], linewidth=2,
            label=f'ρ = {rho}')
    
    # 标记最小方差组合点
    ax.scatter(mvp_vol, mvp_ret, color=colors[idx], marker='*', s=150,
               edgecolors='black', zorder=5)
    
    # 如果需要计算 0.45 时的特定值
    if rho == 0.45:
        # 存储 MVP 波动率
        result['mvp_vol_at_rho45'] = round(mvp_vol, 6)
        
        # 目标收益 10% 对应的最小波动率 (即有效前沿上收益=10%的点)
        # 由于有效前沿是上方部分，若 target_return >= mvp_ret，则存在唯一解。
        if target_return >= mvp_ret:
            # 在有效前沿点中寻找最接近目标收益的点，或者直接解析计算
            # 解析法：对于两资产，给定组合收益 r_p = w1*r1 + w2*r2, w1+w2=1
            # w1 = (r_p - r2)/(r1 - r2), w2 = 1 - w1
            w1_target = (target_return - asset_returns[1]) / (asset_returns[0] - asset_returns[1])
            w2_target = 1 - w1_target
            w_target = np.array([w1_target, w2_target])
            target_var = w_target @ cov_matrix @ w_target
            target_vol = np.sqrt(target_var)
            result['frontier_vol_at_target'] = round(target_vol, 6)
        else:
            # 如果目标收益低于MVP收益，理论上最小方差组合是下边界，但有效前沿要求收益>=MVP，此时无解或者取MVP。
            # 根据题目语境目标10%通常高于MVP收益，经检查确实高于。
            # 保底设置
            target_vol = mvp_vol
            result['frontier_vol_at_target'] = round(target_vol, 6)

# 进一步装饰图形
ax.set_xlabel('Portfolio Volatility (Standard Deviation)', fontsize=12)
ax.set_ylabel('Portfolio Expected Return', fontsize=12)
ax.set_title('Mean-Variance Efficient Frontier for Two Risky Assets', fontsize=14)
ax.legend(loc='lower right')
ax.grid(True, linestyle='--', alpha=0.7)

# 添加最小方差组合的额外标注（针对0.45的情况）
# 从result提取并显示在图上（可选）
mvp_vol_045 = result['mvp_vol_at_rho45']
front_vol_target = result['frontier_vol_at_target']
# 在图上添加文本注释
ax.annotate(f'ρ=0.45 MVP vol: {mvp_vol_045:.4f}\nVol at 10% return: {front_vol_target:.4f}',
            xy=(0.05, 0.15), xycoords='axes fraction', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5))

# 保存图形
figure_filename = 'efficient_frontier.png'
fig.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close(fig)  # 释放内存

result['figure_path'] = figure_filename

# 打印结果供检查
print("Result dictionary:")
for key, value in result.items():
    print(f"  {key}: {value}")

# ==========================================
# 最终：result 字典已包含所有要求输出
# ==========================================
