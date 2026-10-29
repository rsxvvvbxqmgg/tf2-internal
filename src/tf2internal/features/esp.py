"""ESP overlay: draw boxes, health bars, names for visible enemies."""
from __future__ import annotations

from ...config.schema import ESPConfig
from ..injector.attach import TF2Process
from ..injector.offsets import OffsetTable
from ..overlay.window import DrawList
from ..shared.player import read_local_player, read_entities


class ESPOverlay:
    def __init__(self, proc: TF2Process, offsets: OffsetTable, cfg: ESPConfig):
        self.proc = proc
        self.offsets = offsets
        self.cfg = cfg
        self._draw: DrawList | None = None

    def bind(self, draw: DrawList) -> None:
        self._draw = draw

    def tick(self) -> None:
        if not self.cfg.enabled or self._draw is None:
            return
        me = read_local_player(self.proc, self.offsets)
        if me is None:
            return
        for ent in read_entities(self.proc, self.offsets):
            if ent is me or ent.health <= 0 or ent is None:
                continue
            if ent.team == me.team:
                continue
            dist = (ent.origin - me.origin).length()
            if dist > self.cfg.distance:
                continue
            color = self.cfg.enemy_color
            if self.cfg.box:
                self._draw.box_world(ent.origin, color)
            if self.cfg.health_bar:
                self._draw.health(ent.health, ent.origin, color)
            if self.cfg.name:
                self._draw.text(ent.name, ent.origin, color)