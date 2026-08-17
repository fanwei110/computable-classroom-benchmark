import numpy as np

def main():
    # 给定数据
    rf = 0.023          # 无风险利率
    market_ret = 0.094  # 市场期望收益
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51
    actual_ret_y = 0.131  # Y的实际年收益

    # 市场风险溢价
    market_premium = market_ret - rf

    # 1. CAPM 期望收益计算
    er_x = rf + beta_x * market_premium
    er_y = rf + beta_y * market_premium
    er_z = rf + beta_z * market_premium

    # 2. Y 的 alpha
    alpha_y = actual_ret_y - er_y

    # 3. 存入 result 字典
    result = {
        'er_x': er_x,
        'er_y': er_y,
        'er_z': er_z,
        'alpha_y': alpha_y
    }

    # 输出结果以供课堂查看
    print("CAPM 计算结果：")
    print(f"无风险利率: {rf:.4f} ({rf*100:.2f}%)")
    print(f"市场期望收益: {market_ret:.4f} ({market_ret*100:.2f}%)")
    print(f"市场风险溢价: {market_premium:.4f} ({market_premium*100:.2f}%)")
    print(f"X 的 beta: {beta_x}, 期望收益: {er_x:.6f} ({er_x*100:.4f}%)")
    print(f"Y 的 beta: {beta_y}, 期望收益: {er_y:.6f} ({er_y*100:.4f}%)")
    print(f"Z 的 beta: {beta_z}, 期望收益: {er_z:.6f} ({er_z*100:.4f}%)")
    print(f"Y 实际收益: {actual_ret_y:.4f} ({actual_ret_y*100:.2f}%)")
    print(f"Y 的 alpha: {alpha_y:.6f} ({alpha_y*100:.4f}%)")
    
    return result

# 保持脚本独立运行，并确保 result 被赋值
if __name__ == "__main__":
    result = main()
