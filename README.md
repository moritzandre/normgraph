# normgraph (private)

Single source of truth for **NormGraph**, a DSR project: a graph of German
civil-law norms and a learned fact-conditional traversal policy (Gutachten paths)
from court decisions. This repository is the artifact the paper reports.

- Read `CLAUDE.md` first. Project contract and decisions: `docs/project/`
  (canonical spine; claude.ai project knowledge is the mirror).
- **Private by design** until DD-010 (data licensing) clears anything for
  publication. Do not redistribute repo contents.

## Quickstart

    uv sync
    uv run pytest
    uv run ruff check .

Paper build:

    cd paper && latexmk -pdf main.tex

## Layout

- `src/normgraph/` — the package (grows via spec'd C-items; currently empty by design)
- `paper/` — LaTeX manuscript (Gregor & Hevner 2013 schema) + `notes/` drafts
- `docs/project/` — brief, literature map, decision register, specs
- `spikes/` — frozen exploratory code (C-01), never imported
- `data/samples/` — small committed samples; `data/raw|processed/` local only
