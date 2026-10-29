# VAC / Detection notes (educational)

This is a **research notebook**, not a bypass. We document what we know about
how TF2's VAC module behaves so contributors understand the risk surface of
this project.

- TF2 still runs a user-mode VAC module (as of late 2025). Kernel-mode VAC is
  for CS2 / newer titles.
- VAC scans for known cheat signatures in loaded modules and in memory regions
  flagged as executable + private.
- Running tf2-internal on a VAC-secured server will likely result in a ban.
- Use a private / community server with VAC disabled for testing.

Do **not** submit PRs that add "bypass" logic to this repo. Bypass research
belongs in private forks.