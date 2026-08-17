import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
RISK_FREE_RATE = 0.023   # 无风险利率
MARKET_RETURN = 0.094    # 市场期望收益
# ================================================

def plot_sml(rf: float, rm: float):
    """绘制证券市场线并标注股票X、Y、Z"""
    # 市场风险溢价（SML 斜率）
    market_premium = rm - rf
    
    # 生成 β 网格
    beta_vals = np.linspace(0, 2, 100)
    er_vals = rf + market_premium * beta_vals
    
    # 股票数据：名称、beta、收益
    stocks = {
        'X': (0.62, 0.081),
        'Y': (1.18, 0.131),
        'Z': (1.51, 0.099)
    }
    
    # 绘图
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(beta_vals, er_vals, 'b-', linewidth=2, label='SML')
    
    # 标注市场组合点 (β=1, rm)
    ax.scatter(1.0, rm, color='green', s=100, zorder=5, label='Market (β=1)')
    ax.annotate('Market', (1.0, rm), textcoords="offset points",
                xytext=(5, 5), fontsize=9, color='green')
    
    # 标注无风险资产 (β=0, rf)
    ax.scatter(0.0, rf, color='red', s=100, zorder=5, label='Risk-free (β=0)')
    ax.annotate('RF', (0.0, rf), textcoords="offset points",
                xytext=(5, -10), fontsize=9, color='red')
    
    # 标注股票 X, Y, Z
    colors = ['orange', 'purple', 'brown']
    for (name, (beta, ret)), color in zip(stocks.items(), colors):
        ax.scatter(beta, ret, color=color, s=100, zorder=5, label=f'Stock {name}')
        ax.annotate(name, (beta, ret), textcoords="offset points",
                    xytext=(5, 5), fontsize=9, color=color)
    
    ax.set_xlabel('Beta (β)', fontsize=12)
    ax.set_ylabel('Expected Return', fontsize=12)
    ax.set_title('Security Market Line (SML)', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=9)
    
    # 设置 y 轴显示为百分比格式
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))
    
    plt.tight_layout()
    
    # 保存图像
    figure_path = os.path.abspath('sml_plot.png')
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)   # 释放内存
    return market_premium, figure_path

def main():
    rf = RISK_FREE_RATE
    rm = MARKET_RETURN
    
    # 计算斜率
    slope = rm - rf
    # 计算 β=1.27 处的期望收益
    beta_target = 1.27
    er_target = rf + slope * beta_target
    
    # 绘图并获取图片路径
    _, figure_path = plot_sml(rf, rm)
    
    # 将结果存入字典
    result = {
        'sml_slope': slope,
        'er_at_beta_127': er_target,
        'figure_path': figure_path
    }
    
    # 输出结果供查看（也满足输出契约，便于直接复制）
    print("=== 结果字典 ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    return result

if __name__ == "__main__":
    result = main()
