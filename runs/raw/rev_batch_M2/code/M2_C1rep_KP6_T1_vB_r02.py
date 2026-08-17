# 由于缺少基金的日收益率序列数据，无法计算年化夏普比率，将其设为 None。
# 归因分析基于提供的数据计算配置效应、选择效应和交互效应。

# 输入数据
weights_p = [0.45, 0.35, 0.2]          # 组合行业权重
returns_p = [0.083, 0.021, -0.014]     # 组合行业收益
weights_b = [0.4, 0.4, 0.2]            # 基准行业权重
returns_b = [0.067, 0.034, -0.009]     # 基准行业收益

# 计算归因效应（Brinson 模型）
allocation_effect = sum((wp - wb) * rb for wp, wb, rb in zip(weights_p, weights_b, returns_b))
selection_effect = sum(wb * (rp - rb) for wb, rp, rb in zip(weights_b, returns_p, returns_b))
interaction_effect = sum((wp - wb) * (rp - rb) for wp, wb, rp, rb in zip(weights_p, weights_b, returns_p, returns_b))

# 结果字典
result = {
    'sharpe_annual': None,               # 无法计算：缺少基金日收益率序列
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 显示结果
result
