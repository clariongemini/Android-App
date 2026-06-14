#!/usr/bin/env python3
"""Validate YAPILACAKLAR.md phase discipline — single active phase, status vocabulary."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
YAP = ROOT / "YAPILACAKLAR.md"
PHASE_AGENTS = ROOT / "governance" / "phase-agents.json"
VALID = frozenset({"bekliyor", "işleniyor", "tamamlandı", "isleniyor"})


def load_phase_agents() -> dict:
    if not PHASE_AGENTS.exists():
        return {}
    data = json.loads(PHASE_AGENTS.read_text(encoding="utf-8"))
    return data.get("phases", {})


def sync_active_agents(text: str, active_phase: str | None) -> str:
    if not active_phase or active_phase == "none":
        return text
    phases = load_phase_agents()
    info = phases.get(active_phase)
    if not info:
        return text
    agents = ", ".join(f"`{a}`" for a in info.get("agents", []))
    layers = info.get("manifest_layers", [])
    layer_hint = ""
    if layers:
        paths = ", ".join(f"`layer-{n:02d}.yaml`" for n in layers[:6])
        if len(layers) > 6:
            paths += f" … (+{len(layers) - 6})"
        layer_hint = f" · manifest: {paths}"
    value = f"{agents}{layer_hint}"
    if re.search(r"^\| Aktif ajanlar \|", text, re.MULTILINE):
        text = re.sub(
            r"^\| Aktif ajanlar \| .+ \|$",
            f"| Aktif ajanlar | {value} |",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        # insert after Aktif faz row
        text = re.sub(
            r"(^\| Aktif faz \| .+ \|$)",
            rf"\1\n| Aktif ajanlar | {value} |",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    return text


def is_uninitialized(text: str) -> bool:
    return "yapilacaklar-state: uninitialized" in text


def main() -> int:
    if not YAP.exists():
        print("   ❌ YAPILACAKLAR.md missing — run /baslat or init-new-app.sh")
        return 1

    text = YAP.read_text(encoding="utf-8")

    if is_uninitialized(text):
        print("   ⏸ YAPILACAKLAR uninitialized — factory template (run /baslat or init-new-app.sh)")
        return 0

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

    if not phase_headers:
        errors.append("No phase structure found")

    if errors:
        for e in errors:
            print(f"   ❌ {e}")
        return 1

    active = in_progress[0] if in_progress else "none"
    updated = sync_active_agents(text, active)
    if updated != text:
        YAP.write_text(updated, encoding="utf-8")
        text = updated

    rows = len(re.findall(r"\| F\d+\.\d+ \|", text))
    print(f"   ✅ YAPILACAKLAR.md valid — active phase: {active}, task rows: {rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
