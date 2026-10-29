"""Triggerbot: fire when crosshair overlaps enemy hitbox."""
from __future__ import annotations

import keyboard

from ...config.schema import TriggerbotConfig
from ..injector.attach import TF2Process
from ..injector.offsets import OffsetTable
from ..shared.player import read_crosshair_entity, read_local_player


class Triggerbot:
    def __init__(self, proc: TF2Process, offsets: OffsetTable, cfg: TriggerbotConfig):
        self.proc = proc
        self.offsets = offsets
        self.cfg = cfg
        self._arming = False

    def tick(self) -> None:
        if not self.cfg.enabled or not keyboard.is_pressed(self.cfg.key):
            return
        me = read_local_player(self.proc, self.offsets)
        if me is None:
            return
        hit = read_crosshair_entity(self.proc, self.offsets)
        if hit is None or (hit.team == me.team):
            return
        if hit.health <= 0:
            return
        try:
            import mouse
            mouse.click(button="left")
        except Exception:
            pass