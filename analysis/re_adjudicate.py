"""Re-run adjudication for items that fell back to a single coder's vote
(adjudicator returned empty/unparseable under the small token budget).
Larger max_tokens; MiniMax-M3 with M2.7 fallback. Updates final_coded.csv
in place and regenerates fig2_data.csv + headline stats."""

import io
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
AUTO = ROOT / "coding" / "auto"
ITEMS = ROOT / "coding" / "items"
CLASSES = ["CD", "CV", "CN", "VZ"]
SLUGS = ["minimax/minimax-m3", "minimax/minimax-m2.7"]

api_key = re.search(r"sk-or-[\w-]+",
                    Path(r"D:\onedrive\桌面\论文\可计算课堂\api.txt").read_text(
                        encoding="utf-8")).group(0)


def adjudicate(bid, qrow, lrow):
    item = (ITEMS / f"{bid}.txt").read_text(encoding="utf-8")[:6000]
    prompt = (
        "你是金融学错误分类的仲裁人。两位编码员对下面这条AI生成代码的失败记录"
        "给出了不同分类。类别定义：CD=纯编程错误；CV=模型正确但用了错误的、"
        "有教科书地位的惯例（年化天数/复利/单位/符号/ddof/vega报价等）；"
        "CN=概念或公式本身用错（含硬编码四舍五入常数）；VZ=数对图错。"
        "机械判据：换惯例重算能变对且该惯例有教科书地位→CV，否则CN。\n\n"
        f"编码员1判 {qrow['coder_Q']}\n编码员2判 {lrow['coder_K']}\n\n"
        f"=== 记录 ===\n{item}\n\n"
        '只输出JSON：{"primary_class":"CD|CV|CN|VZ"}')
    for slug in SLUGS:
        for attempt in range(2):
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json={"model": slug, "max_tokens": 30000,
                          "messages": [{"role": "user", "content": prompt}]},
                    timeout=300, headers={"Authorization": f"Bearer {api_key}"})
                r.raise_for_status()
                text = r.json()["choices"][0]["message"]["content"] or ""
                m = re.search(r"\{.*?\}", text, re.S)
                if m:
                    d = json.loads(m.group(0))
                    if d.get("primary_class") in CLASSES:
                        return d["primary_class"], slug
            except (requests.RequestException, json.JSONDecodeError):
                pass
            time.sleep(3)
    return None, None


df = pd.read_csv(AUTO / "final_coded.csv")
todo = df[df.source == "fallback_Q"]
print(f"re-adjudicating {len(todo)} items")
n_fixed = 0
for idx, row in todo.iterrows():
    cls, slug = adjudicate(row.blind_id, row, row)
    if cls:
        df.loc[idx, "final_class"] = cls
        df.loc[idx, "source"] = f"adjudicated:{slug.split('/')[1]}"
        n_fixed += 1
    if (n_fixed % 10) == 0:
        print(f"  {n_fixed} fixed...", flush=True)
df.to_csv(AUTO / "final_coded.csv", index=False, encoding="utf-8-sig")
print(f"fixed {n_fixed}/{len(todo)}; remaining fallback: "
      f"{(df.source == 'fallback_Q').sum()}")

# regenerate Fig.2 data + headline stats
res = pd.read_csv(ROOT / "runs" / "results_formal.csv")
cd_auto = res[(res.condition == "C1") & (res.bucket == "code_error")]
fig2 = df[df.condition == "C1"][["model", "final_class", "hardcoded", "declared"]]
fig2 = pd.concat([fig2, pd.DataFrame(
    {"model": cd_auto.model, "final_class": "CD", "hardcoded": 0,
     "declared": "N"})], ignore_index=True)
fig2.to_csv(AUTO / "fig2_data.csv", index=False, encoding="utf-8-sig")
n = len(fig2)
print(f"\nFig.2 N={n}")
for c in CLASSES:
    k = (fig2.final_class == c).sum()
    print(f"  {c}: {k} ({100*k/n:.1f}%)")
print(f"  hardcoded within CN: {int(fig2.hardcoded.sum())}")
cv1 = df[(df.condition == "C1") & (df.final_class == "CV")]
print(f"  declared among C1 CV: {(cv1.declared=='Y').sum()}/{len(cv1)} "
      f"= {(cv1.declared=='Y').mean()*100:.1f}%")
print("\nsource mix:", df.source.value_counts().to_dict())
