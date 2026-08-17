# 假设Vega值为0.15（即隐波每变化1%，期权价格变化0.15元）
vega = 0.15

# 隐波上涨1个点（1%）时的价格变化
price_change = vega * 1  # 因为1个点通常指1%

# 存入result字典
result = {
    'price_change': price_change
}
