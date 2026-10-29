# Architecture

```
src/App                 CLI entrypoint (argparse + bootstrap)
src/tf2internal/
  bootstrap.py          wires attach -> features -> overlay
  config/               YAML schema + loader
  injector/             pymem attach, offset table, sig scanning
  features/             aimbot, triggerbot, esp
  overlay/              transparent window + DrawList sink
  shared/               math, logging, player memory reader
offsets/current.json    current client.dll offsets
scripts/dump_offsets.py rescan sigs -> offsets
tests/                  pytest suite
```

Rendering backends (ImGui/D3D11) are intentionally out of scope of the Python
tree — see `overlay/window.py` for the DrawList contract they consume.
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>