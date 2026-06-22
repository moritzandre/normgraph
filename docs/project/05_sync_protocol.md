# 05 · Sync protocol — git ⇄ claude.ai, and the end-of-task check

Status: standing method doc · Lane: all (infrastructure) · Companion to 00 brief · Established after C-02 (repo layer). Lives at `docs/project/05_sync_protocol.md`; reaches the claude.ai mirror via the connector (it is inside `docs/project/`).

## 0. One sentence
The git repo `normgraph` is canonical for everything; the claude.ai project knowledge is a **read-only mirror of the spine**, pulled from git by the GitHub connector on a **manual "Sync now"**; every session ends with a **SYNC BLOCK** naming what changed and the exact step to propagate it.

## 1. Canonical vs. mirror
- **Canonical:** the git repo — spine (`docs/project/`), code (`src/`, `tests/`, …), manuscript (`paper/`). On any disagreement, **git wins**: re-sync from git; never hand-edit the mirror to "fix" a discrepancy.
- **Mirror:** claude.ai project knowledge. Holds only the spine, populated by the GitHub connector. It is a snapshot **as fresh as the last "Sync now"** — not a live view of the repo.

## 2. Connector configuration (one-time)
Enable the GitHub integration in this project and authorize the Claude GitHub App for the private `normgraph` repo. Select **only**:
- `docs/project/` — 00, 01, 02, this file, and `specs/` (C-01, C-02, …)
- *(optional)* `paper/notes/` if PAPER drafts should be visible here
- *(optional)* `CLAUDE.md` if you want the repo contract readable in claude.ai too

Do **not** select `src/`, `data/`, or `paper/` build output — not spine, and they eat the context budget. Once a folder is connector-covered, **stop pasting those files by hand** — one mechanism per file, or the two copies drift.

## 3. The two directions — who does what
The connector moves files **git → here only**, and only when *you* click "Sync now." There is no auto-sync on push, and nothing moves **here → git** except a human commit.

**After changing the repo (IDE / Claude Code):**
1. commit + push
2. on claude.ai, click **Sync now** on the connector
→ the mirror is current.

**After a claude.ai session produces a spine change:**
1. the session emits the update block (the new file content)
2. paste it into the matching `docs/project/<file>` in the repo
3. commit + push
4. click **Sync now**
→ canonical updated, then mirror updated. Until step 3, the repo is *behind* the session.

## 4. End-of-task check — the SYNC BLOCK
Every session ends by emitting a SYNC BLOCK. It is a **handoff, not a guarantee**: each surface can verify only its own side.

**Claude Code session (in the repo):**
- Changed: <files>
- Git: committed? pushed? (show `git status` / the commit hash; if unpushed, say so)
- Spine touched? If any `docs/project/` file changed → "On claude.ai: click Sync now."
- Feeds: which DD / spec / paper section, per 00 brief §2 coupling

**claude.ai session (here):**
- Updates: <which spine file> — paste-ready content is above
- Propagate: paste into `docs/project/<file>` → commit + push → Sync now
- Note: the repo (canonical) is behind until you do this

## 5. Drift check (possible once the connector is on)
At task start or end, a claude.ai session can scan the synced spine for obvious inconsistencies and flag them (it cannot auto-fix):
- a reference to `specs/C-0X_…md` that isn't present in the mirror (the C-02 case that bit us)
- a spec whose status says "pending" but whose changelog says executed (status not flipped)
- a file named in the brief's inventory / repo-layer note that's missing
This is a **sanity net only** — the synced view is as fresh as the last "Sync now," so a clean scan means "consistent as of last sync," not "consistent with the live repo."

## 6. Limitations — do not over-trust
- "Sync now" is manual; a forgotten sync = stale mirror.
- Claude Code sees git and the working tree, not project knowledge. A claude.ai session sees the last-synced snapshot, not the live repo. **Neither can confirm the other's current state.**
- The connector is read-only, pull-only. All here → git is a human commit.
- Git is the single source of truth. Mirror disagrees → re-sync, don't patch the mirror.

## 7. Setup checklist
- [ ] GitHub connector enabled; Claude GitHub App authorized for `normgraph` (private)
- [ ] Selected `docs/project/` (+ optional `paper/notes/`, `CLAUDE.md`)
- [ ] Sync now; confirm 00 / 01 / 02 + specs (C-01, C-02) + this file appear
- [ ] Stopped manual pasting for connected files
- [ ] CLAUDE.md clause added (Appendix A) and committed
- [ ] Project-instructions clause added (Appendix B) in project settings
- [ ] This file committed as `docs/project/05_sync_protocol.md`; Sync now

## Changelog
- 2026-06-22 · Established alongside enabling the GitHub connector; defines canonical/mirror, the SYNC BLOCK ritual, and the drift check. (C-02 repo layer is the prerequisite.)

---

## Appendix A — insert into `CLAUDE.md` (repo)

Add as a top-level section:

```markdown
## Sync discipline (git ⇄ claude.ai)
This repo is canonical. The claude.ai project knowledge is a read-only mirror of
`docs/project/`, pulled by the GitHub connector on a manual "Sync now" — no
auto-sync on push, and nothing flows here → repo except a human commit. End every
session with a SYNC BLOCK: what changed, whether it is committed and pushed, and --
if any `docs/project/` file changed -- a reminder that the user must click "Sync
now" on claude.ai. Never assume the mirror is fresher than this repo; on conflict,
the repo wins. Full protocol: docs/project/05_sync_protocol.md.
```

## Appendix B — insert into project instructions (§5, claude.ai settings)

Add as clause (7):

```
(7) Sync discipline: the git repo `normgraph` is canonical; this project knowledge
is its mirror via the GitHub connector (docs/project/), refreshed by manual "Sync
now". End every session with a SYNC BLOCK stating what changed and the exact
propagation step (paste into the repo file -> commit + push -> Sync now). On
conflict, git wins; never treat the mirror as canonical. See 05_sync_protocol.md.
```
