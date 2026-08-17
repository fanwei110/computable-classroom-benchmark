import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

def compute_rolling_sharpe(data_path, window=60, risk_free_rate=0.021, fund_col='fund'):
    """
    读取课程数据快照，计算60日滚动年化夏普比率，并报告最后窗口的夏普值。
    
    参数:
        data_path: 数据文件路径
        window: 滚动窗口长度 (默认60)
        risk_free_rate: 无风险利率 (默认2.1%)
        fund_col: 基金日收益列名 (默认'fund')
    
    返回:
        result: 包含滚动夏普最后值和图表路径的字典
    """
    
    # 1. 读取数据
    df = pd.read_csv(data_path)
    
    # 确保日期列存在并设为索引
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
    
    # 提取基金日收益
    fund_returns = df[fund_col].dropna()
    
    # 2. 计算滚动年化夏普比率
    # 计算日无风险利率
    daily_risk_free = (1 + risk_free_rate) ** (1/252) - 1
    
    # 计算滚动平均超额收益
    rolling_mean_excess = fund_returns.rolling(window=window).mean() - daily_risk_free
    
    # 计算滚动标准差
    rolling_std = fund_returns.rolling(window=window).std()
    
    # 计算滚动夏普比率（年化）
    # 年化夏普 = sqrt(252) * (日超额收益均值 / 日收益标准差)
    rolling_sharpe = np.sqrt(252) * (rolling_mean_excess / rolling_std)
    
    # 3. 获取最后一个窗口的夏普值
    rolling_sharpe_last = rolling_sharpe.iloc[-1]
    
    # 4. 绘制时间序列图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(rolling_sharpe.index, rolling_sharpe.values, 
            linewidth=1.5, color='#2E86AB', label=f'{window}-Day Rolling Sharpe Ratio')
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.axhline(y=rolling_sharpe_last, color='#A23B72', linestyle='--', 
               linewidth=1.5, alpha=0.8, label=f'Last Value: {rolling_sharpe_last:.4f}')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
    ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio\nRisk-Free Rate: {risk_free_rate*100}%', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', frameon=True, shadow=True)
    
    # 添加统计信息文本框
    stats_text = f'Last Window Stats:\nSharpe: {rolling_sharpe_last:.4f}\nWindow: {window} days\nRisk-Free: {risk_free_rate*100}%'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    # 保存图表
    figure_path = 'rolling_sharpe_ratio.png'
    plt.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. 构建结果字典
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': figure_path
    }
    
    return result

# 执行分析
if __name__ == "__main__":
    # 这里假设数据文件名为 'fund_data.csv'，请根据实际文件名修改
    data_file = 'fund_data.csv'  # 用户可能需要修改这个文件名
    
    # 设置窗口长度（可调整）
    window_length = 60
    
    try:
        result = compute_rolling_sharpe(data_file, window=window_length)
        print(f"最后一个{window_length}日窗口的年化夏普比率: {result['rolling_sharpe_last']:.4f}")
        print(f"图表已保存至: {result['figure_path']}")
        
        # 输出最终结果字典
        print("\n最终结果字典:")
        print(result)
        
    except FileNotFoundError:
        print(f"错误: 找不到数据文件 '{data_file}'")
        print("请确保数据文件存在并包含'date'和'fund'列")
        # 创建一个示例结果以便测试
        result = {
            'rolling_sharpe_last': None,
            'figure_path': None
        }
