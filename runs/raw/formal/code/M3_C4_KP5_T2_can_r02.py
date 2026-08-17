import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，防止弹窗且确保在无GUI环境下可复现运行
import matplotlib.pyplot as plt

def calculate_and_plot_var():
    # ==================== 参数设置 ====================
    position = 1_000_000            # 头寸金额（人民币元）
    confidence_level = 0.95         # 置信水平（可调参数）
    csv_path = 'data/market_snapshot_v1.csv'
    figure_path = 'hist_var_plot.png'

    # ==================== 1. 读取数据并构造日损益 ====================
    # 读取CSV数据快照
    df = pd.read_csv(csv_path)
    
    # 提取'fund'列的日收益率序列（小数形式）
    daily_returns = df['fund']
    
    # 构造日损益（P&L）：收益率 × 头寸规模
    pnl = daily_returns * position

    # ==================== 2. 计算95%一日历史VaR ====================
    # 损失分位数对应的下尾概率 alpha
    alpha = 1 - confidence_level
    
    # 使用numpy默认的线性插值法计算经验分位数
    # np.quantile 默认 method='linear'，符合课程计算约定
    var_pnl_point = np.quantile(pnl, alpha)
    
    # VaR报告为正的损失金额：取分位数的相反数
    # （若分位数为负，损失为正；若极端盈利分位数为正，则VaR为负，符合金融惯例）
    hist_var_95_1d = -var_pnl_point

    # ==================== 3. 画直方图并加带标注的VaR线 ====================
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制损益分布直方图
    ax.hist(pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

    # 绘制VaR竖线
    ax.axvline(var_pnl_point, color='red', linestyle='--', linewidth=2,
               label=f'{confidence_level*100:.0f}% 1-Day Hist VaR\n'
                     f'= {hist_var_95_1d:,.2f} RMB')

    # 添加标注与图表格式
    ax.set_title(f'Daily P&L Distribution and {confidence_level*100:.0f}% Historical VaR')
    ax.set_xlabel('P&L (RMB)')
    ax.set_ylabel('Frequency')
    ax.legend(loc='upper left', fontsize=12, framealpha=1)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # ==================== 4. 保存图形并填充结果 ====================
    fig.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 按输出契约要求存入字典
    result = {
        'hist_var_95_1d': hist_var_95_1d,
        'figure_path': figure_path
    }

    return result

if __name__ == '__main__':
    result = calculate_and_plot_var()
    print(result)
