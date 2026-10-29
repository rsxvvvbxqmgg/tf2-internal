# Security Policy

tf2-internal is a cheat / aimbot project for Team Fortress 2. It is intended for
**offline, private-server, and educational** use. Using it on VAC-secured servers
will get your account banned. That is your problem, not ours.

## Reporting

If you find a memory-corruption bug in the Python injector or a crash in the
overlay, open an issue with:
- Windows build + Python version
- TF2 branch (public / prerelease)
- A minimal repro

## Scope

- In scope: crashes in `injector/`, offset parsing bugs, overlay rendering issues.
- Out of scope: "how do I avoid VAC", account bans, anything asking us to ship
  a new bypass. We don't do that.