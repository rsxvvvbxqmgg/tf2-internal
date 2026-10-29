"""Read player entities from memory using the current OffsetTable."""
from __future__ import annotations

from dataclasses import dataclass

from ..injector.attach import TF2Process
from ..injector.offsets import OffsetTable
from .mathutil import Vec3


@dataclass
class Player:
    index: int
    health: int
    team: int
    name: str
    origin: Vec3
    eye: Vec3
    view_angle: float

    def bone_pos(self, bone_id: int) -> Vec3:
        idx = bone_id % 8
        return Vec3(self.origin.x, self.origin.y, self.origin.z + 0.08 * idx)


def read_local_player(proc: TF2Process, offsets: OffsetTable) -> Player | None:
    try:
        base = offsets.resolve(proc.client_base, "dwLocalPlayer")
        idx = proc.pm.read_int(base)
    except Exception:
        return None
    if idx in (0, -1):
        return None
    return _read_player(proc, offsets, idx)


def read_entities(proc: TF2Process, offsets: OffsetTable) -> list[Player]:
    out: list[Player] = []
    for i in range(1, 65):
        p = _read_player(proc, offsets, i)
        if p and p.health > 0:
            out.append(p)
    return out


def read_crosshair_entity(proc: TF2Process, offsets: OffsetTable) -> Player | None:
    try:
        addr = offsets.resolve(proc.client_base, "dwCrosshairEntity")
        idx = proc.pm.read_int(addr)
    except Exception:
        return None
    if idx <= 0:
        return None
    return _read_player(proc, offsets, idx)


def _read_player(proc: TF2Process, offsets: OffsetTable, index: int) -> Player | None:
    try:
        ent_list = proc.pm.read_longlong(proc.client_base + offsets.get("dwEntityList"))
        ent = proc.pm.read_longlong(ent_list + 0x10 * index)
        if not ent:
            return None
        hp = proc.pm.read_int(ent + offsets.get("m_iHealth"))
        team = proc.pm.read_int(ent + offsets.get("m_iTeamNum"))
        ox = proc.pm.read_float(ent + offsets.get("m_vecOrigin"))
        oy = proc.pm.read_float(ent + offsets.get("m_vecOrigin") + 0x4)
        oz = proc.pm.read_float(ent + offsets.get("m_vecOrigin") + 0x8)
        vx = proc.pm.read_float(ent + offsets.get("m_angEyeAnglesYaw"))
        return Player(
            index=index,
            health=hp,
            team=team,
            name=f"player_{index}",
            origin=Vec3(ox, oy, oz),
            eye=Vec3(ox, oy, oz + 0.65),
            view_angle=vx,
        )
    except Exception:
        return None