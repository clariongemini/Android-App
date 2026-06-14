#!/usr/bin/env bash
# Geçici dizinde template Android iskeleti derler (CI + JDK doğrulama).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${CI_TEMPLATE_BUILD_DIR:-$(mktemp -d)}"
KEEP="${CI_KEEP_BUILD_DIR:-0}"

cleanup() {
  [[ "$KEEP" == "1" ]] || [[ "$WORK" == /* && "$WORK" == *"/tmp/"* ]] && rm -rf "$WORK" 2>/dev/null || true
}
trap cleanup EXIT

echo "==> CI template build"
echo "    Workdir: $WORK"

"$ROOT/scripts/scaffold-android-project-to.sh" "$WORK/ci-smoke" "FactoryCiSmoke" "com.ulas.factory.ci"
bash "$ROOT/scripts/bootstrap-gradle-wrapper.sh" "$WORK/ci-smoke" &>/dev/null

if ! command -v java &>/dev/null; then
  echo "HATA: JDK 17+ gerekli"
  exit 1
fi

(cd "$WORK/ci-smoke" && ./gradlew assembleDebug --no-daemon --quiet)
echo "==> CI template build başarılı."
