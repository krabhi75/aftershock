"""Aftershock package."""

__all__ = ["main"]


def main() -> None:
    from aftershock.cli import main as cli_main

    raise SystemExit(cli_main())
