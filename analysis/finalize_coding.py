"""Merge the three coding layers into final error classes + reliability stats.

Final-class rule (pre-declared):
  1. mechanical match (definitionally correct under the registered
     mechanical criterion) wins;
  2. else, if the two AI coders agree, their class stands;
  3. else, a third non-evaluated model (Llama-4-Maverick) adjudicates
     between the two AI votes (given both rationales, blinded like them).

Also: bucket code_error items are auto-CD (frozen rule) and join the
Fig.2 population; format failures stay a separately-reported category.

Outputs: coding/auto/final_coded.csv, fig2_data.csv, stats printout.
Usage: python finalize_coding.py --key-file <path>
"""

import argparse
import io
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
AUTO = ROOT / "coding" / "auto"
ITEMS = ROOT / "coding" / "items"
ADJUDICATOR = "meta-llama/llama-4-maverick"
CLASSES = ["CD", "CV", "CN", "VZ"]


def kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    a, b = pd.Series(a), pd.Series(b)
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in set(a) | set(b))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def load_ai(coder):
    rows = [json.loads(x) for x in
            (AUTO / f"ai_coder_{coder}.jsonl").read_text(encoding="utf-8").splitlines()]
    df = pd.DataFrame(rows).drop_duplicates("blind_id", keep="last")
    return df.set_index("blind_id")


def adjudicate(blind_id, qrow, krow, api_key):
    item = (ITEMS / f"{blind_id}.txt").read_text(encoding="utf-8")[:6000]
    prompt = (
        "你是金融学错误分类的仲裁人。两位编码员对下面这条AI生成代码的失败记录"
        "给出了不同分类。类别定义：CD=纯编程错误；CV=模型正确但用了错误的、"
        "有教科书地位的惯例（年化天数/复利/单位/符号/ddof/vega报价等）；"
        "CN=概念或公式本身用错（含硬编码四舍五入常数 hardcoded_constant）；"
        "VZ=数对图错。机械判据：换惯例重算能变对且该惯例有教科书地位→CV，否则CN。\n\n"
        f"编码员1判 {qrow['primary_class']}，理由：{qrow.get('rationale','')}\n"
        f"编码员2判 {krow['primary_class']}，理由：{krow.get('rationale','')}\n\n"
        f"=== 记录 ===\n{item}\n\n"
        '只输出JSON：{"primary_class":"CD|CV|CN|VZ","rationale":"30字内"}')
    body = {"model": ADJUDICATOR,
            "messages": [{"role": "user", "content": prompt}], "max_tokens": 8192}
    for attempt in range(3):
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              json=body, timeout=300,
                              headers={"Authorization": f"Bearer {api_key}"})
            r.raise_for_status()
            text = r.json()["choices"][0]["message"]["content"] or ""
            m = re.search(r"\{.*\}", text, re.S)
            if m:
                d = json.loads(m.group(0))
                if d.get("primary_class") in CLASSES:
                    return d["primary_class"]
        except (requests.RequestException, json.JSONDecodeError):
            pass
        time.sleep(5)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-file", required=True)
    args = ap.parse_args()
    api_key = re.search(r"sk-or-[\w-]+",
                        Path(args.key_file).read_text(encoding="utf-8")).group(0)

    key = pd.read_csv(ROOT / "coding" / "_key_do_not_open.csv").set_index("blind_id")
    mech = pd.read_csv(AUTO / "mechanical_coded.csv").set_index("run_id")
    q, k = load_ai("Q"), load_ai("K")

    rows = []
    for bid, krow_key in key.iterrows():
        run_id = krow_key["run_id"]
        m = mech.loc[run_id]
        qc = q.loc[bid] if bid in q.index else None
        kc = k.loc[bid] if bid in k.index else None
        q_cls = qc["primary_class"] if qc is not None else None
        k_cls = kc["primary_class"] if kc is not None else None

        if m["mech_class"] in CLASSES:
            final, source = m["mech_class"], "mechanical"
        elif q_cls and k_cls and q_cls == k_cls:
            final, source = q_cls, "ai_agree"
        elif q_cls and k_cls:
            adj = adjudicate(bid, qc, kc, api_key)
            final, source = (adj, "adjudicated") if adj else (q_cls, "fallback_Q")
        else:
            final, source = (q_cls or k_cls or "UNRESOLVED"), "single_coder"

        # declared: AI coders agree -> theirs; else mechanical auto-detection
        if qc is not None and kc is not None and qc["declared"] == kc["declared"]:
            declared = qc["declared"]
        else:
            declared = m["declared_auto"]

        rows.append({"run_id": run_id, "blind_id": bid,
                     "condition": krow_key["condition"], "model": krow_key["model"],
                     "bucket": krow_key["bucket"],
                     "mech_class": m["mech_class"], "mech_detail": m["mech_detail"],
                     "coder_Q": q_cls, "coder_K": k_cls,
                     "final_class": final, "source": source,
                     "declared": declared,
                     "hardcoded": int(m["mech_detail"] == "hardcoded_constant")})

    df = pd.DataFrame(rows)
    df.to_csv(AUTO / "final_coded.csv", index=False, encoding="utf-8-sig")

    # ---- reliability stats -------------------------------------------------
    both = df.dropna(subset=["coder_Q", "coder_K"])
    print(f"items: {len(df)}; with both AI votes: {len(both)}")
    print(f"AI-AI agreement: {(both.coder_Q == both.coder_K).mean()*100:.1f}% ; "
          f"Cohen's kappa = {kappa(both.coder_Q, both.coder_K):.3f}")
    mech_sub = both[both.mech_class.isin(CLASSES)]
    print(f"vs mechanical (n={len(mech_sub)}): "
          f"Q agree {(mech_sub.coder_Q == mech_sub.mech_class).mean()*100:.1f}% ; "
          f"K agree {(mech_sub.coder_K == mech_sub.mech_class).mean()*100:.1f}%")
    print("final source mix:", df.source.value_counts().to_dict())

    # ---- Fig.2 population: C1 strict failures excl. format ----------------
    res = pd.read_csv(ROOT / "runs" / "results_formal.csv")
    cd_auto = res[(res.condition == "C1") & (res.bucket == "code_error")]
    fig2 = df[(df.condition == "C1")][["model", "final_class", "hardcoded", "declared"]]
    fig2 = pd.concat([fig2, pd.DataFrame(
        {"model": cd_auto.model, "final_class": "CD", "hardcoded": 0,
         "declared": "N"})], ignore_index=True)
    fig2.to_csv(AUTO / "fig2_data.csv", index=False, encoding="utf-8-sig")
    n = len(fig2)
    print(f"\nFig.2 population (C1, excl. format failures): N={n}")
    shares = fig2.final_class.value_counts()
    for c in CLASSES:
        print(f"  {c}: {shares.get(c, 0)} ({100*shares.get(c, 0)/n:.1f}%)")
    print(f"  hardcoded_constant subtag within CN: {int(fig2.hardcoded.sum())}")
    cv1 = df[(df.condition == "C1") & (df.final_class == "CV")]
    if len(cv1):
        print(f"  declared rate among C1 CV failures: "
              f"{(cv1.declared == 'Y').mean()*100:.1f}% ({(cv1.declared == 'Y').sum()}/{len(cv1)})")
    # format failures, separately reported
    fmt = res[(res.condition == "C1") & (res.bucket == "format_failure")]
    print(f"  format failures (separate category): {len(fmt)} "
          f"(no-code: {int((fmt.exec_ok == 0).sum())})")


if __name__ == "__main__":
    main()
