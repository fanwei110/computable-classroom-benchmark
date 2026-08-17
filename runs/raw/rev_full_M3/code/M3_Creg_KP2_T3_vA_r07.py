import numpy as np

def calculate_capm_expected_return():
    """
    根据资本资产定价模型（CAPM）计算股票的预期月收益率。
    公式: E(Ri) = Rf + β * (Rm - Rf)
    """
    # 已知参数
    beta = 1.42                     # 股票的 Beta 值
    market_return_monthly = -0.058  # 市场上个月的收益率 (-5.8%)
    risk_free_rate_annual = 0.047   # 无风险年利率 (4.7%)
    
    # 将年化无风险利率转换为月度无风险利率
    # 金融学标准惯例中，将年化无风险利率折算为月度利率通常使用简单除法
    risk_free_rate_monthly = risk_free_rate_annual / 12
    
    # 应用 CAPM 公式
    # 预期收益率 = 无风险月利率 + Beta * (市场收益率 - 无风险月利率)
    capm_return_monthly = (risk_free_rate_monthly + 
                           beta * (market_return_monthly - risk_free_rate_monthly))
    
    # 按照输出契约构建结果字典
    result = {
        'capm_return_monthly': capm_return_monthly
    }
    
    return result

if __name__ == "__main__":
    result = calculate_capm_expected_return()
    print(result)
