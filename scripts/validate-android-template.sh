#!/usr/bin/env bash
# Android şablon kalite denetimi — placeholder yok, wrapper tam.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$ROOT/templates/android/project"
ERRORS=0

echo "==> Android Şablon Kalite Denetimi"

check() {
  local path="$1"
  local msg="$2"
  if [[ ! -e "$TEMPLATE/$path" ]]; then
    echo "HATA: $msg — $path"
    ERRORS=$((ERRORS + 1))
  fi
}

check "gradlew" "Gradle wrapper script"
check "gradlew.bat" "Gradle wrapper bat"
check "gradle/wrapper/gradle-wrapper.jar" "Gradle wrapper jar"
check "gradle/wrapper/gradle-wrapper.properties" "Gradle wrapper properties"

if [[ -f "$TEMPLATE/gradlew" ]] && grep -q "placeholder\|henüz oluşturulmadı" "$TEMPLATE/gradlew"; then
  echo "HATA: gradlew hâlâ placeholder"
  ERRORS=$((ERRORS + 1))
fi

# Kotlin/Java placeholder taraması
while IFS= read -r -d '' file; do
  if grep -qE '/\* (context|retry|via Hilt)|/\* context via Hilt \*/' "$file" 2>/dev/null; then
    echo "HATA: Placeholder kod — ${file#$ROOT/}"
    ERRORS=$((ERRORS + 1))
  fi
done < <(find "$TEMPLATE" \( -name '*.kt' -o -name '*.java' \) -print0 2>/dev/null)

# BillingRepository Hilt context zorunlu
BILLING="$TEMPLATE/feature/premium/src/main/java/{{PACKAGE_PATH}}/feature/premium/data/BillingRepository.kt"
if [[ -f "$BILLING" ]]; then
  if ! grep -q '@ApplicationContext' "$BILLING"; then
    echo "HATA: BillingRepository @ApplicationContext eksik"
    ERRORS=$((ERRORS + 1))
  fi
  if ! grep -q 'BillingClient.newBuilder(context)' "$BILLING"; then
    echo "HATA: BillingRepository context ile build edilmiyor"
    ERRORS=$((ERRORS + 1))
  fi
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Şablon kalite denetimi BAŞARISIZ ($ERRORS)"
  exit 1
fi

echo "==> Android şablon kalitesi doğrulandı."
