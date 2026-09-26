# Paste into the lablab form

The fields below match the IBM Bob 2.0 hackathon page, section "What to submit?"
Deadline on that page: 27 September 2026, 8:30 PM IST, which is 11:00 AM ET.

## Project title

Aftershock

## Short description

Aftershock names every sibling an incident fix left behind. A structural scan decides. IBM Bob only writes the patch, in parallel, inside 40 Bobcoins.

## Long description — Problem and solution statement

The problem starts the moment an incident ticket is marked closed. The fix lands in one function. Sibling functions still have the same fault, and the next failure is that sibling, not a new bug. On the Harborline sample, delivery confirmation now ignores a retried carrier event. Pickup, customs release, and exception handling still apply that event twice. Other functions still call datetime.now() with no timezone, or write a label and then a manifest with no rollback. Asking a model to search the repository for "similar bugs" spends the context window on looking, and the list can change the next time the question is asked.

Aftershock closes the class. An incident note names the function that was fixed and the fault shape. A local Python scan walks Harborline with the ast module and lists every other module-level function that still has that shape. Functions that already have the guard stay closed. The board shows the count, the reason, the file, the line, and the exact task to hand to IBM Bob.

The people who use it are application and platform engineers after a production fix. They open the board, filter to the incident, read the evidence, and copy one sibling task. They do not wait for the sibling to page them.

The part a judge has not seen done this way is the split between the fact and the repair. The model does not decide what is still broken. The structural scan does, in milliseconds, for zero of the 40 Bobcoins. IBM Bob only writes the patch. Three subagents run in parallel. Each one may read one function and write one new file. The parent applies those three functions, updates the three seed assertions, and runs the test suite once. On a fresh clone the board shows 3 incidents, 3 anchors that stayed closed, and 8 siblings still open. Tests lock the behavior: a delivery retry is a no-op, a pickup retry is not, the closed deadline is timezone-aware, and a failed manifest rolls back only on the path that uses a unit of work. The incident notes and the Harborline code were written for this repository. They contain no personal information and no client data.

## IBM Bob usage statement

IBM Bob is the closer. It is not the search engine, so the 40 hackathon Bobcoins stay on two tasks.

Task 1 is a new task in Ask mode. Bob reads only incidents/INC-1042.md. It quotes the sentence that says how the duplicate scan happened, and it calls the fault class "Retry wrote twice." It does not open another file, and it does not patch anything. That task is the document-understanding step: the incident note is the document.

Task 2 is a new task in Aftershock mode, or in Agent mode if that mode is not listed. Bob reads the same incident, runs python3 -m aftershock scan --incident INC-1042, and spawns three general subagents in one parallel batch. Each subagent task starts with "Confirm one open Aftershock sibling by reading only that function." The first writes only closures/confirm_pickup.py. The second writes only closures/release_customs_hold.py. The third writes only closures/resolve_exception.py. Those subagents do not edit harborline or the tests, and they do not run commands. The parent replaces those three functions in harborline/movement.py, changes three assertions in tests/test_aftershock.py, and runs python3 -m unittest discover -s tests -v once. Then it stops. INC-1108 and INC-1177 stay on the local board, because listing them costs nothing.

The instructions Bob loads are in this repository: .bob/skills/aftershock/SKILL.md, .bob/custom_modes.yaml, .bob/agents/sibling-fixer.md, and .bob/rules/aftershock.md. DEMO.md is the full text of the two tasks. The scanner, the board, and the tests are local Python. They do not call a model.

This project does not use IBM watsonx.ai or IBM watsonx Orchestrate.

The task prompts are in DEMO.md. Consumption-summary screenshots are taken from the hackathon IBM Bob account in us-east after those two tasks and placed in bob_sessions/. The repository does not contain stand-in screenshots.

## Technology and category tags

IBM Bob, Python, Developer tools, AI agents, Application maintenance

## What the form also requires

- Public repository: https://github.com/krabhi75/aftershock
- Cover image: submission/cover.png, PNG, 16:9
- Slide presentation: submission/Aftershock-slides.pdf
- Video: submission/Aftershock-demo.mp4, 2 minutes 6 seconds, narrated, with the board on screen for at least 90 seconds
- Demo application URL: https://krabhi75.github.io/aftershock/
- Local board, same page with a live scan: `python3 -m aftershock serve`, then http://127.0.0.1:8765
- IBM Bob task session summary screenshots in bob_sessions/, one PNG per task, from the hackathon account
