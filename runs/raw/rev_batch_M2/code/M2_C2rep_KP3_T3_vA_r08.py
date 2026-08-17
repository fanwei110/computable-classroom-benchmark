import numpy as np

# 债券参数（假设半年付息，国际惯例）
face_value = 100.0        # 面值
coupon_rate = 0.046       # 年票息率
ytm = 0.053               # 到期收益率（年化）
maturity = 7              # 剩余年限
freq = 2                  # 每年付息次数
delta_y = 0.0080          # 收益率上升 80 个基点

# 构造现金流时间（以年为单位）
n = int(maturity * freq)                          # 总付息期数
t_arr = np.arange(1, n + 1) / freq               # 各期现金流发生时间（年）
coupon = face_value * coupon_rate / freq
cf_arr = np.full(n, coupon)
cf_arr[-1] += face_value                         # 最后一期加入本金

# 各期贴现因子
disc = (1 + ytm / freq) ** (-np.arange(1, n + 1))
# 各期现金流现值
pv = cf_arr * disc

# 当前价格
price = np.sum(pv)

# 麦考利久期（年）
mac_dur = np.sum(t_arr * pv) / price

# 修正久期（年）
mod_dur = mac_dur / (1 + ytm / freq)

# 凸性（标准离散公式，年单位调整）
# 凸性 = 1/(P*(1+y/f)^2) * sum( t*(t+1/f)*CF_t / (1+y/f)^t ) 注意这里 t 以年为单位。
# 更稳健：直接用修正久期对收益率的二阶导定义。
convexity = np.sum(cf_arr * t_arr * (t_arr + 1/freq) * disc) / (price * (1 + ytm / freq)**2)

# 使用修正久期与凸性估算价格变动比例
delta_p_pct_approx = -mod_dur * delta_y + 0.5 * convexity * delta_y ** 2

# 跌幅（正数百分比），即价格大约下跌的百分比
price_drop_pct = -delta_p_pct_approx * 100.0

# 存入结果字典
result = {
    'price_drop_pct': round(price_drop_pct, 6)  # 保留6位小数，确保可复现
}

# 输出结果供投屏展示
if __name__ == "__main__":
    print("=== 债券敏感性分析 ===")
    print(f"面值: {face_value}, 票息: {coupon_rate*100}%, 收益率: {ytm*100}%")
    print(f"期限: {maturity}年, 付息频率: 每半年")
    print(f"当前价格: {price:.6f}")
    print(f"麦考利久期: {mac_dur:.6f} 年")
    print(f"修正久期:   {mod_dur:.6f} 年")
    print(f"凸性:       {convexity:.6f}")
    print(f"收益率变化: +{delta_y*100} 基点")
    print(f"价格变动比例（近似）: {delta_p_pct_approx*100:.4f}%")
    print(f"跌幅估算:   {price_drop_pct:.4f}%")
    print("\n结果字典:")
    print(result)
