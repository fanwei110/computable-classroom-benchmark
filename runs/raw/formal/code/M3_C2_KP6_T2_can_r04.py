import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 可调参数与假设 ====================
ANNUAL_RF = 0.021           # 年化无风险利率 2.1%
WINDOW = 60                 # 滚动窗口长度（可调）
TRADING_DAYS = 252           # 一年交易日天数
FIGURE_PATH = 'rolling_sharpe_ratio.png'
DATA_PATH = 'data/market_snapshot_v1.csv'

# ==================== 计算假设 ====================
# 1. 日无风险利率：使用简单除法 Rf_daily = Rf_annual / 252
# 2. 年化夏普比率 = (日超额收益均值 / 日超额收益标准差) * sqrt(252)
# 3. 标准差采用样本标准差 (ddof=1)
# 4. 基金日收益率以小数形式表示（如 0.015 代表 1.5%）
# =======================================================

def main():
    # 1. 读取快照 CSV
    df = pd.read_csv(DATA_PATH)
    
    # 容错处理：寻找 'fund' 列（不区分大小写）
    fund_col = [c for c in df.columns if c.lower() == 'fund']
    if not fund_col:
        raise ValueError("数据集中未找到 'fund' 列。")
    fund_col = fund_col[0]
    
    # 识别并设置日期索引（若存在），以便图表横轴更直观
    date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
    if date_cols:
        df = df.set_index(date_cols[0])
        
    # 2. 计算 60 日滚动年化夏普比率
    daily_rf = ANNUAL_RF / TRADING_DAYS
    daily_returns = df[fund_col]
    excess_returns = daily_returns - daily_rf
    
    # 计算滚动均值与滚动标准差
    rolling_mean = excess_returns.rolling(window=WINDOW).mean()
    rolling_std = excess_returns.rolling(window=WINDOW).std()
    
    # 计算滚动年化夏普比率
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)
    
    # 3. 报告最后一个窗口的值
    # 使用 dropna().iloc[-1] 确保获取最后一个有效值
    rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]
    
    # 画出时间序列图
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_sharpe.dropna(), label=f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', color='blue')
    plt.axhline(y=0, color='red', linestyle='--', linewidth=1)
    plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Risk-Free Rate = {ANNUAL_RF*100:.1f}%/yr)')
    plt.xlabel('Date / Observation')
    plt.ylabel('Sharpe Ratio')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 4. 保存图形并填充 result
    plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
    plt.close()
    
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': FIGURE_PATH
    }
    
    return result

if __name__ == '__main__':
    result = main()
    print(result)
