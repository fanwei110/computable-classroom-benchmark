"""
马科维茨均值-方差组合理论：两资产有效前沿演示
- 两只资产：期望年收益 7.1% / 12.4%，年化波动率 16.3% / 28.9%
- 相关系数：0.15, 0.45, 0.75
- 满仓约束 (w1 + w2 = 1)，权重扫描 [0,1]
- 标注每条前沿的最小方差组合 (MVP)
- 汇报 ρ=0.45 时 MVP 波动率，以及目标收益 10% 时的最小波动率
"""
import matplotlib
matplotlib.use("Agg")  # 无界面环境下保证可保存图像
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------
# 1. 输入参数
# ----------------------------------------------------------------------
mu = np.array([0.071, 0.124])          # 期望年收益
sigma = np.array([0.163, 0.289])       # 年化波动率
rhos = [0.15, 0.45, 0.75]              # 三种相关系数
target_return = 0.10                   # 目标收益 10%

# ----------------------------------------------------------------------
# 2. 准备权重扫描 (满仓约束 w1+w2=1)
# ----------------------------------------------------------------------
n_pts = 1001
w1_grid = np.linspace(0.0, 1.0, n_pts)
W = np.vstack([w1_grid, 1.0 - w1_grid]).T   # shape (n_pts, 2)

# ----------------------------------------------------------------------
# 3. 解析公式（用于校验与精确计算）
# ----------------------------------------------------------------------
def mvp_weights(s1, s2, rho):
    """两资产最小方差组合权重 (资产1的权重)"""
    num = s2**2 - rho * s1 * s2
    den = s1**2 + s2**2 - 2.0 * rho * s1 * s2
    w1 = num / den
    return np.array([w1, 1.0 - w1])

def portfolio_stats(w, mu_vec, cov):
    ret = float(w @ mu_vec)
    var = float(w @ cov @ w)
    return ret, np.sqrt(var)

# ----------------------------------------------------------------------
# 4. 绘图：三条相关系数下的有效前沿
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7))
colors = {0.15: "#1f77b4", 0.45: "#ff7f0e", 0.75: "#2ca02c"}
mvp_records = {}

mvp_vol_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    cov = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2],
    ])

    # 全部可行组合（满仓）
    port_ret = W @ mu                       # (n_pts,)
    port_var = np.einsum("ij,jk,ik->i", W, cov, W)
    port_vol = np.sqrt(port_var)

    # 最小方差组合
    w_mvp = mvp_weights(sigma[0], sigma[1], rho)
    mvp_ret, mvp_vol = portfolio_stats(w_mvp, mu, cov)
    mvp_records[rho] = (w_mvp, mvp_ret, mvp_vol)

    # 有效前沿：方差最小组合之上的部分
    eff_mask = port_ret >= mvp_ret

    # 画整条可行边界（淡色细线）
    ax.plot(port_vol, port_ret, color=colors[rho], lw=1.2, alpha=0.45)
    # 画有效前沿（粗实线）
    ax.plot(port_vol[eff_mask], port_ret[eff_mask],
            color=colors[rho], lw=2.4,
            label=f"ρ = {rho:.2f}  (MVP σ={mvp_vol*100:.2f}%)")

    # 标出 MVP
    ax.scatter([mvp_vol], [mvp_ret], color=colors[rho],
               s=90, edgecolor="black", zorder=5)

    # 处理 ρ = 0.45 的额外要求
    if abs(rho - 0.45) < 1e-12:
        mvp_vol_rho45 = mvp_vol

        # 目标收益 10% 下的权重（满时，权重唯一）
        w1_t = (target_return - mu[1]) / (mu[0] - mu[1])
        w_t = np.array([w1_t, 1.0 - w1_t])
        t_ret, t_vol = portfolio_stats(w_t, mu, cov)
        # 校验 t_ret ≈ target_return
        assert abs(t_ret - target_return) < 1e-10
        frontier_vol_at_target = t_vol

        # 在图上标记目标组合
        ax.scatter([t_vol], [t_ret], marker="*", s=260,
                   color="red", edgecolor="black", zorder=6,
                   label="ρ=0.45, 目标 10% 组合")

# ----------------------------------------------------------------------
# 5. 图表美化
# ----------------------------------------------------------------------
ax.axhline(target_return, color="gray", ls="--", lw=1, alpha=0.6,
           label="目标收益 10%")
ax.set_xlabel("组合波动率 (年化 σ)", fontsize=12)
ax.set_ylabel("组合期望收益 (年化 μ)", fontsize=12)
ax.set_title("马科维茨两资产有效前沿（不同相关系数）", fontsize=13)
ax.grid(alpha=0.3)
ax.legend(loc="best", fontsize=9)
fig.tight_layout()

# ----------------------------------------------------------------------
# 6. 保存图像并组装结果
# ----------------------------------------------------------------------
fig_path = "efficient_frontier.png"
fig.savefig(fig_path, dpi=120)
plt.close(fig)

result = {
    "mvp_vol_at_rho45": float(mvp_vol_rho45),
    "frontier_vol_at_target": float(frontier_vol_at_target),
    "figure_path": fig_path,
}

# 控制台打印，便于课堂投屏查看
print("=" * 60)
print("马科维茨两资产组合结果汇总")
print("=" * 60)
for rho, (w_mvp, r, v) in mvp_records.items():
    print(f"ρ={rho:.2f}: MVP w=({w_mvp[0]:.4f},{w_mvp[1]:.4f}), "
          f"μ={r*100:.3f}%, σ={v*100:.3f}%")
print("-" * 60)
print(f"ρ=0.45 时最小方差组合波动率: "
      f"{result['mvp_vol_at_rho45']*100:.4f}%")
print(f"ρ=0.45 目标收益 10% 时最小波动率: "
      f"{result['frontier_vol_at_target']*100:.4f}%")
print(f"图像已保存至: {result['figure_path']}")
print("=" * 60)
