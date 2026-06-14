#!/usr/bin/env bash
# Fabrika reposunda governance ağacının git/policy uyumu.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ERRORS=0

echo "==> Fabrika Governance Ağacı Denetimi"

# Runtime dosyalar repo kökünde tracked olmamalı
RUNTIME_PATHS=(
  "governance/executive/SPRINT_LOCK.json"
  "governance/executive/APPROVAL_QUEUE.md"
  "governance/project.config.json"
  "governance/reality/PRODUCT_REALITY_SCORE.json"
)

if [[ -d "$ROOT/.git" ]]; then
  for p in "${RUNTIME_PATHS[@]}"; do
    if git -C "$ROOT" ls-files --error-unmatch "$p" &>/dev/null; then
      echo "HATA: Runtime dosya git'te tracked — $p (gitignore + untrack gerekir)"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi

# Zorunlu charter'lar
REQUIRED_CHARTERS=(
  "governance/cao/DEPARTMENT_CHARTER.md"
  "governance/analytics/DEPARTMENT_CHARTER.md"
  "governance/product_decision/DEPARTMENT_CHARTER.md"
  "governance/execution/DEPARTMENT_CHARTER.md"
  "governance/market/DEPARTMENT_CHARTER.md"
  "governance/linguistic/DEPARTMENT_CHARTER.md"
  "governance/curriculum/DEPARTMENT_CHARTER.md"
  "governance/blue_ocean/DEPARTMENT_CHARTER.md"
  "governance/trends/DEPARTMENT_CHARTER.md"
  "governance/finance/DEPARTMENT_CHARTER.md"
  "governance/localization/DEPARTMENT_CHARTER.md"
  "governance/clinical/DEPARTMENT_CHARTER.md"
  "governance/egc/DEPARTMENT_CHARTER.md"
  "governance/csgb/DEPARTMENT_CHARTER.md"
  "governance/cdid/DEPARTMENT_CHARTER.md"
)

for c in "${REQUIRED_CHARTERS[@]}"; do
  if [[ ! -f "$ROOT/$c" ]]; then
    echo "HATA: Charter eksik — $c"
    ERRORS=$((ERRORS + 1))
  fi
done

# Policy belgesi
[[ -f "$ROOT/governance/FACTORY_REPO_POLICY.md" ]] || {
  echo "HATA: governance/FACTORY_REPO_POLICY.md eksik"
  ERRORS=$((ERRORS + 1))
}

# dependency-rules şablonu
[[ -f "$ROOT/governance/dependency-rules.json" ]] || {
  echo "HATA: governance/dependency-rules.json eksik"
  ERRORS=$((ERRORS + 1))
}

# Governance templates
for t in SPRINT_LOCK.template.json APPROVAL_QUEUE.template.md project.config.template.json; do
  [[ -f "$ROOT/templates/governance/$t" ]] || {
    echo "HATA: templates/governance/$t eksik"
    ERRORS=$((ERRORS + 1))
  }
done

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Governance ağacı denetimi BAŞARISIZ ($ERRORS)"
  exit 1
fi

echo "==> Fabrika governance ağacı doğrulandı."
