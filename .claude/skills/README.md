# Generated Claude skill adapters

Do not add or edit `SKILL.md` files here manually.

Run `python3 scripts/sync_skills.py` on POSIX or `py -3 scripts/sync_skills.py` on
Windows to generate one portable text adapter for each canonical skill under
`.agents/skills`. Each adapter points at `.agents/skills/<skill-name>/SKILL.md`
relative to the repository root.
