import numpy as np

# ==================== 1. 参数设置 ====================
# 假设所有的百分比率在计算中均转换为小数形式，以保证内部一致性
rf = 0.023        # 无风险利率 2.3%
erm = 0.094       # 市场期望收益 9.4%

beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

actual_ry = 0.131 # Y 的实际年收益 13.1%

# ==================== 2. CAPM 计算 ====================
# 套用 CAPM 公式: E[Ri] = rf + beta * (E[Rm] - rf)
er_x = rf + beta_x * (erm - rf)
er_y = rf + beta_y * (erm - rf)
er_z = rf + beta_z * (erm - rf)

# ==================== 3. Alpha 计算 ====================
# Alpha 定义为实际收益偏离证券市场线(SML)预测期望收益的部分
# alpha_y = actual_ry - er_y
alpha_y = actual_ry - er_y

# ==================== 4. 填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 5. 终端输出展示(辅助投屏阅读) ====================
print("="*40)
print("CAPM 与证券市场线计算结果")
print("="*40)
print(f"X 股票期望收益 (er_x): {er_x:.4%}")
print(f"Y 股票期望收益 (er_y): {er_y:.4%}")
print(f"Z 股票期望收益 (er_z): {er_z:.4%}")
print(f"Y 股票 Alpha   (alpha_y): {alpha_y:.4%}")
print("="*40)

# 验证字典内部结构，供直接调用
# print(result)
