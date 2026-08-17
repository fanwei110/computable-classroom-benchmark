import numpy as np
from scipy import stats

# ==========================================
// 参数法计算在险价值
// ==========================================

// 给定参数
position = 1850000  # 头寸：185万元，单位：人民币元
annual_vol = 0.218  # 年化波动率：21.8%

// 假设处理：
// 1. 一年按252个交易日计算（金融市场标准假设）
// 2. 短期VaR计算中，假设期望收益率为0（在险价值计算的标准简化假设）
trading_days_per_year = 252

// 步骤1：将年化波动率换算到一日期限
// sigma_1d = sigma_annual / sqrt(T)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

// 步骤2：套用正态分位数（使用scipy获取标准正态分布的逆累积分布函数）
z_95 = stats.norm.ppf(0.95)
z_99 = stats.norm.ppf(0.99)

// 步骤3：计算VaR并缩放期限
// 95%置信水平的一日VaR
// VaR_95_1d = 头寸 * Z_95 * sigma_1d
var_95_1d = position * z_95 * daily_vol

// 99%置信水平的十日VaR
// 先将波动率缩放至10日：sigma_10d = sigma_1d * sqrt(10)
// VaR_99_10d = 头寸 * Z_99 * sigma_10d
vol_10d = daily_vol * np.sqrt(10)
var_99_10d = position * z_99 * vol_10d

// 步骤4：填充 result，保留两位小数（符合人民币最小单位分）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

// 输出结果供课堂投屏展示
print(f"95%置信水平的一日VaR: ¥{result['var_95_1d']:,.2f}")
print(f"99%置信水平的十日VaR: ¥{result['var_99_10d']:,.2f}")
