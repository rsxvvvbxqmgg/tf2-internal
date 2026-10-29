from pathlib import Path

import pytest

from tf2internal.injector.offsets import OffsetTable


def test_load_and_len():
    tbl = OffsetTable.load("offsets/current.json")
    assert len(tbl) >= 4
    assert tbl.get("m_iHealth") == 240


def test_missing_offset_raises():
    tbl = OffsetTable(data={"m_iHealth": 240})
    with pytest.raises(KeyError):
        tbl.get("dwEntityList")


def test_resolve_chain():
    tbl = OffsetTable(data={"dwLocalPlayer": 0x1000})
    assert tbl.resolve(0x400000, "dwLocalPlayer", 0x10) == 0x401010


def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        OffsetTable.load(Path("/nonexistent/offsets.json"))