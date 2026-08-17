import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
rf = 0.023  # 无风险利率（可调）
market_return = 0.094  # 市场期望收益（可调）

# 计算SML斜率
sml_slope = market_return - rf

# 计算beta=1.27对应的期望收益
beta_127 = 1.27
er_at_beta_127 = rf + beta_127 * sml_slope

# 绘制SML图
beta_range = np.linspace(0, 2, 100)
sml_returns = rf + beta_range * sml_slope

plt.figure(figsize=(10, 6))
plt.plot(beta_range, sml_returns, label='Security Market Line (SML)', color='blue')

# 标记三个点
points = {'X': (0.62, 0.081), 'Y': (1.18, 0.131), 'Z': (1.51, 0.099)}
for label, (beta, ret) in points.items():
    plt.scatter(beta, ret, color='red')
    plt.text(beta, ret, f' {label}', verticalalignment='bottom', horizontalalignment='right')

plt.title('Security Market Line (SML)')
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.grid(True)
plt.legend()
plt.xlim(0, 2)
plt.ylim(0, 0.2)  # 20%以内

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
