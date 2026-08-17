import numpy as np

# ================= 债券参数设定 =================
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率 4.6%
maturity = 7              # 期限 7 年
ytm = 0.053               # 到期收益率 5.3%

# ================= 现金流构建 =================
# 每年支付的票息
coupon_payment = face_value * coupon_rate

# 生成时间序列与对应的现金流
times = np.arange(1, maturity + 1)
cash_flows = np.full(maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期归还本金

# ================= 1. 计算价格 =================
# 按年复利贴现
discount_factors = (1 + ytm) ** times
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# ================= 2. 计算久期 =================
# 麦考利久期 = Σ[t * PV(CF_t)] / P
macaulay_duration = np.sum(times * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1+y)
modified_duration = macaulay_duration / (1 + ytm)

# ================= 3. 计算凸性 =================
# 凸性 = Σ[t(t+1) * CF_t / (1+y)^(t+2)] / P
convexity = np.sum(times * (times + 1) * cash_flows / (1 + ytm) ** (times + 2)) / price

# ================= 4. 填充结果 =================
# 转换为原生Python浮点数以保证后续处理(如JSON序列化)的兼容性
result = {
    'price': float(price),
    'macaulay_duration_years': float(macaulay_duration),
    'modified_duration_years': float(modified_duration),
    'convexity': float(convexity)
}

# 控制台输出展示（供课堂投屏验证）
if __name__ == "__main__":
    print(f"债券价格 (Price): {result['price']:.4f}")
    print(f"麦考利久期 (Macaulay Duration): {result['macaulay_duration_years']:.4f} 年")
    print(f"修正久期 (Modified Duration): {result['modified_duration_years']:.4f} 年")
    print(f"凸性 (Convexity): {result['convexity']:.4f} 年^2")
