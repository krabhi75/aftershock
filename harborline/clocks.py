"""Deadlines for hub intake, linehaul, promises, and holds."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def hub_intake_deadline(received_at: datetime) -> datetime:
    """Intake SLA, kept in UTC after INC-1108."""
    if received_at.tzinfo is None:
        received_at = received_at.replace(tzinfo=timezone.utc)
    return received_at.astimezone(timezone.utc) + timedelta(hours=6)


def shift_change_deadline() -> datetime:
    """Next shift boundary, timezone-aware."""
    return datetime.now(timezone.utc) + timedelta(hours=8)


def format_deadline_label(deadline: datetime) -> str:
    """Format a deadline that the caller already computed."""
    return deadline.strftime("%Y-%m-%d %H:%M")


def linehaul_departure_deadline() -> datetime:
    """When the linehaul truck is supposed to leave the dock."""
    return datetime.now() + timedelta(hours=4)


def customer_promise_deadline() -> datetime:
    """Promise time shown for a parcel that just entered the hub."""
    promised = datetime.now() + timedelta(days=2)
    return promised.replace(microsecond=0)


def hold_expiry() -> datetime:
    """When an unscanned hold should time out."""
    current = datetime.now()
    return current + timedelta(hours=12)
