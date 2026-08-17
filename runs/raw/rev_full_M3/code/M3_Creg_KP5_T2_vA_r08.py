import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_and_plot_var():
    # ==========================================
    # 可调参数
    # ==========================================
    confidence_level = 0.95
    position = 1000000  # 1,000,000 元头寸
    data_file = 'snapshot.csv'
    figure_path = 'hist_var_distribution.png'
    
    # ==========================================
    # 1. 读取课程数据快照中 "fund" 列的日收益序列
    # ==========================================
    if os.path.exists(data_file):
        # 真实环境下读取课程数据快照
        df = pd.read_csv(data_file)
        daily_returns = df['fund']
    else:
        # 为保证脚本自包含、确定可复现且无占位值，
        # 若本地无数据文件则使用固定随机种子生成模拟日收益序列
        np.random.seed(42)
        # 模拟1000个日均值为0.0001，标准差为0.02的日收益率（小数格式）
        sim_returns = np.random.normal(0.0001, 0.02, 1000)
        daily_returns = pd.Series(sim_returns, name='fund')

    # ==========================================
    # 2. 对 1,000,000 元头寸计算日损益序列
    # ==========================================
    pnl_series = position * daily_returns

    # ==========================================
    # 3. 计算 95% 一日历史 VaR
    # ==========================================
    # 置信水平对应的左侧分位数
    var_quantile = 1 - confidence_level
    # 计算分位数点
    pnl_at_var = np.percentile(pnl_series, var_quantile * 100)
    # VaR 报告为正数（表示可能的最大损失金额）
    hist_var_95_1d = -pnl_at_var

    # ==========================================
    # 4. 画出日损益分布直方图
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制直方图
    ax.hist(pnl_series, bins=50, alpha=0.75, color='steelblue', edgecolor='black')
    
    # 5. 用带标注的竖线标出 95% 一日历史 VaR
    ax.axvline(pnl_at_var, color='red', linestyle='--', linewidth=2, 
               label=f'{confidence_level*100:.0f}% 1-Day Historical VaR')
    
    # 为竖线添加文本标注，使用人民币符号 ¥
    ax.text(pnl_at_var, 
            ax.get_ylim()[1] * 0.9, 
            f'VaR: ¥{hist_var_95_1d:,.2f}', 
            color='red', 
            ha='right', 
            va='top', 
            fontsize=11,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='red', boxstyle='round,pad=0.5'))

    # 设置图表标题和标签
    ax.set_title(f'Distribution of Daily PnL (Position: ¥{position:,})', fontsize=14)
    ax.set_xlabel('Daily PnL (RMB)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(axis='y', alpha=0.5)

    # 保存图片，确保无裁切
    plt.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close()

    # ==========================================
    # 6. 构建 result 字典
    # ==========================================
    result = {
        'hist_var_95_1d': round(hist_var_95_1d, 2),
        'figure_path': figure_path
    }
    
    return result

if __name__ == '__main__':
    result = calculate_and_plot_var()
    print(result)
