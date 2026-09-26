---
name: aftershock
description: Close the open siblings of one incident inside the 40 Bobcoin budget. Use when the user names an incident id or asks to run Aftershock.
user-invocable: true
---

The hackathon account has 40 Bobcoins total. This skill spends them on one incident, INC-1042, unless the user names a different id.

Do not read the repository tree. Do not mention folders with @. Do not refactor, restyle, or start a second incident. Do not spawn a critic.

<Steps>
<Step>
Read only the incident file the user named. Quote the sentence that states the failure. Name the fault class in plain words: "Retry wrote twice" for INC-1042.
</Step>
<Step>
Run `python3 -m aftershock scan --incident INC-1042` from the repo root. The scanner is local and spends 0 Bobcoins.
</Step>
<Step>
Spawn three general subagents in one parallel batch, one per open sibling. Do not patch `harborline/movement.py` in the parent yet.

Each task description must begin with: Confirm one open Aftershock sibling by reading only that function.

Give each subagent one symbol and the exact replacement function from the user message. The subagent writes only `closures/<function_name>.py`.
</Step>
<Step>
After the three files exist, replace `confirm_pickup`, `release_customs_hold`, and `resolve_exception` in `harborline/movement.py` with those functions. Do not change `confirm_delivery`.
</Step>
<Step>
Apply the test edits from the user message in `tests/test_aftershock.py`. Leave `RuleTests` unchanged.
</Step>
<Step>
Run `python3 -m unittest discover -s tests -v` once. Then stop.
</Step>
</Steps>
