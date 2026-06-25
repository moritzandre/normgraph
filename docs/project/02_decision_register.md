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

Status: **decided** · Date: 2026-06-23 · Lanes affected: ARCH → PAPER, CODE

**Question:** What exactly is a node, relative to "a norm"? What does a node *contain*, what is its identity, and what lives elsewhere (on edges, in path state, in payload)?

**Context & constraints:** The choice must support (a) supervision extraction from Urteilsstil decisions, (b) seeding from published Prüfungsschemata, (c) interpretable inference output (a readable Gutachten path), (d) temporal law change (a.F./n.F., e.g. Schuldrechtsreform 2002, Kaufrecht/§§ 327 ff. 2022), (e) tractable annotation/canonicalization cost.

**Options considered:**

- **A — Node = § (paragraph level).** Pro: cheap, matches citation surface forms. Con: conflates distinct Ansprüche (§ 433 I vs. II) and distinct functions of Absätze; cannot host Tatbestandsmerkmale coherently (Merkmale are Anspruchs-specific, so a bare § hosting two Ansprüche has no well-defined Merkmal set).
- **B — Node = Einzelnorm (§ + Abs. + ggf. Satz), temporally versioned.** Pro: correct legal granularity for Anspruchsgrundlagen; one clean Merkmal set per node. Con: citation canonicalization is harder (deferred to C-03).
- **C — Two-level: Einzelnorm nodes + Tatbestandsmerkmal slots.** Pro: most interpretable, closest to the Gutachten; transitions between Einzelnormen are mediated by Merkmale; the layer at which cases are actually decided becomes addressable. Con: writes a supervision cheque DD-003 must cash (Merkmal-granular trajectory reconstruction).
- **D — C + doctrine/Fallgruppen nodes** (ungeschriebene Institute: Verkehrssicherungspflichten, § 242-Fallgruppen, Rahmenrechte des § 823 I) and AGB-type quasi-norms (MB/KK, AVB cited statute-style, per C-01 F7). Pro: needed eventually for the growth mechanism and for PKV-type slices whose Anspruchskette runs through Musterbedingungen. Con: larger annotation surface; coupled to the v1 slice (DD-004, open).

**Decision:**

The node model is **option C**: a two-level **law-layer** comprising **Einzelnorm nodes** (§ + Abs. + ggf. Satz) with **first-class, addressable Tatbestandsmerkmal slots** beneath them. Specifically:

1. **Merkmale are first-class graph objects** (sub-question 4), not opaque payload of the norm node. They are addressable: the Subsumtions-Gate (DD-007, open) labels them, and the policy's action space *may* land on them.
2. **Subsumtion state does not live on the law-layer** (sub-question 3). The law-layer (Einzelnorm nodes + Merkmal slots + edges) is **case-invariant**. Each case's subsumtion outcomes (*bejaht / verneint / streitig*) live in a **per-case overlay** that references Merkmal nodes by ID and carries the label plus the facts that drove it. A trajectory (DD-003, open) *is* such an overlay: an ordered walk over law-layer nodes carrying per-step subsumtion state.
3. **Symbolic identity is primary; embeddings are derived and swappable** (guardrail). A node's identity is its canonical ID, never its vector. Embeddings are an index over the node's text payload, attached as a swappable attribute — they never participate in identity. This keeps the store and the vectorisation mechanism a free choice for DD-005 (open) rather than a hard coupling.
4. **Temporal model = versioned node copies** (sub-question 2). When an Einzelnorm changes, the pre- and post-reform versions are **distinct nodes** linked by a `succeeds` / `amended_by` edge (edge-versioning itself is DD-002, open). Identity *includes* the Geltungszeitraum. This preserves the invariant **one node = one Merkmal set = one subsumtion target** (a single node cannot host two Merkmal sets across time), and makes requirement (d) and the §§ 327 ff. post-2022 growth test (DD-009, open) first-class graph structure rather than a query-time filter.
5. **Identity / ID scheme = own canonical hierarchical IDs** (sub-question 1), path-structured, ELI-informed but not ELI-bound:
   - Einzelnorm version: `BGB/§433/Abs1/[2022-01-01..]`
   - Merkmal slot (nesting allowed, for sub-Merkmale): `VVG/§192/Abs1/[..]/Merkmal:medizinische_Notwendigkeit/Erforderlichkeit`
   - **ELI is carried as an optional attribute** on Einzelnorm nodes where one exists (interoperability, Gesetze-im-Internet alignment), never as the primary key.

**Action space at inference (sub-question 6) — partially decided:** the representation *permits* Merkmal-level actions (it must, given (1)). *How aggressively the phase-1 policy actively emits Merkmal-level steps* is a separately stageable knob, deferred to DD-006 (policy formulation) / DD-007 (Subsumtions-Gate).

**Deferred, not decided here:**
- **Sub-question 5 (canonicalization targets for fuzzy citations: "§§ 145 ff.", "i.V.m.", "analog", "a.F.").** Deferred to **C-03**. The node model constrains C-03's target: a citation string resolves to an **Einzelnorm *version*** via (string + decision date → correct version node), per decision (4).
- **Merkmal slug governance** (who fixes the canonical string for a Merkmal; how two annotators converge). This is a DD-003 annotation-guideline question (canonical Merkmal-Vokabular). The node model commits only that IDs are hierarchical and addressable down to sub-Merkmale; it does not fix the slugs.
- **Option-D nodes** (doctrine/Fallgruppen nodes; AGB/AVB-as-nodes). Not included in v1 as decided; **coupled to DD-004** (scope slice, open) — a PKV slice would force AVB-as-node, a Kaufrecht/Delikt slice would not. To be promoted to its own DD once DD-004 lands. The growth mechanism (DD-008, open) will need doctrine nodes eventually.

**Rationale:**

Merkmale are first-class because **Merkmale are the level at which cases turn.** C-01 evidence: in the sample (LG Nürnberg-Fürth, 8 O 4860/25, PKV/Abnehmspritze), the Anspruchsgrundlage (§ 192 Abs. 1 VVG, § 1 Abs. 2 S. 1 MB/KK) is uncontested; the Klage dies on a single Merkmal — *medizinische Notwendigkeit*, specifically the *Erforderlichkeit* prong (Eignung bejaht at point a., Erforderlichkeit verneint at point b.). A norm-only representation records "the court examined § 192 VVG" and loses the entire ratio. The decisive signal lives one layer below the norm.

The overlay separation (decision 2) is what lets case law attach **at the right layer** while keeping a single shared graph: a Merkmal node is part of *the law* (the same "Erforderlichkeit" object for every PKV case under § 192 VVG); the outcome *verneint* is true only of *this* case. Putting subsumtion state on the node would make two cases overwrite each other and destroy graph-sharing across the corpus. References-from-overlay preserve the modularity (case evidence keyed to a specific Merkmal, sharpening DD-007 and conditioning DD-006) without mutating shared structure.

Versioned copies (decision 4) over validity-intervals: reforms change *Merkmale*, and a single time-attributed node would host two Merkmal sets across time, defeating the one-node-one-subsumtion-target invariant that makes the overlay clean. The likely v1 slice (Kaufrecht, if DD-004 so lands) is precisely the reformed area (2002, 2022), so the temporal structure earns its keep rather than taxing a stable corpus.

Own IDs over ELI-as-primary (decision 5): ELI addresses legislation, not Merkmale — the layer that matters has no ELI by construction; AGB-type quasi-norms (MB/KK, AVB) have no ELI at all; and ELI's German temporal granularity is the least reliable part to lean on for requirement (d). Own IDs as primary + ELI as attribute mirrors the embeddings guardrail: a stable symbolic spine with external identifiers and vectors hanging off it as swappable attributes.

Schema-seeding fit (vom Brocke 2007, reference-model reuse): Prüfungsschemata *are* Merkmal trees. Seeding the graph from them (instantiation/specialization) naturally produces hierarchical Merkmal slots, which is why the ID scheme must permit sub-Merkmal nesting.

**Rejected because:**
- **A (§-level):** cannot host Merkmale coherently (Anspruchs-specific Merkmale have no well-defined attachment to a § hosting multiple Ansprüche); the only thing A buys — matching citation surface forms — is a C-03 canonicalization concern, not a representation concern. A is dominated by B on legal correctness.
- **Norm-only (Merkmale as payload):** cheaper and closer to what C-01 directly observed, but the produced path becomes a norm sequence with the Gutachten substance hidden inside nodes — i.e. "next-norm prediction with a trace," which is close to the framing Nielsen (2020) is invoked to *reject*. The interpretability contribution and the eval units (subsumtion F1) require addressable Merkmale.
- **Validity-interval temporal model:** lighter for the (common) unchanging norm, but blurs the Merkmal set across reforms — rejected for breaking the one-node-one-subsumtion-target invariant; see rationale.
- **ELI as primary key:** rejected per rationale (no ELI for Merkmale or AGB-quasi-norms; weak German temporal granularity). Retained as an optional attribute.

**Consequences → PAPER:**
- Grounds a Level-2 design principle on **representational fidelity at decision granularity**: *represent the reasoning unit at the granularity at which cases are decided (Tatbestandsmerkmal), and separate the case-invariant Normgraph (law-layer) from the case-specific Subsumtions-Overlay.* (DP phrasing per Seidel et al. 2018 / Chandra Kruse et al. 2022.)
- Substantiates the Nielsen (2020) re-problematization: the path's substance is Merkmal-level Subsumtion, not a norm sequence.
- Schema-seeding as kernel-theory lens (vom Brocke 2007): Prüfungsschemata as reference models instantiated/specialized into the Merkmal hierarchy.
- Supplies the formal trajectory object the Evaluation section already assumes (subsumtion F1, path edit distance; `paper/sections/05_evaluation.tex`).
- Temporal versioning makes requirement (d) and the §§ 327 ff. post-2022 growth test (DD-009) reportable as graph structure.

**Consequences → CODE:**
- Defines the graph schema's logical model (Einzelnorm nodes + Merkmal slots + per-case overlay) — **DD-005 (store/schema, open) implements this**; nothing here pre-empts the store choice (property-graph + vector index, polyglot, RDF, relational + pgvector all remain open for DD-005).
- **Symbolic-identity-primary** is a binding constraint on DD-005/DD-006: embeddings attach as a derived, swappable index, never as identity.
- ID scheme = own canonical hierarchical IDs (`Gesetz/§/Abs/[Geltungszeitraum]`, Merkmal sub-paths); ELI optional attribute. Annotation guideline (DD-003) governs Merkmal slugs.
- **C-03 canonicalization target is constrained:** citation string + decision date → Einzelnorm *version* node. (Full target list still DD-001.5 → C-03.)
- **Forward dependency / de-risking flag:** the representation commits DD-003 to **Merkmal-granular trajectory reconstruction from Urteilsstil prose that does not label Merkmale** (the a./b. Gliederung is a recoverable anchor per C-01 F6, but recovery quality and inter-annotator agreement are unproven, n=1). Recommend a small DD-003 reconstruction pilot on a handful of cases **before the schema hardens** in DD-005.

**Unblocks:** DD-002 (edge taxonomy — now has node endpoints + versioning to build on), DD-005 (graph store/schema). **Inherited obligation:** DD-003 (Merkmal-granular trajectories; slug governance). **Still gated elsewhere:** C-03 canonicalization full target list (sub-question 5); active-use action space (sub-question 6 → DD-006).

**Evidence / sources:** C-01 data spike (`docs/project/specs/C-01_data_spike.md`; sample LG Nürnberg-Fürth 8 O 4860/25 — Merkmal-decisive ratio at F4/F6; AVB option-D provocation at F7; full-form-bias caveat n=1). Prüfungsschemata (Lehrbuch/Repetitorium) as Merkmal trees. Gesetze-im-Internet XML structure; ELI (German federal publication) as attribute source. vom Brocke (2007), reference-model reuse / schema seeding (`docs/project/01_literature_map.md`). Nielsen (2020), problematization. Seidel et al. (2018) / Chandra Kruse et al. (2022), design-principle phrasing.

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
