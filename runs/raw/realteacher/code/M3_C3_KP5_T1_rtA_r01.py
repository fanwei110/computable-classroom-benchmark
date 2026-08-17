import scipy.stats as stats
import math

result = {
    'var_95_1d': 1850000 * stats.norm.ppf(0.95) * (0.218 / math.sqrt(252)),
    'var_99_10d': 1850000 * stats.norm.ppf(0.99) * (0.218 * math.sqrt(10 / 252))
}

# 保留两位小数输出符合金融金额惯例
result = {k: round(v, 2) for k, v in result.items()}
