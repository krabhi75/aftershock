# Aftershock mode

One incident per task. The budget is 40 Bobcoins for the whole hackathon.

The parent reads the incident file and runs `python3 -m aftershock scan`. Three sibling-fixer subagents run in parallel and each writes one file under `closures/`. They do not edit `harborline/`.

The parent applies those three functions, updates the test lines named in the user message, runs the test suite once, and stops.

Do not spawn a critic. Do not open a second incident. Do not read the tree.
