# Tiny Hack 2 (kit dry run #2)

Build a small command-line tool that turns a folder of messy receipt text dumps into an
expense summary. One track. This is a rehearsal event: brief, data and deadlines are fake.

Official rules: none (rehearsal). The idea and the areas: [IDEA.md](IDEA.md).

Smoke: `python3 -m unittest discover -s tests -t . && python3 -m expenses samples/`

The product that ships is `main`: the last commit that passed the smoke check.

Board: https://github.com/users/atiladeokegab/projects/4

## Deadlines

Your agent checks these every session against the UTC column. GitHub milestones keep only the
date, so this UTC column is the clock, never the milestone.

| Deadline | Event time | UTC |
|---|---|---|
| build start | 2026-09-29T12:04+01:00 | 2026-09-29T11:04Z |
| code freeze | 2026-09-29T13:04+01:00 | 2026-09-29T12:04Z |
| reality test | 2026-09-29T13:14+01:00 | 2026-09-29T12:14Z |
| submit | 2026-09-29T13:29+01:00 | 2026-09-29T12:29Z |

## Judging criteria

- Correct totals: 50%
- Handles messy input: 30%
- Engineering: 20%

## Team

| Name | GitHub | Role |
|---|---|---|
| Atilade | @atiladeokegab | Lead; owns core and totals; reviews and merges |
| Matrix | @Atilmatrix | Parse area |

The lead's agents: Zeus plans, reviews, merges and builds the lead's tasks. When this page
or a review says "the lead", it may be Zeus acting for the lead.
