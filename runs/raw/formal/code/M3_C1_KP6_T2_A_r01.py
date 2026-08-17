# ============================================================
# 输出契约
# ============================================================

result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

print("=" * 60)
print("RESULT:")
print(f"  rolling_sharpe_last = {result['rolling_sharpe_last']:.6f}")
print(f"  figure_path = {result['figure_path']}")
print("=" * 60)
