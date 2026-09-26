"""Shared report types."""

from __future__ import annotations

from dataclasses import dataclass, field


PLAIN_NAMES = {
    "retry_blind_write": "Retry wrote twice",
    "naive_deadline": "Clock forgot its timezone",
    "partial_commit": "Two writes, no rollback",
}


@dataclass(frozen=True)
class Finding:
    symbol: str
    file: str
    line: int
    fault_class: str
    reason: str
    recommended_change: str

    def to_dict(self) -> dict[str, object]:
        return {
            "symbol": self.symbol,
            "file": self.file,
            "line": self.line,
            "fault_class": self.fault_class,
            "reason": self.reason,
            "recommended_change": self.recommended_change,
        }


@dataclass(frozen=True)
class FunctionSite:
    symbol: str
    file: str
    line: int


@dataclass(frozen=True)
class Anchor:
    symbol: str
    status: str
    file: str | None
    line: int | None

    def to_dict(self) -> dict[str, object]:
        return {
            "symbol": self.symbol,
            "status": self.status,
            "file": self.file,
            "line": self.line,
        }


@dataclass
class IncidentResult:
    incident_id: str
    title: str
    fault_class: str
    plain_name: str
    excerpt: str
    anchor: Anchor
    open_siblings: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.incident_id,
            "title": self.title,
            "fault_class": self.fault_class,
            "plain_name": self.plain_name,
            "excerpt": self.excerpt,
            "anchor": self.anchor.to_dict(),
            "open_siblings": [item.to_dict() for item in self.open_siblings],
        }


@dataclass
class Report:
    duration_ms: float
    incidents: list[IncidentResult]

    @property
    def open_count(self) -> int:
        return sum(len(item.open_siblings) for item in self.incidents)

    @property
    def closed_count(self) -> int:
        return sum(1 for item in self.incidents if item.anchor.status == "closed")

    def to_dict(self) -> dict[str, object]:
        return {
            "project": "Aftershock",
            "bobcoins": 0,
            "duration_ms": round(self.duration_ms, 1),
            "open_count": self.open_count,
            "closed_count": self.closed_count,
            "dataset": "Original synthetic incidents and Harborline code. No personal information.",
            "incidents": [item.to_dict() for item in self.incidents],
        }
