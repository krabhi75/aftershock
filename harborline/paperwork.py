"""Label, manifest, and route writes."""

from __future__ import annotations

from harborline.model import Parcel, Store


def print_outbound_label(store: Store, parcel: Parcel) -> None:
    """Print the outbound label and record the manifest together."""
    with store.unit_of_work():
        store.write_label(parcel)
        store.write_manifest(parcel)


def quote_label_cost(store: Store, parcel: Parcel) -> int:
    """Price a label without writing anything."""
    return store.read_rate(parcel)


def book_return_leg(store: Store, parcel: Parcel) -> None:
    """Print a return label and add the parcel to the return manifest."""
    store.write_label(parcel)
    store.write_manifest(parcel)


def reroute_mid_flight(store: Store, parcel: Parcel) -> None:
    """Replace the label and record the new route."""
    store.write_label(parcel)
    store.write_route(parcel)
