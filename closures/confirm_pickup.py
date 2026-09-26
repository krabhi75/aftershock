from harborline.models import Parcel


def confirm_pickup(parcel: Parcel, event_id: str) -> Parcel:
    """Mark the parcel picked up at the counter."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "picked_up"
    parcel.events.append(event_id)
    return parcel
