"""Load and resolve TF2 netvar / entity offsets from JSON dumps."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OffsetTable:
    data: dict[str, int]
    source: str = ""

    def __len__(self) -> int:
        return len(self.data)

    def get(self, name: str, default: int | None = None) -> int:
        if name in self.data:
            return self.data[name]
        if default is not None:
            return default
        raise KeyError(f"offset '{name}' missing — run scripts/dump_offsets.py")

    def resolve(self, base: int, name: str, *chain: int) -> int:
        addr = base + self.get(name)
        for off in chain:
            addr = addr + off
        return addr

    @classmethod
    def load(cls, path: str | Path) -> "OffsetTable":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"offset file not found: {p}")
        raw = json.loads(p.read_text(encoding="utf-8"))
        return cls(data={k: int(v) for k, v in raw.items()}, source=str(p))