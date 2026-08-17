import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. 资产参数
# ------------------------------
mu = np.array([0.071, 0.124])          # 年化期望收益
sigma = np.array([0.163, 0.289])       # 年化波动率

# 相关系数列表
rho_list = [0.15, 0.45, 0.75]
colors = ['blue', 'red', 'green']      # 对应三个相关系数

# 扫描权重的范围 (允许卖空，覆盖足够区域)
w1 = np.linspace(-1.0, 2.0, 5000)
w2 = 1.0 - w1

# ------------------------------
# 2. 准备绘图
# ------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# 用于存储计算的数值结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# ------------------------------
# 3. 对每个相关系数计算并绘制有效前沿
# ------------------------------
for rho, color in zip(rho_list, colors):
    # 协方差矩阵元素
    cov12 = rho * sigma[0] * sigma[1]
    # 组合方差 (向量化计算)
    var = (w1**2) * (sigma[0]**2) + (w2**2) * (sigma[1]**2) + 2 * w1 * w2 * cov12
    vol = np.sqrt(var)
    ret = w1 * mu[0] + w2 * mu[1]

    # --- 解析计算最小方差组合 (MVP) ---
    # 权重公式 (满仓约束，允许卖空)
    denom = sigma[0]**2 + sigma[1]**2 - 2 * rho * sigma[0] * sigma[1]
    w1_mvp = (sigma[1]**2 - rho * sigma[0] * sigma[1]) / denom
    w2_mvp = 1.0 - w1_mvp
    ret_mvp = w1_mvp * mu[0] + w2_mvp * mu[1]
    vol_mvp = np.sqrt(w1_mvp**2 * sigma[0]**2 + w2_mvp**2 * sigma[1]**2 +
                      2 * w1_mvp * w2_mvp * rho * sigma[0] * sigma[1])

    # 记录 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        mvp_vol_at_rho45 = vol_mvp

    # --- 提取有效前沿部分 (收益 >= MVP 收益) ---
    # 过滤扫描点，只保留收益不低于 MVP 收益的点
    mask = ret >= ret_mvp - 1e-12  # 微小容差以便包含 MVP 点
    ret_eff = ret[mask]
    vol_eff = vol[mask]

    # 合并 MVP 精确点，确保起点准确
    ret_eff = np.append(ret_eff, ret_mvp)
    vol_eff = np.append(vol_eff, vol_mvp)

    # 按收益排序，使曲线单调
    order = np.argsort(ret_eff)
    ret_eff = ret_eff[order]
    vol_eff = vol_eff[order]

    # 绘制有效前沿曲线
    ax.plot(vol_eff, ret_eff, color=color, linewidth=2, label=f'ρ = {rho}')
    # 在最小方差组合处标记点 (不显示在图例中)
    ax.scatter(vol_mvp, ret_mvp, color=color, marker='o', s=80, zorder=5,
               edgecolors='k', linewidths=0.5)

# ------------------------------
# 4. 计算 ρ=0.45, 目标收益 10% 时的最小波动率
# ------------------------------
target_return = 0.10
rho_target = 0.45
# 两只资产下，给定收益的权重唯一确定
w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
w2_target = 1.0 - w1_target
cov12_target = rho_target * sigma[0] * sigma[1]
vol_target = np.sqrt(w1_target**2 * sigma[0]**2 + w2_target**2 * sigma[1]**2 +
                     2 * w1_target * w2_target * cov12_target)
frontier_vol_at_target = vol_target

# ------------------------------
# 5. 图形修饰与保存
# ------------------------------
ax.set_xlabel('年化波动率 (标准差)', fontsize=12)
ax.set_ylabel('年化期望收益', fontsize=12)
ax.set_title('两只资产的有效前沿 (不同相关系数)', fontsize=14)
ax.legend(loc='lower right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(left=0.12, right=0.36)  # 适当展示区域
ax.set_ylim(bottom=0.06, top=0.14)
fig.tight_layout()

# 保存图片
figure_path = 'effective_frontier.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ------------------------------
# 6. 组装结果字典
# ------------------------------
result = {
    'mvp_vol_at_rho45': round(mvp_vol_at_rho45, 6),
    'frontier_vol_at_target': round(frontier_vol_at_target, 6),
    'figure_path': figure_path
}

# 打印结果以便教师检查
print(result)
