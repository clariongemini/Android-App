#!/usr/bin/env python3
"""Validate PDC → Execution mandatory consumption layer (rule enforcement)."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "governance" / "execution" / "ROADMAP_CONSUMPTION_MANIFEST.json"

REQUIRED_MARKER = "PDC ZORUNLU TÜKETİM"
REQUIRED_PATH = "roadmap_priorities.json"

AGENTS = [
    ("cpo", ".cursor/rules/01-product-cpo.mdc"),
    ("architect", ".cursor/rules/02-architect.mdc"),
    ("android", ".cursor/rules/03-android-elite.mdc"),
    ("security", ".cursor/rules/04-auditor-security.mdc"),
    ("oem", ".cursor/rules/05-oem-compat-auditor.mdc"),
]


def _check_rule(agent_id: str, rel_path: str) -> dict:
    path = ROOT / rel_path
    if not path.exists():
        return {
            "agent_id": agent_id,
            "rule_file": rel_path,
            "exists": False,
            "enforced": False,
            "missing": ["rule_file"],
        }
    text = path.read_text(encoding="utf-8")
    has_marker = REQUIRED_MARKER in text
    has_path = REQUIRED_PATH in text
    has_reject = "rejected_features.json" in text
    enforced = has_marker and has_path and has_reject
    missing = []
    if not has_marker:
        missing.append("PDC ZORUNLU TÜKETİM section")
    if not has_path:
        missing.append("roadmap_priorities.json reference")
    if not has_reject:
        missing.append("rejected_features.json reference")
    return {
        "agent_id": agent_id,
        "rule_file": rel_path,
        "exists": True,
        "enforced": enforced,
        "missing": missing,
    }


def main() -> int:
    results = [_check_rule(aid, path) for aid, path in AGENTS]
    enforced_count = sum(1 for r in results if r["enforced"])
    total = len(results)
    enforcement_pct = int(100 * enforced_count / total) if total else 0
    layer_active = enforced_count == total

    now = datetime.now(timezone.utc).isoformat()
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    else:
        manifest = {}
    manifest["generated_at"] = now
    manifest["enforcement_layer"] = "active" if layer_active else "incomplete"
    manifest["enforcement_pct"] = enforcement_pct
    manifest["agents_enforced"] = enforced_count
    manifest["agents_total"] = total
    manifest["validation_results"] = results
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"   PDC consumption enforcement: {enforced_count}/{total} agents ({enforcement_pct}%)")
    for r in results:
        status = "✅" if r["enforced"] else "❌"
        print(f"   {status} {r['agent_id']}: {r['rule_file']}")
        if r.get("missing"):
            print(f"      missing: {', '.join(r['missing'])}")

    return 0 if layer_active else 1


if __name__ == "__main__":
    raise SystemExit(main())
