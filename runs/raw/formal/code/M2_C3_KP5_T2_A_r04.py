import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数区 ====================
file_path = 'data/market_snapshot_v1.csv'  # 数据文件
position = 1_000_000                       # 头寸（元）
confidence_level = 0.95                    # 置信水平（可调）
output_fig = 'hist_var_figure.png'         # 图片保存路径
# ===============================================

# 1. 读取数据
df = pd.read_csv(file_path)
# 假设日收益率在 'fund' 列，且已经是小数（如 0.01 表示 1%）
returns = df['fund'].dropna().astype(float)

# 2. 计算日损益序列
pnl = position * returns  # 损益（正为盈利，负为损失）

# 3. 计算历史 VaR（95% 一日，报告为正的损失金额）
var_percentile = 100 * (1 - confidence_level)  # 对应 5% 分位
var_loss = -np.percentile(pnl, var_percentile)  # 损失取正数

# 4. 画直方图并标注 VaR
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, label='Daily PnL')
plt.axvline(x=-var_loss, color='red', linestyle='--', linewidth=2,
            label=f'{confidence_level*100:.0f}% 1-Day Hist VaR = {var_loss:,.2f}')
plt.title('Historical VaR (1-Day, 95%)')
plt.xlabel('Profit / Loss (CNY)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_fig, dpi=150)
plt.close()

# 5. 结果存入字典
result = {
    'hist_var_95_1d': round(var_loss, 2),
    'figure_path': output_fig
}

print("VaR 计算结果：", result['hist_var_95_1d'], "元")
print("图片已保存至：", result['figure_path'])
print("完整字典：", result)
