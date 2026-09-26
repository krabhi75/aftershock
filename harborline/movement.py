"""Status transitions for a parcel moving through a hub."""

from __future__ import annotations

from harborline.model import Parcel


def confirm_delivery(parcel: Parcel, event_id: str) -> Parcel:
    """Mark the parcel delivered. A retried carrier webhook must not apply twice."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "delivered"
    parcel.events.append(event_id)
    return parcel


def confirm_pickup(parcel: Parcel, event_id: str) -> Parcel:
    """Mark the parcel picked up at the counter."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "picked_up"
    parcel.events.append(event_id)
    return parcel


def release_customs_hold(parcel: Parcel, event_id: str) -> Parcel:
    """Clear a customs hold after the broker posts a release."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "released"
    parcel.events.append(event_id)
    return parcel


def resolve_exception(parcel: Parcel, event_id: str) -> Parcel:
    """Close an exception after the hub records a resolution."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "resolved"
    parcel.events.append(event_id)
    return parcel


def record_weighstation(parcel: Parcel, event_id: str) -> Parcel:
    """Record a weigh-station pass. Retries are ignored."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "weighed"
    parcel.events.append(event_id)
    return parcel


def preview_status(parcel: Parcel) -> str:
    """Return the current status without changing it."""
    return parcel.status
