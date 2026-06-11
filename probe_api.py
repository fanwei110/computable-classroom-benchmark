"""Minimal connectivity probe: one tiny completion per configured model.
Verifies the API key and the three OpenRouter slugs before any real run.
Usage: python probe_api.py --key-file <path>
"""

import argparse
import re
import time
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((ROOT / "config" / "models.yaml").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-file", required=True)
    args = ap.parse_args()
    key = re.search(r"sk-or-[\w-]+",
                    Path(args.key_file).read_text(encoding="utf-8")).group(0)
    url = CONFIG["api"]["base_url"].rstrip("/") + "/chat/completions"
    for mk, m in CONFIG["models"].items():
        body = {"model": m["openrouter_slug"],
                "messages": [{"role": "user", "content": "回答一个数字：1+1=?"}],
                "max_tokens": 200}
        t0 = time.perf_counter()
        try:
            r = requests.post(url, json=body, timeout=120,
                              headers={"Authorization": f"Bearer {key}"})
            dt = time.perf_counter() - t0
            if r.status_code == 200:
                d = r.json()
                content = (d["choices"][0]["message"]["content"] or "").strip()
                print(f"[OK]   {mk} {m['openrouter_slug']}: "
                      f"provider={d.get('provider')} model={d.get('model')} "
                      f"{dt:.1f}s reply={content[:40]!r}")
            else:
                print(f"[FAIL] {mk} {m['openrouter_slug']}: "
                      f"HTTP {r.status_code} {r.text[:200]}")
        except requests.RequestException as e:
            print(f"[FAIL] {mk} {m['openrouter_slug']}: {e!r}")


if __name__ == "__main__":
    main()
