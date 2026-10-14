# CLAUDE.md — Caffeinated Nerds · BIOS Hackathon

> You are working in the shared repo of team **Caffeinated Nerds** for the **BIOS Hackathon (Thapar)**.
> Problem: **Fast and Secure Online Transaction Authentication**. We're building a real-time risk service that returns **allow / challenge / block** for a transaction and explains the signals behind the decision.

> **Not set up yet?** (no clone, no git identity, or a new teammate) → follow [`SETUP.md`](SETUP.md) first.

## 0. Rule #1: sync before anything else

A `SessionStart` hook in `.claude/settings.json` runs `git pull --rebase --autostash` automatically.
- Check its output at the start of the session. If it **failed** or shows a **merge conflict**, tell the user right away and help resolve it before doing other work.
- If the hook didn't run (no pull output in context), run `git pull --rebase --autostash` yourself first.
- Before finishing any task that changed files: `git add -A && git commit -m "<type>: <what>" && git pull --rebase && git push`. See `CONTRIBUTING.md` for commit types.

## 1. Read in this order (save context, don't read everything)

1. **`STATUS.md`**: where the project is right now, who's doing what, and what's next. **Always read it.**
2. **`docs/00-index.md`**: a one-line summary of every doc. Use it to choose which files to open.
3. Open only the docs your task needs. Use the routing table below.

## 2. Routing table: task → files

| If the task is about…                         | Read                                                        |
|-----------------------------------------------|-------------------------------------------------------------|
| What the problem asks / judging / scope        | `docs/01-problem/problem-statement.md`, `docs/01-problem/scope.md` |
| Fraud signals, datasets, existing solutions     | `docs/02-research/` (start with its `README.md`)            |
| System design, components, data flow           | `docs/03-design/architecture.md`                            |
| API request/response shape                     | `docs/03-design/api-contract.md`                            |
| How the risk score / decision is computed      | `docs/03-design/risk-engine.md`                             |
| Why something was decided                      | `docs/03-design/decisions.md`                               |
| Who owns what, deadlines, task list            | `docs/04-plan/`                                             |
| Demo, pitch, deck                              | `docs/05-pitch/`                                            |
| Writing or changing code                       | `src/README.md`, then the folder's own `README.md`          |
| Running / testing                              | `README.md` (Quickstart), `tests/README.md`                 |

## 3. Repo map

```
CLAUDE.md            ← you are here (agent entry point)
STATUS.md            ← live project state: read every session, update after meaningful work
README.md            ← human overview + quickstart
CONTRIBUTING.md      ← git workflow (HTTPS, no SSH), commit style
SETUP.md             ← step-by-step onboarding that Claude runs for new teammates
docs/
  00-index.md        ← one-line summary of every doc (keep updated!)
  01-problem/        ← official statement, scope, judging
  02-research/       ← signals, datasets, prior art
  03-design/         ← architecture, API contract, risk engine, decision log
  04-plan/           ← team roles, timeline, task board
  05-pitch/          ← demo script, deck notes, Q&A prep
src/
  api/               ← HTTP service exposing /v1/authenticate
  risk_engine/       ← feature extraction + scoring + explanations
  dashboard/         ← demo UI: live decisions + "why" panel
data/                ← sample/synthetic data (raw data is git-ignored)
tests/               ← unit + scenario tests
scripts/             ← data generation, load testing, helpers
```

## 4. House rules for agents

- **Docs are the source of truth.** If code and docs disagree, flag it to the user. Don't silently "fix" either one.
- **Keep the index in sync.** If you add, rename or delete a doc, update `docs/00-index.md` in the same commit.
- **Record decisions.** For any non-trivial choice (stack, model, threshold, scope cut), append an entry to `docs/03-design/decisions.md`.
- **Update `STATUS.md`** at the end of meaningful work: what changed, what's next, and any blockers.
- **Small, focused docs.** If a doc grows past roughly 200 lines, split it and link the parts from the index.
- **No secrets in the repo.** Use `.env` (git-ignored) and document keys in `.env.example`.
- **Don't rewrite teammates' docs wholesale.** Make additive edits, and note open disagreements under "Open questions".
- Each `src/*` folder has a `README.md` describing its purpose, entry point and interfaces. Keep it current when you change code there.
