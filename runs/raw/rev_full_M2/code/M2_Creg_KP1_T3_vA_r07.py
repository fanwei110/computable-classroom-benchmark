import numpy as np

def main():
    # 给定参数
    sigma_A = 0.184      # 资产 A 年化波动率
    sigma_B = 0.297      # 资产 B 年化波动率
    w_A = 0.6            # A 权重
    w_B = 0.4            # B 权重
    rho_before = 0.3     # 原相关系数
    rho_after = 0.8      # 新相关系数

    # 组合方差计算函数
    def portfolio_vol(w1, w2, s1, s2, rho):
        var = (w1 * s1)**2 + (w2 * s2)**2 + 2 * w1 * w2 * s1 * s2 * rho
        return np.sqrt(var)

    vol_before = portfolio_vol(w_A, w_B, sigma_A, sigma_B, rho_before)
    vol_after  = portfolio_vol(w_A, w_B, sigma_A, sigma_B, rho_after)

    # 按输出契约构建结果字典
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    # 打印以便查看（保留足够精度）
    print(result)

if __name__ == "__main__":
    main()
