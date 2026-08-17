import numpy as np

# ==================== 输入数据 ====================
# 百分比转化为小数形式进行计算
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
actual_return_y = 0.131  # 股票 Y 的实际收益 13.1%

# ==================== 步骤1：套用 CAPM 计算期望收益 ====================
# 市场风险溢价
market_premium = rm - rf

# E[Ri] = rf + beta * (E[Rm] - rf)
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ==================== 步骤2：计算 Y 的 Alpha ====================
# Alpha = 实际收益 - CAPM 预期收益
alpha_y = actual_return_y - er_y

# ==================== 步骤3：填充 result ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 控制台输出展示 (供投屏参考) ====================
if __name__ == "__main__":
    print("=== CAPM 与证券市场线计算结果 ===")
    print(f"市场风险溢价 (E[Rm] - Rf): {market_premium:.4%}\n")
    
    print("各股票 CAPM 期望收益:")
    print(f"  E[R_x] = {er_x:.4%}")
    print(f"  E[R_y] = {er_y:.4%}")
    print(f"  E[R_z] = {er_z:.4%}\n")
    
    print(f"股票 Y 的实际收益: {actual_return_y:.4%}")
    print(f"股票 Y 的 Alpha:   {alpha_y:.4%}")
    
    print("\n=== result 字典内容 ===")
    for k, v in result.items():
        print(f"'{k}': {v}")
