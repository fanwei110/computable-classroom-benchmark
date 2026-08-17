import numpy as np
from scipy.stats import norm

def main():
    # ------------------------------
    # 输入参数
    # ------------------------------
    position_value = 2_700_000      # 头寸价值（元）
    annual_vol = 0.24               # 年化波动率
    confidence_level = 0.95         # 置信水平（95%）
    
    # ------------------------------
    # 假设：一年交易天数 = 252
    # 这是业界常用的换算基准，保证内部一致
    # ------------------------------
    trading_days_per_year = 252

    # ------------------------------
    # 1. 年化波动率换算为一日波动率
    # σ_daily = σ_annual / sqrt(252)
    # ------------------------------
    daily_vol = annual_vol / np.sqrt(trading_days_per_year)

    # ------------------------------
    # 2. 计算95%置信水平下的正态分位数（z值）
    # 对于VaR，我们需要左尾分位数（α = 1 - 置信水平 = 0.05）
    # ppf(0.05) 给出负值，取绝对值得到损失的正向度量
    # ------------------------------
    alpha = 1 - confidence_level       # 0.05
    z_score = norm.ppf(alpha)          # 约 -1.64485
    
    # VaR公式：VaR = - 头寸价值 × 日波动率 × z_α
    # 由于 z_α 为负，-z_α 为正，得到损失金额
    var_95_1d = - position_value * daily_vol * z_score

    # ------------------------------
    # 3. 存入结果字典
    # ------------------------------
    result = {
        'var_95_1d': var_95_1d
    }

    # ------------------------------
    # 输出结果
    # ------------------------------
    print("=== 参数法 (Delta-Normal) 一日VaR 计算 ===")
    print(f"头寸价值:           {position_value:,.2f} 元")
    print(f"年化波动率:         {annual_vol*100:.1f}%")
    print(f"交易日/年:          {trading_days_per_year}")
    print(f"日波动率:           {daily_vol:.6f} ({daily_vol*100:.4f}%)")
    print(f"置信水平:           {confidence_level*100:.0f}%")
    print(f"正态分位数 (z):     {-z_score:.5f}")
    print(f"95% 一日VaR:        {var_95_1d:,.2f} 元")
    print("\n结果字典:")
    print(result)

    return result

# 执行脚本
if __name__ == "__main__":
    result = main()
