import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats  # 虽然本计算未用到，但按要求导入

# ===================== 参数设定 =====================
beta = 1.42                     # 股票贝塔
market_return_monthly = -0.058  # 上个月市场收益率（-5.8%）
risk_free_annual = 0.047        # 年化无风险利率（4.7%）

# 将年化无风险利率折算为月利率
# 假设：年利率为单利报价（APR），直接按月等分，这是CAPM常用处理方式
risk_free_monthly = risk_free_annual / 12.0

# ===================== CAPM 计算 =====================
# 公式：E(R_i) = R_f + β * (R_m - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# ===================== 输出结果 =====================
result = {
    'capm_return_monthly': capm_return_monthly
}

if __name__ == "__main__":
    print("证券市场线（CAPM）计算")
    print(f"年化无风险利率: {risk_free_annual*100:.2f}%")
    print(f"折算月无风险利率: {risk_free_monthly*100:.4f}%")
    print(f"市场月收益率: {market_return_monthly*100:.2f}%")
    print(f"股票贝塔: {beta}")
    print(f"CAPM预期月收益率: {capm_return_monthly*100:.4f}%")
    print("\n结果字典:")
    print(result)
