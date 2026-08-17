import numpy as np

def calculate_capm_monthly_return():
    """
    计算 CAPM 下股票的月度期望收益率
    """
    # 已知参数
    beta = 1.42                   # 股票的 Beta 值
    market_return_monthly = -0.058  # 上个月市场收益率 (-5.8%)
    risk_free_rate_annual = 0.047   # 年化无风险利率 (4.7%)
    
    # 1. 把年无风险利率折算为月利率
    # 假设：给定的年无风险利率为有效年利率(EAR)，采用复利折算方式得到有效月利率。
    # 这样能准确反映1个月资金的真实时间价值。
    risk_free_rate_monthly = np.power(1 + risk_free_rate_annual, 1/12) - 1
    
    # 2. 在月度层面套用 CAPM
    # CAPM 公式: E(R_i) = R_f + Beta * (E(R_m) - R_f)
    # 此处使用给定的上月市场实际收益率作为 E(R_m) 的代理变量
    capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)
    
    # 3. 填充 result
    result = {
        'capm_return_monthly': capm_return_monthly
    }
    
    return result

if __name__ == "__main__":
    result = calculate_capm_monthly_return()
    
    # 输出结果，确保可复现
    print("=== CAPM 月度收益计算结果 ===")
    print(f"结果字典: {result}")
    print(f"按 CAPM 本该收益: {result['capm_return_monthly']:.4%}")
