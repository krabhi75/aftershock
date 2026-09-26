"""Scanner rules, the seeded Harborline tree, and the local board."""

from __future__ import annotations

import json
import sys
import threading
import unittest
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aftershock.report import build_report, format_text  # noqa: E402
from aftershock.scan import match_function, scan_source  # noqa: E402
from aftershock.serve import make_server  # noqa: E402
from harborline.clocks import (  # noqa: E402
    customer_promise_deadline,
    hold_expiry,
    hub_intake_deadline,
    linehaul_departure_deadline,
    shift_change_deadline,
)
from harborline.model import Parcel, Store  # noqa: E402
from harborline.movement import confirm_delivery, confirm_pickup  # noqa: E402
from harborline.paperwork import book_return_leg, print_outbound_label  # noqa: E402

OPEN_SIBLINGS = {
    "INC-1042": {
        "harborline.movement.confirm_pickup",
        "harborline.movement.release_customs_hold",
        "harborline.movement.resolve_exception",
    },
    "INC-1108": {
        "harborline.clocks.linehaul_departure_deadline",
        "harborline.clocks.customer_promise_deadline",
        "harborline.clocks.hold_expiry",
    },
    "INC-1177": {
        "harborline.paperwork.book_return_leg",
        "harborline.paperwork.reroute_mid_flight",
    },
}

CLOSED_OR_SAFE = {
    "harborline.movement.confirm_delivery",
    "harborline.movement.record_weighstation",
    "harborline.movement.preview_status",
    "harborline.clocks.hub_intake_deadline",
    "harborline.clocks.shift_change_deadline",
    "harborline.clocks.format_deadline_label",
    "harborline.paperwork.print_outbound_label",
    "harborline.paperwork.quote_label_cost",
}


def _only_function(source: str):
    import ast

    tree = ast.parse(source)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(funcs) != 1:
        raise AssertionError(f"expected one function, found {len(funcs)}")
    return funcs[0]


class RuleTests(unittest.TestCase):
    def test_guarded_status_write_is_not_a_sibling(self) -> None:
        source = """
def confirm_delivery(parcel, event_id):
    if event_id in parcel.applied_events:
        return parcel
    parcel.status = "delivered"
"""
        self.assertIsNone(match_function(_only_function(source), "retry_blind_write"))

    def test_already_applied_helper_counts_as_a_guard(self) -> None:
        source = """
def confirm_delivery(parcel, event_id):
    if already_applied(parcel, event_id):
        return parcel
    parcel.status = "delivered"
"""
        self.assertIsNone(match_function(_only_function(source), "retry_blind_write"))

    def test_regressed_anchor_still_matches(self) -> None:
        source = """
def confirm_delivery(parcel, event_id):
    parcel.status = "delivered"
"""
        findings, _sites = scan_source(source, "harborline.movement", "retry_blind_write")
        self.assertEqual([item.symbol for item in findings], ["harborline.movement.confirm_delivery"])

    def test_aware_now_is_not_naive(self) -> None:
        source = """
def shift_change_deadline():
    return datetime.now(timezone.utc)
"""
        self.assertIsNone(match_function(_only_function(source), "naive_deadline"))

    def test_utcnow_is_naive(self) -> None:
        source = """
def hold_expiry():
    return datetime.utcnow()
"""
        matched = match_function(_only_function(source), "naive_deadline")
        self.assertIsNotNone(matched)
        assert matched is not None
        self.assertIn("datetime.utcnow", matched[0])

    def test_single_write_is_not_a_partial_commit(self) -> None:
        source = """
def quote(store, parcel):
    store.write_label(parcel)
"""
        self.assertIsNone(match_function(_only_function(source), "partial_commit"))

    def test_unit_of_work_closes_the_pair(self) -> None:
        source = """
def print_outbound_label(store, parcel):
    with store.unit_of_work():
        store.write_label(parcel)
        store.write_manifest(parcel)
"""
        self.assertIsNone(match_function(_only_function(source), "partial_commit"))

    def test_compensating_except_closes_the_pair(self) -> None:
        source = """
def book_with_undo(store, parcel):
    try:
        store.write_label(parcel)
        store.write_manifest(parcel)
    except Exception:
        store.void_label(parcel)
"""
        self.assertIsNone(match_function(_only_function(source), "partial_commit"))


class SeedTests(unittest.TestCase):
    def test_seed_has_eight_open_siblings_and_three_closed_anchors(self) -> None:
        report = build_report(ROOT)
        self.assertEqual(report.open_count, 8)
        self.assertEqual(report.closed_count, 3)
        self.assertEqual(report.to_dict()["bobcoins"], 0)
        for incident in report.incidents:
            self.assertEqual(incident.anchor.status, "closed")
            self.assertEqual(
                {item.symbol for item in incident.open_siblings},
                OPEN_SIBLINGS[incident.incident_id],
            )
        opened = {item.symbol for incident in report.incidents for item in incident.open_siblings}
        self.assertTrue(CLOSED_OR_SAFE.isdisjoint(opened))

    def test_text_report_names_each_open_sibling(self) -> None:
        text = format_text(build_report(ROOT))
        for symbols in OPEN_SIBLINGS.values():
            for symbol in symbols:
                self.assertIn(symbol, text)

    def test_one_incident_filter(self) -> None:
        report = build_report(ROOT, incident_id="INC-1177")
        self.assertEqual(report.open_count, 2)
        self.assertEqual(len(report.incidents), 1)

    def test_delivery_retry_is_a_no_op_and_pickup_retry_is_not(self) -> None:
        delivered = Parcel("HBL-44021")
        confirm_delivery(delivered, "evt-1")
        confirm_delivery(delivered, "evt-1")
        self.assertEqual(delivered.events, ["evt-1"])
        self.assertEqual(delivered.status, "delivered")

        picked = Parcel("HBL-44021")
        confirm_pickup(picked, "evt-1")
        confirm_pickup(picked, "evt-1")
        self.assertEqual(picked.events, ["evt-1", "evt-1"])

    def test_open_clocks_are_naive_and_the_closed_one_is_aware(self) -> None:
        self.assertIsNone(linehaul_departure_deadline().tzinfo)
        self.assertIsNone(customer_promise_deadline().tzinfo)
        self.assertIsNone(hold_expiry().tzinfo)
        self.assertIsNotNone(shift_change_deadline().tzinfo)
        local = datetime(2026, 3, 12, 18, 10, tzinfo=timezone(timedelta(hours=-7)))
        deadline = hub_intake_deadline(local)
        self.assertEqual(deadline.tzinfo, timezone.utc)
        self.assertEqual(deadline.hour, 7)
        self.assertEqual(deadline.day, 13)

    def test_failed_manifest_rolls_back_only_on_the_closed_path(self) -> None:
        closed = Store(fail_manifest=True)
        with self.assertRaises(RuntimeError):
            print_outbound_label(closed, Parcel("HBL-44021"))
        self.assertEqual(closed.labels, [])

        opened = Store(fail_manifest=True)
        with self.assertRaises(RuntimeError):
            book_return_leg(opened, Parcel("HBL-44021"))
        self.assertEqual(opened.labels, ["HBL-44021"])
        self.assertEqual(opened.manifests, [])


class BoardTests(unittest.TestCase):
    def test_board_serves_the_report_and_the_page(self) -> None:
        server = make_server("127.0.0.1", 0)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/report") as response:
                payload = json.load(response)
            self.assertEqual(payload["open_count"], 8)
            self.assertEqual(payload["bobcoins"], 0)
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as response:
                html = response.read().decode("utf-8")
            self.assertIn("Aftershock", html)
            self.assertIn("Scan again", html)
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/missing")
            self.assertEqual(caught.exception.code, 404)
            caught.exception.close()
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
