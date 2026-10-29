"""Wire up process attach, offset load, feature modules, and overlay."""
from __future__ import annotations

import time
from dataclasses import dataclass

from .config.schema import Config
from .injector.attach import ProcessAttachError, attach_to_tf2
from .injector.offsets import OffsetTable
from .features.aimbot import Aimbot
from .features.esp import ESPOverlay
from .features.triggerbot import Triggerbot
from .overlay.window import OverlayWindow
from .shared.log import get_logger

log = get_logger("bootstrap")


@dataclass
class Bootstrap:
    cfg: Config
    overlay: bool = True
    dry_run: bool = False

    def run(self) -> None:
        offsets = OffsetTable.load(self.cfg.offsets_path)
        log.info("loaded %d offsets from %s", len(offsets), self.cfg.offsets_path)

        if self.dry_run:
            log.info("dry-run: skipping attach")
            return

        try:
            proc = attach_to_tf2()
        except ProcessAttachError as exc:
            log.error("attach failed: %s", exc)
            raise SystemExit(2)

        aimbot = Aimbot(proc, offsets, self.cfg.aimbot)
        trigger = Triggerbot(proc, offsets, self.cfg.triggerbot)
        esp = ESPOverlay(proc, offsets, self.cfg.esp) if self.cfg.esp.enabled else None

        win = OverlayWindow(self.cfg.overlay) if self.overlay else None
        if win:
            win.attach(aimbot, trigger, esp)

        log.info("tf2-internal running — press INSERT to toggle, END to exit")
        try:
            while proc.is_alive():
                aimbot.tick()
                trigger.tick()
                if esp:
                    esp.tick()
                time.sleep(1.0 / max(self.cfg.tick_rate, 1))
        finally:
            if win:
                win.detach()