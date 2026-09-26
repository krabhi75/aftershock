# Finish inside 40 Bobcoins

The app, tests, and board are already built. Bob must not rebuild them. The 40 Bobcoins are only for two fresh tasks on the hackathon account.

Coins are not a flat fee per click. Every new message resends the whole conversation, so a long thread costs more than a new short task. Do not reply "continue", "also do the others", or "make it better" in the same chat.

## Before you type

1. Open this folder in Bob IDE v2.0.2 or later.
2. Settings → General. Select the hackathon instance from the invite email (`ibm-hackathon-xxxx`, region us-east). A personal account spends the wrong coins and does not count.
3. Note the Bobcoin number on that screen. If it is already near the cap, do only Task 2.
4. Mode: Aftershock. If it is missing, use Agent for Task 2 and Ask for Task 1.

## Task 1 — read the incident

New task. Ask mode. Send this and nothing else.

```
Read only incidents/INC-1042.md. Quote the sentence that says how the duplicate scan happened. Call the fault class "Retry wrote twice". Do not open any other file. Do not patch anything.
```

Screenshot the consumption summary to `bob_sessions/aftershock_task01_read_incident_summary.png`.

Stop. Do not send a follow-up in that task.

## Task 2 — three parallel siblings, then one apply

New task. Aftershock mode, or Agent mode. Paste this whole block once.

```
Use the Aftershock skill. Budget is the remaining hackathon Bobcoins. Do only INC-1042.

Read only incidents/INC-1042.md and quote the failure sentence.
Run: python3 -m aftershock scan --incident INC-1042
Do not read the rest of the tree.

Spawn three general subagents in one parallel batch. Each task description must start with:
Confirm one open Aftershock sibling by reading only that function.

Subagent 1 writes only closures/confirm_pickup.py with this function and nothing else:

def confirm_pickup(parcel: Parcel, event_id: str) -> Parcel:
    """Mark the parcel picked up at the counter."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "picked_up"
    parcel.events.append(event_id)
    return parcel

Subagent 2 writes only closures/release_customs_hold.py:

def release_customs_hold(parcel: Parcel, event_id: str) -> Parcel:
    """Clear a customs hold after the broker posts a release."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "released"
    parcel.events.append(event_id)
    return parcel

Subagent 3 writes only closures/resolve_exception.py:

def resolve_exception(parcel: Parcel, event_id: str) -> Parcel:
    """Close an exception after the hub records a resolution."""
    if event_id in parcel.applied_events:
        return parcel
    parcel.applied_events.add(event_id)
    parcel.status = "resolved"
    parcel.events.append(event_id)
    return parcel

Those subagents must not edit harborline or tests and must not run commands.

When all three files exist, replace those three functions in harborline/movement.py. Do not change confirm_delivery.

In tests/test_aftershock.py make only these edits:
- set OPEN_SIBLINGS["INC-1042"] to an empty set
- change self.assertEqual(report.open_count, 8) to self.assertEqual(report.open_count, 5)
- change the confirm_pickup assertion self.assertEqual(picked.events, ["evt-1", "evt-1"]) to self.assertEqual(picked.events, ["evt-1"])
Do not edit RuleTests.

Run python3 -m unittest discover -s tests -v once. Then stop.
```

Screenshot to `bob_sessions/aftershock_task02_parallel_siblings_summary.png`. The parallel subagent panel should be visible in that task.

## Stop here

Do not run INC-1108 or INC-1177 in Bob. The local scanner already lists those five siblings, and it costs 0 coins:

```bash
python3 -m aftershock scan
python3 -m aftershock serve
```

Do not ask Bob to polish the UI, rewrite the README, or review the whole repo.

## If the meter is already high

If Settings shows most of the 40 coins gone before Task 2, skip the three subagents. Paste Task 2 with this sentence added at the top: "Do not spawn subagents. Apply the three functions yourself." You still get a real Bob task screenshot. The parallel panel is worth it only while coins remain.

## Screenshots

Tasks → open the task → click the task header → PNG of the consumption summary. Save both files in `bob_sessions/`. Then submit the public repo on https://lablab.ai/ai-hackathons/ibm-bob-2-hackathon before 27 September 2026, 20:30 IST.
