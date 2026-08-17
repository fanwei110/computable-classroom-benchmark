import numpy as np
from scipy.stats import norm

def main():
    # 输入参数
    position = 2_700_000          # 头寸金额
    annual_vol = 0.24             # 年化波动率
    trading_days = 252            # 年交易日数
    confidence = 0.95             # 置信水平

    # 单日波动率
    daily_vol = annual_vol / np.sqrt(trading_days)

    # 对应置信水平的标准正态分位数（95% 右尾，取 z 值）
    z_score = norm.ppf(confidence)

    # 95% 单日 VaR (损失用正数表示)
    var_95_1d = position * daily_vol * z_score

    # 输出契约
    result = {
        'var_95_1d': var_95_1d
    }

    print(result)

if __name__ == "__main__":
    main()
