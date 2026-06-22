# CLAUDE.md — normgraph

## What this repo is
The single source of truth for **NormGraph**: a Design Science Research project
building a graph of German civil-law norms plus a learned fact-conditional
traversal policy (Gutachten paths) from court decisions. This repository is itself
the Level-1 artifact (instantiation) the paper reports. It hosts all three lanes:
- **CODE** — `src/`, `tests/`, `spikes/`, `data/` (pipeline, graph store, models,
  experiments)
- **ARCH** — `docs/project/02_decision_register.md` (design decisions DD-xxx)
- **PAPER** — `paper/` (LaTeX manuscript + `paper/notes/` drafts)

## Canonical project documents
`docs/project/` is the **canonical spine** of the whole project:
- `00_project_brief.md` — vision, lanes, session protocol
- `01_literature_map.md` — DSR method canon (PAPER lane)
- `02_decision_register.md` — design decisions DD-xxx — **the contract**
- `specs/` — CODE work-package specs (C-xx)

The claude.ai project mirrors these files (flat, same names). After any change
here, the user pastes the updated file(s) into the mirror. Never assume the mirror
is fresher than this directory.

## Lane & session discipline
- State the lane and work item at session start (e.g. "CODE · C-03" or
  "PAPER · section 3"). One work item per session.
- End every session with the matching record update: CODE -> the spec in
  `docs/project/specs/`; ARCH -> the register entry; PAPER -> one line in
  `paper/notes/CHANGELOG.md` (plus the draft itself).

## Hard rules
1. **Consult `docs/project/02_decision_register.md` before any design-relevant
   work.** Respect decided DDs; reference open DDs by their ID; never silently
   commit code or prose that answers an open DD. If a task needs an undecided DD,
   stop and say which one. Currently blocking: DD-001 (node model), DD-002 (edge
   taxonomy), DD-005 (graph store) — therefore: no graph schema, no DB choice, no
   fixed citation-canonicalization target list in code yet.
2. German legal terminology stays German in prose (Gutachten, Anspruchsgrundlage,
   Tatbestandsmerkmal, Einrede, Prüfungspfad); code identifiers and comments are
   English.
3. Data discipline: `data/samples/` = small, hand-carried, committed (decision
   bodies are gemeinfrei per § 5 UrhG). `data/raw/` and `data/processed/` = local
   only, gitignored. Open Legal Data platform extras (refs dumps, citation network)
   have unverified licensing (DD-010): keep to per-case comparison snippets, and do
   not publish anything from this repo — it is private by design.
4. Spikes are frozen under `spikes/` — never import from there. Productionize into
   `src/normgraph/` only via a spec'd C-item.

## CODE lane
- Python >= 3.12, managed by **uv**: `uv sync`, `uv run pytest`, `uv run ruff check .`
- Tests in `tests/` (pytest). Lint/format: ruff, line length 100. No network calls
  from tests.
- Corpus fetching is explicit pipeline code (C-03+); OLD API base
  `https://de.openlegaldata.io/api/` (open for direct read clients), bulk via dumps
  at `https://static.openlegaldata.io/dumps/de/`.

## PAPER lane
- Manuscript structure follows the **Gregor & Hevner (2013) DSR publication
  schema** (see skeleton in `paper/main.tex`). Reported process backbone:
  **Peffers et al. (2007) DSRM**; evaluation framing: FEDS (Venable et al. 2016)
  plus Sonnenberg & vom Brocke (2012) Eval 1-4. The function of every canon paper
  is mapped in `docs/project/01_literature_map.md` — follow it.
- Never assert a design claim that lacks a decided DD behind it. Mark DD support
  inline as (DD-00x) while drafting; these markers are stripped at submission.
- Every entry in `paper/bib/references.bib` is an UNVERIFIED SEED until checked
  against the course PDFs. No fabricated references, ever; if a needed entry is
  unverified, say so.
- German legal terms \emph{}-italicized on first use. Manuscript language: English.
- Keep `paper/sections/*.tex` venue-agnostic: no class-specific commands. Venue
  (and class) is an open PAPER-lane decision; plain `article` until then.

## Build & checks
- Code: `uv sync && uv run pytest && uv run ruff check .`
- Paper: from `paper/`: `latexmk -pdf main.tex` · clean: `latexmk -c`. Do not
  commit aux files or `main.pdf`.
