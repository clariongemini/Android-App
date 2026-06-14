#!/usr/bin/env python3
"""Validate YAPILACAKLAR.md phase discipline — single active phase, status vocabulary."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
YAP = ROOT / "YAPILACAKLAR.md"
VALID = frozenset({"bekliyor", "işleniyor", "tamamlandı", "isleniyor"})  # ascii fallback


def main() -> int:
    if not YAP.exists():
        print("   ❌ YAPILACAKLAR.md missing — run /baslat or init-new-app.sh")
        return 1

    text = YAP.read_text(encoding="utf-8")
    errors: list[str] = []

    phase_headers = re.findall(
        r"^## (F\d+) — .+ · `(bekliyor|işleniyor|isleniyor|tamamlandı)`",
        text,
        re.MULTILINE,
    )
    in_progress = [p for p, s in phase_headers if s in ("işleniyor", "isleniyor")]
    if len(in_progress) > 1:
        errors.append(f"Multiple phases in progress: {', '.join(in_progress)}")
    if len(in_progress) == 0:
        f8_done = re.search(r"## F8 — .+ · `tamamlandı`", text)
        if not f8_done:
            errors.append("No active phase (işleniyor) — set exactly one until F8 completes")

    for line in text.splitlines():
        if "| bekliyor |" in line or "| işleniyor |" in line or "| tamamlandı |" in line:
            continue
        m = re.search(r"\| (bekliyor|işleniyor|isleniyor|tamamlandı) \|?\s*$", line)
        if m and m.group(1) not in VALID:
            errors.append(f"Invalid status in line: {line[:80]}")

    summary = re.search(r"\| F0 \| .+ \| (\w+) \|", text)
    if not summary and not phase_headers:
        errors.append("No phase structure found")

    if errors:
        for e in errors:
            print(f"   ❌ {e}")
        return 1

    active = in_progress[0] if in_progress else "none"
    rows = len(re.findall(r"\| F\d+\.\d+ \|", text))
    print(f"   ✅ YAPILACAKLAR.md valid — active phase: {active}, task rows: {rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
