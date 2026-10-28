#!/usr/bin/env python3
"""Check a CreteXtract output CSV against the locked schema (schema/schema_v1.0.csv).

Read-only, in the same sense as the application's validation step: the script
reports problems and never changes the input.

Usage:
    python scripts/check_output_against_schema.py output.csv [--schema schema/schema_v1.0.csv]

Exit status 0 when the output conforms, 1 otherwise.
"""
import argparse
import csv
import sys
from pathlib import Path


def load_schema(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = []
    for r in rows:
        name = r["column"].strip()
        if name.startswith("<<<"):
            print(f"warning: schema row {r['position']} is an unresolved placeholder; skipping it", file=sys.stderr)
            continue
        cols.append({
            "name": name,
            "type": r["type"].strip(),
            "required": r["required"].strip().lower() == "yes",
        })
    return cols


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output_csv")
    ap.add_argument("--schema", default=str(Path(__file__).resolve().parent.parent / "schema" / "schema_v1.0.csv"))
    args = ap.parse_args()

    schema = load_schema(args.schema)
    expected = [c["name"] for c in schema]

    with open(args.output_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)

    problems = []

    missing = [c for c in expected if c not in header]
    extra = [c for c in header if c not in expected and not c.startswith("__")]  # __-prefixed = application metadata
    if missing:
        problems.append(("structural", "-", f"missing columns: {missing}"))
    if extra:
        problems.append(("structural", "-", f"columns outside the locked schema: {extra}"))

    for i, row in enumerate(rows, start=2):  # line 2 is the first data row
        for c in schema:
            if c["name"] not in row:
                continue
            v = (row[c["name"]] or "").strip()
            if c["required"] and v == "":
                problems.append(("presence", i, f"required field '{c['name']}' empty"))
            if v != "" and c["type"] == "number" and not is_number(v):
                problems.append(("structural", i, f"'{c['name']}' not numeric: {v!r}"))

    if problems:
        print(f"{len(problems)} problem(s) in {args.output_csv}:")
        for cat, line, msg in problems:
            print(f"  [{cat}] line {line}: {msg}")
        sys.exit(1)
    print(f"{args.output_csv}: {len(rows)} rows conform to {len(expected)} schema columns")


if __name__ == "__main__":
    main()
