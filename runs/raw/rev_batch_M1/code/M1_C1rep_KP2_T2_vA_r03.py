import matplotlib.pyplot as plt
import numpy as np
import os

# 参数设置（可调）
rf = 2.3  # 无风险利率（%）
market_return = 9.4  # 市场期望收益（%）

# 计算SML斜率
sml_slope = market_return - rf

# 计算beta=1.27对应的期望收益
beta_127 = 1.27
er_at_beta_127 = rf + beta_127 * (market_return - rf)

# 绘制SML
betas = np.linspace(0, 2, 100)
expected_returns = rf + betas * (market_return - rf)

plt.figure(figsize=(10, 6))
plt.plot(betas, expected_returns, label='Security Market Line (SML)', color='blue')

# 标记三个点
points = {'X': (0.62, 8.1), 'Y': (1.18, 13.1), 'Z': (1.51, 9.9)}
for label, (beta, er) in points.items():
    plt.scatter(beta, er, color='red')
    plt.text(beta, er + 0.5, f'{label}({beta}, {er}%)', ha='center', color='red')

plt.title('Security Market Line (SML)')
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return (%)')
plt.grid(True)
plt.legend()
plt.xlim(0, 2)
plt.ylim(0, 15)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 存入结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
