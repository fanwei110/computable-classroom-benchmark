import numpy as np

def main():
    # 给定参数
    rf = 0.023          # 无风险利率
    rm = 0.094          # 市场期望收益
    mrp = rm - rf       # 市场风险溢价

    # 各股票的 beta
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51

    # 计算 CAPM 期望收益
    er_x = rf + beta_x * mrp
    er_y = rf + beta_y * mrp
    er_z = rf + beta_z * mrp

    # 股票 Y 的实际收益与 alpha
    actual_y = 0.131
    alpha_y = actual_y - er_y

    # 存储结果
    result = {
        'er_x': er_x,
        'er_y': er_y,
        'er_z': er_z,
        'alpha_y': alpha_y
    }

    # 打印结果以确保可复现
    print(result)
    return result

if __name__ == "__main__":
    result = main()
