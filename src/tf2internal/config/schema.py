"""Typed config schema for aimbot / esp / triggerbot sections."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AimbotConfig:
    enabled: bool = True
    key: str = "mouse4"
    fov: float = 8.0
    smooth: float = 3.2
    target_bone: str = "head"  # head | chest | pelvis
    team_check: bool = True
    visibility_check: bool = True


@dataclass
class TriggerbotConfig:
    enabled: bool = True
    key: str = "shift"
    delay_ms: int = 40
    hitbox: str = "head"


@dataclass
class ESPConfig:
    enabled: bool = True
    box: bool = True
    health_bar: bool = True
    name: bool = True
    distance: float = 400.0
    team_color: tuple[int, int, int] = (90, 200, 255)
    enemy_color: tuple[int, int, int] = (255, 60, 60)


@dataclass
class OverlayConfig:
    width: int = 1920
    height: int = 1080
    vsync: bool = False
    font: str = "Consolas"


@dataclass
class Config:
    offsets_path: str = "offsets/current.json"
    tick_rate: int = 144
    aimbot: AimbotConfig = field(default_factory=AimbotConfig)
    triggerbot: TriggerbotConfig = field(default_factory=TriggerbotConfig)
    esp: ESPConfig = field(default_factory=ESPConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)