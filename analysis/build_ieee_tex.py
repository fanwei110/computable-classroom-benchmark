"""Convert TALE2026_paper_C_journal.md -> IEEE Access LaTeX (paper_C_ieee/main.tex).

Pandoc converts every prose fragment; the seven tables and four figures are
injected as hand-authored LaTeX via @@tokens@@ so pandoc never touches them;
numeric [n] citations become \\cite{refN} AFTER pandoc (so they are not
escaped); Unicode math/symbols are sanitized to LaTeX so the document
compiles under pdflatex. References become a thebibliography.
"""

import re
import subprocess
import sys
from pathlib import Path

# manuscript folder = two levels above this script (…/<paper-folder>/benchmark/analysis/)
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "TALE2026_paper_C_EN_final.md"
OUTDIR = ROOT / "paper_C_ieeeaccess"
OUTDIR.mkdir(exist_ok=True)

# Keep the compile directory's figure copies in lockstep with the sources.
# (\graphicspath puts ./ first, so a stale local copy silently shadows a
# regenerated figure -- this is exactly how a figure fix once failed to reach
# the compiled PDF.)
FIGSRC = ROOT / "benchmark" / "figures"
for _f in ("fig1_architecture.pdf", "fig2_errors.pdf",
           "fig3_2x2_heatmap.pdf", "fig4_latency.pdf"):
    _s = FIGSRC / _f
    if _s.exists():
        _d = OUTDIR / _f
        if (not _d.exists()) or _s.stat().st_mtime > _d.stat().st_mtime:
            _d.write_bytes(_s.read_bytes())
            print(f"synced figure -> {_f}")

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
    # hand-authored literal [n] / [n, m]
    s = re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", repl, s)
    # pandoc escapes prose brackets to {[}n{]}; convert those too (integers only,
    # so numeric CIs like {[}22.4, 46.9{]} and {[}-7.0, +10.2{]} are left alone)
    s = re.sub(r"\{\[\}(\d+(?:\s*,\s*\d+)*)\{\]\}", repl, s)
    return s


UNI = [
    ("10⁻⁴", "$10^{-4}$"), ("10⁻³", "$10^{-3}$"),
    ("τ\\_abs", "$\\tau_{\\mathrm{abs}}$"), ("τ\\_rel", "$\\tau_{\\mathrm{rel}}$"),
    ("τ_abs", "$\\tau_{\\mathrm{abs}}$"), ("τ_rel", "$\\tau_{\\mathrm{rel}}$"),
    ("τ", "$\\tau$"), ("κ", "$\\kappa$"), ("×", "$\\times$"),
    ("≤", "$\\le$"), ("≥", "$\\ge$"), ("≈", "$\\approx$"),
    ("−", "$-$"), ("σ", "$\\sigma$"), ("Φ", "$\\Phi$"), ("Σ", "$\\Sigma$"),
    ("¥", "\\textyen{}"), ("…", "\\ldots{}"),
    ("∈", "$\\in$"), ("≫", "$\\gg$"), ("≪", "$\\ll$"), ("≠", "$\\ne$"),
    ("·", "$\\cdot$"), ("→", "$\\rightarrow$"),
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
b = re.sub(r"\*\*TABLE IV\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL4@@\n\n", b)
b = re.sub(r"\*\*TABLE V\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL5@@\n\n", b)
b = re.sub(r"\*\*TABLE VI\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL6@@\n\n", b)
b = re.sub(r"\*\*TABLE VII\.[^\n]*\*\*\n+(?:\|[^\n]*\n)+", "\n\n@@TBL7@@\n\n", b)
b = re.sub(r"^\*Note:\*.*$", "", b, flags=re.M)
# safety net: any pipe-table rows that survived become nothing (caught by floats)
b = re.sub(r"^(?:\|[^\n]*\n)+", "", b, flags=re.M)
b = re.sub(r"\*\*Fig\. 1\.[^\n]*\*\*\s*\n+\[Figure 1[^\]]*\]", "\n\n@@FIG1@@\n\n", b)
b = re.sub(r"\*\*Fig\. 2\.[^\n]*\*\*\s*\n+\[Figure 2[^\]]*\]", "\n\n@@FIG2@@\n\n", b)
b = re.sub(r"\*\*Fig\. 3\.[^\n]*\*\*\s*\n+\[Figure 3[^\]]*\]", "\n\n@@FIG3@@\n\n", b)
b = re.sub(r"\*\*Fig\. 4\.[^\n]*\*\*\s*\n+\[Figure 4[^\]]*\]", "\n\n@@FIG4@@\n\n", b)
# strip manual section/subsection numbering for IEEEtran auto-numbering
b = re.sub(r"^## [IVX]+\.\s+", "## ", b, flags=re.M)
b = re.sub(r"^### [A-F]\.\s+", "### ", b, flags=re.M)

body_tex = pandoc(b, shift=True)
# appendix heading -> IEEE appendix command (single appendix)
body_tex = re.sub(
    r"\\section\{Appendix: System and Configuration Specification\}",
    r"\\appendix[System and Configuration Specification]", body_tex)
for tok, tex_ in [("@@TBL1@@", "TBL1"), ("@@TBL2@@", "TBL2"), ("@@TBL3@@", "TBL3"),
                  ("@@TBL4@@", "TBL4"), ("@@TBL5@@", "TBL5"), ("@@TBL6@@", "TBL6"), ("@@TBL7@@", "TBL7"),
                  ("@@FIG1@@", "FIG1"), ("@@FIG2@@", "FIG2"),
                  ("@@FIG3@@", "FIG3"), ("@@FIG4@@", "FIG4")]:
    body_tex = body_tex.replace(tok, "%%" + tex_ + "%%")  # mark; fill below

# ---- hand LaTeX floats -----------------------------------------------------
TBL1 = r"""\begin{table*}[t]
\caption{Computable knowledge units and benchmark task instances. A generated 18-task audit index maps inputs, outputs, ground-truth methods, tolerances, and frozen prompt files (\texttt{benchmark/docs/task\_audit\_table.md} and \texttt{.csv}).}
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

TBL3 = r"""\begin{table*}[t]
\caption{Reconciliation of all 2,160 pre-registered generations by mutually exclusive outcome category. Flow: 18 tasks $\times$ 4 conditions $\times$ 3 models $\times$ 10 repetitions $\rightarrow$ code extraction $\rightarrow$ execution $\rightarrow$ \texttt{result} format check $\rightarrow$ oracle judgment; T2 figures are rated separately on condition-specific denominators. Rows sum to 540. ``Contract violation'' includes no runnable code or execution without \texttt{result} (parenthetical: no-code subset); strict correctness equals ``Strict correct''/540.}
\label{tab:accounting}\centering\small
\begin{tabular}{@{}lccccccc@{}}
\toprule
Condition & Contract viol. (no code) & Crash & Silent wrong & Inad. figure & Defensible (T3) & Strict correct & Total \\
\midrule
C1 & 49 (35) & 40 & 264 & 0 & 2 & 185 & 540 \\
C2 & 19 (8) & 36 & 127 & 0 & 13 & 345 & 540 \\
C3 & 52 (37) & 35 & 249 & 1 & 10 & 193 & 540 \\
C4 & 19 (7) & 25 & 20 & 0 & 0 & 476 & 540 \\
\bottomrule
\end{tabular}
\end{table*}"""

TBL4 = r"""\begin{table}[t]
\caption{Completed wording $\times$ structural-framing factorial, no-convention row (post-hoc; deviation \#11). Creg/C1wS were collected August 4--5, 2026, and byte-identical C1/C2 replays August 6; these adjacent windows reduce but do not eliminate temporal or provider-routing imbalance. Strict correctness pooled across models; $n=540$ per cell; brackets are paired task-cluster bootstrap 95\% CIs ($B=10{,}000$). Mixed-model variational-posterior, GEE, and provider-adjusted GEE results are reported in Section V.B.}
\label{tab:crossing}\centering\small
\begin{tabular}{@{}llll@{}}
\toprule
Cell & Wording & Structural framing & Correct \% [95\% CI] \\
\midrule
C1rep & improvised & none & 33.9 [21.5, 46.9] \\
C1wS & improvised & CKU wrapper & 54.3 [36.7, 70.7] \\
Creg & regularized & none & 56.9 [38.1, 75.2] \\
C2rep & regularized & CKU wrapper & 69.8 [57.8, 80.2] \\
\bottomrule
\end{tabular}
\end{table}"""

TBL5 = r"""\begin{table}[t]
\caption{Numerical correctness (\%) by task type and condition, pooled across models. Pre-registered data, exploratory (descriptive) comparison.}
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

TBL6 = r"""\begin{table*}[t]
\caption{System and configuration specification of the evaluated pipeline. The released configuration file (\texttt{config/models.yaml}, frozen at preregistration) and the raw logs (full request bodies and response metadata for every call) allow the exact experimental calls to be reproduced or re-priced.}
\label{tab:spec}\centering\small
\begin{tabular}{@{}p{3.6cm}p{13.0cm}@{}}
\toprule
Item & Specification \\
\midrule
Model identifiers (requested) & M1 \texttt{mistralai/mistral-large-2512} (Mistral AI, released 2025-12); M2 \texttt{deepseek/deepseek-v4-pro} (DeepSeek, released 2026-04-24); M3 \texttt{z-ai/glm-5.1} (Z.ai/Zhipu, released 2026-04-07) \\
Endpoint and routing & OpenRouter \texttt{POST /api/v1/chat/completions}; the aggregator may route a requested identifier across hosting providers, so the serving provider and model ID of every call are recorded from the response metadata \\
Client region and network path & All requests issued from Zhengzhou, mainland China, over the public Internet to the aggregator's global endpoint; no region pinning was requested. The aggregator does not disclose the hosting region of the serving provider, so region is not a controlled variable here; what is auditable instead is the per-call serving-provider record, and Section V.B reports a provider-adjusted sensitivity analysis \\
Request schema & A single user message containing the frozen prompt; no system message; no tools; \texttt{max\_tokens} $=$ 32768 (deviation \#6); no other parameters transmitted \\
Decoding policy & Provider-default: \texttt{temperature}, \texttt{top\_p}, and reasoning parameters deliberately not transmitted (deployment-realistic; some reasoning APIs reject custom temperature); decoding sensitivity checked in Section V.F \\
Retry and error handling & Transport failures and HTTP 429/5xx retried up to 3 times (backoff 5/15/60\,s; timeout 300\,s); model content never retried; \texttt{finish\_reason} logged per generation \\
Collection dates & Pre-registered run: API snapshot 2026-06-11; real-instructor validation: June 2026; factorial new cells: 2026-08-04/05; byte-identical C1/C2 replays: 2026-08-06; same requested identifiers \\
Execution environment & Python 3.11; numpy, pandas, scipy, statsmodels, and matplotlib pinned in \texttt{requirements.txt}; container specification in \texttt{environment/Dockerfile}; generated code executed as a script (Section IV.B) \\
Latency and cost definitions & API latency $=$ request submission to completion received; total latency adds local execution and judging; tokens and cost from the per-call \texttt{usage} field at provider list prices \\
\bottomrule
\end{tabular}
\end{table*}"""

TBL7 = r"""\begin{table*}[t]
\caption{Registered outcome contrasts and complete factorial-model estimates. Panel A reports paired task-cluster bootstrap intervals (20,000 draws). Panel B reports every fixed-effect term; mixed-model entries are variational-posterior means with approximate 95\% intervals, while GEE entries use task-cluster-robust frequentist 95\% CIs. The final mixed-model entry is a random-effect standard deviation, not an odds ratio.}
\label{tab:inference}\centering\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llp{3.3cm}p{3.5cm}p{4.0cm}@{}}
\toprule
Panel & Item & Task-bootstrap $\Delta$ pp [95\%] & Mixed VB estimate [approx. 95\%] & GEE estimate [95\% CI], $p$ \\
\midrule
A & H1 bundle: C4--C1 & +53.9 [41.9, 65.7] & -- & -- \\
A & H2a convention-only: C3--C1 & +1.5 [$-$8.9, 11.7] & -- & -- \\
A & H2b convention within structure: C4--C2 & +24.3 [13.9, 35.6] & -- & -- \\
A & Structure: C2--C1 & +29.6 [17.2, 42.0] & -- & -- \\
A & Interaction: (C4--C2)--(C3--C1) & +22.8 [6.5, 39.8] & -- & task sign-flip $p=0.018$ \\
\midrule
B & Intercept & -- & OR 0.260 [0.234, 0.289] & OR 0.424 [0.207, 0.868], $p=0.019$ \\
B & M2 vs. M1 & -- & OR 2.370 [1.970, 2.850] & OR 2.012 [1.340, 3.019], $p=0.001$ \\
B & M3 vs. M1 & -- & OR 2.148 [1.787, 2.582] & OR 1.859 [1.210, 2.855], $p=0.005$ \\
B & Convention & -- & OR 1.088 [0.925, 1.280] & OR 1.066 [0.692, 1.642], $p=0.771$ \\
B & Structure bundle & -- & OR 4.903 [4.173, 5.762] & OR 3.485 [2.006, 6.056], $p<0.001$ \\
B & Convention $\times$ structure & -- & OR 5.307 [4.018, 7.009] & OR 4.536 [1.898, 10.837], $p=0.001$ \\
B & Task random-intercept SD & -- & 1.192 [0.859, 1.653] & -- \\
\bottomrule
\end{tabular}
\end{table*}"""

FIG1 = r"""\begin{figure*}[t]\centering
\includegraphics[width=0.9\textwidth]{fig1_architecture.pdf}
\caption{Architecture of the computable classroom and the CKU pipeline: two reliable layers bounded by a hard perimeter, out-of-library questions harvested into the library, and instructor verification closing the loop. Beyond the perimeter, a convention header alone does not repair improvised generation (Section VI.B). Conceptual diagram (contains no data); the architecture is a design proposal (Section VI).}
\label{fig:arch}\end{figure*}"""

# Fig.2 = heatmap (first result figure mentioned, in Section V.A);
# Fig.3 = error distribution (Section V.B). Ordered by first in-text mention.
FIG2 = r"""\begin{figure}[t]\centering
\includegraphics[width=\columnwidth]{fig3_2x2_heatmap.pdf}
\caption{$2\times2$ heatmap of numerical correctness (pooled across models). Pre-registered conditions. Rows: structural scaffolding; columns: convention information. Correctness jumps along the structure axis but is nearly flat along the convention axis without structure---the interaction.}
\label{fig:heatmap}\end{figure}"""

FIG3 = r"""\begin{figure}[t]\centering
\includegraphics[width=\columnwidth]{fig2_errors.pdf}
\caption{Mechanically decidable composition of improvised (C1) failures, by model ($N=355$ C1 failures). Pre-registered data. Only mechanically decidable categories are shown, deliberately excluding the unreliable conventional/conceptual split; silent wrong outputs are the majority (264, about 74\%)---precisely the class an instructor cannot catch at a glance.}
\label{fig:err}\end{figure}"""

FIG4 = r"""\begin{figure}[t]\centering
\includegraphics[width=\columnwidth]{fig4_latency.pdf}
\caption{Latency and the cost of truncation (pooled across models). Exploratory analysis of pre-registered latency data. (A) End-to-end latency by condition, with a long right tail; (B) share of \emph{correct} generations discarded if the instructor truncates at $t$ seconds (45\,s discards 34.9\%, 60\,s discards 24.4\%), costly because slow generations are often correct.}
\label{fig:latency}\end{figure}"""

for tag, tex_ in [("TBL1", TBL1), ("TBL2", TBL2), ("TBL3", TBL3),
                  ("TBL4", TBL4), ("TBL5", TBL5), ("TBL6", TBL6), ("TBL7", TBL7),
                  ("FIG1", FIG1), ("FIG2", FIG2), ("FIG3", FIG3), ("FIG4", FIG4)]:
    body_tex = body_tex.replace("%%" + tag + "%%", tex_)
body_tex = re.sub(r"@@\w+@@", "", body_tex)
# ieeeaccess drop-cap (\PARstart) on the first word of the Introduction
body_tex = re.sub(r"(\\section\{Introduction\}[^\n]*\n+)([A-Z])([a-z]+)",
                  r"\1\\PARstart{\2}{\3}", body_tex, count=1)

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

# Official IEEE Access template (ieeeaccess.cls + shipped fonts) staged in OUTDIR.
# Front matter follows access.tex: \history/\doi, \author{\uppercase..\authorrefmark},
# \address[n], \tfootnote, \markboth{..\headeretal..}, \corresp, keywords env, \PARstart, \EOD.
doc = r"""\documentclass{ieeeaccess}
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{booktabs}
\usepackage{array}
\graphicspath{{./}{../benchmark/figures/}}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

\begin{document}
\history{Date of publication XX XXXX XXXX, date of current version XX XXXX XXXX.}
\doi{10.1109/ACCESS.2026.0000000}

\title{Structure Before Convention: A Pre-Registered Reliability Benchmark and Two-Layer Deployment Architecture for Classroom LLM-Generated Financial Code}
\author{\uppercase{Ping Guo}\authorrefmark{1},
\uppercase{Wei Fan}\authorrefmark{2},
\uppercase{Jiaqiang Yang}\authorrefmark{3},
AND \uppercase{Xiaorui Li}\authorrefmark{2}}
\address[1]{School of Foreign Languages, Henan University of Technology, Zhengzhou 450001, China (e-mail: guopingapple@haut.edu.cn; ORCID: 0009-0005-3867-1007)}
\address[2]{Business School, Zhengzhou University, Zhengzhou 450001, China. Wei Fan (e-mail: vincentfan@whu.edu.cn; ORCID: 0000-0002-4174-1345); Xiaorui Li (ORCID: 0009-0003-5119-4079)}
\address[3]{Zhongyuan Critical Metals Laboratory, Zhengzhou University, Zhengzhou 450001, China (e-mail: jqyang@zzu.edu.cn; ORCID: 0000-0003-4707-2928)}
\tfootnote{This work was supported by the Zhengzhou University Undergraduate Education and Teaching Reform Project ``Construction and Practice of a Generative-AI-Enabled `Computable Classroom' for Securities Investment''; by the Zhengzhou University Graduate Education Research Project ``Innovation in the Full-Process Industry--Education Integration Training Model for the Master of Finance Programme'' (Grant No. YJSJY2025005); by the Henan Provincial Soft Science Research Program under Grant 252400411308 (``Carbon-Finance Innovation Mechanisms from the Perspectives of Risk Prevention and Simulation-Based Empirical Analysis,'' 2025); and by the Key Program of the Henan Provincial Soft Science Research Program under Grant 262400411016 (``Pathways and Policy Mechanisms for Building a Digital-Intelligent Sharing System for Large Scientific Instruments in Henan Province,'' 2026).}

\markboth
{P. Guo \headeretal: Structure Before Convention}
{P. Guo \headeretal: Structure Before Convention}

\corresp{Corresponding author: Ping Guo (e-mail: guopingapple@haut.edu.cn).}

\begin{abstract}
%%ABS%%
\end{abstract}

\begin{keywords}
%%KW%%
\end{keywords}

\titlepgskip=-21pt

\maketitle

%%BODY%%

\section*{Data and Code Availability}
%%DATA%%

\section*{Disclosure of AI Use}
%%DISC%%

\section*{Acknowledgment}
%%ACK%%

\begin{thebibliography}{00}
%%BIB%%
\end{thebibliography}

\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{photos/guo.jpg}}]{Ping Guo}
is a Lecturer with the School of Foreign Languages, Henan University of Technology, Zhengzhou, China, and is the corresponding author. Her work centers on the pedagogy of AI-assisted instruction and on the reliability of large language models when they are used to teach live in the classroom, and she currently leads a Ministry of Education Industry--University--Research Innovation Fund project on the AI-enabled digital transformation of English-major teaching. A recognized teaching innovator, she has been named a Henan Province Teaching Star, serves as principal investigator of a Henan Province First-Class Undergraduate Course, and has received First Prize in the Henan Provincial Education System Teaching Skills Competition, the Grand Prize in the cross-cultural track at the Henan round of the 14th National College Foreign Language Teaching Competition, and both the university teaching-competition First Prize and the President's Quality Award at Henan University of Technology, together with commendations from the Henan Provincial Department of Human Resources and Social Security in 2024 and 2025. She has supervised students to national awards in the FLTRP--Guocai Cup ``Understanding Contemporary China'' international-communication contest. Extending the benchmarking approach of the present study to the humanities, her companion paper, ``Can LLMs Teach Classical Literature Live? Benchmarking Quotation Fidelity and Textual Grounding,'' has been accepted at an IEEE conference. In this work she led the design of the computable-classroom framework and its reliability-benchmark methodology.
\end{IEEEbiography}

\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{photos/fan.jpg}}]{Wei Fan}
is an Associate Professor and doctoral supervisor with the Business School, Zhengzhou University, Zhengzhou, China, where he teaches securities investment. His research interests lie in quantitative finance and computational economics, spanning asset pricing, risk measurement, and the empirical methods that underpin them. In this study he anchored the financial-domain content (the curriculum's knowledge points, the analytic ground truth, and the conventions against which the generated code is judged), so that correctness is assessed as a finance instructor would assess it.
\end{IEEEbiography}

\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{photos/yang.jpg}}]{Jiaqiang Yang}
is with the Zhongyuan Critical Metals Laboratory, Zhengzhou University, Zhengzhou, China, working at the intersection of artificial intelligence and machine learning, where he has authored more than twenty peer-reviewed papers. His expertise in model evaluation and machine-learning methodology shaped the benchmark's technical design, including the format-neutral judging harness, the error-coding pipeline, and the cluster-robust statistical inference, grounding the study's reliability claims in rigorous evaluation practice.
\end{IEEEbiography}

\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{photos/li.jpg}}]{Xiaorui Li}
is a Master's student with the Business School, Zhengzhou University, Zhengzhou, China. She contributed to the study through data organization, experiment execution, and result verification. Her research interests include financial technology and the application of AI in finance education.
\end{IEEEbiography}

\EOD

\end{document}
"""
# Convert [n] -> \cite{refN} on CONTENT pieces only, never on the frontmatter
# template (which legitimately uses \address[1] etc. that must not become \cite).
doc = (doc.replace("%%ABS%%", cites(abstract_tex)).replace("%%KW%%", keywords)
       .replace("%%BODY%%", cites(body_tex)).replace("%%DATA%%", cites(data_tex))
       .replace("%%DISC%%", cites(disc_tex)).replace("%%ACK%%", cites(ack_tex))
       .replace("%%BIB%%", bib))
doc = sanitize(doc)

(OUTDIR / "main.tex").write_text(doc, encoding="utf-8")
print(f"wrote {OUTDIR/'main.tex'} ({len(doc)} chars, {len(bibitems)} refs)")
