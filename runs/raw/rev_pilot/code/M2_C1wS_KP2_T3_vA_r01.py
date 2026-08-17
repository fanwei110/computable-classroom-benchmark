import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ============================================================
# 题目：一只 beta=1.42 的股票，上个月市场跌了 5.8%，
#       无风险利率为每年 4.7%。按 CAPM 计算该股票上个月
#       的预期（本该有的）收益。
# ============================================================

# 给定参数
beta = 1.42
market_return_monthly = -0.058          # 市场月度收益（-5.8%）
risk_free_annual = 0.047                # 年化无风险利率 4.7%

# ------------------------------------------------------------
# 1. 年化无风险利率折算为月利率
# 假设：采用单利折算，即月利率 = 年利率 / 12。
# 在实务与教学中，若无特别说明，通常按比例折算。
# ------------------------------------------------------------
risk_free_monthly = risk_free_annual / 12.0

# ------------------------------------------------------------
# 2. 套用 CAPM 公式（月度层面）
# E(R_i) = R_f + beta_i * (E(R_m) - R_f)
# 其中 E(R_m) 是市场月度收益，R_f 是月度无风险利率。
# ------------------------------------------------------------
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# ============================================================
# 按要求构造输出字典
# ============================================================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 仅用于本地验证或课堂投屏展示（不会影响最终 result 结构）
if __name__ == '__main__':
    print(f"月无风险利率: {risk_free_monthly:.6f} ({risk_free_monthly*100:.4f}%)")
    print(f"市场月度收益: {market_return_monthly:.4%}")
    print(f"股票 beta     : {beta}")
    print(f"CAPM 预期月度收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
    print("\nresult 字典内容:", result)
