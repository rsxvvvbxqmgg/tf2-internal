"""Attach to a running hl2.exe (TF2) process and grab module bases."""
from __future__ import annotations

import os
from dataclasses import dataclass

import pymem
import pymem.process


class ProcessAttachError(RuntimeError):
    pass


@dataclass
class TF2Process:
    pm: pymem.Pymem
    pid: int
    client_base: int
    engine_base: int

    def is_alive(self) -> bool:
        try:
            self.pm.read_int(self.client_base)
            return True
        except Exception:
            return False


def attach_to_tf2(process_name: str = "hl2.exe") -> TF2Process:
    try:
        pm = pymem.Pymem(process_name)
    except pymem.exception.ProcessNotFound as exc:
        raise ProcessAttachError(f"{process_name} not running (start TF2 first)") from exc

    client = pymem.process.module_from_name(pm.process_handle, "client.dll")
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll")
    if client is None or engine is None:
        raise ProcessAttachError("client.dll / engine.dll not found — wrong process?")

    return TF2Process(pm=pm, pid=pm.process_id, client_base=client.lpBaseOfDll, engine_base=engine.lpBaseOfDll)


__all__ = ["TF2Process", "ProcessAttachError", "attach_to_tf2", "os"]