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


def main():
    files = sorted((HERE / "C2").glob("KP*_T*.md"))
    if len(files) != 18:
        print(f"FAIL: expected 18 C2 prompts, found {len(files)}")
        sys.exit(1)
    leaks = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for pat, what in FORBIDDEN:
            for m in re.finditer(pat, text, re.I):
                line = text[:m.start()].count("\n") + 1
                leaks.append(f"{f.name}:{line}: '{m.group(0)}' ({what})")
    if leaks:
        print("CONVENTION LEAKS FOUND IN C2:")
        for x in leaks:
            print("  " + x)
        sys.exit(1)
    print("OK: 18/18 C2 prompts contain zero convention information "
          f"({len(FORBIDDEN)} forbidden patterns checked)")


if __name__ == "__main__":
    main()
