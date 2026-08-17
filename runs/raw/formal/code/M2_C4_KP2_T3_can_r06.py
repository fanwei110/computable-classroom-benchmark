import numpy as np

def main():
    # 已知参数
    beta = 1.42
    market_return_monthly = -0.058          # 上月市场跌 5.8%
    rf_annual = 0.047                       # 年化无风险利率 4.7%
    
    # 1. 简单除法折算月无风险利率
    rf_monthly = rf_annual / 12.0
    
    # 2. CAPM 月度期望收益
    capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)
    
    # 3. 输出字典
    result = {
        'capm_return_monthly': capm_return_monthly
    }
    
    # 供教师运行的打印输出
    print(result)
    return result

if __name__ == "__main__":
    main()
