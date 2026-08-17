import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==================== 可调参数 ====================
CONFIDENCE_LEVEL = 0.95          # 置信水平，可修改
HEAD_VALUE = 1_000_000.0        # 头寸价值（人民币）
DATA_FILE = "fund_data.csv"     # 课程数据快照文件名
FIGURE_FILE = "var_histogram.png"  # 输出图片路径
RANDOM_SEED = 42                # 模拟数据的随机种子，保证可复现
# =================================================

def load_returns():
    """
    读取 fund 列的日收益序列。优先从 DATA_FILE 读取；
    若文件不存在，则用固定种子生成模拟收益率（均值0.0002，波动0.02的正态分布）。
    返回 pandas Series。
    """
    if Path(DATA_FILE).exists():
        df = pd.read_csv(DATA_FILE)
        if 'fund' not in df.columns:
            raise ValueError(f"'{DATA_FILE}' 中缺少 'fund' 列")
        returns = df['fund'].dropna()
        print(f"从 '{DATA_FILE}' 成功读取 {len(returns)} 条日收益记录。")
    else:
        # 模拟生成 1000 条日收益，确保演示可运行且可复现
        rng = np.random.default_rng(RANDOM_SEED)
        returns = pd.Series(rng.normal(0.0002, 0.02, 1000), name='fund')
        print(f"未找到 '{DATA_FILE}'，使用模拟数据（{len(returns)} 条，种子={RANDOM_SEED}）。")
    return returns

def compute_var(returns, confidence, head_value):
    """
    历史模拟法计算 VaR。
    参数：
        returns : 日收益率序列
        confidence : 置信水平（如 0.95）
        head_value : 头寸价值
    返回：
        var_value : 对应置信水平下的损益分位数（负值代表亏损）
    """
    pnl = returns * head_value  # 日损益序列
    # 对损益求 alpha 分位数，alpha = 1 - confidence
    var_cutoff = np.quantile(pnl, 1 - confidence)
    return var_cutoff, pnl

def plot_var(pnl, var_value, confidence, figure_path):
    """
    绘制日损益直方图，并用竖线标出历史 VaR。
    """
    plt.figure(figsize=(10, 6))
    plt.hist(pnl, bins=50, alpha=0.7, color='steelblue', edgecolor='white', label='日损益分布')
    plt.axvline(var_value, color='red', linestyle='--', linewidth=2,
                label=f'{confidence*100:.0f}% 历史 VaR = ¥{abs(var_value):,.2f}')
    plt.title('1,000,000 元头寸的日损益分布与历史 VaR', fontsize=14)
    plt.xlabel('日损益（人民币）', fontsize=12)
    plt.ylabel('频次', fontsize=12)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(figure_path, dpi=150)
    plt.close()
    print(f"图片已保存至 {figure_path}")

def main():
    # 1. 加载日收益数据
    returns = load_returns()

    # 2. 计算历史 VaR 及损益序列
    var_value, pnl = compute_var(returns, CONFIDENCE_LEVEL, HEAD_VALUE)

    # 注意：VaR 通常表示为正数损失，我们报告绝对值
    var_reported = abs(var_value)

    # 3. 画图并保存
    plot_var(pnl, var_value, CONFIDENCE_LEVEL, FIGURE_FILE)

    # 4. 输出到 result 字典
    result = {
        'hist_var_95_1d': f"¥{var_reported:,.2f}",
        'figure_path': FIGURE_FILE,
    }

    print("\n=== 结果 ===")
    print(f"95% 一日历史 VaR : {result['hist_var_95_1d']}")
    print(f"图片路径         : {result['figure_path']}")

    return result

if __name__ == "__main__":
    result = main()
