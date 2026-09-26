# Aftershock

This repository is the Aftershock hackathon project.

When the user asks to close an incident, follow `.bob/skills/aftershock/SKILL.md`.

Run `python3 -m aftershock scan` before searching the tree by hand. Spawn one sibling-fixer subagent per open sibling, in parallel. The fault-critic reviews the patches.

The seeded bugs in `harborline/` are intentional until a Bob task closes them. Do not "clean them up" outside that workflow.
