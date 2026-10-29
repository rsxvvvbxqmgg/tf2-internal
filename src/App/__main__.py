"""tf2-internal entrypoint."""
from __future__ import annotations

import argparse
import sys

from colorama import init as colorama_init

from tf2internal.bootstrap import Bootstrap
from tf2internal.config.loader import load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tf2-internal", description="TF2 cheats / aimbot toolkit")
    parser.add_argument("-c", "--config", default="config/default.yaml")
    parser.add_argument("--no-overlay", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="parse offsets, do not attach")
    args = parser.parse_args(argv)

    colorama_init()
    cfg = load_config(args.config)
    boot = Bootstrap(cfg, overlay=not args.no_overlay, dry_run=args.dry_run)
    try:
        boot.run()
    except KeyboardInterrupt:
        print("[tf2-internal] interrupted")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())