#!/usr/bin/env python3
"""Check a Surf Call webhook payload before you send it.

Catches the things that silently break the screen: text longer than the
layout allows, unknown board IDs, `prog` sent as a string, and payloads
over TRMNL's 2 KB webhook limit (5 KB on TRMNL+).

Usage:
  python3 tools/validate_payload.py payload.json [more.json ...]
  python3 tools/validate_payload.py --boards 96,80,68,72,64 payload.json
"""
import argparse
import json
import sys

CATEGORIES = {"LONGBOARD", "MIDLENGTH", "PUSH", "NOGO"}
LIMITS = {  # max characters per field; keep in sync with PAYLOAD.md
    "why": 110, "window": 16, "board_why": 34, "swell": 18, "wind": 24,
    "tide": 20, "suit": 16, "hazard": 64, "next": 60,
}
SPOT_LIMITS = {"name": 22}
MAX_BYTES = 2048


def check(payload: dict, boards: set) -> list:
    errs = []
    v = payload.get("merge_variables")
    if not isinstance(v, dict):
        return ["top level must be {\"merge_variables\": {...}}"]
    size = len(json.dumps(payload, ensure_ascii=False).encode())
    if size > MAX_BYTES:
        errs.append(f"payload is {size} bytes; TRMNL's limit is {MAX_BYTES} (5 KB on TRMNL+)")
    if v.get("cat") not in CATEGORIES:
        errs.append(f"cat must be one of {sorted(CATEGORIES)}, got {v.get('cat')!r}")
    for k, n in LIMITS.items():
        s = v.get(k) or ""
        if len(s) > n:
            errs.append(f"{k} is {len(s)} chars (max {n}): {s!r}")
    if not isinstance(v.get("prog", False), bool):
        errs.append("prog must be a JSON boolean (true/false), not a string")
    go = v.get("cat") != "NOGO"
    for k in ("board", "alt", "backup"):
        b = str(v.get(k) or "")
        if b and b not in boards:
            errs.append(f"{k}={b!r} is not a known board ID {sorted(boards)}")
    if go and not v.get("board"):
        errs.append("board is required unless cat is NOGO")
    if v.get("prog") and not v.get("backup"):
        errs.append("prog is true but no backup board was given")
    spots = v.get("spots", [])
    if not isinstance(spots, list):
        errs.append("spots must be a list")
        spots = []
    if len(spots) > 3:
        errs.append(f"{len(spots)} spots sent; only the first 3 are shown")
    for i, s in enumerate(spots):
        for k, n in SPOT_LIMITS.items():
            if len(s.get(k, "")) > n:
                errs.append(f"spots[{i}].{k} is {len(s[k])} chars (max {n})")
        b = str(s.get("board") or "")
        if b and b not in boards:
            errs.append(f"spots[{i}].board={b!r} is not a known board ID")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--boards", default="96,80,68,72,64", help="comma-separated board IDs from your markup's q_ids")
    args = ap.parse_args()
    boards = set(args.boards.split(","))
    bad = 0
    for f in args.files:
        errs = check(json.load(open(f)), boards)
        print(f"{'OK  ' if not errs else 'FAIL'} {f}")
        for e in errs:
            print(f"     - {e}")
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
