import numpy as np  # 本脚本只用到基本运算，numpy 未强制使用但符合课程允许的库

def main():
    # 给定参数（小数表示）
    beta = 1.42
    market_return_monthly = -0.058  # 上个月市场跌了 5.8%
    rf_annual = 0.047               # 年化无风险利率 4.7%

    # 1. 将年无风险利率按简单除法折算为月利率
    rf_monthly = rf_annual / 12

    # 2. 在月度层面套用 CAPM：E(R) = Rf + beta * (Rm - Rf)
    capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

    # 3. 按要求填充结果字典
    result = {
        'capm_return_monthly': capm_return_monthly
    }

    # 输出结果供教师投屏查看
    print(result)
    return result

if __name__ == "__main__":
    result = main()
