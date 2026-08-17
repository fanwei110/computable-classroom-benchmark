import numpy as np
import matplotlib.pyplot as plt

# -------------------- 输入数据 --------------------
rf = 0.023                # 无风险利率
market_return = 0.094     # 市场期望收益
market_premium = market_return - rf   # 市场风险溢价

# 各股票 beta 值
beta_X = 0.62
beta_Y = 1.18
beta_Z = 1.51

# 股票 Y 的实际收益
actual_return_Y = 0.131

# -------------------- CAPM 计算 --------------------
er_X = rf + beta_X * market_premium
er_Y = rf + beta_Y * market_premium
er_Z = rf + beta_Z * market_premium

# Alpha 计算 (仅 Y)
alpha_Y = actual_return_Y - er_Y

# -------------------- 输出结果 --------------------
result = {
    'er_x': er_X,
    'er_y': er_Y,
    'er_z': er_Z,
    'alpha_y': alpha_Y
}

print("CAPM 计算结果：")
for key, value in result.items():
    print(f"{key}: {value:.6f} ({value*100:.4f}%)")

# -------------------- 可视化（SML） --------------------
plt.figure(figsize=(8, 5))

# 绘制 SML 线
beta_range = np.linspace(0, 1.8, 100)
sml = rf + beta_range * market_premium
plt.plot(beta_range, sml, 'k-', linewidth=2, label='SML (CAPM)')

# 标出 X, Y, Z 的 CAPM 预期点
plt.scatter([beta_X, beta_Y, beta_Z], [er_X, er_Y, er_Z],
            color='blue', s=80, zorder=5)
plt.text(beta_X, er_X, ' X', fontsize=12, verticalalignment='bottom')
plt.text(beta_Y, er_Y, ' Y (CAPM)', fontsize=12, verticalalignment='bottom')
plt.text(beta_Z, er_Z, ' Z', fontsize=12, verticalalignment='bottom')

# 标出 Y 的实际收益点，并画 alpha 虚线
plt.scatter(beta_Y, actual_return_Y, color='red', s=80, zorder=5)
plt.text(beta_Y, actual_return_Y, ' Y (actual)', fontsize=12,
         verticalalignment='bottom', color='red')
plt.plot([beta_Y, beta_Y], [er_Y, actual_return_Y], 'r--', linewidth=1.5, 
         label=f'α = {alpha_Y:.4f} ({alpha_Y*100:.2f}%)')
plt.legend()

plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML) & Alpha of Stock Y')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
