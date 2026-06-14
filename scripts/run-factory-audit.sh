#!/usr/bin/env bash
# Fabrika özelliklerini adım adım denetler → docs/AUDIT_REPORT.md
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="$REPO_ROOT/templates/android/project"
REPORT="$REPO_ROOT/docs/AUDIT_REPORT.md"
DATE="$(date +%Y-%m-%dT%H:%M:%S%z)"

PASS=0
FAIL=0
SKIP=0
WARN=0

check() {
  local id="$1"
  local name="$2"
  local result="$3"
  local detail="${4:-}"
  case "$result" in
    pass) PASS=$((PASS + 1)); icon="✅" ;;
    fail) FAIL=$((FAIL + 1)); icon="❌" ;;
    skip) SKIP=$((SKIP + 1)); icon="⏭️" ;;
    warn) WARN=$((WARN + 1)); icon="⚠️" ;;
  esac
  RESULTS+=("| $id | $name | $icon $result | $detail |")
}

RESULTS=()

echo "==> Fabrika audit başlıyor..."
bash "$REPO_ROOT/scripts/factory/print-mission.sh"

check "F0.1" "first-setup.sh mevcut" "$([[ -x "$REPO_ROOT/scripts/first-setup.sh" ]] && echo pass || echo fail)"
check "F0.2" "init-governance.sh mevcut" "$([[ -x "$REPO_ROOT/scripts/governance/init-governance.sh" ]] && echo pass || echo fail)"
check "F0.3" "docs/00-INDEX.md" "$([[ -f "$REPO_ROOT/docs/00-INDEX.md" ]] && echo pass || echo fail)"
check "F0.M" "FACTORY_MISSION.md" "$([[ -f "$REPO_ROOT/FACTORY_MISSION.md" ]] && echo pass || echo fail)"
check "F0.4" "YAPILACAKLAR stub veya validator" \
  "$( [[ -f "$REPO_ROOT/YAPILACAKLAR.md" ]] && python3 "$REPO_ROOT/scripts/governance/validate-yapilacaklar.py" &>/dev/null && echo pass || echo fail)"
check "F0.5" "validate-audit-chain.py" \
  "$(python3 "$REPO_ROOT/scripts/governance/validate-audit-chain.py" &>/dev/null && echo pass || echo fail)"

if bash "$REPO_ROOT/scripts/check-mcp.sh" --warn &>/dev/null; then
  check "F0.MCP" "check-mcp.sh P0" "pass"
else
  check "F0.MCP" "check-mcp.sh P0" "warn" "MCP PAT yerel — docs/MCP_SETUP.md"
fi

check "F1.1" "docs/FACTORY_META/PRODUCT_BRIEF.md" \
  "$([[ -f "$REPO_ROOT/docs/FACTORY_META/PRODUCT_BRIEF.md" ]] && echo pass || echo fail)"
check "F1.2" "templates/vision mevcut" \
  "$([[ -f "$REPO_ROOT/templates/vision/PRODUCT_BRIEF.template.md" ]] && echo pass || echo fail)"

check "F2.1" "ANDROID_STRUCTURE.md" \
  "$([[ -f "$REPO_ROOT/docs/02-ARCHITECTURE/ANDROID_STRUCTURE.md" ]] && echo pass || echo fail)"
check "F2.2" "MODULE_MAP.md" \
  "$([[ -f "$REPO_ROOT/docs/02-ARCHITECTURE/MODULE_MAP.md" ]] && echo pass || echo fail)"
check "F2.3" "33 layer slices (33 dosya)" \
  "$(ls "$REPO_ROOT/docs/33-LAYER-MANIFEST"/layer-*.yaml 2>/dev/null | wc -l | tr -d ' ' | grep -q '^33$' && echo pass || echo fail)"
check "F2.4" "audit-module-map.sh" \
  "$(bash "$REPO_ROOT/scripts/audit-module-map.sh" &>/dev/null && echo pass || echo fail)"

MODULE_COUNT=0
if [[ -f "$TEMPLATE_DIR/settings.gradle.kts" ]]; then
  MODULE_COUNT="$(grep -cE '^\s*":' "$TEMPLATE_DIR/settings.gradle.kts" 2>/dev/null || echo 0)"
fi
check "F3.1" "templates/android/project/settings.gradle.kts" \
  "$([[ -f "$TEMPLATE_DIR/settings.gradle.kts" ]] && echo pass || echo fail)"
check "F3.2" "10 modül (template settings)" \
  "$([[ "$MODULE_COUNT" -ge 10 ]] && echo pass || echo fail)" "include count=$MODULE_COUNT"
check "F3.3" "audit-android-scaffold (template)" \
  "$(bash "$REPO_ROOT/scripts/audit-android-scaffold.sh" &>/dev/null && echo pass || echo fail)"
check "F3.4" "GlassCard.kt şablon" \
  "$([[ -f "$TEMPLATE_DIR/core/designsystem/src/main/java/{{PACKAGE_PATH}}/core/designsystem/component/GlassCard.kt" ]] && echo pass || echo fail)"

check "F4.1" "locales tr.json + en.json (template)" \
  "$([[ -f "$TEMPLATE_DIR/app/src/main/assets/locales/tr.json" && -f "$TEMPLATE_DIR/app/src/main/assets/locales/en.json" ]] && echo pass || echo fail)"

check "F5.1" "audit-security.sh" "$(bash "$REPO_ROOT/scripts/audit-security.sh" &>/dev/null && echo pass || echo fail)"
check "F5.2" "audit-oem-compat.sh" "$(bash "$REPO_ROOT/scripts/audit-oem-compat.sh" &>/dev/null && echo pass || echo fail)"
check "F5.3" "RootDetector.kt şablon" \
  "$([[ -f "$TEMPLATE_DIR/core/security/src/main/java/{{PACKAGE_PATH}}/core/security/RootDetector.kt" ]] && echo pass || echo fail)"

check "F6.1" "SPRINT_P schema template" \
  "$([[ -f "$REPO_ROOT/templates/governance/SPRINT_P_SCHEMA.template.json" ]] && echo pass || echo fail)"

check "CX.1" "gradle-build-loop.sh" "$([[ -x "$REPO_ROOT/scripts/gradle-build-loop.sh" ]] && echo pass || echo fail)"
check "CX.2" "state-recovery.sh" "$([[ -x "$REPO_ROOT/scripts/state-recovery.sh" ]] && echo pass || echo fail)"
check "CX.3" "validate-layer-slices.sh" \
  "$(bash "$REPO_ROOT/scripts/validate-layer-slices.sh" &>/dev/null && echo pass || echo fail)"
check "CX.4" "phase-agents.json" "$([[ -f "$REPO_ROOT/governance/phase-agents.json" ]] && echo pass || echo fail)"
check "CX.5" "18-state-recovery.mdc" "$([[ -f "$REPO_ROOT/.cursor/rules/18-state-recovery.mdc" ]] && echo pass || echo fail)"

REASONING="$REPO_ROOT/.cursor/rules/19-claude-reasoning.mdc"
CURSORRULES="$REPO_ROOT/.cursorrules"
check "V2.1" "19-claude-reasoning.mdc mevcut" "$([[ -f "$REASONING" ]] && echo pass || echo fail)"
check "V2.2" "19-claude-reasoning alwaysApply: true" \
  "$(grep -q 'alwaysApply: true' "$REASONING" 2>/dev/null && echo pass || echo fail)"
check "V2.3" "thinking + architecture_check şablon (.mdc)" \
  "$(grep -q '<thinking>' "$REASONING" && grep -q '<architecture_check>' "$REASONING" && echo pass || echo fail)"
check "V2.4" ".cursorrules Claude-Native protokol" \
  "$(grep -q 'Claude-Native' "$CURSORRULES" && grep -q '<thinking>' "$CURSORRULES" && echo pass || echo fail)"
check "V2.5" "docs/CLAUDE_REASONING.md" "$([[ -f "$REPO_ROOT/docs/CLAUDE_REASONING.md" ]] && echo pass || echo fail)"
check "V2.6" "20-aistudio-import (19 reasoning ayrımı)" \
  "$([[ -f "$REPO_ROOT/.cursor/rules/20-aistudio-import.mdc" ]] && ! [[ -f "$REPO_ROOT/.cursor/rules/19-aistudio-import.mdc" ]] && echo pass || echo fail)"
check "V2.7" "validate-reasoning-template-xml.sh" \
  "$(bash "$REPO_ROOT/scripts/validate-reasoning-template-xml.sh" &>/dev/null && echo pass || echo fail)"
check "V2.8" "negative_constraints şablon (.mdc)" \
  "$(grep -q '<negative_constraints>' "$REASONING" && grep -q '</negative_constraints>' "$REASONING" && echo pass || echo fail)"
check "V2.9" "kelime cap 150-200 (.mdc)" \
  "$(grep -q '150–200' "$REASONING" && echo pass || echo fail)"
check "V2.10" "validate-reasoning-transcript.sh (v2.2)" \
  "$(bash "$REPO_ROOT/scripts/validate-reasoning-transcript.sh" &>/dev/null && echo pass || echo fail)"

check "V3.1" "factory/README.md (Intelligence Layer)" \
  "$([[ -f "$REPO_ROOT/factory/README.md" ]] && echo pass || echo fail)"
check "V3.2" "docs/FACTORY_V3.md" \
  "$([[ -f "$REPO_ROOT/docs/FACTORY_V3.md" ]] && echo pass || echo fail)"
check "V3.3" "scripts/factory/validate-intelligence.sh" \
  "$(bash "$REPO_ROOT/scripts/factory/validate-intelligence.sh" &>/dev/null && echo pass || echo fail)"
check "V3.4" "templates/factory/proof_registry.template.json" \
  "$([[ -f "$REPO_ROOT/templates/factory/proof_registry.template.json" ]] && echo pass || echo fail)"
check "V3.5" "AGENTS.md freeze (agents_freeze)" \
  "$(python3 -c "import json; m=json.load(open('$REPO_ROOT/.factory/meta.json')); exit(0 if m.get('agents_freeze') else 1)" &>/dev/null && echo pass || echo warn)"

check "QG.1" "validate-code.sh" "$(bash "$REPO_ROOT/scripts/validate-code.sh" &>/dev/null && echo pass || echo fail)"
check "QG.2" "audit-layers.sh" "$(bash "$REPO_ROOT/scripts/audit-layers.sh" &>/dev/null && echo pass || echo fail)"
check "QG.3" "audit-layer-components.sh" "$(bash "$REPO_ROOT/scripts/audit-layer-components.sh" &>/dev/null && echo pass || echo fail)"
FH_OUT="$(bash "$REPO_ROOT/scripts/factory-health.sh" 2>&1 || true)"
check "QG.4" "factory-health.sh 100" \
  "$(echo "$FH_OUT" | grep -q '100 / 100' && echo pass || echo warn)"

JAVA_OK=false
command -v java &>/dev/null && java -version &>/dev/null 2>&1 && JAVA_OK=true
if [[ "$JAVA_OK" == true ]]; then
  set +e
  bash "$REPO_ROOT/scripts/ci-template-build.sh" &>/dev/null
  rc=$?
  set -e
  check "BUILD" "ci-template-build assembleDebug" "$([[ $rc -eq 0 ]] && echo pass || echo fail)" "exit $rc"
else
  check "BUILD" "ci-template-build assembleDebug" "skip" "JDK yok — CI smoke-build job kanıtı"
fi

SCORE=$((PASS * 100 / (PASS + FAIL + WARN + 1)))

cat > "$REPORT" <<EOF
# Factory Audit Report

> Oluşturulma: $DATE  
> Fabrika: \`$REPO_ROOT\`  
> Kaynak: \`templates/android/project\`

## Özet

| Metrik | Değer |
|--------|-------|
| ✅ Geçti | $PASS |
| ❌ Başarısız | $FAIL |
| ⚠️ Uyarı | $WARN |
| ⏭️ Atlandı | $SKIP |

## Adım denetimi

| ID | Adım | Sonuç | Detay |
|----|------|-------|-------|
$(printf '%s\n' "${RESULTS[@]}")

## Komutlar

\`\`\`bash
./scripts/run-factory-audit.sh
./scripts/factory-quality-gate.sh
./scripts/ci-template-build.sh   # JDK + template derleme
\`\`\`
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Audit: ✅ $PASS  ❌ $FAIL  ⚠️ $WARN  ⏭️ $SKIP"
echo "  Rapor: $REPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ $FAIL -eq 0 ]]
