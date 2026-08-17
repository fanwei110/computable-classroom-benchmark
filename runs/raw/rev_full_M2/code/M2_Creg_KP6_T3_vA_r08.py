import numpy as np
import pandas as pd
import os

# -------------------- 数据准备 --------------------
# 优先从课程数据文件读取 'fund' 列。
# 如果文件不存在，则使用下方的示例数据（以便复现）。
file_path = 'course_data.csv'  # 根据实际情况调整文件名
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    if 'fund' in df.columns:
        returns = df['fund'].dropna().values
        print("已从文件加载 fund 列数据。")
    else:
        raise ValueError("文件中不存在 'fund' 列，请检查列名。")
else:
    # 示例月度收益率数据（以小数形式表示）
    returns = np.array([0.008, 0.012, -0.009, 0.025, -0.003,
                        0.007, 0.015, -0.011, 0.020, 0.013,
                       -0.006, 0.018])
    print("警告：未找到数据文件，使用内置示例数据。")

# -------------------- 参数设置 --------------------
rf_annual = 0.021          # 年化无风险利率
freq = 12                  # 数据频率（12 代表月度，252 代表日度）

# -------------------- 计算年化夏普比率 --------------------
rf_period = rf_annual / freq                      # 单期无风险利率
mean_return = np.mean(returns)                    # 平均单期收益率
excess_return = mean_return - rf_period           # 平均超额收益率
std_period = np.std(returns, ddof=1)              # 单期收益率的标准差（样本标准差）
sharpe_annual = np.sqrt(freq) * (excess_return / std_period)  # 年化夏普比率

# -------------------- 保存结果 --------------------
result = {'sharpe_annual': sharpe_annual}

# 输出结果
print(f"年化夏普比率: {sharpe_annual:.4f}")
print(result)
