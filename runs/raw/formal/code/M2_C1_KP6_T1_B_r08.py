# 由于未提供基金的日收益率序列，无法计算年化夏普比率，因此设为 None
# 如需计算，请提供基金的日收益率数据。

# 归因分析计算
# 组合权重和收益
w_p = [0.45, 0.35, 0.2]
r_p = [0.083, 0.021, -0.014]

# 基准权重和收益
w_b = [0.4, 0.4, 0.2]
r_b = [0.067, 0.034, -0.009]

# 基准总收益
Rb = sum(w_b[i] * r_b[i] for i in range(3))

# 配置效应： sum((w_p - w_b) * r_b)
allocation_effect = sum((w_p[i] - w_b[i]) * r_b[i] for i in range(3))

# 选择效应： sum(w_b * (r_p - r_b))
selection_effect = sum(w_b[i] * (r_p[i] - r_b[i]) for i in range(3))

# 交互效应： sum((w_p - w_b) * (r_p - r_b))
interaction_effect = sum((w_p[i] - w_b[i]) * (r_p[i] - r_b[i]) for i in range(3))

# 构建结果字典
result = {
    'sharpe_annual': None,  # 缺少日收益序列，无法计算
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}
