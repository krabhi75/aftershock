from harborline.models import Parcel


def release_customs_hold(parcel: Parcel, event_id: str) -> Parcel:
    """Clear a customs hold after the broker posts a release."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "released"
    parcel.events.append(event_id)
    return parcel
