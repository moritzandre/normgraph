# 02 · Design decision register

Purpose: every granular design question becomes one numbered entry (DD-xxx), worked in exactly one ARCH session, then recorded here. This file is the contract between PAPER, ARCH, and CODE. Format follows the Architecture Decision Record (ADR) pattern, extended with DSR consequences.

Statuses: `open` → `in work` → `decided` → (`superseded by DD-yyy`)

## Entry template

```
## DD-0XX — Title
Status: open | in work | decided | superseded · Date: · Lanes affected:
Question:
Context & constraints:
Options considered: (A/B/C … with one-line pro/con each)
Decision:
Rationale:
Rejected because:
Consequences → PAPER: (which design requirement / design principle this feeds)
Consequences → CODE: (what gets built/changed; spec reference)
Evidence / sources:
```

---

## DD-001 — Role & representation of a node (norm model)

Status: **open — scheduled as first ARCH session** · Lanes: ARCH → PAPER, CODE

**Question:** What exactly is a node, relative to "a norm"? What does a node *contain*, what is its identity, and what lives elsewhere (on edges, in path state, in payload)?

**Context & constraints:** The choice must support (a) supervision extraction from Urteilsstil decisions, (b) seeding from published Prüfungsschemata, (c) interpretable inference output (a readable Gutachten path), (d) temporal law change (a.F./n.F., e.g. Schuldrechtsreform 2002, Kaufrecht/§§ 327 ff. 2022), (e) tractable annotation/canonicalization cost.

**Options sketched (to be worked):**

- **A — Node = § (paragraph level).** Cheap, matches citation surface forms. But conflates distinct Ansprüche (§ 433 I vs. II) and distinct functions of Absätze; traversal semantics get muddy.
- **B — Node = Einzelnorm (§ + Abs. + ggf. Satz), temporally versioned.** Correct legal granularity for Anspruchsgrundlagen; citation canonicalization is harder ("§§ 145 ff.", "i.V.m.").
- **C — Two-level: Einzelnorm nodes + Tatbestandsmerkmal slots.** Transitions between norms are *mediated by Merkmale* (you jump from § 433 II's Merkmal "wirksamer Kaufvertrag" into §§ 145 ff.) — most interpretable and closest to the Gutachten; highest modeling and annotation effort.
- **D — C + doctrine/Fallgruppen nodes** for ungeschriebene Institute (Verkehrssicherungspflichten, § 242-Fallgruppen, Rahmenrechte des § 823 I). Needed eventually for the growth mechanism; question is whether v1 includes them.

**Open sub-questions:**
1. Node identity & ID scheme (ELI-style URIs? own canonical IDs: Gesetz/§/Abs/Satz/Geltungszeitraum?)
2. Temporal versioning model: validity intervals on one node vs. versioned node copies?
3. Where does subsumtion state live — on the node, on the path step, or in a separate case-layer overlay?
4. Are Merkmale graph nodes or structured payload of the norm node? (Affects what the policy's action space is.)
5. Canonicalization targets for fuzzy citations: "§§ 145 ff.", "i.V.m.", "analog", "a.F." — what do they resolve to?
6. What is the action space at inference: norms only, or Merkmal-level steps too?

**Decision:** —
**Consequences → PAPER:** will ground DR/DP on representational fidelity & interpretability.
**Consequences → CODE:** defines graph schema (DD-005 depends on this), citation canonicalizer spec, annotation guideline.
**Evidence / sources:** Prüfungsschemata (Lehrbuch/Repetitorium), Gesetze-im-Internet XML structure, citation-form inventory from a decision sample (C-01).

---

## Backlog (stubs — promote to full entries when scheduled)

## DD-002 — Edge taxonomy & condition representation
Edge types (statutory Verweisung / schema seed / learned transition / Einwendung / Einrede / Anspruchskonkurrenz); how the fact-condition on a learned edge is represented (embedding vs. symbolic predicate vs. hybrid); edge attributes (frequency, provenance, court weight, validity period). Depends on DD-001.

## DD-003 — Trajectory definition (the training example)
Formal schema of one training trajectory; station labels (bejaht / verneint / streitig / implizit bejaht); reconstruction protocol from Urteilsstil (LLM-assisted, schema-anchored); how facts are attached per step; inter-annotator/agreement check design.

## DD-004 — Scope slice for v1
Kaufrecht/Gewährleistung (§§ 433–479) vs. Deliktsrecht (§ 823) vs. other. Criteria: schema density, published case-law volume, annotation effort, demonstration value, evaluation cleanliness.

## DD-005 — Graph store & canonical schema
Neo4j (+ vector index) vs. alternatives; Cypher schema implementing DD-001/002; staging area & versioning design.

## DD-006 — Policy formulation & candidate set
LLM-agent-over-graph (phase 1) vs. trained pointer policy (phase 2); candidate set construction (neighbors + dense retrieval + STOP); history encoding.

## DD-007 — Subsumtion gate
Per-Merkmal classification (erfüllt / nicht erfüllt / streitig); model choice; how gate outputs condition traversal and backtracking.

## DD-008 — Growth & staging governance
Proposal triggers (low policy confidence + out-of-neighborhood retrieval; unmatched reasoning segments); commit thresholds (k independent decisions, court hierarchy, verification pass, human review); provenance & rollback.

## DD-009 — Evaluation design ↔ FEDS / Eval 1–4 mapping
Metrics (next-norm hits@k, path edit distance / Kendall's tau, outcome agreement with Tenor, subsumtion F1, calibration); temporal & court-level splits; the §§ 327 ff. post-2022 growth test; jurist study design.

## DD-010 — Data sources, licensing, legal boundaries
Open Legal Data, Rechtsprechung im Internet, Landesportale; § 5 UrhG scope (decisions gemeinfrei; editorial Leitsätze/Randnummern of juris/beck protected — excluded); publication-bias documentation; RDG / EU-AI-Act note for any future productization.
