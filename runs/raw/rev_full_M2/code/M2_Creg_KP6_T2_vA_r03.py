import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
WINDOW = 60                 # 滚动窗口长度（天）
RISK_FREE_RATE = 0.021      # 年化无风险利率
TRADING_DAYS = 252          # 每年交易日数
DATA_FILE = "fund_data.csv" # 课程数据快照文件路径
FIGURE_FILE = "rolling_sharpe.png"  # 输出图片路径
# =================================================

def load_data(filepath):
    """读取数据文件，返回 'fund' 列日收益率序列"""
    df = pd.read_csv(filepath)
    if 'fund' not in df.columns:
        raise ValueError("数据文件中缺少 'fund' 列")
    # 假设 'fund' 列已经是日收益率（例如 0.01 表示1%）
    returns = df['fund'].dropna().astype(float)
    return returns

def compute_rolling_sharpe(returns, window, daily_rf, trading_days):
    """计算滚动年化夏普比率"""
    # 滚动计算平均收益率和标准差
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    # 年化夏普比率 = (日超额收益均值 / 日收益标准差) * sqrt(年交易日数)
    rolling_sharpe = (rolling_mean - daily_rf) / rolling_std * np.sqrt(trading_days)
    return rolling_sharpe

def main():
    # 1. 准备日度无风险利率
    daily_rf = RISK_FREE_RATE / TRADING_DAYS   # 算术日利率

    # 2. 读取数据
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"数据文件不存在: {DATA_FILE}")
    returns = load_data(DATA_FILE)

    if len(returns) < WINDOW:
        raise ValueError(f"数据长度不足，无法计算 {WINDOW} 日滚动窗口（当前长度：{len(returns)}）")

    # 3. 计算滚动夏普
    rolling_sharpe = compute_rolling_sharpe(returns, WINDOW, daily_rf, TRADING_DAYS)

    # 4. 提取最后一个窗口的夏普值
    rolling_sharpe_last = rolling_sharpe.iloc[-1]
    # 处理可能为NaN的情况（所有窗口标准差为0时）
    if np.isnan(rolling_sharpe_last):
        rolling_sharpe_last = float('nan')

    # 5. 画图并保存
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_sharpe.index, rolling_sharpe.values, color='navy', linewidth=1)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.title(f"{WINDOW}-Day Rolling Annualized Sharpe Ratio (Fund)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Annualized Sharpe Ratio")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_FILE, dpi=150)
    plt.close()

    # 6. 组装输出结果
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': os.path.abspath(FIGURE_FILE)
    }

    # 打印结果便于检查
    print("result =", result)
    return result

if __name__ == "__main__":
    result = main()
