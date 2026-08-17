import numpy as np
import pandas as pd
from scipy import stats

def main():
    # ============================================================
    # 第一部分：计算年化夏普比率
    # ============================================================
    
    # 读取CSV数据快照
    df = pd.read_csv('data/market_snapshot_v1.csv')
    
    # 提取基金列的日收益
    fund_returns_daily = df['fund'].values
    
    # 无风险利率参数
    annual_risk_free_rate = 0.021  # 2.1%年化
    trading_days_per_year = 252  # 标准假设：252个交易日
    
    # 日化无风险利率
    daily_risk_free_rate = annual_risk_free_rate / trading_days_per_year
    
    # 计算超额收益（基金日收益 - 日无风险利率）
    excess_returns_daily = fund_returns_daily - daily_risk_free_rate
    
    # 计算年化超额收益
    annualized_excess_return = np.mean(excess_returns_daily) * trading_days_per_year
    
    # 计算年化波动率（标准差）
    annualized_volatility = np.std(fund_returns_daily, ddof=1) * np.sqrt(trading_days_per_year)
    
    # 计算年化夏普比率
    sharpe_annual = annualized_excess_return / annualized_volatility
    
    # ============================================================
    # 第二部分：业绩归因分析 - 配置效应、选择效应、交互效应
    # ============================================================
    
    # 投资组合权重
    portfolio_weights = np.array([0.45, 0.35, 0.20])
    
    # 投资组合中各行业的收益
    portfolio_returns = np.array([0.083, 0.021, -0.014])
    
    # 基准权重
    benchmark_weights = np.array([0.40, 0.40, 0.20])
    
    # 基准中各行业的收益
    benchmark_returns = np.array([0.067, 0.034, -0.009])
    
    # 计算整体组合收益和基准收益
    total_portfolio_return = np.sum(portfolio_weights * portfolio_returns)
    total_benchmark_return = np.sum(benchmark_weights * benchmark_returns)
    
    # 配置效应：权重差异 * 基准收益差异（行业表现以基准为准，看配置差异贡献）
    allocation_effect = np.sum(
        (portfolio_weights - benchmark_weights) * (benchmark_returns - total_benchmark_return)
    )
    
    # 选择效应：基准权重 * 收益差异（行业表现中，以组合收益减去基准收益，看选股贡献）
    selection_effect = np.sum(
        benchmark_weights * (portfolio_returns - benchmark_returns)
    )
    
    # 交互效应：权重差异 * 收益差异（配置与选择的交互部分）
    interaction_effect = np.sum(
        (portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns)
    )
    
    # 验证：总主动收益应等于配置、选择、交互效应之和
    active_return = total_portfolio_return - total_benchmark_return
    sum_effects = allocation_effect + selection_effect + interaction_effect
    
    # 打印验证信息（教学用途）
    print(f"总主动收益: {active_return:.6f}")
    print(f"配置效应: {allocation_effect:.6f}")
    print(f"选择效应: {selection_effect:.6f}")
    print(f"交互效应: {interaction_effect:.6f}")
    print(f"效应之和: {sum_effects:.6f}")
    print(f"效应之和与主动收益的匹配度: {np.abs(active_return - sum_effects):.10f}")
    
    # ============================================================
    # 填充结果字典
    # ============================================================
    
    result = {
        'sharpe_annual': sharpe_annual,
        'allocation_effect': allocation_effect,
        'selection_effect': selection_effect,
        'interaction_effect': interaction_effect
    }
    
    # 输出结果
    print("\n" + "="*50)
    print("最终结果字典:")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    return result

if __name__ == "__main__":
    result = main()
