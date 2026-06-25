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


## DD-002 — Edge taxonomy & condition representation

Status: **decided** · Date: 2026-06-25 · Lanes affected: ARCH → PAPER, CODE

**Question:** Given the DD-001 node model (Einzelnorm nodes + first-class Tatbestandsmerkmal slots, versioned copies, symbolic identity primary), what is the edge taxonomy? Specifically: (i) what does an edge connect — Einzelnorm↔Einzelnorm or Merkmal-mediated; (ii) how is the fact-condition on a learned edge represented (embedding / symbolic predicate / hybrid); (iii) what are the edge attributes; and (iv) are edges themselves temporally versioned (DD-001 flagged this and deferred it here)?

**Context & constraints:** Edges must support (a) interpretable inference output — the Prüfungspfad must read as a Gutachten, so each edge should encode *which doctrinal move* it is (a Verweisung is not a defeater is not a next-station); (b) seeding from Prüfungsschemata (schema = Merkmal tree with typed transitions; vom Brocke 2007 reference-model reuse, accepted in DD-001); (c) supervision extraction from Urteilsstil decisions and the OLD case-to-case network (C-01 F2); (d) the DD-001 guardrail — symbolic identity primary, embeddings derived/swappable — applied now to edge conditions; (e) temporal law change, consistently with DD-001's versioned node copies; (f) leaving DD-005 (store), DD-006 (policy), DD-007 (Subsumtions-Gate), DD-008 (growth) genuinely open.

**Options considered:**

*Endpoint geometry (sub-question i):*
- **A — Uniform Einzelnorm-level.** Edges only connect Einzelnorm versions; Merkmale stay overlay/annotation targets. Pro: simplest store schema. Con: loses structural encoding of *why* a transition fires; sits against DD-001's own worked example (»wirksamer Kaufvertrag« Merkmal of § 433 II → §§ 145 ff.).
- **B — Uniform Merkmal-mediated.** Everything routes through Merkmale. Con: artificial — structural Verweisungen (e.g. § 709 ZPO) have no natural Merkmal source; manufactures phantom Merkmale.
- **C — Type-dependent (heterogeneous) endpoints.** Endpoint geometry is a declared property of the edge type. Pro: matches doctrine; costs ~nothing since DD-001 already made Merkmale first-class addressable. Con: more than one endpoint shape to implement.

*Type axis:*
- **Single "type" enum** mixing provenance (statutory / schema / learned) and doctrinal function (Einwendung / Einrede / Anspruchskonkurrenz). Con: not one axis — a "learned transition" is not a peer of an Einwendung; it *is* an Einwendung whose provenance is learned. Encodes provenance twice (stub already lists it as an attribute).
- **Two orthogonal dimensions:** provenance as an attribute; semantic relation type as the taxonomy.

*Fact-condition representation (sub-question ii):* embedding-primary / symbolic-predicate-only / **hybrid symbolic-primary**.

*Edge-versioning (sub-question iv):* validity-interval on a single persistent edge / **version-scoping with optional explicit Geltungszeitraum, inherited from endpoints when absent**.

**Decision:**

**1. Endpoint geometry = type-dependent (Option C).** Endpoint shape is declared per relation type:
- **structural/statutory** (Verweisung, Prüfungsschritt-scaffold): Einzelnorm-version ↔ Einzelnorm-version, and may attach to a Merkmal where the relation points into one;
- **examination / learned transition** (Prüfungsschritt): **Merkmal-anchored source permitted**, target a Merkmal or an Einzelnorm — this is the »wirksamer Kaufvertrag« → §§ 145 ff. case (source = Merkmal, target = entered Einzelnorm);
- **Einwendung / Einrede / Anspruchskonkurrenz**: Einzelnorm ↔ Einzelnorm (Anspruch ↔ Gegennorm or konkurrierende Anspruchsgrundlage). An Einrede sits *beside* the Anspruch; it does not negate one of its Merkmale.

Permitting a Merkmal endpoint costs nothing in the schema (DD-001 already made Merkmale first-class addressable). *Declaring* Merkmal-anchored edges is separated from *how eagerly the policy populates* learned Merkmal-sourced edges — the latter is a staged knob owned by DD-006 / DD-008.

**2. Two orthogonal dimensions.**
- **Provenance** = `statutory` (extracted) / `schema` (seeded) / `learned` (induced from DD-003 trajectories) is an **edge attribute**, not a type. It is what DD-008 growth governance gates on, and it lets "the same Einwendung edge, now learned-corroborated" be expressed without a new type.
- **Relation type** (semantic/doctrinal axis) is the taxonomy proper.

**3. Relation-type taxonomy.** Two families.

*Family A — reasoning/doctrinal edges (the traversal policy walks these):*
1. **Verweisung** — statutory cross-reference; Einzelnorm↔Einzelnorm (may land on a Merkmal). Sub-flag **Rechtsgrundverweisung** (referenced Tatbestand must be re-prüft → traverse into its Merkmale) vs. **Rechtsfolgenverweisung** (borrow only the Rechtsfolge → no Tatbestand re-examination). The flag is structure fixed here; how the policy consumes it is DD-006.
2. **Prüfungsschritt** (examination transition) — the "next station" scaffold; the schema-seeded + learned workhorse; Merkmal-anchored sources allowed (per decision 1). Hosts the »wirksamer Kaufvertrag« → §§ 145 ff. transition.
3. **Einwendung** — negates the Anspruch (rechtshindernd / rechtsvernichtend); examined *von Amts wegen*.
4. **Einrede** — blocks *Durchsetzbarkeit*, does not negate; examined only if *geltend gemacht* (streitig-conditional → conditions DD-007). Sub-flag **peremptorisch** (dauerhaft, e.g. Verjährung § 214) vs. **dilatorisch** (vorübergehend, e.g. § 320).
5. **Anspruchskonkurrenz** — lateral relation between competing Anspruchsgrundlagen; governs Prüfungsreihenfolge / Sperrwirkung (e.g. EBV §§ 987 ff. over Delikt/Bereicherung), not a defeater.
6. **Konkretisierung** — a Merkmal → the norm or doctrine that defines it. Splits by target: **Legaldefinition-target** (»Sache« → § 90 BGB) = Einzelnorm endpoint, **populatable in v1**; **doctrine/case-law target** (»Erforderlichkeit« → a Vertretbarkeit-doctrine node) needs the option-D doctrine nodes DD-001 deferred → **declared now, doctrine-half deferred, coupled to DD-004 (open)**. Same declare-now/stage-population discipline used for endpoints.

*Family B — structural/maintenance edges (the policy does NOT walk these as Prüfungsschritte):*
7. **Versionierung** — `succeeds` / `amended_by` (introduced by DD-001), Einzelnorm-version ↔ Einzelnorm-version. They connect temporal node versions; they are graph-maintenance structure, excluded from the traversal candidate set (DD-006).

Provenance × relation type is the grid: an Einwendung or Prüfungsschritt edge may be `schema` or `learned`; a Verweisung is `statutory` (optionally schema-confirmed); Versionierung edges are `statutory`.

**4. Fact-condition on a learned edge = hybrid, symbolic-primary.** A learned/examination edge carries:
- a **symbolic condition descriptor** (identity-bearing): a reference to the Merkmal-state(s) / fact-pattern in the per-case overlay that gates the transition (e.g. fires when a named Merkmal is *verneint* / *streitig*);
- an **optional derived embedding** of the fact-condition, attached as a swappable retrieval index, **never identity-bearing**.

This mirrors the DD-001 node guardrail exactly: symbolic spine, vectors hanging off as swappable attributes. The learned *representation the policy consumes* (and candidate-set construction) is DD-006; DD-002 fixes only what the edge *stores*.

**5. Edge-versioning = version-scoped, with optional explicit Geltungszeitraum.** Because endpoints are version-specific nodes (DD-001), most edges are implicitly version-scoped by their endpoints. An edge carries an **optional Geltungszeitraum attribute; when absent, validity is inherited from the endpoint versions.** Only an edge whose validity window differs from its endpoints' — a Verweisung valid in one Geltungszeitraum while both endpoint versions persist — carries an explicit window. Consistent with DD-001's versioned-copies-over-validity-intervals choice; a pure interval-on-one-persistent-edge model is rejected for the same invariant reason.

**6. Edge attributes.**
- `relation_type` (Family A 1–6 / Family B 7) · `provenance` (statutory/schema/learned)
- `frequency` / corpus support (count of supporting trajectories; learned edges)
- `court_weight` (instance/hierarchy of supporting decisions; learned edges)
- `geltungszeitraum` (optional; else inherited from endpoints)
- relation-specific sub-flags: `verweisung_kind` (Rechtsgrund/Rechtsfolgen); `einrede_kind` (peremptorisch/dilatorisch); `konkretisierung_target` (Legaldefinition/doctrine)
- `condition_descriptor` (symbolic) + optional `condition_embedding` (swappable; learned/Prüfungsschritt edges)
- `staging_state` (proposed/verified/committed) — **owned by DD-008**; named here as the attribute slot, not specified.

**Deferred, not decided here:**
- **Konkretisierung doctrine-target half** — declared, not populated in v1; coupled to DD-004 (scope slice) and the option-D doctrine nodes (DD-001 deferred).
- **Candidate-set construction & how the policy consumes condition descriptors / Verweisung kind / Einrede conditionality** — DD-006.
- **Staging/verification semantics on `staging_state`** — DD-008.
- **Subsumtion-driven firing of Einrede/streitig edges** — DD-007.

**Rationale:**

Type-dependent endpoints (decision 1) because the geometry genuinely differs by relation: Merkmal-anchored examination transitions and Einzelnorm-level structural cross-references are not the same shape, and forcing uniformity either discards the Merkmal-source information (Option A) or manufactures phantom Merkmale for structural Verweisungen (Option B). DD-001 already paid for Merkmal addressability, so heterogeneity is nearly free. The load-bearing evidence is doctrinal structure — Prüfungsschemata are Merkmal trees with typed transitions (Leenen 2011, *Anspruchsaufbau und Gesetz*; see `06_legal_methodology_primer.md` §1) — not the single C-01 case, which only corroborates (n=1, full-form-bias caveat).

Two-axis split (decision 2) because provenance and doctrinal function are orthogonal: collapsing them into one enum cannot express a learned-and-then-corroborated Einwendung without inventing types, and it duplicates provenance (already an attribute in the stub). The split is exactly what makes the growth loop expressible as design-knowledge accumulation (vom Brocke 2020): provenance upgrades `learned → corroborated` on a *stable* relation edge.

Keeping Einwendung / Einrede / Anspruchskonkurrenz distinct (decision 3) because they have different traversal semantics — negate (von Amts wegen) vs. block-only-if-raised (streitig-conditional) vs. lateral ordering/Sperrwirkung. That difference *is* the interpretability payload DD-001 bought; merging them would flatten the Gutachten back toward "next-norm with a trace," the framing Nielsen (2020) is invoked to reject. The three map onto the standard three-level Anspruchsprüfung (entstanden / nicht erloschen / durchsetzbar; `06` primer §1).

Konkretisierung declared-now/half-populated (decision 3.6) keeps the taxonomy honest about the C-01 ratio (»medizinische Notwendigkeit«/»Erforderlichkeit« concretized by a BGH-Vertretbarkeitsmaßstab — a Konkretisierung none of types 1–5 captures) without pre-empting DD-004: the doctrine-target half rests on undecided option-D nodes, so it is flagged, not asserted as v1 structure.

Versionierung as a separate non-traversed family (decision 3.7) so the policy's candidate set is clean: `succeeds`/`amended_by` are how the law-layer represents temporal change as graph structure (DD-001), not reasoning moves; the policy must not emit them as Prüfungsschritte.

Hybrid symbolic-primary conditions (decision 4) is the DD-001 guardrail applied to edges: if conditions carried identity as embeddings, the store and vectoriser would be hard-coupled, foreclosing DD-005. A symbolic descriptor keyed to overlay Merkmal-state keeps identity stable and the embedding swappable.

Version-scoped edges with optional explicit window (decision 5) inherits DD-001's reasoning: validity-intervals blur across reforms; endpoint-inherited validity plus an explicit override only where needed preserves the clean version model without taxing the common unchanging edge.

**Rejected because:**
- **Uniform Einzelnorm endpoints (A):** loses the structural encoding of Merkmal-sourced transitions and contradicts DD-001's own worked example; the only thing it buys (schema simplicity) is outweighed by interpretability loss.
- **Uniform Merkmal-mediated endpoints (B):** manufactures phantom Merkmale for structural Verweisungen that have no Merkmal source.
- **Single type enum (provenance+function):** not one axis; cannot express provenance upgrades on a stable relation; duplicates provenance.
- **Embedding-primary conditions:** violates the DD-001 symbolic-identity guardrail; hard-couples DD-005/DD-006.
- **Validity-interval edge-versioning (single persistent edge):** blurs validity across reforms; rejected for the same invariant reason as the node-level interval model in DD-001.
- **Konkretisierung deferred whole:** would leave the taxonomy unable to name the C-01 ratio at all; the Legaldefinition-half is cleanly v1-populatable, so half-population dominates whole-deferral.

**Consequences → PAPER:**
- Grounds a Level-2 design principle on **typed doctrinal transitions**: *represent each traversal edge as a named doctrinal relation (Verweisung / Prüfungsschritt / Einwendung / Einrede / Anspruchskonkurrenz / Konkretisierung) with declared endpoint geometry, so the generated Prüfungspfad reads as a Gutachten rather than a norm sequence.* (DP phrasing per Seidel et al. 2018 / Chandra Kruse et al. 2022.)
- The provenance × relation-type separation substantiates the growth-as-accumulation claim (vom Brocke et al. 2020): the artifact improves with use by upgrading provenance on stable relations, not by mutating structure.
- Verweisung sub-types and Einrede streitig-conditionality constrain the Evaluation (DD-009): path edit distance must treat Einrede edges as appearing only when *geltend gemacht*, and must distinguish Rechtsgrund- from Rechtsfolgenverweisung traversal.
- Reinforces the Nielsen (2020) re-problematization: edges encode doctrinal moves, not generic next-norm steps.
- Evidence trail for the edge semantics now has a primary-source spine (`06_legal_methodology_primer.md`), feeding the domain-corpus review.

**Consequences → CODE:**
- Defines the edge logical model for **DD-005 (store/schema, open)**: typed edges (two families), endpoint geometry per type, attribute set (decision 6). Nothing here pre-empts the store choice.
- **Symbolic-primary condition** is a binding constraint on DD-005/DD-006: `condition_descriptor` is identity-bearing; `condition_embedding` is a derived swappable index.
- **Versionierung edges** (`succeeds`/`amended_by`) must be excluded from the DD-006 traversal candidate set; the store distinguishes Family A from Family B.
- **C-03:** OLD's „Zitiert von" case-to-case network (C-01 F2) = candidate provenance source for `learned`/case-supported edges; statutory Verweisung extraction reuses the citation-chain parser (F4/F6). Per the n=1 caveat, do **not** bake edge-type priors from the single LG case.
- **DD-008** owns `staging_state` transitions (proposed → verified → committed), commit thresholds, court-weight/frequency gating, and rollback.
- **DD-007** owns the firing condition that turns an Einrede / streitig edge live from Subsumtions-Gate output.

**Unblocks:** DD-005 (store/schema — now has node + edge logical models), DD-006 (policy — candidate set excludes Family B; consumes Verweisung kind, Einrede conditionality, condition descriptors). **Inherited obligations:** DD-003 (trajectories must record which relation-type each step traverses, and the overlay Merkmal-state a condition descriptor references); DD-004 (unlocks Konkretisierung doctrine-half + option-D nodes). **Still gated elsewhere:** DD-007 (Einrede/streitig firing), DD-008 (staging semantics), C-03 (edge-provenance extraction harness).

**Evidence / sources:** DD-001 (node endpoints, versioned copies, symbolic-identity guardrail) — `docs/project/02_decision_register.md`. `docs/project/06_legal_methodology_primer.md`: Leenen (2011) *Anspruchsaufbau und Gesetz* (structure-of-statute ≙ structure-of-Fallbearbeitung — load-bearing for typed transitions); Einwendung (rechtshindernd/rechtsvernichtend) vs. Einrede (rechtshemmend; peremptorisch/dilatorisch) vs. Anspruchskonkurrenz doctrine; Rechtsgrund-/Rechtsfolgenverweisung; Prüfungsschemata as Merkmal trees (Bezzenberger/Wandtke schema collections; Medicus/Petersen Anspruchskonkurrenz ordering). C-01 spike (`docs/project/specs/C-01_data_spike.md`): „Zitiert von" network (F2), citation chains (F4/F6) as edge-surface evidence; **n=1 full-form-bias caveat — corroboration, not basis**. Method canon (`docs/project/01_literature_map.md`): vom Brocke (2007) reference-model reuse / schema seeding; Nielsen (2020) problematization; vom Brocke et al. (2020) accumulation; Seidel et al. (2018) / Chandra Kruse et al. (2022) DP phrasing.

---

## Backlog (stubs — promote to full entries when scheduled)

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
