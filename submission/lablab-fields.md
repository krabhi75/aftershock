# Paste into lablab

## Project title

Aftershock

## Short description

Aftershock finds every sibling of a bug an incident fix left behind. IBM Bob closes that class in parallel. The search spends 0 of the 40 Bobcoins.

## Long description

Aftershock is a post-incident maintenance workflow. A team closes a ticket on one function, and the same fault is still sitting in sibling code. Delivery confirmation now ignores a retried carrier event. Pickup, customs release, and exception handling still apply that event twice. Other modules still call datetime.now() with no timezone, or write a label and a manifest with no rollback. The next incident is a sibling of the one that was just fixed.

Aftershock reads the incident note and runs a local structural scan. The scan lists every function that still has that shape, and it leaves the already-fixed anchors marked closed. The board shows the count, the reason, and a task a developer can hand to IBM Bob. Bob is the closer. The Aftershock skill reads the incident, Agent mode runs the scanner, and three subagents write one replacement function each, in parallel. A project rule then blocks that shape on the next edit. The scan spends none of the 40 hackathon Bobcoins, so the coins stay on reading the incident and applying the patches.

The sample is Harborline, a fictional parcel-hub library. The three incident notes are original and synthetic. They contain no personal information, no client data, and no material copied from a website. On a fresh clone the board shows 3 incidents, 3 anchors that stayed closed, and 8 siblings still open. Tests lock those facts: a delivery retry is a no-op, a pickup retry is not, the closed deadline is timezone-aware, and a failed manifest rolls back only on the path that uses a unit of work.

The audience is application and platform engineers who maintain production code after an incident. They use Aftershock to close a fault class before the next deploy, instead of waiting for the sibling to page them.

## Technology and category tags

IBM Bob, Python, Developer tools, AI agents, Application maintenance

## Files to upload

- Cover image: submission/cover.png (1920×1080 PNG)
- Slides: submission/Aftershock-slides.pdf
- Video: submission/Aftershock-demo.mp4
- Repository: this project, public
- Application: run `python3 -m aftershock serve` and open http://127.0.0.1:8765

## Still required from the Bob IDE

The September guide requires PNG screenshots of each Bob task's consumption summary in `bob_sessions/`. Those images have to be captured from the hackathon Bob account. This pack does not include stand-in screenshots.
