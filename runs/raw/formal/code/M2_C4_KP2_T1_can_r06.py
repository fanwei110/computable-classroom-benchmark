import pandas as pd

# ---------- 给定参数 ----------
rf = 0.023          # 无风险利率
rm = 0.094          # 市场期望收益
market_premium = rm - rf   # 市场风险溢价

# 各股票 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# Y 股票实际收益
actual_return_y = 0.131

# ---------- 1. CAPM期望收益计算 ----------
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ---------- 2. 计算 alpha_y ----------
alpha_y = actual_return_y - er_y

# ---------- 3. 填入结果字典 ----------
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 便于课堂展示，打印 DataFrame
df = pd.DataFrame(
    data={
        '股票': ['X', 'Y', 'Z', 'Y(实际)'],
        'Beta': [beta_x, beta_y, beta_z, beta_y],
        'CAPM期望收益(小数)': [er_x, er_y, er_z, None],
        '实际收益(小数)': [None, actual_return_y, None, actual_return_y],
        'Alpha(小数)': [None, alpha_y, None, alpha_y]
    }
).set_index('股票')

print("=== CAPM 与 Alpha 计算结果 ===")
print(f"无风险利率 (rf): {rf:.4f}  ({rf*100:.2f}%)")
print(f"市场期望收益 (rm): {rm:.4f}  ({rm*100:.2f}%)")
print(f"市场风险溢价 (rm-rf): {market_premium:.4f}  ({market_premium*100:.2f}%)")
print()
print(df.to_string(float_format=lambda x: f"{x:.6f}" if pd.notna(x) else 'N/A'))
print()
print("结果字典 result:")
print(result)
