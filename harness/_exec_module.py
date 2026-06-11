"""Subprocess executor: import a generated module and serialize its `result`.

Usage: python _exec_module.py <module_path> <output_json_path>

The module's prints go to stdout/stderr freely; the extraction outcome is
written to <output_json_path> so noisy modules cannot corrupt the protocol.
Extraction is deliberately format-generous (format-neutral judging): dicts,
Mappings, pandas Series, and single-row DataFrames are all accepted; numpy
scalars, 0-d arrays, Decimals, and sequences are coerced to plain floats.
"""

import json
import sys
import traceback
from collections.abc import Mapping
from decimal import Decimal


def coerce_scalar(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        return v
    try:
        import numpy as np
        if isinstance(v, np.generic):
            return v.item()
        if isinstance(v, np.ndarray):
            if v.ndim == 0:
                return v.item()
            return [coerce_scalar(x) for x in v.tolist()]
    except ImportError:
        pass
    try:
        import pandas as pd
        if isinstance(v, pd.Series):
            if len(v) == 1:
                return coerce_scalar(v.iloc[0])
            return [coerce_scalar(x) for x in v.tolist()]
    except ImportError:
        pass
    if isinstance(v, (list, tuple)):
        return [coerce_scalar(x) for x in v]
    return repr(v)


def extract_result(obj):
    """Return (dict, container_kind) or (None, reason)."""
    if isinstance(obj, Mapping):
        return {str(k): coerce_scalar(v) for k, v in obj.items()}, "mapping"
    try:
        import pandas as pd
        if isinstance(obj, pd.Series):
            return {str(k): coerce_scalar(v) for k, v in obj.items()}, "series"
        if isinstance(obj, pd.DataFrame):
            if len(obj) == 1:
                row = obj.iloc[0]
                return {str(k): coerce_scalar(v) for k, v in row.items()}, "dataframe_row"
            return None, f"DataFrame with {len(obj)} rows (need exactly 1)"
    except ImportError:
        pass
    return None, f"unsupported result type {type(obj).__name__}"


def main():
    module_path, out_path = sys.argv[1], sys.argv[2]
    out = {"exec_ok": False, "has_result": False, "result": None,
           "container": None, "error_type": None, "error": None}
    try:
        # Execute the generated file the way a classroom would run a script
        # (python file.py): run_name="__main__" so `if __name__ == "__main__"`
        # guards fire. Disclosed amendment to the original import-based
        # loader - see DEVIATIONS.md #5; judging rules are unchanged.
        import runpy
        namespace = runpy.run_path(module_path, run_name="__main__")
        out["exec_ok"] = True
        if "result" in namespace:
            extracted, kind = extract_result(namespace["result"])
            if extracted is not None:
                out["has_result"] = True
                out["result"] = extracted
                out["container"] = kind
            else:
                out["container"] = kind  # reason string
    except BaseException as e:  # noqa: BLE001 - we must capture SystemExit etc.
        out["error_type"] = type(e).__name__
        out["error"] = "".join(traceback.format_exception_only(type(e), e)).strip()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
