import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
POSITION = 1_000_000          # 头寸100万元人民币
CONFIDENCE_LEVEL = 0.95       # 置信水平（可调参数，如0.99, 0.90等）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'daily_pnl_var_hist.png'

# ==================== 1. 数据读取与损益构造 ====================
# 读取快照CSV
df = pd.read_csv(DATA_PATH)

# 计算fund列的日收益率，并剔除首行NaN
daily_returns = df['fund'].pct_change().dropna()

# 构造头寸的日损益（RMB）
daily_pnl = daily_returns * POSITION

# ==================== 2. 历史VaR计算 ====================
# 显著性水平
alpha = 1 - CONFIDENCE_LEVEL

# 由经验分布计算alpha分位数（例如95%置信水平对应5%分位数）
# 分位数通常为负数，代表损失
var_quantile = np.percentile(daily_pnl, alpha * 100)

# 按照金融风险管理的惯例，VaR以正数表示“在险价值”（即可能损失的最大金额）
hist_var_value = abs(var_quantile)

# ==================== 3. 画直方图并加带标注的VaR线 ====================
plt.figure(figsize=(10, 6))

# 绘制日损益直方图
plt.hist(daily_pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 绘制VaR线（使用原始分位数定位，即在损失侧画线）
plt.axvline(var_quantile, color='red', linestyle='--', linewidth=2, 
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-day Hist VaR = {hist_var_value:,.2f} RMB')

# 添加标注与格式美化
plt.title(f'Daily PnL Distribution and {CONFIDENCE_LEVEL*100:.0f}% Historical VaR')
plt.xlabel('Daily PnL (RMB)')
plt.ylabel('Frequency')
plt.legend(loc='upper right')
plt.grid(axis='y', alpha=0.5)

# ==================== 4. 保存图形并填充result ====================
# 保存图形
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# 输出VaR数值至控制台
print(f"{CONFIDENCE_LEVEL*100:.0f}% 1-day Historical VaR is: {hist_var_value:,.2f} RMB")

# 封装结果到result字典
result = {
    'hist_var_95_1d': hist_var_value,
    'figure_path': FIGURE_PATH
}
