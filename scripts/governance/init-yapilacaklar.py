#!/usr/bin/env python3
"""Inject source prompt into YAPILACAKLAR.md safely."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
YAP = ROOT / "YAPILACAKLAR.md"
PLACEHOLDER = "*(Mimar promptu buraya)*"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", nargs="+", help="Mimar source prompt words")
    args = p.parse_args()
    if not args.prompt:
        return 0
    if not YAP.exists():
        print("YAPILACAKLAR.md missing")
        return 1
    text = YAP.read_text(encoding="utf-8")
    prompt = " ".join(args.prompt).strip()[:2000]
    if PLACEHOLDER not in text:
        # replace existing Kaynak prompt line
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("| Kaynak prompt |"):
                lines[i] = f"| Kaynak prompt | {prompt} |"
                break
        text = "\n".join(lines) + "\n"
    else:
        text = text.replace(PLACEHOLDER, prompt)
    YAP.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
