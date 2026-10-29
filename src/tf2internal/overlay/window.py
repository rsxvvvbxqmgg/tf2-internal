"""Transparent overlay window skeleton. Rendering hooks are stubbed for
ImGui/DirectX backends that ship separately — this module only manages the
window lifecycle and a DrawList queue."""
from __future__ import annotations

from dataclasses import dataclass, field

from ...config.schema import OverlayConfig
from ..shared.log import get_logger
from ..shared.mathutil import Vec3

log = get_logger("overlay")


@dataclass
class DrawList:
    commands: list[tuple] = field(default_factory=list)

    def box_world(self, origin: Vec3, color: tuple[int, int, int]) -> None:
        self.commands.append(("box", origin, color))

    def health(self, hp: int, origin: Vec3, color: tuple[int, int, int]) -> None:
        self.commands.append(("health", hp, origin, color))

    def text(self, value: str, origin: Vec3, color: tuple[int, int, int]) -> None:
        self.commands.append(("text", value, origin, color))

    def flush(self) -> list[tuple]:
        out = list(self.commands)
        self.commands.clear()
        return out


class OverlayWindow:
    def __init__(self, cfg: OverlayConfig):
        self.cfg = cfg
        self.draw = DrawList()
        self._aimbot = None
        self._trigger = None
        self._esp = None

    def attach(self, aimbot, trigger, esp) -> None:
        self._aimbot, self._trigger, self._esp = aimbot, trigger, esp
        if esp is not None:
            esp.bind(self.draw)
        log.info("overlay attached (%dx%d)", self.cfg.width, self.cfg.height)

    def detach(self) -> None:
        log.info("overlay detached")