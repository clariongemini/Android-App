#!/usr/bin/env bash
# Gradle wrapper dosyalarını indirir (gradlew + gradle-wrapper.jar).
# Kullanım: ./scripts/bootstrap-gradle-wrapper.sh [hedef-dizin]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$ROOT/templates/android/project}"
GRADLE_VERSION="8.11.1"
BASE="https://raw.githubusercontent.com/gradle/gradle/v${GRADLE_VERSION}"

if [[ ! -d "$TARGET" ]]; then
  echo "HATA: Hedef dizin yok: $TARGET"
  exit 1
fi

echo "==> Gradle wrapper bootstrap (v${GRADLE_VERSION})"
echo "    Hedef: $TARGET"

mkdir -p "$TARGET/gradle/wrapper"

curl -fsSL "$BASE/gradlew" -o "$TARGET/gradlew"
curl -fsSL "$BASE/gradlew.bat" -o "$TARGET/gradlew.bat"
curl -fsSL "$BASE/gradle/wrapper/gradle-wrapper.jar" -o "$TARGET/gradle/wrapper/gradle-wrapper.jar"

chmod +x "$TARGET/gradlew"

# properties zaten var; yoksa oluştur
PROPS="$TARGET/gradle/wrapper/gradle-wrapper.properties"
if [[ ! -f "$PROPS" ]]; then
  cat > "$PROPS" <<EOF
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
EOF
fi

if [[ ! -f "$TARGET/gradle/wrapper/gradle-wrapper.jar" ]]; then
  echo "HATA: gradle-wrapper.jar indirilemedi"
  exit 1
fi

if ! head -1 "$TARGET/gradlew" | grep -q '^#!/bin/sh'; then
  echo "HATA: gradlew geçersiz"
  exit 1
fi

echo "==> Gradle wrapper hazır ($(du -h "$TARGET/gradle/wrapper/gradle-wrapper.jar" | awk '{print $1}'))"
