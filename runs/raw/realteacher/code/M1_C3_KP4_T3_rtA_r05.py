# 假设Vega已知（例如通过Black-Scholes模型计算得到）
vega = 0.12  # 示例值，表示隐波变化1%时价格变化0.12元

# 隐波涨1个点（0.01）时的价格变化
price_change = vega * 0.01

# 存入结果字典
result = {
    'price_change': price_change
}
