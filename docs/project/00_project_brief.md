# 00 · Project brief & working method — NormGraph

Working title: **NormGraph** — Learning fact-conditional traversal of German civil-law norms from court decisions. (Rename freely; update everywhere if you do.)

## 1. Vision

We build a system that represents German civil law as a graph — nodes for norms (plus Merkmal slots and doctrine nodes), edges for examination transitions — and learns a fact-conditional traversal policy from court decisions. A new case yields a Prüfungspfad through the graph (a structured Gutachten, station by station: bejaht / verneint / streitig). The graph grows iteratively through staged, verified edge and node proposals, so the system improves with use. Scientific framing: a Design Science Research (DSR) project in Information Systems, producing a Level-1 instantiation plus Level-2 design principles (Gregor & Hevner 2013).

## 2. Three parallel lanes

**PAPER** — the DSR paper. Backbone: Peffers et al. (2007) DSRM. Owns: research question, literature review (method canon + domain corpus), design requirements → design principles → design features chain, evaluation design (FEDS), manuscript.

**ARCH** — conceptual design. Owns: the design decision register (file 02). Every granular question (node model, edge semantics, trajectory definition, …) is worked here, one decision per session, and recorded.

**CODE** — implementation. Owns: repository, data pipeline, graph store, models, experiments. Consumes decided DDs as specs; produces evaluation results that feed PAPER.

Coupling: a decided DD states its consequences for PAPER (which design requirement/principle it supports) and for CODE (what to build). Evaluation numbers flow back from CODE into PAPER. The register is the contract between all three.

## 3. How claude.ai Projects actually behave — and what that means

- Project knowledge (files + project instructions) is available in **every** chat inside the project. Individual chats do **not** see each other's content; the only durable shared state is project knowledge.
- "Search past chats", if enabled in Settings, lets a chat retrieve from previous conversations within the same project — useful as backup, but not a substitute for the register.
- Claude cannot write into project knowledge. Updates happen by you pasting/replacing file contents.

Consequence: **files are the spine, chats are disposable working sessions.** Don't maintain three eternal chats — they'll bloat and lose focus. Instead, open a fresh chat per work item, named by lane and ID:

- `ARCH · DD-001 — node model`
- `PAPER · P-01 — DSR Grid`
- `CODE · C-02 — citation parser`

## 4. Session protocol

1. Open a chat, name it, state the item ID in the first message ("We're working DD-001").
2. Work granularly: one decision or work package per session, in steps. Claude asks at most one focused question at a time.
3. End every session by requesting an **update block**: the finished register entry (ARCH), a paper-section delta (PAPER), or a spec/changelog note (CODE).
4. Paste the update block into the corresponding project-knowledge file (replace the file). The next session starts from the updated state.
5. A DD counts as *decided* only when it has: decision, rationale, rejected options, consequences → PAPER and → CODE, and evidence/sources.

## 5. Ready-to-paste project instructions

> This project develops "NormGraph": a DSR (Information Systems) research project building a graph-based system that learns fact-conditional traversal of German civil-law norms (Gutachten paths) from court decisions. Three lanes: PAPER, ARCH, CODE.
>
> Always: (1) Consult 02_decision_register.md before proposing designs — respect decided DDs, reference open ones by their ID. (2) Work granularly and in steps: one work item per session; ask at most one focused question at a time. (3) End every working session with a paste-ready update block for the relevant project file. (4) Keep German legal terminology in German (Gutachten, Anspruchsgrundlage, Tatbestandsmerkmal, Einrede); write prose in English unless I switch. (5) In PAPER sessions, follow the method canon as mapped in 01_literature_map.md: Peffers et al. (2007) as process backbone, Gregor & Hevner (2013) for positioning, FEDS (Venable et al. 2016) plus Sonnenberg & vom Brocke (2012) for evaluation. (6) Flag any design claim that lacks a decided DD behind it.

## 6. Project-knowledge file inventory (target state)

| File | Lane | Purpose |
|---|---|---|
| 00_project_brief.md | all | this document |
| 01_literature_map.md | PAPER | method canon → function in our paper |
| 02_decision_register.md | ARCH | granular design decisions (DD-xxx) |
| 05_sync_protocol.md | all | git ⇄ claude.ai sync discipline + SYNC BLOCK ritual |
| 06_legal_methodology_primer.md | ARCH/PAPER | Gutachtenstil/Prüfungsschemata sources grounding DD-001/002 |
| 03_paper/ (outline, drafts) | PAPER | added as they emerge |
| 04_specs/ (per-component) | CODE | added as DDs are decided |
| Literature PDFs | PAPER | upload the course papers |

### Repo layer (since C-02)

One private repository `normgraph` is the single source of truth and is itself the
Level-1 artifact the paper reports. It hosts the **canonical spine**
`docs/project/` (00, 01, 02, specs/), the code lane (`src/`, `tests/`, `spikes/`,
`data/`), and the manuscript (`paper/`, with PAPER markdown drafts in
`paper/notes/`). The claude.ai project knowledge is the **mirror** of the spine:
flat copies, same filenames, refreshed by paste after each change in git. Sync
direction is git → claude.ai. See `specs/C-02_repo_bootstrap.md`.

## 7. Immediate next steps

1. You: create the project, paste the instructions (§5), upload these three files + the literature PDFs.
2. ARCH session 1 → **DD-001** (role & representation of a node) — already framed in the register.
3. PAPER session 1 → **P-01**: fill the DSR Grid (vom Brocke & Maedche 2019) as a one-pager; it forces early clarity on problem, solution, input/output knowledge.
4. CODE session 1 → **C-01**: environment spike — pull an Open Legal Data sample, segment one decision (Tenor / Tatbestand / Entscheidungsgründe), extract norm citations. No architecture commitments yet (those wait on DD-001/002/005).
