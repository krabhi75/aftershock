"""Parcel and store types shared by the sample workflows."""

from __future__ import annotations


class Parcel:
    def __init__(self, parcel_id: str) -> None:
        self.parcel_id = parcel_id
        self.status = "created"
        self.applied_events: set[str] = set()
        self.events: list[str] = []


class UnitOfWork:
    """Rollback label and manifest writes when the block raises."""

    def __init__(self, store: Store) -> None:
        self._store = store
        self._labels: list[str] = []
        self._manifests: list[str] = []
        self._routes: list[str] = []

    def __enter__(self) -> Store:
        self._labels = list(self._store.labels)
        self._manifests = list(self._store.manifests)
        self._routes = list(self._store.routes)
        return self._store

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: object) -> bool:
        if exc_type is not None:
            self._store.labels = self._labels
            self._store.manifests = self._manifests
            self._store.routes = self._routes
        return False


class Store:
    def __init__(self, fail_manifest: bool = False) -> None:
        self.labels: list[str] = []
        self.manifests: list[str] = []
        self.routes: list[str] = []
        self.fail_manifest = fail_manifest

    def write_label(self, parcel: Parcel) -> None:
        self.labels.append(parcel.parcel_id)

    def write_manifest(self, parcel: Parcel) -> None:
        if self.fail_manifest:
            raise RuntimeError("manifest unavailable")
        self.manifests.append(parcel.parcel_id)

    def write_route(self, parcel: Parcel) -> None:
        self.routes.append(parcel.parcel_id)

    def read_rate(self, parcel: Parcel) -> int:
        return 12

    def unit_of_work(self) -> UnitOfWork:
        return UnitOfWork(self)
