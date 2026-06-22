# 04_specs / C-02 — Repo bootstrap: single private monorepo, git-canonical spine

Status: **specified — execution pending via Claude Code** · Date: 2026-06-12 · Lane: CODE · Feeds: all lanes (infrastructure) · **No DD touched** — DD-001/002/005 remain open; nothing in this bootstrap presupposes node model, edge taxonomy, or graph store.

## Decisions taken (infrastructure level, not DDs)

- **D1 — One private monorepo: `normgraph`.** User decision (2026-06-12), superseding the initially sketched two-repo split. The repository is the single source of truth for all three lanes and is itself the **Level-1 artifact (instantiation)** the paper reports: one versioned object holds the artifact (`src/`, `data/`, `spikes/`), the design knowledge (`docs/project/` incl. the decision register), and the manuscript (`paper/`). Gains: no cross-repo sync, evaluation numbers and figures flow into `paper/` by ordinary commits, atomic history across lanes, and the paper can cite the repo as the artifact without ambiguity. Private until the DD-010 licensing check clears anything beyond § 5 UrhG decision bodies.
- **D2 — Spine relocation (user-confirmed).** Canonical home of the project documents is `docs/project/` in the repo (00 brief, 01 literature map, 02 register, `specs/`). claude.ai project knowledge is the **paste-mirror** (sync direction: git → claude.ai). Gains: version history for the register; Claude Code sessions read the same contract the claude.ai sessions do. The mirror stays flat (claude.ai has no folders); mapping is 1:1 by filename. PAPER markdown drafts live in `paper/notes/` and are mirrored when relevant (as 03_… files).
- **D3 — Code toolchain.** Python ≥ 3.12 · uv · src-layout package `normgraph` (hatchling) · pytest · ruff (line length 100). No runtime dependencies yet; the C-01 spike stays frozen under `spikes/c01/` and is never imported from `src/`.
- **D4 — Data discipline.** `data/samples/` = small, hand-carried, committed (decision bodies are gemeinfrei, § 5 UrhG). `data/raw/`, `data/processed/` = gitignored. OLD platform extras (refs dump, citation network): per-case comparison snippets only, pending DD-010.
- **D5 — Manuscript build.** Lives in `paper/`; plain `article` class + natbib/bibtex + latexmk (pdflatex, run from `paper/`), deliberately venue-agnostic; section skeleton = Gregor & Hevner (2013) publication schema, with comments wiring each section to the method canon (01_literature_map). Rationale for natbib over biblatex: plausible DSR venues (e.g. DESRIST/Springer LNCS) are bibtex-based, and biblatex→bibtex is the costlier conversion direction. `paper/bib/references.bib` is seeded with canon entries, all flagged unverified — per 01_literature_map, exact bibliographic details come from the course PDFs.
- **D6 — Contract.** A single root `CLAUDE.md` encodes: repo-as-artifact framing, lane & session discipline, the DD discipline (consult 02 before design-relevant work; currently blocking: DD-001/002/005), CODE and PAPER lane rules, the German-terminology rule, and the data-licensing rule.

## Rejected options

- **Two repos (`normgraph` + `normgraph-paper`)** — initially proposed for history hygiene (data-heavy pipeline vs. venue churn) and independent later open-sourcing; rejected by the user: one instantiation, one true repo, the repo *is* the paper's artifact. The separation benefits don't outweigh cross-repo sync overhead; if a split is ever needed, extracting `paper/` later is a cheap subtree/filter-repo operation.
- **Overleaf-primary manuscript** — no CLAUDE.md / Claude Code integration; git sync is behind Overleaf's paywall; local latexmk + private GitHub achieves the same with full control. (Overleaf can still be attached later as a secondary remote if a co-author needs it.)
- **Keep claude.ai-canonical spine** — no version history on the register; Claude Code sessions couldn't see the contract without a manual copy anyway, creating two ad-hoc mirrors instead of one defined one. Spine relocation explicitly confirmed by the user.

## Execution

Via handoff file `C-02_handoff_claude_code.md`, run by **Claude Code** from the intended parent directory (claude.ai sessions have no local filesystem access). Staging: user places the five project documents (00, 01, 02, C-01, this file) — plus, optionally, the four C-01 spike artifacts — into `_inbox/` under the parent directory before running. Operator steps end-to-end: `C-02_setup_tutorial.md`.

## Done-criteria (flip status to **done** when all hold)

- [ ] Repo exists locally with the specified tree; two initial commits made; private remote pushed (or remote-TODO lines reported if `gh` was unavailable)
- [ ] `uv sync`, `uv run pytest`, `uv run ruff check .` all green
- [ ] `latexmk -pdf main.tex` (run in `paper/`) builds `main.pdf`
- [ ] Docs spine in place under `docs/project/` including this spec; 00 brief amended with the repo-layer note (handoff Appendix C)
- [ ] claude.ai mirror refreshed: amended `00_project_brief.md` pasted, this file added, status flipped to done + date in both places

## Changelog

- 2026-06-12 · C-02 specified in claude.ai session; handoff produced; execution delegated to Claude Code (local filesystem required). Constraints set by user: LaTeX separated within the project; repo private.
- 2026-06-12 · Revised after user clarification: **single monorepo** instead of two repos (D1); spine relocation (D2) user-confirmed; handoff, 00-amendment, and setup tutorial updated accordingly.
- (pending) · Executed via Claude Code; status → done.
