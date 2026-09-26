from harborline.models import Parcel


def resolve_exception(parcel: Parcel, event_id: str) -> Parcel:
    """Close an exception after the hub records a resolution."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "resolved"
    parcel.events.append(event_id)
    return parcel
