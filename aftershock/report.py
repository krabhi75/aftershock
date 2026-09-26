"""Build the class-closure report from incidents plus the local scan."""

from __future__ import annotations

import time
from pathlib import Path

from aftershock.incidents import Incident, load_incidents
from aftershock.models import PLAIN_NAMES, Anchor, IncidentResult, Report
from aftershock.scan import scan_tree


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _excerpt(incident: Incident) -> str:
    return incident.excerpt


def build_report(root: Path | None = None, incident_id: str | None = None) -> Report:
    started = time.perf_counter()
    root = root or repo_root()
    incidents = load_incidents(root / "incidents")
    if incident_id is not None:
        incidents = [item for item in incidents if item.incident_id == incident_id]
        if not incidents:
            raise ValueError(f"no incident named {incident_id}")
    results: list[IncidentResult] = []
    for incident in incidents:
        findings, index = scan_tree(root, incident.fault_class)
        by_symbol = {item.symbol: item for item in findings}
        anchor_site = index.get(incident.fixed_symbol)
        if incident.fixed_symbol in by_symbol:
            status = "regressed"
            line = by_symbol[incident.fixed_symbol].line
            file = by_symbol[incident.fixed_symbol].file
        elif anchor_site is not None:
            status = "closed"
            line = anchor_site.line
            file = anchor_site.file
        else:
            status = "missing"
            line = None
            file = None
        open_siblings = [item for item in findings if item.symbol != incident.fixed_symbol]
        results.append(
            IncidentResult(
                incident_id=incident.incident_id,
                title=incident.title,
                fault_class=incident.fault_class,
                plain_name=PLAIN_NAMES[incident.fault_class],
                excerpt=_excerpt(incident),
                anchor=Anchor(
                    symbol=incident.fixed_symbol,
                    status=status,
                    file=file,
                    line=line,
                ),
                open_siblings=open_siblings,
            )
        )
    elapsed_ms = (time.perf_counter() - started) * 1000
    return Report(duration_ms=elapsed_ms, incidents=results)


def format_text(report: Report) -> str:
    lines = [
        "Aftershock",
        f"{report.open_count} open siblings, {report.closed_count} closed anchors, 0 Bobcoins, {report.duration_ms:.1f} ms",
        "",
    ]
    for incident in report.incidents:
        lines.append(f"{incident.incident_id}  {incident.plain_name}")
        lines.append(f"  {incident.anchor.status:9}  {incident.anchor.symbol}")
        if not incident.open_siblings:
            lines.append("  (no open siblings)")
        for sibling in incident.open_siblings:
            lines.append(f"  open       {sibling.symbol}:{sibling.line}")
            lines.append(f"             {sibling.reason}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
