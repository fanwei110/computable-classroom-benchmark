import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
V = 1_850_000        # 头寸价值（人民币元）
sigma_ann = 0.218    # 年化收益波动率（小数表示）
trading_days = 252   # 每年交易日数

# ==================== 步骤 1：去年化波动率到一日 ====================
# 波动率按 sqrt(T) 缩放，从年化转换为一日
sigma_daily = sigma_ann / np.sqrt(trading_days)

# ==================== 步骤 2：单尾正态分位数 ====================
# 使用 scipy.stats.norm.ppf 计算单尾分位数，均值取零
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤 3：计算 VaR ====================
# 95% 一日 VaR = 头寸价值 × z_95 × 日波动率
var_95_1d = V * z_95 * sigma_daily

# 99% 十日 VaR = 头寸价值 × z_99 × 日波动率 × sqrt(10)
var_99_10d = V * z_99 * sigma_daily * np.sqrt(10)

# ==================== 步骤 4：填充 result ====================
# 报告为正的损失金额，保留两位小数（符合人民币金额习惯）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 打印结果供课堂展示
if __name__ == "__main__":
    print(f"日波动率 (sigma_daily): {sigma_daily:.6f}")
    print(f"95% 单尾正态分位数 (z_95): {z_95:.6f}")
    print(f"99% 单尾正态分位数 (z_99): {z_99:.6f}")
    print("-" * 40)
    print(f"95% 一日 VaR: ¥{result['var_95_1d']:,.2f}")
    print(f"99% 十日 VaR: ¥{result['var_99_10d']:,.2f}")
