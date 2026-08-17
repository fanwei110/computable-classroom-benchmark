import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
confidence_level = 0.95  # 置信水平
position_size = 1_000_000  # 头寸规模（人民币）
data_path = 'data/market_snapshot_v1.csv'  # 数据路径
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)  # 创建输出目录
figure_path = output_dir / 'var_histogram.png'

# 1. 读取数据并计算日损益
try:
    df = pd.read_csv(data_path)
    daily_returns = df['fund'].pct_change().dropna()  # 日收益率
    daily_pnl = daily_returns * position_size  # 日损益（人民币）
except Exception as e:
    raise ValueError(f"数据读取或处理失败: {str(e)}")

# 2. 计算历史VaR
var_percentile = (1 - confidence_level) * 100
historical_var = np.percentile(daily_pnl, var_percentile)

# 3. 绘制直方图并添加VaR线
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

# 添加VaR线
plt.axvline(x=historical_var, color='red', linestyle='--', linewidth=2,
            label=f'{confidence_level:.0%} 1-day VaR: ¥{historical_var:,.2f}')

# 图形美化
plt.title(f'Daily P&L Distribution with {confidence_level:.0%} VaR', fontsize=14)
plt.xlabel('Daily P&L (RMB)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.legend(fontsize=12)

# 保存图形
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 4. 准备结果
result = {
    'hist_var_95_1d': historical_var,
    'figure_path': str(figure_path.resolve())
}

# 输出结果（供教师使用）
print(result)
