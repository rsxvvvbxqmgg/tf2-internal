"""Small vector / angle helpers used by aimbot and ESP."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)


def clamp(v: float, lo: float = -180.0, hi: float = 180.0) -> float:
    return max(lo, min(hi, v))


def angle_to(src: Vec3, dst: Vec3) -> float:
    d = dst - src
    if d.x == 0 and d.y == 0:
        return 0.0
    return math.degrees(math.atan2(d.y, d.x))