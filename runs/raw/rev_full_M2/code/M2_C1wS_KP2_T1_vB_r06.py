import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 以上库仅导入以满足题目要求，本计算未使用，代码保持轻量且不联网

def main():
    # 给定数据（均为小数形式）
    rf = 0.023          # 无风险利率 2.3%
    E_Rm = 0.094        # 市场期望收益 9.4%
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51
    actual_ret_y = 0.131  # Y 实际收益 13.1%

    # CAPM 期望收益计算：E[Ri] = rf + beta * (E[Rm] - rf)
    market_premium = E_Rm - rf  # 市场风险溢价
    er_x = rf + beta_x * market_premium
    er_y = rf + beta_y * market_premium
    er_z = rf + beta_z * market_premium

    # Alpha_Y = 实际收益 - CAPM 预测收益
    alpha_y = actual_ret_y - er_y

    # 结果按指定键名存入字典
    result = {
        'er_x': er_x,
        'er_y': er_y,
        'er_z': er_z,
        'alpha_y': alpha_y
    }

    # 输出结果，满足投屏可读性
    print("CAPM 计算结果（所有数值均为小数形式）:")
    for key, value in result.items():
        # 同时以百分比形式展示，便于理解
        print(f"{key}: {value:.6f}  ({value*100:.4f}%)")

if __name__ == "__main__":
    main()
