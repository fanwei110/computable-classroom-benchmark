# 创建最终结果字典
result = {
    'hist_var_95_1d': var_amount_95,  # 95%置信水平的一日历史VaR金额
    'figure_path': figure_path         # 图表文件路径
}

# 打印结果
print("=" * 60)
print("最终结果:")
print(f"95%历史法一日VaR: ¥{result['hist_var_95_1d']:,.2f}")
print(f"图表路径: {result['figure_path']}")
print("=" * 60)

# 验证文件是否存在
if os.path.exists(result['figure_path']):
    print(f"✓ 图表文件已成功保存: {result['figure_path']}")
    file_size = os.path.getsize(result['figure_path'])
    print(f"✓ 文件大小: {file_size:,} bytes")
else:
    print("✗ 图表文件未找到")
