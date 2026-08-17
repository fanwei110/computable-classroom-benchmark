#!/usr/bin/env bash
# Reproduce every table and figure of FinEdu-CodeGen from the released logs.
# Runs from the FULL artifact (Zenodo archive): the GitHub repo .gitignores
# runs/raw/ and coding/, but runs/results_formal.csv is committed and
# coding/auto/*.csv ship in the Zenodo archive. No API key needed for this
# script (regenerating raw generations from scratch does -- see README).
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python}"

echo "[1/7] Headline grid + journal stats             -> runs/journal_stats.txt"
"$PYTHON_BIN" analysis/journal_revision_stats.py

echo "[2/7] Outcome reconciliation (Table III)        -> runs/accounting_table.txt"
"$PYTHON_BIN" analysis/accounting_table.py
"$PYTHON_BIN" analysis/build_task_audit_table.py

echo "[3/7] Robustness: convention bound / leave-one-out -> runs/redteam_stats.txt"
"$PYTHON_BIN" analysis/redteam_verify.py
echo "      task-level reliability / sign-flip test    -> runs/l2_stats.txt"
"$PYTHON_BIN" analysis/l2_stats.py
echo "      pre-registered mixed logit + GEE           -> runs/mixed_logit_stats.txt"
"$PYTHON_BIN" analysis/mixed_logit.py runs/results_formal.csv > runs/mixed_logit_stats.txt

echo "[4/7] Factorial completion, wording x scaffold (Table IV)"
echo "                                                 -> runs/rev_crossing_stats.txt"
"$PYTHON_BIN" analysis/rev_crossing_stats.py

echo "[5/7] Secondary outcomes: visualization adequacy, error coding, cost"
"$PYTHON_BIN" analysis/vis_stats.py > runs/vis_stats.txt
"$PYTHON_BIN" analysis/human_coding_stats.py --condition C1
"$PYTHON_BIN" analysis/cost_analysis.py > runs/cost_stats.txt

echo "[6/7] Supplementary experiments + real-instructor validation"
"$PYTHON_BIN" analysis/exp_analyze.py > runs/exp_stats.txt
"$PYTHON_BIN" analysis/validate_realteacher.py > runs/realteacher_validation.txt

echo "[7/7] Figures (architecture, error mix, 2x2 heatmap, latency) -> figures/*.pdf"
"$PYTHON_BIN" figures/fig1_architecture.py
"$PYTHON_BIN" figures/fig2_errors.py
"$PYTHON_BIN" figures/fig3_2x2_heatmap.py
"$PYTHON_BIN" figures/fig4_latency.py

echo
echo "Done. The released numerical tables and source figures are regenerated above:"
echo "  Table II  <- runs/journal_stats.txt"
echo "  Table III <- runs/accounting_table.txt"
echo "  Table IV  <- runs/rev_crossing_stats.txt"
echo "  Table V   <- runs/journal_stats.txt (by task type)"
echo "  Table VI  <- config/models.yaml + runs/raw/*/*.jsonl (request metadata)"
echo "  Task audit <- docs/task_audit_table.md + docs/task_audit_table.csv"
echo "  Figs. 1-4 <- figures/*.pdf"
echo "  (Optional) rebuild results_formal.csv from raw logs: $PYTHON_BIN analysis/aggregate_formal.py"
