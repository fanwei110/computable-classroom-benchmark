import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 可调参数 ====================
CONF_LEVEL = 0.95                # 置信水平，例如 0.95 表示 95%
CAPITAL = 1_000_000              # 头寸金额（人民币）
DATA_FILE = "fund_data.csv"      # 课程数据快照文件，需包含 "fund" 列
FIGURE_FILE = "var_figure.png"   # 输出图表文件名
# =================================================

def load_data(filepath):
    """读取数据快照中 'fund' 列的日收益序列"""
    df = pd.read_csv(filepath)
    if 'fund' not in df.columns:
        raise ValueError(f"数据文件 {filepath} 中缺少 'fund' 列")
    return df['fund'].dropna().values

def compute_daily_pnl(returns, capital):
    """根据日收益率序列和本金计算每日损益序列"""
    return capital * returns

def historical_var_1d(pnl, conf_level):
    """
    计算历史模拟法下的一日 VaR（金额，正数表示损失）。
    pnl: 日损益序列（盈利为正，亏损为负）
    conf_level: 置信水平，如 0.95
    """
    # VaR 对应损益分布的下侧分位数
    percentile = 100 * (1 - conf_level)
    var_threshold = np.percentile(pnl, percentile)
    # 通常 VaR 报告为损失的绝对值，若分位数为负，取相反数；若为正则不常见，按定义报告损失
    var_loss = -var_threshold if var_threshold < 0 else 0.0
    return var_loss, var_threshold

def plot_pnl_histogram_with_var(pnl, var_threshold, conf_level, figure_path):
    """绘制日损益直方图，并标出 VaR 阈值线"""
    plt.figure(figsize=(10, 6))
    plt.hist(pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.8, label='日损益分布')
    plt.axvline(x=var_threshold, color='red', linestyle='--', linewidth=2,
                label=f'{conf_level*100:.0f}% 历史VaR: ¥{abs(var_threshold):,.2f}')
    plt.xlabel('日损益（人民币）')
    plt.ylabel('频数')
    plt.title(f'日损益分布与 {conf_level*100:.0f}% 一日历史VaR (本金 ¥{CAPITAL:,})')
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=150)
    plt.close()
    return figure_path

def main():
    # 读取数据
    returns = load_data(DATA_FILE)
    # 计算损益
    pnl = compute_daily_pnl(returns, CAPITAL)
    # 计算历史VaR
    var_loss, var_threshold = historical_var_1d(pnl, CONF_LEVEL)
    # 输出报告
    print(f"本金: ¥{CAPITAL:,}")
    print(f"置信水平: {CONF_LEVEL*100:.0f}%")
    print(f"95% 一日历史 VaR（损失金额）: ¥{var_loss:,.2f}")
    # 绘图并保存
    fig_path = plot_pnl_histogram_with_var(pnl, var_threshold, CONF_LEVEL, FIGURE_FILE)
    # 按要求构建结果字典
    result = {
        'hist_var_95_1d': var_loss,
        'figure_path': fig_path
    }
    print(f"\n图表已保存至: {fig_path}")
    return result

if __name__ == "__main__":
    result = main()
    # 脚本运行结束后，result 字典可供后续使用
    # 可在此处打印或检查 result
    print("\n结果字典:", result)
