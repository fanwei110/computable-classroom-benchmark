result = {
    'sharpe_annual': None,  # 缺少fund日收益数据列，无法计算具体值。若有数据df['fund']，计算代码为：((df['fund'].mean() - 0.021/252) / df['fund'].std()) * (252**0.5)
    'allocation_effect': 0.00165,
    'selection_effect': 0.0002,
    'interaction_effect': 0.00145
}
