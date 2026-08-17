import numpy as np
from scipy.stats import norm

# ---------- 输入参数 ----------
portfolio_value = 1_850_000.0   # 头寸价值
annual_vol = 0.218              # 年化收益波动率
trading_days = 252              # 一年交易天数（行业惯例）
confidence_95 = 0.95            # 95% 置信水平
confidence_99 = 0.99            # 99% 置信水平

# ---------- Delta-Normal 模型计算 ----------
# 1) 从年化波动率转换为日波动率及十日波动率
# 假设收益率序列独立同分布，均值假设为0（短期VaR计算常规处理）
sigma_daily = annual_vol / np.sqrt(trading_days)
sigma_10d = sigma_daily * np.sqrt(10)

# 2) 标准正态分布对应置信水平的分位数（单尾）
z_95 = norm.ppf(confidence_95)
z_99 = norm.ppf(confidence_99)

# 3) 计算 VaR（正值表示潜在损失金额）
var_95_1d = portfolio_value * z_95 * sigma_daily
var_99_10d = portfolio_value * z_99 * sigma_10d

# ---------- 按契约组织输出 ----------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 如果脚本独立运行，打印结果以供查看
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:,.2f}")
