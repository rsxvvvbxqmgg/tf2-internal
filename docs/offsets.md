# TF2 Offsets

Offsets in `offsets/current.json` are relative to `client.dll` base and must be
regenerated after every Valve update.

## Currently tracked

| name                  | notes                                       |
|-----------------------|---------------------------------------------|
| `dwLocalPlayer`       | pointer to local player entity index        |
| `dwEntityList`        | entity list head (indexed by 0x10 * idx)    |
| `dwCrosshairEntity`   | entity under crosshair (triggerbot uses)    |
| `m_iHealth`           | health (int)                                |
| `m_iTeamNum`          | team id (int)                               |
| `m_vecOrigin`         | world origin (float xyz)                    |
| `m_angEyeAnglesYaw`   | yaw angle (float) — used by aimbot          |

## Rebuilding

```
python scripts/dump_offsets.py > offsets/current.json
```

If `dwLocalPlayer` etc. come back as `0`, the sigs in `scripts/dump_offsets.py`
are stale — update them from the current `client.dll`.