#!/usr/bin/env python3
"""Apply the CreteXtract validation rules (validation/validation_config.json)
to a CSV of extracted rows and print per-rule pass counts.

Read-only: the input file is never modified. Requires pandas.

Usage:
    python scripts/apply_validation_rules.py output.csv [--config validation/validation_config.json]

Exit status 0 when every enabled rule passes on every row, 1 otherwise.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd  # noqa: F401  (the rule expressions reference pd and df by name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--config", default=str(Path(__file__).resolve().parent.parent / "validation" / "validation_config.json"))
    args = ap.parse_args()

    cfg = json.load(open(args.config, encoding="utf-8"))
    df = pd.read_csv(args.csv)

    any_fail = False
    print(f"{cfg['name']}: {len(df)} rows, {len(cfg['rules'])} rules")
    for rule in cfg["rules"]:
        if not rule.get("enabled", True):
            continue
        missing = [c for c in rule["columns"] if c not in df.columns]
        if missing:
            print(f"  {rule['rule_id']}: column(s) {missing} absent; rule not evaluated")
            any_fail = True
            continue
        # The expressions are plain pandas over `df`; evaluate them in a restricted namespace.
        mask = eval(rule["python_expression"], {"pd": pd, "df": df, "__builtins__": {"str": str, "float": float, "int": int, "bool": bool}})  # noqa: S307
        mask = pd.Series(mask, index=df.index).fillna(False).astype(bool)
        passed = int(mask.sum())
        failed = len(df) - passed
        status = "PASS" if failed == 0 else "FAIL"
        print(f"  {rule['rule_id']}: {rule['name']}: {passed}/{len(df)} rows passed [{rule['severity']}] {status}")
        if failed:
            any_fail = True
            idx = df.index[~mask].tolist()
            print(f"      flagged row indices (0-based): {idx[:20]}{' ...' if len(idx) > 20 else ''}")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
