import numpy as np

# ================= 输入参数 =================
beta = 1.42                      # 股票的 Beta 系数
market_return_monthly = -0.058   # 大盘上个月收益率（跌5.8%即-0.058）
rf_annual = 0.047                # 年化无风险利率（4.7%即0.047）

# ================= 步骤1：年无风险利率折算为月利率 =================
# 假设：采用复利折算（复合增长率），这更符合金融学中不同期限收益率转换的严谨逻辑
# 公式：rf_monthly = (1 + rf_annual)^(1/12) - 1
rf_monthly = (1 + rf_annual) ** (1 / 12) - 1

# ================= 步骤2：月度层面套用 CAPM =================
# CAPM 公式：E(R_i) = R_f + β * (E(R_m) - R_f)
# 此处将大盘上个月的实际收益作为市场组合的已实现期望收益 E(R_m) 代入
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# ================= 结果输出 =================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 课堂投屏展示辅助信息（可选打印，方便教师讲解）
if __name__ == "__main__":
    print(f"--- CAPM 月度收益计算 ---")
    print(f"年化无风险利率: {rf_annual:.2%}")
    print(f"月度无风险利率(复利折算): {rf_monthly:.6f} ({rf_monthly:.4%})")
    print(f"市场月度收益率: {market_return_monthly:.2%}")
    print(f"Beta系数: {beta}")
    print(f"------------------------")
    print(f"按CAPM计算的月度期望收益: {capm_return_monthly:.6f} ({capm_return_monthly:.4%})")
    print(f"\n最终结果字典 result: {result}")
