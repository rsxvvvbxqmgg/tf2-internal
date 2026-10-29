"""Dump TF2 netvar / entity offsets from a running client.dll.

Usage: python scripts/dump_offsets.py > offsets/current.json
"""
from __future__ import annotations

import json
import sys

import pymem
import pymem.process

NETVARS = ["m_iHealth", "m_iTeamNum", "m_vecOrigin", "m_angEyeAnglesYaw"]
SIGS = {
    "dwLocalPlayer": b"\x48\x8B\x05????\x48\x8B\x88",
    "dwEntityList": b"\x48\x8B\x0D????\x48\x89",
    "dwCrosshairEntity": b"\x48\x8B\x0D????\x89\x0D",
}


def scan(handle: int, module_base: int, module_size: int, sig: bytes) -> int:
    import pymem.pattern
    return pymem.pattern.pattern_scan_module(handle, module_base, sig) or 0


def main() -> int:
    try:
        pm = pymem.Pymem("hl2.exe")
    except pymem.exception.ProcessNotFound:
        print("hl2.exe not running", file=sys.stderr)
        return 1
    client = pymem.process.module_from_name(pm.process_handle, "client.dll")
    out = {}
    for name, sig in SIGS.items():
        addr = scan(pm.process_handle, client.lpBaseOfDll, client.SizeOfImage, sig)
        if addr:
            out[name] = addr - client.lpBaseOfDll
    for n in NETVARS:
        out.setdefault(n, 0)
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())