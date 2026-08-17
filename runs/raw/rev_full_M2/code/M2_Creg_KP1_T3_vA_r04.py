import numpy as np
import pandas as pd

def main():
    # 资产年化波动率
    sigma_A = 0.184
    sigma_B = 0.297
    
    # 组合权重
    w_A = 0.6
    w_B = 0.4
    
    # 相关系数
    rho_before = 0.3
    rho_after = 0.8
    
    # 组合方差计算函数
    def portfolio_variance(w1, w2, s1, s2, rho):
        return (w1**2 * s1**2) + (w2**2 * s2**2) + (2 * w1 * w2 * rho * s1 * s2)
    
    var_before = portfolio_variance(w_A, w_B, sigma_A, sigma_B, rho_before)
    var_after = portfolio_variance(w_A, w_B, sigma_A, sigma_B, rho_after)
    
    vol_before_annual = np.sqrt(var_before)
    vol_after_annual = np.sqrt(var_after)
    
    # 输出契约
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }
    
    print("组合年化波动率结果：")
    print(pd.Series(result))
    
    return result

if __name__ == "__main__":
    result = main()
