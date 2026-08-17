import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体，防止图表中文乱码（兼容Windows和Mac）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False # 正常显示负号

# ================= 1. 加载与处理数据 =================
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取fund列并计算日收益率
daily_returns = df['fund'].pct_change().dropna()

# 设定头寸：100万元
position = 1000000 

# 计算日损益 (P&L)
pnl = daily_returns * position

# ================= 2. 计算历史VaR =================
# 设定可调置信水平
confidence_level = 0.95

# 历史模拟法：取损益序列的下 (1 - 置信水平) 分位数
alpha = 1 - confidence_level
var_quantile = np.percentile(pnl, alpha * 100)

# VaR通常以正数表示潜在损失，因此对分位数取负值
hist_var_95_1d = -var_quantile

# 告知VaR的具体数值
print(f"在 {confidence_level*100:.0f}% 置信水平下，1日历史VaR为: {hist_var_95_1d:.2f} 元")

# ================= 3. 绘制直方图并标出VaR =================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, color='steelblue', edgecolor='black')

# 画出VaR分界线（注意：var_quantile是负数，即损失的数值线）
plt.axvline(x=var_quantile, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1日历史VaR: {hist_var_95_1d:.2f} 元')

plt.title('基金日损益分布直方图与历史VaR')
plt.xlabel('日损益 (元)')
plt.ylabel('频数')
plt.legend()

# 保存图表
figure_path = 'pnl_var_histogram.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 4. 构建 result 字典 =================
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

# 验证输出
print("Result字典内容:", result)
