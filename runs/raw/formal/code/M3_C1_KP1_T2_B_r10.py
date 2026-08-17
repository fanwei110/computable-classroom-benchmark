import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文字体和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 资产参数
r1, r2 = 0.071, 0.124
s1, s2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 权重范围（允许卖空以展示完整的双曲线）
w1 = np.linspace(-0.5, 1.5, 500)
w2 = 1 - w1

# 计算组合收益和方差
port_ret = w1 * r1 + w2 * r2

# 存储特定数据的变量
mvp_vol_45 = None
target_vol_45 = None
target_ret = 0.10

plt.figure(figsize=(10, 7))

for rho in rhos:
    # 计算组合波动率
    port_vol = np.sqrt((w1 * s1)**2 + (w2 * s2)**2 + 2 * w1 * w2 * rho * s1 * s2)
    
    # 计算最小方差组合 (MVP)
    w1_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    w2_mvp = 1 - w1_mvp
    ret_mvp = w1_mvp * r1 + w2_mvp * r2
    vol_mvp = np.sqrt((w1_mvp * s1)**2 + (w2_mvp * s2)**2 + 2 * w1_mvp * w2_mvp * rho * s1 * s2)
    
    # 绘制有效前沿
    plt.plot(port_vol, port_ret, label=f'相关系数 ρ={rho}')
    
    # 标出最小方差点
    plt.scatter(vol_mvp, ret_mvp, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\nVol: {vol_mvp:.2%}',
                 xy=(vol_mvp, ret_mvp), 
                 xytext=(vol_mvp + 0.015, ret_mvp - 0.005),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

    # 提取 rho=0.45 时的特定数据
    if rho == 0.45:
        mvp_vol_45 = vol_mvp
        
        # 计算目标收益 10% 下的最小波动率
        w1_target = (target_ret - r2) / (r1 - r2)
        w2_target = 1 - w1_target
        vol_target = np.sqrt((w1_target * s1)**2 + (w2_target * s2)**2 + 2 * w1_target * w2_target * rho * s1 * s2)
        target_vol_45 = vol_target
        
        # 在图上标出目标收益10%的点
        plt.scatter(vol_target, target_ret, color='red', marker='x', s=100, zorder=5)
        plt.annotate(f'目标收益10%\nVol: {vol_target:.2%}',
                     xy=(vol_target, target_ret),
                     xytext=(vol_target + 0.02, target_ret + 0.005),
                     arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=5))

# 图表美化
plt.title('两资产有效前沿 (不同相关系数)')
plt.xlabel('波动率')
plt.ylabel('收益率')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.10, 0.50)
plt.ylim(0.04, 0.16)

# 保存图表
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约构建结果字典
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': target_vol_45,
    'figure_path': fig_path
}

print(result)
