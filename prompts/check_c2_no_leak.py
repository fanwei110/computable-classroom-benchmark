"""Verify that no C2 prompt leaks convention information (stage-1 check #5).

Scans every prompts/C2/*.md against a forbidden-pattern list covering all
conventions in conventions/course_conventions.md (binding and defensible
alternatives). Any hit is a leak. Exits nonzero on failure.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

FORBIDDEN = [
    (r"\b252\b", "annualization factor"),
    (r"\b250\b", "annualization factor"),
    (r"\b365\b", "annualization factor"),
    (r"trading[- ]day", "annualization basis"),
    (r"calendar[- ]day", "annualization basis"),
    (r"compound", "compounding convention"),
    (r"continuous", "compounding convention"),
    (r"ACT\s*/\s*360", "day count"),
    (r"day[- ]?count", "day count"),
    (r"ddof", "std estimator"),
    (r"sample standard deviation", "std estimator"),
    (r"population", "std estimator"),
    (r"one[- ]tailed|two[- ]tailed", "quantile convention"),
    (r"positive (CNY|loss)", "VaR sign convention"),
    (r"\bdecimal", "unit convention"),
    (r"per percent(age)? point", "vega quotation"),
    (r"linear(ly)? interp", "percentile convention"),
    (r"numpy default", "percentile convention"),
    (r"Brinson|BHB|Hood|Beebower", "attribution scheme"),
    (r"first[- ]named|60% in A|order named", "weight-mapping convention"),
    (r"geometric", "rate conversion"),
    (r"simple division|annual\s*/\s*12|annual\s*/\s*252|/\s*252|/\s*12\b", "rate conversion"),
    (r"sqrt\(\s*252\s*\)|sqrt\(\s*10\s*\)", "scaling rule"),
    (r"zero[- ]mean", "VaR mean assumption"),
    (r"rule of thumb|first[- ]order|second[- ]order", "approximation order"),
    (r"\(1\s*\+\s*y\)", "duration/convexity formula detail"),
    (r"Macaulay\s*/", "duration formula detail"),
    (r"dC/dsigma|per unit of volatility", "vega quotation"),
    (r"annual(ly)?[- ]compounded|annual compounding", "compounding convention"),
]


FORBIDDEN_ZH = [
    (r"\b252\b", "年化天数"),
    (r"\b250\b", "年化天数"),
    (r"\b365\b", "年化天数"),
    (r"交易日", "年化基准"),
    (r"日历日|自然日", "年化基准"),
    (r"复利", "复利约定"),
    (r"连续", "复利约定"),
    (r"ddof", "标准差估计量"),
    (r"样本标准差|总体标准差", "标准差估计量"),
    (r"单尾|双尾", "分位数约定"),
    (r"正的损失|正的人民币|报为正", "VaR 符号约定"),
    (r"小数", "单位约定"),
    (r"线性插值|numpy 默认", "分位数插值约定"),
    (r"Brinson|布林森|BHB|Hood|Beebower", "归因方案"),
    (r"提及的顺序|A 占 60", "权重对应约定"),
    (r"几何", "利率折算"),
    (r"简单除法|年利率\s*/\s*12|年利率\s*/\s*252|/\s*252|/\s*12\b", "利率折算"),
    (r"sqrt\(\s*252\s*\)|sqrt\(\s*10\s*\)", "缩放规则"),
    (r"零均值|均值取零", "VaR 均值假设"),
    (r"经验法则|一阶|二阶", "近似阶数"),
    (r"\(1\s*\+\s*y\)", "久期/凸性公式细节"),
    (r"dC/dσ|每单位波动率", "vega 报价"),
    (r"年复利|按年付息一次于付息日", "复利约定"),
]


def scan(folder, patterns, label):
    files = sorted((HERE / folder).glob("KP*_T*.md"))
    if len(files) != 18:
        print(f"FAIL: expected 18 prompts in {folder}, found {len(files)}")
        sys.exit(1)
    leaks = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for pat, what in patterns:
            for m in re.finditer(pat, text, re.I):
                line = text[:m.start()].count("\n") + 1
                leaks.append(f"{folder}/{f.name}:{line}: '{m.group(0)}' ({what})")
    if leaks:
        print(f"CONVENTION LEAKS FOUND IN {label}:")
        for x in leaks:
            print("  " + x)
        sys.exit(1)
    print(f"OK: 18/18 {label} prompts contain zero convention information "
          f"({len(patterns)} forbidden patterns checked)")


def main():
    scan("C2", FORBIDDEN, "C2 (en)")
    if (HERE / "C2_zh").exists():
        scan("C2_zh", FORBIDDEN_ZH, "C2_zh (zh-CN)")


if __name__ == "__main__":
    main()
