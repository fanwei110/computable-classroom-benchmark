import numpy as np
from scipy.optimize import brentq

def calculate_bond_price_and_sensitivity():
    """
    计算7年期债券（面值100，票面利率4.6%，收益率5.3%）的利率敏感性
    并估算收益率上升80个基点的价格影响
    """
    
    # 债券参数
    face_value = 100.0        # 面值
    coupon_rate = 0.046       # 票面利率 4.6%
    ytm = 0.053               # 当前到期收益率 5.3%
    maturity = 7              # 到期年限
    coupon_frequency = 1      # 假设年付息一次
    
    # 构建现金流时间序列
    cash_flow_times = np.arange(1, maturity + 1)  # 第1年到第7年
    coupon_payment = face_value * coupon_rate     # 每年票息 = 4.6
    
    # 现金流（最后一期包含本金和票息）
    cash_flows = np.full(maturity, coupon_payment)
    cash_flows[-1] += face_value  # 最后一年 = 票息 + 本金 = 104.6
    
    # 贴现因子
    discount_factors = (1 + ytm) ** (-cash_flow_times)
    
    # 计算债券价格 PV
    present_values = cash_flows * discount_factors
    bond_price = np.sum(present_values)
    
    # 计算麦考利久期和修正久期
    # 麦考利久期 = Σ(t × PV_t) / Σ(PV_t)
    weighted_times = cash_flow_times * present_values
    macaulay_duration = np.sum(weighted_times) / bond_price
    
    # 修正久期 = 麦考利久期 / (1 + ytm)
    modified_duration = macaulay_duration / (1 + ytm)
    
    # 计算凸性
    # 凸性 = Σ[t × (t+1) × PV_t] / [Σ(PV_t) × (1 + ytm)^2]
    convexity_weights = cash_flow_times * (cash_flow_times + 1) * present_values
    convexity = np.sum(convexity_weights) / (bond_price * (1 + ytm)**2)
    
    # 收益率变动（上升80个基点 = 0.008）
    delta_y = 0.008  # 80 bp upward
    
    # 使用久期和凸性估算价格变动百分比
    # ΔP/P ≈ -Modified_Duration × Δy + 0.5 × Convexity × (Δy)^2
    price_change_pct_approx = -modified_duration * delta_y + 0.5 * convexity * (delta_y)**2
    
    # 实际精确计算：收益率上升后的新价格
    ytm_new = ytm + delta_y  # 5.3% + 0.8% = 6.1%
    discount_factors_new = (1 + ytm_new) ** (-cash_flow_times)
    present_values_new = cash_flows * discount_factors_new
    bond_price_new = np.sum(present_values_new)
    
    # 精确的价格变动百分比
    price_change_pct_exact = (bond_price_new - bond_price) / bond_price * 100
    
    # 输出结果
    print(f"债券当前价格 (YTM={ytm*100:.1f}%): {bond_price:.4f}")
    print(f"债券新价格 (YTM={ytm_new*100:.1f}%): {bond_price_new:.4f}")
    print(f"麦考利久期: {macaulay_duration:.4f} 年")
    print(f"修正久期: {modified_duration:.4f}")
    print(f"凸性: {convexity:.4f}")
    print(f"\n收益率上升80bp的影响:")
    print(f"  - 近似跌幅（久期+凸性）: {price_change_pct_approx*100:.4f}%")
    print(f"  - 精确跌幅: {price_change_pct_exact:.4f}%")
    
    # 存储结果
    result = {
        'price_drop_pct': round(price_change_pct_exact, 4)
    }
    
    return result

# 执行计算
result = calculate_bond_price_and_sensitivity()

print(f"\n{'='*50}")
print(f"输出结果字典:")
print(f"result = {result}")
print(f"{'='*50}")
