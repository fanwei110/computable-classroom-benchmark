"""从冻结任务 YAML 生成逐题审计索引。

输出 Markdown 与 CSV 两种格式，供论文、回复函和复现审计引用。脚本只读取
冻结任务、提示和评分配置，不读取盲化密钥，也不改动任何原始数据。
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "tasks"
DOC_DIR = ROOT / "docs"
FIELDS = [
    "task_id",
    "knowledge_point",
    "task_type",
    "title",
    "inputs_and_data",
    "required_outputs",
    "ground_truth_and_scoring",
    "tolerances",
    "frozen_prompt_variants",
]


def compact_json(value: Any) -> str:
    """把 YAML 值压缩为稳定、可审计的单行 JSON。

    Parameters
    ----------
    value : Any
        YAML 解析后的值。

    Returns
    -------
    str
        保留 Unicode、键顺序稳定的单行 JSON。
    """

    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def prompt_index(task_id: str) -> str:
    """列出某题实际存在的冻结提示文件。

    Parameters
    ----------
    task_id : str
        任务标识，如 KP1_T1。

    Returns
    -------
    str
        以分号分隔的仓库相对路径；缺文件时立即报错。
    """

    expected = [
        ROOT / "prompts" / "C1_final" / f"{task_id}_A.md",
        ROOT / "prompts" / "C1_final" / f"{task_id}_B.md",
        ROOT / "prompts" / "C2_zh" / f"{task_id}.md",
        ROOT / "prompts" / "C3_final" / f"{task_id}_A.md",
        ROOT / "prompts" / "C3_final" / f"{task_id}_B.md",
        ROOT / "prompts" / "C4_zh" / f"{task_id}.md",
    ]
    missing = [path for path in expected if not path.exists()]
    if missing:
        raise FileNotFoundError(f"缺少冻结提示：{missing}")
    return "; ".join(path.relative_to(ROOT).as_posix() for path in expected)


def scoring_text(task: dict[str, Any]) -> tuple[str, str]:
    """汇总逐输出项的评分方法和数值容差。

    Parameters
    ----------
    task : dict[str, Any]
        单个任务 YAML。

    Returns
    -------
    tuple[str, str]
        评分方法与容差。图路径等非数值输出明确标为可视审计项。
    """

    rules = {
        rule["key"]: rule
        for rule in task.get("scoring", {}).get("keys", [])
    }
    methods = []
    tolerances = []
    for key in task.get("required_keys", []):
        rule = rules.get(key)
        if rule is None:
            methods.append(f"{key}: file/visual audit")
            tolerances.append(f"{key}: n/a")
            continue
        methods.append(f"{key}: {rule.get('method', 'unspecified')}")
        tau_rel = rule.get("tau_rel", "n/a")
        tau_abs = rule.get("tau_abs", "n/a")
        tolerances.append(f"{key}: rel={tau_rel}, abs={tau_abs}")
    ground_truth = "tasks/answers/answers.json; " + "; ".join(methods)
    return ground_truth, "; ".join(tolerances)


def build_rows() -> list[dict[str, str]]:
    """读取18个任务并构造审计表行。

    Returns
    -------
    list[dict[str, str]]
        已按任务标识排序的18行。
    """

    rows: list[dict[str, str]] = []
    task_paths = sorted(TASK_DIR.glob("KP*_T*.yaml"))
    if len(task_paths) != 18:
        raise ValueError(f"预期18个任务 YAML，实际发现 {len(task_paths)} 个")
    for path in task_paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        ground_truth, tolerances = scoring_text(task)
        inputs = compact_json(task.get("inputs", {}))
        data_file = task.get("data_file") or "none"
        rows.append({
            "task_id": task["id"],
            "knowledge_point": task["knowledge_point"],
            "task_type": task["task_type"],
            "title": task["title"],
            "inputs_and_data": f"inputs={inputs}; data_file={data_file}",
            "required_outputs": ", ".join(task.get("required_keys", [])),
            "ground_truth_and_scoring": ground_truth,
            "tolerances": tolerances,
            "frozen_prompt_variants": prompt_index(task["id"]),
        })
    return rows


def md_escape(value: str) -> str:
    """转义 Markdown 表格中的分隔符。"""

    return value.replace("|", chr(92) + "|").replace(chr(10), " ")


def write_outputs(rows: list[dict[str, str]]) -> None:
    """写出 CSV 与 Markdown 审计表。

    Parameters
    ----------
    rows : list[dict[str, str]]
        build_rows 生成的审计行。
    """

    DOC_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DOC_DIR / "task_audit_table.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    md_path = DOC_DIR / "task_audit_table.md"
    header = [
        "# Frozen 18-task audit index",
        "",
        "Generated from tasks/KP*_T*.yaml; ground-truth values are in "
        "tasks/answers/answers.json. Paths below are repository-relative. "
        "The table contains no blind key or raw API content.",
        "",
        "| " + " | ".join(FIELDS) + " |",
        "| " + " | ".join(["---"] * len(FIELDS)) + " |",
    ]
    body = [
        "| " + " | ".join(md_escape(row[field]) for field in FIELDS) + " |"
        for row in rows
    ]
    md_path.write_text(chr(10).join(header + body) + chr(10), encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"wrote {md_path}")


def main() -> None:
    """生成并校验逐题审计索引。"""

    rows = build_rows()
    if len({row["task_id"] for row in rows}) != 18:
        raise ValueError("任务标识不唯一或数量不足18")
    write_outputs(rows)


if __name__ == "__main__":
    main()
