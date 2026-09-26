"""Read incident write-ups. The file's prose is what Bob reads; the front matter drives the local scan."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aftershock.models import PLAIN_NAMES


@dataclass(frozen=True)
class Incident:
    incident_id: str
    title: str
    fault_class: str
    fixed_symbol: str
    body: str
    path: Path

    @property
    def excerpt(self) -> str:
        paragraphs = [part.strip() for part in self.body.split("\n\n") if part.strip()]
        return paragraphs[0] if paragraphs else ""


def parse_incident(path: Path) -> Incident:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} is missing front matter")
    meta: dict[str, str] = {}
    index = 1
    while index < len(lines) and lines[index].strip() != "---":
        if ":" in lines[index]:
            key, value = lines[index].split(":", 1)
            meta[key.strip()] = value.strip()
        index += 1
    if index >= len(lines) or lines[index].strip() != "---":
        raise ValueError(f"{path} front matter does not close")
    fault_class = meta.get("fault_class", "")
    if fault_class not in PLAIN_NAMES:
        known = ", ".join(sorted(PLAIN_NAMES))
        raise ValueError(f"{path} has unknown fault_class {fault_class!r}. Known: {known}")
    required = ("id", "title", "fault_class", "fixed_symbol")
    missing = [key for key in required if not meta.get(key)]
    if missing:
        raise ValueError(f"{path} is missing {', '.join(missing)}")
    body = "\n".join(lines[index + 1 :]).strip()
    return Incident(
        incident_id=meta["id"],
        title=meta["title"],
        fault_class=fault_class,
        fixed_symbol=meta["fixed_symbol"],
        body=body,
        path=path,
    )


def load_incidents(directory: Path) -> list[Incident]:
    paths = sorted(directory.glob("INC-*.md"))
    return [parse_incident(path) for path in paths]
