# Aftershock

Aftershock is a post-incident maintenance workflow for IBM Bob 2.0. An incident fix closes one function. Sibling functions still fail the same way. Aftershock names those siblings, then Bob's Agent mode closes them in parallel.

The sample tree is Harborline, a fictional parcel-hub library. The incident write-ups are original and synthetic. There is no personal information in them.

## What the scan shows on a fresh clone

| | Count |
| --- | --- |
| Incidents | 3 |
| Anchors that stayed closed | 3 |
| Siblings still open | 8 |
| Bobcoins spent by the scan | 0 |

The eight open sites:

- `confirm_pickup`, `release_customs_hold`, `resolve_exception` still apply a retried event twice. `confirm_delivery` does not.
- `linehaul_departure_deadline`, `customer_promise_deadline`, `hold_expiry` still call `datetime.now()` with no timezone. `hub_intake_deadline` keeps UTC.
- `book_return_leg` and `reroute_mid_flight` still do two writes with no rollback. `print_outbound_label` rolls back inside `unit_of_work`.

## Run it

```bash
python3 -m unittest discover -s tests -v
python3 -m aftershock scan
python3 -m aftershock serve
```

Open http://127.0.0.1:8765 . The board is the demo surface. Click an open block, then use the subagent task it writes.

Python 3.11 or newer. The standard library is enough. No API keys.

## How Bob is the core

The scanner is the deterministic half, so the 40 hackathon Bobcoins are not spent on search. Bob IDE does the rest, through files this repo already contains:

- `.bob/skills/aftershock/SKILL.md` reads the incident (document understanding), runs the scan, and directs the work.
- `.bob/custom_modes.yaml` defines the Aftershock mode with the `subagent` tool group.
- `.bob/agents/sibling-fixer.md` and `.bob/agents/fault-critic.md` are the parallel personas.
- `.bob/rules/aftershock.md` is the rule that keeps the same shape from coming back.

`DEMO.md` is the two-task script that fits in the 40 Bobcoins. Those tasks are what you screenshot into `bob_sessions/`.

## Submission pack

Deadline on lablab is 27 September 2026, 15:00 UTC (20:30 IST). Paste-ready fields and upload files:

| lablab field | File |
| --- | --- |
| Title, short text, long text, tags | `submission/lablab-fields.md` |
| Cover image, 1920×1080 PNG | `submission/cover.png` |
| Slide deck PDF | `submission/Aftershock-slides.pdf` |
| Demo video, MP4 | `submission/Aftershock-demo.mp4` |

The board runs at http://127.0.0.1:8765 after `python3 -m aftershock serve`.

The September Bob guide also requires PNG screenshots of each Bob task consumption summary in `bob_sessions/`. Capture those from the hackathon Bob account with the prompts in `DEMO.md`. This repo does not contain stand-in screenshots.

Keep secrets out of the repo. This tree has none.
