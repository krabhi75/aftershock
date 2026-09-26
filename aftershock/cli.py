"""Command line for the local scan and the demo server."""

from __future__ import annotations

import argparse
import json
import sys

from aftershock.report import build_report, format_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aftershock",
        description="Find sibling faults an incident fix left in the tree.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="scan Harborline and print the sibling report")
    scan.add_argument("--incident", help="limit the scan to one incident id, such as INC-1042")
    scan.add_argument("--json", action="store_true", help="print the report as JSON")

    serve = sub.add_parser("serve", help="open the local class-closure board")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--host", default="127.0.0.1")

    args = parser.parse_args(argv)
    if args.cmd == "scan":
        report = build_report(incident_id=args.incident)
        if args.json:
            json.dump(report.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            sys.stdout.write(format_text(report))
        return 0
    if args.cmd == "serve":
        from aftershock.serve import serve

        serve(args.host, args.port)
        return 0
    return 2
