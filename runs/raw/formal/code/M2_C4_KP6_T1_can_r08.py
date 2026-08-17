import pandas as pd
import numpy as np

def main():
    # =========================
    # 第一部分：年化夏普比率
    # =========================
    # 读取日收益数据
    df = pd.read_csv("data/market_snapshot_v1.csv")
    fund_daily = df["fund"]  # 小数形式的日收益

    # 无风险利率（年化）折算为日利率
    rf_annual = 0.021
    rf_daily = rf_annual / 252.0

    # 日超额收益
    excess_daily = fund_daily - rf_daily

    # 样本均值与样本标准差（ddof=1）
    mu_d = excess_daily.mean()
    sigma_d = excess_daily.std(ddof=1)

    # 年化夏普比率
    sharpe_annual = np.sqrt(252.0) * mu_d / sigma_d

    # =========================
    # 第二部分：Brinson归因
    # =========================
    # 组合
    w_p = np.array([0.45, 0.35, 0.20])
    r_p = np.array([0.083, 0.021, -0.014])

    # 基准
    w_b = np.array([0.40, 0.40, 0.20])
    r_b = np.array([0.067, 0.034, -0.009])

    # 配置效应：Σ(w_p - w_b) * r_b
    allocation_effect = np.sum((w_p - w_b) * r_b)

    # 选择效应：Σ w_b * (r_p - r_b)
    selection_effect = np.sum(w_b * (r_p - r_b))

    # 交互效应：Σ (w_p - w_b) * (r_p - r_b)
    interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

    # =========================
    # 输出结果
    # =========================
    result = {
        'sharpe_annual': sharpe_annual,
        'allocation_effect': allocation_effect,
        'selection_effect': selection_effect,
        'interaction_effect': interaction_effect
    }

    # 打印便于教师查看
    for k, v in result.items():
        print(f"{k}: {v:.6f}")

    return result

if __name__ == "__main__":
    result = main()
