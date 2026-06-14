#!/usr/bin/env python3
"""Resolve per-project metadata from .factory/project.json (generic factory default)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT = {
    "app_name": "App",
    "package_name": "com.example.app",
    "slug": "app",
}


def load_project_meta(root: Path | None = None) -> dict:
    root = root or ROOT
    meta_path = root / ".factory" / "project.json"
    if meta_path.exists():
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            return {**DEFAULT, **data}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULT)


def package_java_dir(root: Path | None = None) -> Path:
    meta = load_project_meta(root)
    rel = meta["package_name"].replace(".", "/")
    return (root or ROOT) / "app" / "src" / "main" / "java" / rel


def kotlin_path(root: Path | None = None, *parts: str) -> Path:
    return package_java_dir(root).joinpath(*parts)
