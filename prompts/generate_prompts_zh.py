"""Generate the Chinese (zh-CN) C2/C4 prompt sets.

Disclosed post-registration change (before ANY model generation): the locked
deployment config fixes prompt_language = zh-CN to match classroom practice
and the C1/C3 instructor phrasings, so the C2/C4 prompts must be Chinese as
well - otherwise the C1-vs-C2 contrast would confound structure with
language. These zh prompts mirror the frozen English ones section for
section and step for step; the English originals remain in C2/ and C4/ for
the record. Zero-convention-leak for C2_zh is verified by
check_c2_no_leak.py (Chinese forbidden-pattern list).
"""

from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TASKS = HERE.parent / "tasks"

ROLE = ("你是某大学《证券投资学》课程的课堂实时编程助手。教师将当堂运行你的"
        "代码并投屏给全班，因此代码必须正确且自包含。")

CODE_QUALITY = ("写一个自包含的 Python 脚本。只使用 numpy、scipy、pandas、"
                "matplotlib。不可联网，不留占位值，输出确定可复现，变量命名清晰。")

CONVENTION_HEADER = (
    "计算约定：所有年化与去年化一律按每年 252 个交易日；债券收益率按年复利报价；"
    "期权无风险利率按连续复利；所有利率、收益率、波动率与权重用小数表示"
    "（0.05 即 5%）；VaR 报告为正的损失金额；标准差用样本估计量（ddof=1）。")

CONCEPT = {
    "KP1": "概念：马科维茨均值-方差组合理论。组合方差为 w'Σw；最小方差组合在满仓"
           "约束下使其最小；有效前沿给出每一目标收益下的最小波动率。",
    "KP2": "概念：CAPM 与证券市场线。期望收益是 beta 的线性函数；偏离该线的部分"
           "即 alpha。",
    "KP3": "概念：债券定价与久期、凸性。价格是现金流贴现之和；久期与凸性衡量价格"
           "对收益率变动的敏感性。",
    "KP4": "概念：欧式期权的 Black-Scholes 定价与希腊字母。价格、delta 与 vega "
           "由闭式解给出。",
    "KP5": "概念：在险价值（VaR）。损益分布的损失分位数，可用参数法"
           "（delta-normal）或历史数据计算。",
    "KP6": "概念：风险调整后业绩。夏普比率衡量超额收益与总风险之比；业绩归因将"
           "主动收益分解为配置、选择与交互效应。",
}

CONV_TEXT = {
    "ann_252": "年化与去年化一律按每年 252 个交易日（波动率按 sqrt(252) 缩放）。",
    "bond_annual_comp": "债券收益率按年复利报价；修正久期 = 麦考利久期/(1+y)；"
                        "凸性 = Σ[t(t+1)CF_t/(1+y)^(t+2)]/P，单位为年的平方。",
    "opt_cont_comp": "期权无风险利率按连续复利；vega 按每单位波动率报价（dC/dσ）。",
    "decimal_units": "所有利率、收益率、波动率与权重用小数表示（0.05 即 5%）。",
    "var_positive": "VaR 报告为正的损失金额；使用单尾正态分位数，短期限下均值取零。",
    "ddof_1": "标准差用样本估计量（ddof=1）。",
    "rf_simple_split": "年利率折算到更短期限用简单除法（月=年/12，日=年/252）。",
    "hist_var_linear": "历史 VaR 取损益分布的线性插值经验分位数（numpy 默认）。",
    "first_named_first": "组合权重按资产被提及的顺序对应（'A 和 B 的 60/40 组合'"
                         "即 A 占 60%）。",
    "duration_firstorder": "估算收益率变动影响时，课程惯例为一阶近似 "
                           "dP/P = -D_mod × dy。",
    "attr_bhb": "归因采用 Brinson-Hood-Beebower 并单列交互项：配置=Σ(w_p−w_b)r_b；"
                "选择=Σw_b(r_p−r_b)；交互=Σ(w_p−w_b)(r_p−r_b)。",
}

NEUTRAL_CONV = "凡题目未指明的计算选择，请自行采用合适且内部一致的假设。"

NEUTRAL_STATEMENT = {
    "KP1_T1": "三只风险资产的年化波动率分别为 18.7%、24.3%、31.2%；相关系数 "
              "corr(1,2)=0.21、corr(1,3)=-0.13、corr(2,3)=0.37。允许卖空，资金全部"
              "投出。计算全局最小方差组合的权重及其年化波动率。",
    "KP1_T2": "两只风险资产的期望年收益为 7.1% 与 12.4%，年化波动率为 16.3% 与 "
              "28.9%。在同一坐标系（横轴波动率、纵轴期望收益）画出相关系数为 "
              "0.15、0.45、0.75 的均值-方差前沿，并在每条曲线上标出最小方差组合；"
              "允许卖空、满仓。另报告相关系数 0.45 时：最小方差组合的年化波动率，"
              "以及目标期望收益 10% 下可达到的最小年化波动率。",
    "KP2_T1": "无风险利率为每年 2.3%，市场期望收益为每年 9.4%。股票 X、Y、Z 的 "
              "beta 分别为 0.62、1.18、1.51。计算各自的 CAPM 期望年收益。股票 Y "
              "当年实际收益 13.1%，计算其 alpha。",
    "KP2_T2": "无风险利率 2.3%，市场期望收益每年 9.4%。画出 beta 从 0 到 2 的证券"
              "市场线，并把股票 X（beta 0.62，收益 8.1%）、Y（1.18，13.1%）、"
              "Z（1.51，9.9%）作为带标注的点画上。无风险利率与市场收益做成可调"
              "参数。另报告 SML 的斜率与 beta=1.27 处的 CAPM 期望收益。",
    "KP3_T1": "一只到期一次还本的债券：面值 100，票息 4.6%，7 年期，到期收益率 "
              "5.3%。计算价格、麦考利久期、修正久期与凸性。",
    "KP3_T2": "对面值 100、票息 4.6%、7 年期、当前收益率 5.3% 的债券，画出收益率"
              "从 2% 到 9% 的精确价格-收益率曲线，并在当前收益率附近叠加基于久期"
              "的近似，加图例区分；收益率变动幅度做成可调。另报告收益率上升 100 "
              "个基点后的精确价格，以及久期法估计的相对价格变化。",
    "KP4_T1": "一只不分红股票的欧式看涨期权：现价 103.7，行权价 97.5，隐含波动率 "
              "27.6%（年化），无风险利率每年 4.3%，剩余期限 0.58 年。计算期权价格、"
              "delta 与 vega。",
    "KP4_T2": "对行权价 97.5、无风险利率每年 4.3%、剩余 0.58 年、标的不分红的欧式"
              "看涨期权，画出标的价格从 70 到 140 时的 delta 曲线，波动率取 15%、"
              "27.6%、40% 三条并加图例；波动率做成可调参数。另报告标的 110、波动率 "
              "27.6% 时的 delta。",
    "KP5_T1": "某头寸价值 1,850,000 元，年化收益波动率 21.8%。在 delta-normal"
              "（参数法）模型下计算：(i) 95% 一日 VaR；(ii) 99% 十日 VaR。",
    "KP5_T2": "读取课程数据快照中 \"fund\" 列的日收益序列。对 1,000,000 元头寸，"
              "画出日损益分布直方图，并用带标注的竖线标出 95% 一日历史 VaR；置信"
              "水平做成可调参数。另以人民币报告该 95% 一日历史 VaR。",
    "KP6_T1": "第一部分：读取课程数据快照 \"fund\" 列的日收益；无风险利率每年 "
              "2.1%，计算年化夏普比率。第二部分：组合与基准各含三个行业——组合"
              "权重 [0.45, 0.35, 0.20]，行业收益 [0.083, 0.021, -0.014]；基准权重 "
              "[0.40, 0.40, 0.20]，行业收益 [0.067, 0.034, -0.009]。计算配置、选择"
              "与交互效应。",
    "KP6_T2": "读取课程数据快照 \"fund\" 列的日收益。无风险利率每年 2.1%，画出 60 "
              "日滚动年化夏普比率的时间序列，窗口长度做成可调。另报告最后（最近）"
              "一个 60 日窗口的夏普值。",
}

# C4 task statements: neutral statement + task-data pins the neutral version
# strips (payment frequency / valuation date are task data, not conventions).
PIN_EXTRA = {
    "KP3_T1": "票息每年支付一次，于付息日估值（无应计利息）。",
    "KP3_T2": "票息每年支付一次。",
}

CANONICAL_ZH = {
    "KP1_T3": "资产 A 的年化波动率大约 18.4%，资产 B 大约 29.7%。如果二者的相关"
              "系数从 0.3 升到 0.8，A 和 B 的 60/40 组合的波动率会怎么变？",
    "KP2_T3": "一只股票 beta 为 1.42。上个月市场跌了 5.8%，无风险利率为每年 "
              "4.7%。按 CAPM，它上个月本该收益多少？",
    "KP3_T3": "还是我们看过的那只 7 年期债券——面值 100、票息 4.6%、收益率 "
              "5.3%。如果收益率上升 80 个基点，它的价格大概跌多少？",
    "KP4_T3": "还是刚才那只看涨期权——现价 103.7、行权价 97.5、波动率 27.6%、"
              "利率 4.3%、剩 0.58 年。如果隐含波动率上升一个百分点，期权价格涨"
              "多少？",
    "KP5_T3": "交易台报告某头寸年化波动率 24%，头寸 2,700,000 元。95% 一日 VaR "
              "是多少？",
    "KP6_T3": "用课程数据文件里的 fund 列。无风险利率按 2.1%，整个样本的年化夏普"
              "比率是多少？",
}

STEPS = {
    "KP1_T1": {"c4": ["由波动率与相关系数构造协方差矩阵。",
                      "求最小方差权重（闭式解或求解器均可），归一化使其和为 1。",
                      "组合波动率取 w'Σw 的平方根，用小数表示。",
                      "按要求键名填充 result。"],
               "c2": ["由波动率与相关系数构造协方差矩阵。",
                      "求最小方差权重（闭式解或求解器均可），归一化使其和为 1。",
                      "组合波动率取 w'Σw 的平方根。",
                      "按要求键名填充 result。"]},
    "KP1_T2": {"c4": ["对每个相关系数构造协方差矩阵，并在组合权重上扫描画出前沿。",
                      "在每条曲线上标出最小方差组合；图例区分各曲线。",
                      "对相关系数 0.45 计算所需的两个波动率，用小数表示。",
                      "保存图形并填充 result。"],
               "c2": ["对每个相关系数构造协方差矩阵，并在组合权重上扫描画出前沿。",
                      "在每条曲线上标出最小方差组合；图例区分各曲线。",
                      "对相关系数 0.45 计算所需的两个波动率。",
                      "保存图形并填充 result。"]},
    "KP1_T3": {"c4": ["按资产被提及的顺序对应 60/40 权重（A 占 60%）。",
                      "构造相关系数 0.3 与 0.8 两个协方差矩阵。",
                      "计算两个组合波动率，用小数表示。",
                      "填充 result。"],
               "c2": ["自行确定 60/40 权重与两只资产的对应方式。",
                      "构造相关系数 0.3 与 0.8 两个协方差矩阵。",
                      "计算两个组合波动率。",
                      "填充 result。"]},
    "KP2_T1": {"c4": ["对每个 beta 套用 CAPM：E[Ri]=rf+beta(E[Rm]-rf)，用小数表示。",
                      "用 Y 的 CAPM 预测计算其 alpha。",
                      "填充 result。"],
               "c2": ["对每个 beta 套用 CAPM：E[Ri]=rf+beta(E[Rm]-rf)。",
                      "用 Y 的 CAPM 预测计算其 alpha。",
                      "填充 result。"]},
    "KP2_T2": {"c4": ["画出 beta 0 到 2 的 SML，并标出三只股票的点。",
                      "把无风险利率与市场收益参数化。",
                      "报告斜率与 beta=1.27 处的期望收益，用小数表示。",
                      "保存图形并填充 result。"],
               "c2": ["画出 beta 0 到 2 的 SML，并标出三只股票的点。",
                      "把无风险利率与市场收益参数化。",
                      "报告斜率与 beta=1.27 处的期望收益。",
                      "保存图形并填充 result。"]},
    "KP2_T3": {"c4": ["把年无风险利率按简单除法折算为月利率（年利率/12）。",
                      "在月度层面套用 CAPM，用小数表示。",
                      "填充 result。"],
               "c2": ["把年无风险利率以合适方式折算为月利率。",
                      "在月度层面套用 CAPM。",
                      "填充 result。"]},
    "KP3_T1": {"c4": ["按年复利收益率贴现每年票息与到期面值，得到价格。",
                      "计算麦考利久期；除以 (1+y) 得修正久期。",
                      "按 Σ[t(t+1)CF/(1+y)^(t+2)]/P 计算凸性（年平方）。",
                      "填充 result。"],
               "c2": ["按报价收益率贴现现金流，得到价格。",
                      "计算麦考利久期与修正久期。",
                      "计算凸性。",
                      "填充 result。"]},
    "KP3_T2": {"c4": ["在 2% 到 9% 的收益率网格上（年复利）为精确曲线定价。",
                      "在 5.3% 附近叠加一阶久期直线与久期+凸性曲线。",
                      "报告 +100bp 的精确价格与一阶相对变化（小数，下跌为负）。",
                      "保存图形并填充 result。"],
               "c2": ["在 2% 到 9% 的收益率网格上为精确曲线定价。",
                      "在 5.3% 附近叠加基于久期的近似。",
                      "报告 +100bp 的精确价格与久期法估计的相对变化。",
                      "保存图形并填充 result。"]},
    "KP3_T3": {"c4": ["计算当前收益率下的修正久期（年复利）。",
                      "套用课程经验法则 dP/P = -D_mod × dy，dy=0.008。",
                      "把跌幅大小作为正的小数存入 result。"],
               "c2": ["计算该债券在当前收益率下的利率敏感性。",
                      "估算收益率上升 80 个基点的价格影响。",
                      "把跌幅存入 result。"]},
    "KP4_T1": {"c4": ["用连续复利利率计算 d1 与 d2。",
                      "计算期权价格与 delta = N(d1)。",
                      "按每单位波动率计算 vega（dC/dσ），用小数表示。",
                      "填充 result。"],
               "c2": ["计算 d1 与 d2。",
                      "计算期权价格与 delta。",
                      "计算 vega。",
                      "填充 result。"]},
    "KP4_T2": {"c4": ["对每个波动率在标的网格上计算 delta = N(d1)（连续复利利率）。",
                      "画三条带标注曲线，并把波动率参数化。",
                      "报告标的 110、波动率 27.6% 的 delta，用小数表示。",
                      "保存图形并填充 result。"],
               "c2": ["对每个波动率在标的网格上计算 delta。",
                      "画三条带标注曲线，并把波动率参数化。",
                      "报告标的 110、波动率 27.6% 的 delta。",
                      "保存图形并填充 result。"]},
    "KP4_T3": {"c4": ["分别在波动率 28.6% 与 27.6% 下精确重定价（连续复利利率）。",
                      "把精确价差存入 result。"],
               "c2": ["推算期权价格对这一个百分点波动率变化的响应。",
                      "把价格变化存入 result。"]},
    "KP5_T1": {"c4": ["按每年 252 个交易日把波动率去年化到一日。",
                      "用单尾正态分位数（95% 与 99%），均值取零。",
                      "十日 VaR 按 sqrt(10) 缩放；两者均报为正的人民币金额。",
                      "填充 result。"],
               "c2": ["以合适方式把年化波动率换算到一日期限。",
                      "对两个置信水平套用正态分位数。",
                      "以合适方式缩放到十日期限；以人民币报告两个 VaR。",
                      "填充 result。"]},
    "KP5_T2": {"c4": ["读取快照 CSV，构造头寸的日损益。",
                      "按线性插值经验分位数（numpy 默认）计算 95% 历史 VaR，"
                      "报为正的人民币金额。",
                      "画直方图并加带标注的 VaR 线；置信水平参数化。",
                      "保存图形并填充 result。"],
               "c2": ["读取快照 CSV，构造头寸的日损益。",
                      "由经验分布计算 95% 历史 VaR（人民币）。",
                      "画直方图并加带标注的 VaR 线；置信水平参数化。",
                      "保存图形并填充 result。"]},
    "KP5_T3": {"c4": ["按每年 252 个交易日把 24% 波动率去年化到一日。",
                      "用单尾 95% 正态分位数，均值取零。",
                      "把 VaR 作为正的人民币金额存入 result。"],
               "c2": ["以合适方式把 24% 年化波动率换算到一日期限。",
                      "套用 95% 正态分位数。",
                      "把 VaR 金额存入 result。"]},
    "KP6_T1": {"c4": ["读取快照 CSV；基金日收益减去日无风险利率（年利率/252）。",
                      "用样本标准差（ddof=1）计算夏普，按 sqrt(252) 年化。",
                      "按 Brinson-Hood-Beebower 计算配置、选择、交互效应，用小数表示。",
                      "填充 result。"],
               "c2": ["读取快照 CSV；在基金收益中计入无风险利率。",
                      "计算年化夏普比率。",
                      "计算配置、选择、交互效应。",
                      "填充 result。"]},
    "KP6_T2": {"c4": ["读取快照 CSV；日无风险利率取年利率/252。",
                      "计算 60 日滚动夏普（ddof=1），按 sqrt(252) 年化，窗口可调。",
                      "报告最后一个窗口的值（小数）；画出时间序列。",
                      "保存图形并填充 result。"],
               "c2": ["读取快照 CSV；计入无风险利率。",
                      "计算 60 日滚动年化夏普，窗口可调。",
                      "报告最后一个窗口的值；画出时间序列。",
                      "保存图形并填充 result。"]},
    "KP6_T3": {"c4": ["读取快照 CSV；日收益减去日无风险利率（年利率/252）。",
                      "用样本标准差（ddof=1）计算全样本夏普，按 sqrt(252) 年化。",
                      "把结果（小数）存入 result。"],
               "c2": ["读取快照 CSV；计入 2.1% 的无风险利率。",
                      "计算全样本年化夏普比率。",
                      "把结果存入 result。"]},
}


def output_contract(spec):
    keys = ", ".join(f"'{k}'" for k in spec["required_keys"])
    line = f"输出契约：把所有要求的输出存入名为 `result` 的字典，键名严格为：{keys}。"
    if spec["figure_required"]:
        line += " 将图保存为文件，并把文件路径存入 result['figure_path']。"
    return line


def data_note(spec):
    if spec["data_file"]:
        return f"课程数据快照位于 {spec['data_file']}（CSV）。"
    return None


def build_prompt(spec, condition):
    kp = spec["id"].split("_")[0]
    is_t3 = spec["task_type"] == "T3"
    if is_t3:
        task_text = CANONICAL_ZH[spec["id"]]
    elif condition == "c4":
        task_text = NEUTRAL_STATEMENT[spec["id"]]
        if spec["id"] in PIN_EXTRA:
            task_text += PIN_EXTRA[spec["id"]]
    else:
        task_text = NEUTRAL_STATEMENT[spec["id"]]
    conv_block = ("\n".join("- " + CONV_TEXT[c] for c in spec["conventions_binding"])
                  if condition == "c4" else "- " + NEUTRAL_CONV)
    steps = STEPS[spec["id"]][condition]
    parts = [ROLE, "", CONCEPT[kp], "",
             ("课程计算约定：" if condition == "c4" else "假设处理："),
             conv_block, "", "任务：", task_text]
    note = data_note(spec)
    if note:
        parts += ["", note]
    parts += ["", "请按以下步骤进行："]
    parts += [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    parts += ["", CODE_QUALITY, "", output_contract(spec)]
    return "\n".join(parts) + "\n"


def main():
    for folder in ("C2_zh", "C4_zh"):
        (HERE / folder).mkdir(exist_ok=True)
    n = 0
    for f in sorted(TASKS.glob("KP*_T*.yaml")):
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        for cond, folder in (("c2", "C2_zh"), ("c4", "C4_zh")):
            (HERE / folder / f"{spec['id']}.md").write_text(
                build_prompt(spec, cond), encoding="utf-8")
            n += 1
    (HERE / "convention_header_zh.txt").write_text(
        CONVENTION_HEADER + "\n", encoding="utf-8")
    print(f"wrote {n} zh prompts + convention_header_zh.txt")


if __name__ == "__main__":
    main()
