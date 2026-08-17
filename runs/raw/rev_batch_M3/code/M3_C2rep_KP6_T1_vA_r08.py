import pandas as pd
import numpy as np

def main():
    # ==========================================
    # 第一部分：计算年化夏普比率
    # ==========================================
    # 1. 读取快照 CSV
    df = pd.read_csv('data/market_snapshot_v1.csv')
    
    # 提取基金日收益率数据
    fund_daily_returns = df['fund']
    
    # 假设与参数设定
    rf_annual = 0.021  # 年化无风险利率 2.1%
    trading_days = 252 # 一年交易日
    
    # 将年化无风险利率转换为日无风险利率（按单利近似，业界常用且与日收益率频度匹配）
    rf_daily = rf_annual / trading_days
    
    # 在基金收益中计入无风险利率：计算日超额收益（总收益扣除无风险利率）
    excess_daily_returns = fund_daily_returns - rf_daily
    
    # 计算日超额收益的均值与标准差（使用样本标准差 ddof=1）
    mean_excess_daily = np.mean(excess_daily_returns)
    std_daily = np.std(fund_daily_returns, ddof=1) # 总风险使用基金总收益的标准差
    
    # 计算年化夏普比率：年化均值 / 年化标准差 = (日均值 * 252) / (日标准差 * sqrt(252)) 
    sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(trading_days)
    
    # ==========================================
    # 第二部分：业绩归因（BHB模型）
    # ==========================================
    # 组合权重与行业收益
    w_p = np.array([0.45, 0.35, 0.20])
    r_p = np.array([0.083, 0.021, -0.014])
    
    # 基准权重与行业收益
    w_b = np.array([0.40, 0.40, 0.20])
    r_b = np.array([0.067, 0.034, -0.009])
    
    # 主动权重 (AW) 与主动收益 (AR)
    aw = w_p - w_b
    ar = r_p - r_b
    
    # 配置效应: 衡量因偏离基准权重而产生的收益，使用基准行业收益计算
    allocation_effect = np.sum(aw * r_b)
    
    # 选择效应: 衡量因在基准权重下选股优势而产生的收益
    selection_effect = np.sum(w_b * ar)
    
    # 交互效应: 衡量权重偏离与选股优势共同作用产生的交叉收益
    interaction_effect = np.sum(aw * ar)
    
    # 验证归因分解: 配置 + 选择 + 交互 应等于 总主动收益
    total_active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
    assert np.isclose(allocation_effect + selection_effect + interaction_effect, total_active_return), "业绩归因分解不一致！"
    
    # ==========================================
    # 输出契约：填充 result
    # ==========================================
    result = {
        'sharpe_annual': sharpe_annual,
        'allocation_effect': allocation_effect,
        'selection_effect': selection_effect,
        'interaction_effect': interaction_effect
    }
    
    # 课堂投屏输出
    print("="*50)
    print("《证券投资学》课堂实时编程结果")
    print("="*50)
    print(f"年化夏普比率: {result['sharpe_annual']:.4f}")
    print("-" * 50)
    print(f"配置效应: {result['allocation_effect']:.6f}")
    print(f"选择效应: {result['selection_effect']:.6f}")
    print(f"交互效应: {result['interaction_effect']:.6f}")
    print(f"归因合计: {result['allocation_effect'] + result['selection_effect'] + result['interaction_effect']:.6f}")
    print("="*50)

if __name__ == "__main__":
    main()
