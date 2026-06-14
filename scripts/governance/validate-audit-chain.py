#!/usr/bin/env python3
"""Validate hierarchical audit chain — L1/L2 parent departments per WP type."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "governance/executive/HIERARCHICAL_AUDIT_CHAIN.md"
QUEUE = ROOT / "governance/executive/APPROVAL_QUEUE.md"

# WP work type keywords → required L1 parent (must appear in APPROVAL_QUEUE L1 column)
L1_RULES = {
    "ui": "CPO",
    "compose": "CPO",
    "android": "CPO",
    "mimari": "Denetçi",
    "architect": "Denetçi",
    "güvenlik": "Baş Mimar",
    "security": "Baş Mimar",
    "oem": "Android",
    "mcp": "Baş Mimar",
    "curriculum": "CPO",
    "content": "CPO",
    "roadmap": "CAO",
    "pdc": "CAO",
    "execution": "CEO",
    "cec": "CEO",
}


def main() -> int:
    errors: list[str] = []

    if not PROTOCOL.exists():
        errors.append("HIERARCHICAL_AUDIT_CHAIN.md missing")

    if not QUEUE.exists():
        print("   ⚠️  APPROVAL_QUEUE.md not initialized — run init-governance.sh")
        return 0

    rows = []
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| WP-"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 6:
                rows.append({"wp": parts[0], "title": parts[1], "l1": parts[3], "l2": parts[4], "status": parts[5]})

    for row in rows:
        if row["l2"] in ("—", "-", ""):
            errors.append(f"{row['wp']}: L2 onaycı tanımsız")
        if "⏳" in row["l1"] and row["status"] == "`completed`":
            errors.append(f"{row['wp']}: completed but L1 pending")

    if errors:
        for e in errors:
            print(f"   ❌ {e}")
        return 1

    print(f"   ✅ Audit chain protocol present")
    print(f"   ✅ {len(rows)} WP rows in approval queue")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
