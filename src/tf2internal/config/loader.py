"""YAML -> Config loader with sane fallback defaults."""
from __future__ import annotations

from pathlib import Path

import yaml

from .schema import AimbotConfig, Config, ESPConfig, OverlayConfig, TriggerbotConfig


def _section(cls, data: dict | None):
    if not data:
        return cls()
    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def load_config(path: str | Path) -> Config:
    p = Path(path)
    if not p.exists():
        return Config()
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return Config(
        offsets_path=raw.get("offsets_path", "offsets/current.json"),
        tick_rate=int(raw.get("tick_rate", 144)),
        aimbot=_section(AimbotConfig, raw.get("aimbot")),
        triggerbot=_section(TriggerbotConfig, raw.get("triggerbot")),
        esp=_section(ESPConfig, raw.get("esp")),
        overlay=_section(OverlayConfig, raw.get("overlay")),
    )