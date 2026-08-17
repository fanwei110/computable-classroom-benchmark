import numpy as np

P = 1_850_000
sigma = 0.218
z_95 = 1.645
z_99 = 2.326

var_95_1d = P * z_95 * sigma * np.sqrt(1 / 252)
var_99_10d = P * z_99 * sigma * np.sqrt(10 / 252)

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}
