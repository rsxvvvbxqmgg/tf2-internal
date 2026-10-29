"""Aimbot: resolve nearest visible enemy, compute bone angle, smooth-move mouse."""
from __future__ import annotations

import math

import keyboard

from ...config.schema import AimbotConfig
from ..injector.attach import TF2Process
from ..injector.offsets import OffsetTable
from ..shared.log import get_logger
from ..shared.mathutil import angle_to, clamp
from ..shared.player import read_local_player, read_entities

log = get_logger("aimbot")

BONE_HEAD = 0
BONE_CHEST = 6


class Aimbot:
    def __init__(self, proc: TF2Process, offsets: OffsetTable, cfg: AimbotConfig):
        self.proc = proc
        self.offsets = offsets
        self.cfg = cfg
        self._active = False
        self._last_target = None

    def _bone(self) -> int:
        return BONE_CHEST if self.cfg.target_bone == "chest" else BONE_HEAD

    def tick(self) -> None:
        if not self.cfg.enabled:
            return
        pressed = keyboard.is_pressed(self.cfg.key)
        if not pressed:
            self._active = False
            return
        self._active = True

        me = read_local_player(self.proc, self.offsets)
        if me is None:
            return
        best, best_angle = None, self.cfg.fov
        for ent in read_entities(self.proc, self.offsets):
            if ent is me or ent.health <= 0:
                continue
            if self.cfg.team_check and ent.team == me.team:
                continue
            angle = angle_to(me.eye, ent.bone_pos(self._bone()))
            delta = abs(clamp(angle - me.view_angle))
            if delta < best_angle:
                best, best_angle = ent, delta

        if best is None:
            return
        target_angle = angle_to(me.eye, best.bone_pos(self._bone()))
        delta = target_angle - me.view_angle
        step = clamp(delta / max(self.cfg.smooth, 1.0))
        self._move_mouse(step)

    def _move_mouse(self, dx: float) -> None:
        # Windows SendInput hook lives in overlay/window.py; emit an intent event.
        try:
            import mouse  # optional
            mouse.move(int(dx * 4), 0, absolute=False)
        except Exception:
            pass

    @staticmethod
    def _rad2deg(v: float) -> float:
        return v * 180.0 / math.pi