import math

# 输入参数
wA = 0.6
wB = 0.4
sigmaA = 0.184
sigmaB = 0.297
rho_before = 0.3
rho_after = 0.8

# 计算组合方差函数
def portfolio_vol(wA, wB, sigmaA, sigmaB, rho):
    var = (wA**2 * sigmaA**2) + (wB**2 * sigmaB**2) + (2 * wA * wB * rho * sigmaA * sigmaB)
    return math.sqrt(var)

# 计算前后波动率
vol_before = portfolio_vol(wA, wB, sigmaA, sigmaB, rho_before)
vol_after = portfolio_vol(wA, wB, sigmaA, sigmaB, rho_after)

# 存入字典，保留四位小数
result = {
    'vol_before_annual': round(vol_before, 4),
    'vol_after_annual': round(vol_after, 4)
}

# 若需要查看结果，可以打印（实际使用时仅输出字典）
print(result)
