# 计算归因效应
# 组合
w_p = [0.45, 0.35, 0.20]
r_p = [0.083, 0.021, -0.014]
# 基准
w_b = [0.40, 0.40, 0.20]
r_b = [0.067, 0.034, -0.009]

# 总收益
R_p = sum(w * r for w, r in zip(w_p, r_p))  # 0.0419
R_b = sum(w * r for w, r in zip(w_b, r_b))  # 0.0386

# 配置效应: (w_p - w_b) * (r_b - R_b)
alloc = sum((wp - wb) * (rb - R_b) for wp, wb, rb in zip(w_p, w_b, r_b))
# 选择效应: w_b * (r_p - r_b)
select = sum(wb * (rp - rb) for wb, rp, rb in zip(w_b, r_p, r_b))
# 交互效应: (w_p - w_b) * (r_p - r_b)
interact = sum((wp - wb) * (rp - rb) for wp, wb, rp, rb in zip(w_p, w_b, r_p, r_b))

result = {
    'sharpe_annual': None,  # 第一问缺失基金日收益序列，无法计算
    'allocation_effect': round(alloc, 6),    # 0.00165
    'selection_effect': round(select, 6),    # 0.0002
    'interaction_effect': round(interact, 6) # 0.00145
}
