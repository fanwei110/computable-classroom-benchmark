import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========================
# 可调参数
# ========================
POSITION = 1_000_000          # 头寸（元）
CONFIDENCE = 0.95             # 置信水平（可调）
ALPHA = 1 - CONFIDENCE        # 显著性水平
DATA_FILE = "fund_data.csv"   # 数据快照文件名
FIGURE_FILE = "var_histogram.png"  # 图片输出路径

# ========================
# 1. 读取或生成日收益序列
# ========================
if os.path.exists(DATA_FILE):
    # 从课程数据快照读取 fund 列
    df = pd.read_csv(DATA_FILE)
    if "fund" not in df.columns:
        raise ValueError(f"{DATA_FILE} 中缺少 'fund' 列")
    returns = df["fund"].dropna().values
    print(f"已从 {DATA_FILE} 读取 {len(returns)} 个日收益率数据")
else:
    # 文件不存在时，生成可复现的模拟数据（固定随机种子）
    np.random.seed(42)
    n_days = 1000
    # 模拟日收益率：均值=0.0002，标准差=0.015，约合年化波动24%
    returns = np.random.normal(loc=0.0002, scale=0.015, size=n_days)
    pd.DataFrame({"fund": returns}).to_csv(DATA_FILE, index=False)
    print(f"{DATA_FILE} 不存在，已生成 {n_days} 个模拟日收益率并保存")

# ========================
# 2. 计算日损益序列
# ========================
pnl = POSITION * returns          # 金额形式的每日损益

# ========================
# 3. 计算历史 VaR
# ========================
# 历史 VaR 定义为：在置信水平下，一日最大损失（正值）
# 损益分布的下侧 alpha 分位数的绝对值
var_alpha = -np.percentile(pnl, 100 * ALPHA)
# 按人民币格式化为字符串，用于标注
var_label = f"VaR ({CONFIDENCE*100:.0f}% 1-Day)\n¥{var_alpha:,.2f}"

# 存储结果
result = {}
result['hist_var_95_1d'] = round(var_alpha, 2)   # 人民币数值
result['figure_path'] = os.path.abspath(FIGURE_FILE)

# ========================
# 4. 绘制直方图并标注 VaR
# ========================
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
counts, bins, patches = ax.hist(pnl, bins=50, color='steelblue',
                                edgecolor='white', alpha=0.85, density=True,
                                label='日损益分布')

# 标注 VaR 竖线
ax.axvline(x=-var_alpha, color='firebrick', linestyle='--', linewidth=2,
           label=f'{CONFIDENCE*100:.0f}% 历史 VaR: ¥{var_alpha:,.2f}')
# 在竖线顶部添加文字标注
ymin, ymax = ax.get_ylim()
ax.text(-var_alpha, ymax*0.95, var_label,
        ha='center', va='top', fontsize=10, color='firebrick',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# 图形装饰
ax.set_title(f"日损益分布直方图与 {CONFIDENCE*100:.0f}% 一日历史 VaR\n头寸: ¥{POSITION:,}",
             fontsize=14, fontweight='bold')
ax.set_xlabel("日损益 (人民币)")
ax.set_ylabel("频率密度")
ax.legend(loc='upper left')
plt.tight_layout()

# 保存图片
plt.savefig(FIGURE_FILE, dpi=200, bbox_inches='tight')
plt.close()   # 释放内存

print(f"\n计算完成。")
print(f"历史 VaR (95% 1日): ¥{result['hist_var_95_1d']:,.2f}")
print(f"图片已保存至: {result['figure_path']}")

# 结果字典供外部调用（脚本运行后 result 变量保留在内存中）
if __name__ == "__main__":
    # 此处 result 即为要求的输出
    pass
