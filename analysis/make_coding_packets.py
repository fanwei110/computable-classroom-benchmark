"""Generate the blinded double-coding packets for stage 3.

Outputs (under benchmark/coding/, gitignored working materials):
  README_编码说明.md          coder instructions (Chinese)
  calibration/drill_sheet.xlsx   20 planted samples to practice on
  calibration/answer_key.csv     sealed answer key (open only after drill)
  items/B####.txt             one file per failure: code + completion +
                              failed values vs references + harness evidence
  coder_A.xlsx / coder_B.xlsx identical scoring sheets, randomized order,
                              blinded (no model, no condition, no prompt)
  _key_do_not_open.csv        blind_id -> run_id mapping (for the analyst)

Scope: every generation needing human judgment = buckets numeric_wrong,
defensible, vis_failure. Non-executable generations (code_error) are
auto-coded CD per the frozen codebook rule and excluded from manual sheets;
format failures form the separately-reported category. Batch 1 = C1+C4
items (basis of Fig. 2 and the templated-residual analysis), batch 2 =
C2+C3; batch labels do NOT reveal which condition an item came from.
"""

import io
import json
import random
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runs" / "raw" / "formal" / "formal.jsonl"
OUT = ROOT / "coding"
SEED = 20260610

NEED_HUMAN = {"numeric_wrong", "defensible", "vis_failure"}


def failed_summary(details):
    """Compact 'key: got vs ref' lines from judge details."""
    lines = []
    inner = details.get("keys") if isinstance(details.get("keys"), dict) else details
    for k, d in inner.items():
        if isinstance(d, dict) and d.get("ok") is False:
            v, r = d.get("value"), d.get("reference")
            if v is not None and r is not None:
                lines.append(f"{k}: 提交值 {v}  |  参考值 {r}")
            else:
                lines.append(f"{k}: {d.get('reason', 'failed')}")
    if not lines and isinstance(details, dict):
        for k in ("reason", "matched", "evidence"):
            if k in details:
                lines.append(f"{k}: {details[k]}")
    return "\n".join(lines) or "(详见 judge details)"


def main():
    records = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines()]
    items = [r for r in records if r["judge"]["bucket"] in NEED_HUMAN]
    rng = random.Random(SEED)
    rng.shuffle(items)

    (OUT / "items").mkdir(parents=True, exist_ok=True)
    (OUT / "calibration").mkdir(exist_ok=True)

    rows_a, key_rows = [], []
    for i, r in enumerate(items, 1):
        blind_id = f"B{i:04d}"
        batch = 1 if r["condition"] in ("C1", "C4") else 2
        j = r["judge"]
        code_path = ROOT / "runs" / "raw" / "formal" / "code" / f"{r['run_id']}.py"
        code = code_path.read_text(encoding="utf-8") if code_path.exists() else "(无代码)"
        evid = ""
        if isinstance(j.get("details"), dict) and "evidence" in j["details"]:
            evid = f"harness声明探测: {j['details'].get('evidence')}\n"
        body = (
            f"=== {blind_id}  任务 {r['task_id']} ({r['task_id'].split('_')[1]}) ===\n\n"
            f"--- 任务要求的输出键 ---\n"
            f"{', '.join(json.loads((ROOT / 'tasks' / 'answers' / 'answers.json').read_text(encoding='utf-8'))[r['task_id']]['refs'].keys())}\n\n"
            f"--- 判分失败明细 ---\n{failed_summary(j.get('details', {}))}\n{evid}\n"
            f"--- 提取出的代码 ---\n{code}\n\n"
            f"--- 模型完整输出（含文字说明，用于判断 declared）---\n{r['completion']}\n"
        )
        (OUT / "items" / f"{blind_id}.txt").write_text(body, encoding="utf-8")
        rows_a.append({
            "blind_id": blind_id, "批次": batch, "task_id": r["task_id"],
            "task_type": r["task_id"].split("_")[1],
            "失败摘要": failed_summary(j.get("details", {}))[:180],
            "primary_class(CD/CV/CN/VZ)": "",
            "若CV_所用约定(自由填写)": "",
            "declared(Y/N)": "",
            "备注": "",
        })
        key_rows.append({"blind_id": blind_id, "run_id": r["run_id"],
                         "model": r["model"], "condition": r["condition"],
                         "bucket": j["bucket"]})

    df = pd.DataFrame(rows_a).sort_values(["批次", "blind_id"])
    for coder in ("A", "B"):
        with pd.ExcelWriter(OUT / f"coder_{coder}.xlsx", engine="openpyxl") as w:
            df[df["批次"] == 1].to_excel(w, sheet_name="批次1_优先", index=False)
            df[df["批次"] == 2].to_excel(w, sheet_name="批次2", index=False)
    pd.DataFrame(key_rows).to_csv(OUT / "_key_do_not_open.csv", index=False,
                                  encoding="utf-8-sig")

    # calibration drill from the 20 planted adversarial samples
    manifest = yaml.safe_load(
        (ROOT / "harness" / "adversarial" / "expected.yaml").read_text(encoding="utf-8"))
    drill, key = [], []
    for e in manifest["planted"]:
        drill.append({"样例文件": f"harness/adversarial/planted/{e['file']}",
                      "task_id": e["task"],
                      "primary_class(CD/CV/CN/VZ)": "", "declared(Y/N)": "", "备注": ""})
        key.append({"样例文件": e["file"], "正确类别": e["planted_class"],
                    "说明": e.get("note", "")})
    pd.DataFrame(drill).to_excel(OUT / "calibration" / "drill_sheet.xlsx", index=False)
    pd.DataFrame(key).to_csv(OUT / "calibration" / "answer_key.csv", index=False,
                             encoding="utf-8-sig")

    n1 = (df["批次"] == 1).sum()
    readme = f"""# 错误编码操作说明（双人盲评）

## 你要做什么
对每条失败的 AI 生成记录下一个主诊断（四选一）+ 判断它是否声明了所用惯例。
判据手册：benchmark/codebook.md（重点读 §1 四类判据、§2 机械判据、§4 十二个判例）。

## 四个类别代码
- CD = Code 代码病（程序错误；注意：跑不起来的已被自动归为CD，不在你的表里）
- CV = Conventional 约定病（模型/公式对，但用错了某个有教科书地位的惯例：
  年化天数、复利方式、百分比/小数、符号、ddof、付息频率、vega报价、四舍五入手算等）
- CN = Conceptual 概念病（用错模型/公式/定义，任何惯例替换都救不回来）
- VZ = Visualization 图形病（数对图错）

CV/CN 的机械判据：把它实际用的惯例代回去重算，若变对 → CV；否则 → CN。
每条 txt 里已给出"提交值 vs 参考值"，常见比值线索：×100=百分比；×0.83=按365天；
×1.004=按250天；差<0.2%=手算四舍五入（CV，约定=精度处理）。

declared 判断：只看代码注释、文字说明、result里的字符串——代码里出现数字本身不算声明。

## 流程
1. 校准：两人各自填 calibration/drill_sheet.xlsx（材料在 harness/adversarial/planted/），
   填完打开 answer_key.csv 对答案，分歧处对照 codebook 讨论。目标 20/20。
2. 正式编码：A 用 coder_A.xlsx，B 用 coder_B.xlsx（内容相同）。每行的完整材料在
   items/对应blind_id.txt。先做"批次1_优先"（{n1} 条），再做批次2（{len(df)-n1} 条）。
   **期间两人不得交流、不得使用任何 AI 工具辅助判断。**
3. 两份表发回给 Claude Code → 自动算 κ + 出分歧清单 → 两人仅就分歧合议定稿。

## 纪律
- 不要打开 _key_do_not_open.csv（盲评的全部意义所在）
- 拿不准就在备注里写下理由，宁可备注多，不要空着猜
"""
    (OUT / "README_编码说明.md").write_text(readme, encoding="utf-8")
    print(f"生成完成: {len(df)} 条待编码（批次1: {n1}, 批次2: {len(df)-n1}）, "
          f"20 条校准样例, items/ txt 文件 {len(items)} 个")


if __name__ == "__main__":
    main()
