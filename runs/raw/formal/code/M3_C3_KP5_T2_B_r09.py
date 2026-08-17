import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= 参数设置 =================
position = 1000000  # 头寸 100万
confidence_level = 0.95  # 置信度可调
alpha = 1 - confidence_level

# ================= 数据读取与处理 =================
# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列日收益率（根据约定，收益率以小数表示）
daily_returns = df['fund']

# 计算日损益 (PnL)
pnl = position * daily_returns

# ================= 历史法 VaR 计算 =================
# 使用百分位数计算历史VaR (左尾 alpha 分位数)
var_quantile = np.percentile(pnl, alpha * 100)

# VaR 报告为正的损失金额
hist_var_95_1d = -var_quantile

# ================= 绘制损益直方图 =================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='steelblue', alpha=0.75, edgecolor='black')

# 标出 95% 一日 VaR 竖线
plt.axvline(x=var_quantile, color='red', linestyle='--', linewidth=2,
            label=f'{confidence_level*100:.0f}% 1-Day VaR: {hist_var_95_1d:,.2f}')

plt.title('PnL Distribution and Historical VaR', fontsize=14)
plt.xlabel('Profit and Loss', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.5)

# 保存图片
figure_path = 'pnl_var_histogram.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 输出结果 =================
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

print(f"95% 一日历史VaR (正的损失金额): {result['hist_var_95_1d']:,.2f}")
print(f"图表已保存至: {result['figure_path']}")
