"""Rebuild the per-run figure archive for T2 visualization rating.

During the formal run, generated code saved figures to self-chosen paths
that later runs overwrote; the per-run figures were not archived. Every
generation's code IS archived and deterministic (fixed data snapshot, no
randomness in the tasks), so each figure is reproducible: re-execute each
T2 generation's code sequentially (cwd = repo root, headless) and copy the
file at result['figure_path'] to runs/raw/formal/figures/<run_id><ext>.

Resume-safe: run_ids with an archived figure are skipped.
Writes a manifest CSV with the outcome per run.
"""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runs" / "raw" / "formal" / "formal.jsonl"
CODE = ROOT / "runs" / "raw" / "formal" / "code"
FIGS = ROOT / "runs" / "raw" / "formal" / "figures"
FIGS.mkdir(exist_ok=True)

records = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines()
           if "_T2_" in json.loads(x)["run_id"] or json.loads(x)["task_id"].endswith("T2")]

manifest = []
env = dict(os.environ, MPLBACKEND="Agg")
done = {p.stem for p in FIGS.glob("*")}

for i, r in enumerate(records, 1):
    rid = r["run_id"]
    if rid in done:
        manifest.append({"run_id": rid, "status": "already"})
        continue
    code_path = CODE / f"{rid}.py"
    if not code_path.exists() or not r["code_extracted"]:
        manifest.append({"run_id": rid, "status": "no_code"})
        continue
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out_path = tf.name
    try:
        subprocess.run([sys.executable,
                        str(ROOT / "harness" / "_exec_module.py"),
                        str(code_path), out_path],
                       capture_output=True, timeout=90, cwd=str(ROOT), env=env)
        payload = json.loads(Path(out_path).read_text(encoding="utf-8"))
        fp = (payload.get("result") or {}).get("figure_path")
        if payload.get("exec_ok") and fp:
            src = (ROOT / fp) if not os.path.isabs(str(fp)) else Path(str(fp))
            if src.exists() and src.stat().st_size > 0:
                ext = src.suffix or ".png"
                shutil.copy2(src, FIGS / f"{rid}{ext}")
                manifest.append({"run_id": rid, "status": "ok"})
            else:
                manifest.append({"run_id": rid, "status": "fig_missing"})
        else:
            manifest.append({"run_id": rid,
                             "status": "exec_fail" if not payload.get("exec_ok")
                             else "no_figure_path"})
    except Exception as e:  # noqa: BLE001
        manifest.append({"run_id": rid, "status": f"error:{type(e).__name__}"})
    finally:
        try:
            os.unlink(out_path)
        except OSError:
            pass
    if i % 50 == 0:
        ok = sum(1 for m in manifest if m["status"] in ("ok", "already"))
        print(f"{i}/{len(records)} processed, archived {ok}")

df = pd.DataFrame(manifest)
df.to_csv(FIGS / "_manifest.csv", index=False)
print(df.status.value_counts().to_string())
