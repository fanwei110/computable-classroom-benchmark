import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
rf = 0.023  # 无风险利率
market_return = 0.094  # 市场期望收益

# 计算SML斜率
sml_slope = market_return - rf

# 计算beta=1.27对应的期望收益
beta_127 = 1.27
er_at_beta_127 = rf + beta_127 * sml_slope

# 绘制SML图
plt.figure(figsize=(10, 6))
betas = np.linspace(0, 2, 100)
expected_returns = rf + betas * sml_slope

plt.plot(betas, expected_returns, label=f'SML (rf={rf*100:.1f}%, E[Rm]={market_return*100:.1f}%)')

# 标记三个点
points = {'X': (0.62, 0.081), 'Y': (1.18, 0.131), 'Z': (1.51, 0.099)}
for label, (beta, er) in points.items():
    plt.scatter(beta, er, label=f'{label}({beta}, {er*100:.1f}%)')
    plt.text(beta, er, f' {label}', verticalalignment='bottom')

plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 输出结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
