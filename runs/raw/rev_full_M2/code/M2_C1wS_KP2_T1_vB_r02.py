import numpy as np

def main():
    # 给定数据
    rf = 0.023      # 无风险利率 2.3%
    e_rm = 0.094    # 市场期望收益 9.4%
    
    # 三只股票的 beta
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51
    
    # 股票 Y 的实际收益
    actual_return_y = 0.131  # 13.1%
    
    # 1. 根据 CAPM 计算每只股票的期望收益
    # E[Ri] = rf + beta * (E[Rm] - rf)
    market_premium = e_rm - rf  # 市场风险溢价
    
    er_x = rf + beta_x * market_premium
    er_y = rf + beta_y * market_premium
    er_z = rf + beta_z * market_premium
    
    # 2. 计算股票 Y 的 alpha
    # alpha_y = 实际收益 - CAPM 期望收益
    alpha_y = actual_return_y - er_y
    
    # 3. 填充结果字典
    result = {
        'er_x': er_x,
        'er_y': er_y,
        'er_z': er_z,
        'alpha_y': alpha_y
    }
    
    # 输出结果，便于课堂演示查看
    print("=== CAPM 计算结果 ===")
    print(f"无风险利率 (rf):         {rf:.4f} ({rf*100:.1f}%)")
    print(f"市场期望收益 (E[Rm]):    {e_rm:.4f} ({e_rm*100:.1f}%)")
    print(f"市场风险溢价:            {market_premium:.4f} ({market_premium*100:.1f}%)")
    print()
    print(f"股票 X beta: {beta_x:.2f}  |  CAPM 期望收益: {er_x:.6f} ({er_x*100:.4f}%)")
    print(f"股票 Y beta: {beta_y:.2f}  |  CAPM 期望收益: {er_y:.6f} ({er_y*100:.4f}%)")
    print(f"股票 Z beta: {beta_z:.2f}  |  CAPM 期望收益: {er_z:.6f} ({er_z*100:.4f}%)")
    print()
    print(f"股票 Y 实际收益: {actual_return_y:.3f} ({actual_return_y*100:.1f}%)")
    print(f"股票 Y alpha:     {alpha_y:.6f} ({alpha_y*100:.4f}%)")
    
    return result

if __name__ == "__main__":
    result = main()
