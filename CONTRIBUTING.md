# Contributing to tf2-internal

Thanks for wanting to help with the TF2 aimbot / ESP / cheat project.

## Ground rules

- This is an educational reverse-engineering and modding project. Do not submit
  anything that involves monetization, RMT, or selling keys.
- Do not submit hardcoded VAC-bypass signatures. Bypass research goes into
  `docs/vac-notes.md` as prose, not code.
- Keep aimbot smoothing and FOV values configurable, never hardcode a "rage"
  preset that will get people clapped in a casual lobby.

## Workflow

1. Fork and branch off `main`: `git checkout -b feature/better-triggerbot`
2. Add tests under `tests/` for anything touching `core/aimbot` or offset parsing.
3. Run `pytest -q` and `ruff check .` before opening a PR.
4. Update `docs/offsets.md` if you bump any netvar / entity offset.

## Offset updates

TF2 ships updates. When offsets break, run `scripts/dump_offsets.py` against the
current `client.dll` / `engine.dll` and commit the resulting JSON to
`offsets/`. Don't commit your local dumps (see `.gitignore`).