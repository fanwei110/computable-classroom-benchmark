"""Convert TALE2026_paper_C_journal.md -> IEEE Access LaTeX (paper_C_ieee/main.tex).

Pandoc converts every prose fragment; the three tables and two figures are
injected as hand-authored LaTeX via @@tokens@@ so pandoc never touches them;
numeric [n] citations become \\cite{refN} AFTER pandoc (so they are not
escaped); Unicode math/symbols are sanitized to LaTeX so the document
compiles under pdflatex. References become a thebibliography.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\onedrive\桌面\论文\可计算课堂")
SRC = ROOT / "TALE2026_paper_C_journal.md"
OUTDIR = ROOT / "paper_C_ieee"
OUTDIR.mkdir(exist_ok=True)

raw = SRC.read_text(encoding="utf-8")
abstract = re.search(r"## Abstract\s*\n+(.+?)\n+\*\*Keywords", raw, re.S).group(1).strip()
keywords = re.search(r"\*\*Keywords—\*\*\s*(.+)", raw).group(1).strip()
body = raw[raw.index("## I. Introduction"):raw.index("## Data and Code Availability")]
data_avail = re.search(r"## Data and Code Availability\s*\n+(.+?)\n+## Disclosure", raw, re.S).group(1).strip()
disclosure = re.search(r"## Disclosure of AI Use\s*\n+(.+?)\n+## Acknowledgment", raw, re.S).group(1).strip()
ack = re.search(r"## Acknowledgment\s*\n+(.+?)\n+## References", raw, re.S).group(1).strip()
refs_block = raw[raw.index("## References"):]


def pandoc(md, shift=False):
    cmd = ["pandoc", "-f", "gfm", "-t", "latex", "--wrap=preserve"]
    if shift:
        cmd += ["--shift-heading-level-by=-1"]
    pr = subprocess.run(cmd, input=md, capture_output=True, text=True, encoding="utf-8")
    if pr.returncode != 0:
        print("pandoc error:", pr.stderr)
        sys.exit(1)
    return pr.stdout


def cites(s):
    def repl(m):
        return "\\cite{" + ",".join("ref" + n.strip() for n in m.group(1).split(",")) + "}"
    return re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", repl, s)


UNI = [
    ("10⁻⁴", "$10^{-4}$"), ("10⁻³", "$10^{-3}$"),
    ("τ\\_abs", "$\\tau_{\\mathrm{abs}}$"), ("τ\\_rel", "$\\tau_{\\mathrm{rel}}$"),
    ("τ_abs", "$\\tau_{\\mathrm{abs}}$"), ("τ_rel", "$\\tau_{\\mathrm{rel}}$"),
    ("τ", "$\\tau$"), ("κ", "$\\kappa$"), ("×", "$\\times$"),
    ("≤", "$\\le$"), ("≥", "$\\ge$"), ("≈", "$\\approx$"),
    ("−", "$-$"), ("σ", "$\\sigma$"), ("Φ", "$\\Phi$"), ("Σ", "$\\Sigma$"),
    ("¥", "\\textyen{}"), ("…", "\\ldots{}"),
    ("“", "``"), ("”", "''"), ("‘", "`"), ("’", "'"),
]


SUP = {"⁻": "-", "⁰": "0", "¹": "1", "²": "2", "³": "3",
       "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8",
       "⁹": "9"}


def supfix(s):
    return re.sub("[⁻⁰¹²³⁴-⁹]+",
                  lambda m: "$^{" + "".join(SUP[c] for c in m.group(0)) + "}$", s)


def sanitize(s):
    s = supfix(s)
    for a, b in UNI:
        s = s.replace(a, b)
    return s


# ---- transform body: strip md tables/figs to tokens, fix headers ----------
b = body
b = re.sub(r"\*\*TABLE I\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL1@@\n\n", b)
b = re.sub(r"\*\*TABLE II\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL2@@\n\n", b)
b = re.sub(r"\*\*TABLE III\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL3@@\n\n", b)
b = re.sub(r"^\*Note:\*.*$", "", b, flags=re.M)
# safety net: any pipe-table rows that survived become nothing (caught by floats)
b = re.sub(r"^(?:\|[^\n]*\n)+", "", b, flags=re.M)
b = re.sub(r"\*\*Fig\. 2\..*?(\n\[Figure 2[^\]]*\])?\n", "\n\n@@FIG2@@\n\n", b, flags=re.S)
b = b.replace("## III. The Computable Classroom and Its Resource Library",
              "## III. The Computable Classroom and Its Resource Library\n\n@@FIG1@@\n")
# strip manual section/subsection numbering for IEEEtran auto-numbering
b = re.sub(r"^## [IVX]+\.\s+", "## ", b, flags=re.M)
b = re.sub(r"^### [A-E]\.\s+", "### ", b, flags=re.M)

body_tex = pandoc(b, shift=True)
for tok, tex_ in [("@@TBL1@@", "TBL1"), ("@@TBL2@@", "TBL2"), ("@@TBL3@@", "TBL3"),
                  ("@@FIG1@@", "FIG1"), ("@@FIG2@@", "FIG2")]:
    body_tex = body_tex.replace(tok, "%%" + tex_ + "%%")  # mark; fill below

# ---- hand LaTeX floats -----------------------------------------------------
TBL1 = r"""\begin{table*}[t]
\caption{Computable knowledge units and benchmark task instances.}
\label{tab:cku}\centering\small
\begin{tabular}{@{}llp{4.3cm}p{6.0cm}@{}}
\toprule
\# & Knowledge point (pillar) & T1 computation & T3 scenario probe (verbatim, transl.) \\
\midrule
KP1 & Mean--variance frontier (portfolio) & Min-variance weights and volatility, 3 assets & \emph{``If corr(A,B) rises from 0.3 to 0.8, what happens to a 60/40 portfolio's volatility?''} \\
KP2 & CAPM and the SML (asset pricing) & CAPM expected returns and alpha, 3 betas & \emph{``Market fell 5.8\% last month, rf 4.7\%/yr---what should the stock have returned?''} \\
KP3 & Duration and convexity (fixed income) & Price, Macaulay/modified duration, convexity & \emph{``If yields rise 80 bp, roughly how much does its price fall?''} \\
KP4 & Black--Scholes and Greeks (derivatives) & European call price, delta, vega & \emph{``If implied vol rises one point, how much does the call rise?''} \\
KP5 & Value-at-Risk (risk) & 95\%/99\% parametric VaR, 1/10-day & \emph{``Desk reports 24\% annualized vol on a \textyen2.7M position---95\% 1-day VaR?''} \\
KP6 & Sharpe and attribution (portfolio) & Annualized Sharpe; BHB attribution & \emph{``With rf 2.1\%, what was the fund's annualized Sharpe over the sample?''} \\
\bottomrule
\end{tabular}
\end{table*}"""

TBL2 = r"""\begin{table*}[t]
\caption{Benchmark results by model and prompting condition (2$\times$2). Executability / strict correctness in percent; brackets are cluster-bootstrap 95\% CIs over tasks for correctness. Each cell pools 180 generations; pooled rows 540.}
\label{tab:main}\centering\small
\begin{tabular}{@{}lcccc@{}}
\toprule
Model & C1 ($-$conv,$-$struct) & C2 ($-$conv,$+$struct) & C3 ($+$conv,$-$struct) & C4 ($+$conv,$+$struct) \\
 & Exec / Corr & Exec / Corr & Exec / Corr & Exec / Corr \\
\midrule
M1 Mistral Large 2512 & 91.1 / 17.2 [7.2, 30.6] & 99.4 / 56.1 [36.1, 75.0] & 90.6 / 26.1 [10.6, 43.9] & 98.9 / 88.3 [78.3, 96.7] \\
M2 DeepSeek-V4 Pro & 78.3 / 46.1 [31.7, 60.0] & 88.3 / 68.3 [56.7, 78.9] & 83.9 / 45.0 [28.9, 61.1] & 89.4 / 82.8 [75.6, 88.9] \\
M3 GLM-5.1 & 88.9 / 39.4 [22.8, 57.8] & 87.8 / 67.2 [53.3, 79.4] & 85.6 / 36.1 [17.8, 56.1] & 93.9 / 93.3 [90.0, 96.7] \\
\textbf{Pooled} & \textbf{86.1 / 34.3 [22.4, 46.9]} & \textbf{91.9 / 63.9 [52.2, 75.0]} & \textbf{86.7 / 35.7 [20.7, 52.0]} & \textbf{94.1 / 88.1 [84.6, 91.5]} \\
\bottomrule
\end{tabular}
\end{table*}"""

TBL3 = r"""\begin{table}[t]
\caption{Numerical correctness (\%) by task type and condition, pooled across models.}
\label{tab:tasktype}\centering\small
\begin{tabular}{@{}lccccc@{}}
\toprule
Task type & C1 & C2 & C3 & C4 & $\Delta$ \\
\midrule
T1 computation & 27.2 & 73.9 & 30.6 & 88.9 & +61.7 \\
T2 visualization & 50.6 & 69.4 & 57.2 & 85.6 & +35.0 \\
T3 scenario (strict) & 25.0 & 48.3 & 19.4 & 90.0 & +65.0 \\
T3 scenario (defensible) & 26.1 & 55.6 & 25.0 & 90.0 & +63.9 \\
\bottomrule
\end{tabular}
\end{table}"""

FIG1 = r"""\begin{figure*}[t]\centering
\includegraphics[width=0.9\textwidth]{fig1_architecture.pdf}
\caption{Architecture of the computable classroom and the CKU pipeline: two reliable layers bounded by a hard perimeter, out-of-library questions harvested into the library, and instructor verification closing the loop.}
\label{fig:arch}\end{figure*}"""

FIG2 = r"""\begin{figure}[t]\centering
\includegraphics[width=\columnwidth]{fig2_errors.pdf}
\caption{Distribution of primary error classes by model, improvised condition ($N=306$ coded failures). Shares are approximate ($\kappa=0.49$); the text reports the $\kappa$-immune mechanical floor and the between-coder spread.}
\label{fig:err}\end{figure}"""

for tag, tex_ in [("TBL1", TBL1), ("TBL2", TBL2), ("TBL3", TBL3),
                  ("FIG1", FIG1), ("FIG2", FIG2)]:
    body_tex = body_tex.replace("%%" + tag + "%%", tex_)
body_tex = re.sub(r"@@\w+@@", "", body_tex)

# ---- references -----------------------------------------------------------
bibitems = []
for m in re.finditer(r"^\[(\d+)\]\s+(.+)$", refs_block, re.M):
    n, txt = m.group(1), m.group(2).strip().replace("*", "")
    txt = txt.replace("&", "\\&").replace("%", "\\%")
    bibitems.append(f"\\bibitem{{ref{n}}} {txt}")
bib = "\n".join(bibitems)

# ---- assemble + global cite + sanitize ------------------------------------
abstract_tex = pandoc(abstract)
data_tex = pandoc(data_avail)
disc_tex = pandoc(disclosure)
ack_tex = pandoc(ack)

doc = r"""\documentclass[journal]{IEEEtran}
\usepackage{cite}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{amsmath,amssymb}
\usepackage[utf8]{inputenc}
\usepackage{textcomp}
\usepackage{url}
\graphicspath{{../benchmark/figures/}}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

\begin{document}
\title{Can LLMs Teach Finance Live? Structure, Not Conventions, Is the Binding Constraint on Concept-to-Code Generation in a Generative-Inquiry Classroom}
\author{Wei~Fan%
\thanks{Manuscript submitted June 2026. Supported by the Zhengzhou University Undergraduate Education and Teaching Reform Project ``Construction and Practice of a Generative-AI-Enabled `Computable Classroom' for Securities Investment.''}%
\thanks{The author is with Zhengzhou University, Zhengzhou, China (e-mail: fanweigp@gmail.com).}}
\markboth{IEEE Access, 2026}{Fan: Can LLMs Teach Finance Live?}
\maketitle

\begin{abstract}
%%ABS%%
\end{abstract}

\begin{IEEEkeywords}
%%KW%%
\end{IEEEkeywords}

%%BODY%%

\section*{Data and Code Availability}
%%DATA%%

\section*{Disclosure of AI Use}
%%DISC%%

\section*{Acknowledgment}
%%ACK%%

\begin{thebibliography}{99}
%%BIB%%
\end{thebibliography}
\end{document}
"""
doc = (doc.replace("%%ABS%%", abstract_tex).replace("%%KW%%", keywords)
       .replace("%%BODY%%", body_tex).replace("%%DATA%%", data_tex)
       .replace("%%DISC%%", disc_tex).replace("%%ACK%%", ack_tex)
       .replace("%%BIB%%", bib))
doc = cites(doc)
doc = sanitize(doc)

(OUTDIR / "main.tex").write_text(doc, encoding="utf-8")
print(f"wrote {OUTDIR/'main.tex'} ({len(doc)} chars, {len(bibitems)} refs)")
