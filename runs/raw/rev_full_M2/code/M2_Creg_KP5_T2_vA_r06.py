import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings

# ------------------------------
# 可调参数
# ------------------------------
CONFIDENCE_LEVEL = 0.95          # 置信水平，可调节
POSITION = 1_000_000             # 头寸（人民币元）
DATA_FILE = 'course_data.csv'    # 课程数据快照文件名
SIM_DAYS = 500                   # 无数据时模拟序列长度
SIM_MEAN = 0.0                   # 模拟日均收益率
SIM_STD = 0.02                   # 模拟日收益率标准差
SEED = 42                        # 随机种子（确保可复现）
FIG_FILENAME = 'var_histogram.png'

# ------------------------------
# 1. 读取 fund 列的日收益序列
# ------------------------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    if 'fund' not in df.columns:
        raise ValueError(f"文件 {DATA_FILE} 中未找到 'fund' 列")
    fund_returns = df['fund'].values
    print(f"已从 {DATA_FILE} 读取 {len(fund_returns)} 条日收益数据。")
else:
    warnings.warn(f"未找到 '{DATA_FILE}'，使用模拟数据（种子={SEED}）。")
    np.random.seed(SEED)
    fund_returns = np.random.normal(SIM_MEAN, SIM_STD, SIM_DAYS)

# ------------------------------
# 2. 计算日损益
# ------------------------------
pnl = POSITION * fund_returns   # 每日盈亏（元）

# ------------------------------
# 3. 计算历史 VaR
# ------------------------------
# 固定 95% 置信水平 VaR（用于最终报告）
var_95 = -np.quantile(pnl, 1 - 0.95)

# 可调置信水平 VaR（用于绘图和展示）
var_adj = -np.quantile(pnl, 1 - CONFIDENCE_LEVEL)

# ------------------------------
# 4. 画日损益分布直方图，标出 VaR 竖线
# ------------------------------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7,
         label='Daily PnL')
plt.axvline(-var_adj, color='red', linestyle='dashed', linewidth=2,
            label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day Historical VaR: ¥{var_adj:,.2f}')
plt.title('Daily PnL Distribution and Historical VaR')
plt.xlabel('Profit & Loss (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
plt.savefig(FIG_FILENAME, dpi=150, bbox_inches='tight')
plt.close()
figure_path = os.path.abspath(FIG_FILENAME)

# ------------------------------
# 5. 组装结果字典
# ------------------------------
result = {
    'hist_var_95_1d': round(var_95, 2),    # 95% 一日历史 VaR（人民币元）
    'figure_path': figure_path
}

# 脚本直接运行时会打印结果
if __name__ == '__main__':
    print("计算结果：")
    print(f"  95% 一日历史 VaR : ¥{result['hist_var_95_1d']:,.2f}")
    print(f"  图片保存路径     : {result['figure_path']}")
