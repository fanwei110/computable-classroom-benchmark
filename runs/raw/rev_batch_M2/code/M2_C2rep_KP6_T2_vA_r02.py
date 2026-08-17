import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 参数设置
DATA_PATH = 'data/market_snapshot_v1.csv'
RISK_FREE_RATE_ANNUAL = 0.021  # 年化无风险利率 2.1%
WINDOW_SIZE = 60  # 滚动窗口大小（可调）
TRADING_DAYS_PER_YEAR = 252  # 年化交易日数

# 1. 读取数据
df = pd.read_csv(DATA_PATH, parse_dates=True)

# 确保数据包含date和fund列
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

# 提取基金日收益率
fund_returns = df['fund'].values

# 计算日化无风险利率
risk_free_rate_daily = (1 + RISK_FREE_RATE_ANNUAL) ** (1 / TRADING_DAYS_PER_YEAR) - 1

# 2. 计算60日滚动年化夏普比率
def calculate_rolling_sharpe(returns, window, rf_daily, annual_factor):
    """
    计算滚动年化夏普比率
    
    参数:
    returns: 日收益率序列
    window: 滚动窗口大小
    rf_daily: 日化无风险利率
    annual_factor: 年化因子（交易日数）
    """
    n = len(returns)
    rolling_sharpe = np.full(n, np.nan)
    
    for i in range(window - 1, n):
        window_returns = returns[i - window + 1:i + 1]
        
        # 计算超额收益
        excess_returns = window_returns - rf_daily
        
        # 计算年化夏普比率
        mean_excess_daily = np.mean(excess_returns)
        std_excess_daily = np.std(excess_returns, ddof=1)  # 使用样本标准差
        
        if std_excess_daily > 0:
            # 年化
            sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(annual_factor)
            rolling_sharpe[i] = sharpe_annual
        else:
            rolling_sharpe[i] = np.nan
    
    return rolling_sharpe

rolling_sharpe = calculate_rolling_sharpe(
    fund_returns, 
    WINDOW_SIZE, 
    risk_free_rate_daily, 
    TRADING_DAYS_PER_YEAR
)

# 3. 报告最后一个窗口的夏普值
last_sharpe = rolling_sharpe[-1]
print(f"最后一个{WINDOW_SIZE}日窗口的滚动年化夏普比率: {last_sharpe:.4f}")

# 4. 绘制时间序列图
fig, ax = plt.subplots(figsize=(12, 6))

# 创建x轴（日期或索引）
if 'date' in df.columns:
    x_axis = df['date']
    x_label = '日期'
else:
    x_axis = np.arange(len(fund_returns))
    x_label = '交易日序号'

# 绘制滚动夏普比率
ax.plot(x_axis, rolling_sharpe, linewidth=1.5, color='blue', alpha=0.8, label=f'{WINDOW_SIZE}日滚动年化夏普比率')

# 添加零线
ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7, label='零线')

# 标记最后一个窗口的值
if len(x_axis) > 0:
    ax.scatter(x_axis.iloc[-1] if hasattr(x_axis, 'iloc') else x_axis[-1], 
              last_sharpe, 
              color='darkred', s=80, zorder=5, 
              label=f'最后一个窗口: {last_sharpe:.4f}')

# 设置图表属性
ax.set_title(f'基金60日滚动年化夏普比率 (无风险利率: {RISK_FREE_RATE_ANNUAL*100:.1f}%)', 
             fontsize=14, fontweight='bold')
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel('年化夏普比率', fontsize=12)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# 添加统计信息文本框
textstr = f'数据点数: {len(fund_returns)}\n'
textstr += f'窗口大小: {WINDOW_SIZE}天\n'
textstr += f'最后窗口夏普: {last_sharpe:.4f}\n'
textstr += f'无风险利率: {RISK_FREE_RATE_ANNUAL*100:.1f}%'

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
print(f"图形已保存至: {figure_path}")

# 5. 填充result字典
result = {
    'rolling_sharpe_last': float(last_sharpe),
    'figure_path': os.path.abspath(figure_path)
}

print("\n===== 结果输出 =====")
print(f"rolling_sharpe_last: {result['rolling_sharpe_last']:.4f}")
print(f"figure_path: {result['figure_path']}")

# 验证结果
assert 'rolling_sharpe_last' in result, "result字典必须包含'rolling_sharpe_last'键"
assert 'figure_path' in result, "result字典必须包含'figure_path'键"
assert isinstance(result['rolling_sharpe_last'], (int, float)), "rolling_sharpe_last必须是数值类型"
assert not np.isnan(result['rolling_sharpe_last']), "rolling_sharpe_last不能为NaN"
assert os.path.exists(result['figure_path']), f"图形文件未找到: {result['figure_path']}"

print("\n所有验证通过！")
