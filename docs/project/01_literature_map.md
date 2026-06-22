# 01 · Literature map — DSR canon → function in our paper

Scope note: this list is the **methodological canon** (course list, complete per your instruction). The **domain corpus** — legal judgment prediction, legal knowledge graphs, German legal NLP/IR, computational models of legal reasoning — is a separate, to-be-built review whose search process we document per vom Brocke et al. (2009). Exact bibliographic details: take from the course PDFs; this map is functional, not a bibliography.

## Backbone (read first, cite throughout)

- **Peffers et al. (2007), DSRM** — the process skeleton of the entire project and paper: problem identification → objectives of a solution → design & development → demonstration → evaluation → communication. We log every iteration against these six activities; the paper's structure mirrors them.
- **Hevner et al. (2004)** — the seven guidelines and the rigor/relevance cycles; our method section's quality checklist (artifact, problem relevance, evaluation, research contribution, rigor, search process, communication).
- **Gregor & Hevner (2013)** — positioning. Our claim: **improvement quadrant** (known problem: supporting structured legal assessment / judgment prediction; new solution: learned fact-conditional traversal over a seeded norm graph). Contribution levels: Level 1 (instantiation) + Level 2 (design principles for norm-graph legal reasoning systems). Also: the DSR publication schema we'll follow for the manuscript.
- **vom Brocke, Hevner & Maedche (2020)** — contemporary overview; vocabulary and framing for the introduction.
- **Winter (list says 1998; verify — likely Winter 2008, EJIS)** — European, artifact-/engineering-centric DSR tradition; supports our construction-heavy style.

## Research question & literature review

- **Thuan, Drechsler & Antunes (2019)** — structured construction of the DSR research question; we use their patterns to derive RQ v1 from the problem statement.
- **Nielsen (2020)** — problematization: our key rhetorical move is that end-to-end outcome prediction is the *wrong problem framing* for codified law; the traversal/Gutachten framing is the re-problematization. This paper licenses that move.
- **Webster & Watson (2002)** — concept-centric matrix for the domain review (concepts: norm graphs, traversal/policy learning, legal NLP for German, evaluation of legal AI).
- **vom Brocke et al. (2009)** — rigorous documentation of the search (databases, strings, inclusion criteria) — goes into the appendix.
- **Templier & Paré (2015)** — quality framework; our review's self-check before submission.

## Design & development (exemplar papers — mirror their anatomy)

- **Meth, Mueller & Maedche (2015)** — *closest structural analog*: an NLP artifact in IS, with an explicit design requirements → design principles → design features chain and layered evaluation. Our paper imitates this anatomy.
- **Seidel et al. (2018)** — exemplary wording and grounding of design principles; template for formulating our DPs.
- **Leimeister, Ebner & Krcmar (2005)** and **Leimeister et al. (2009)** — component-level design + evaluation pattern (design components, hypothesize effects, evaluate); model for evaluating subcomponents (e.g., subsumtion gate, growth/staging loop) separately.
- **Recker (2021)** — compact improvement-type DSR paper; calibration for what a sharp, scoped contribution looks like.
- **Nunamaker, Chen & Purdin (1991)** — systems development as a legitimate research method; methodological cover for the CODE lane.
- **Braun et al. (2005)** — method construction; relevant if we frame the trajectory-reconstruction pipeline (Urteilsstil → Gutachten order) as a *method* contribution in its own right.
- **Niehaves & Ortbach (2016)** — inner vs outer model of explanatory design theory: outer = why the artifact helps legal practice/education; inner = why graph + learned policy produces valid Prüfungspfade. We use this split to structure the Discussion.
- **Avdiji & Winter (2019)** — typology of knowledge gaps; sharpens the gap statement in the introduction.

## Positioning & evaluation

- **Venable, Pries-Heje & Baskerville (2016), FEDS** — choose and justify the evaluation strategy. Proposal: **Technical Risk & Efficacy** trajectory — formative-artificial early (held-out-decision benchmarks), summative-artificial mid (next-norm hits@k, path edit distance, outcome agreement, subsumtion F1), naturalistic late (jurist study on generated Gutachten).
- **Sonnenberg & vom Brocke (2012)** — Eval 1–4 episodes mapped to us: Eval1 problem validation (practitioner/Jurist interviews, literature), Eval2 ex-ante design validation (DD register reviewed against requirements), Eval3 instantiation validation (benchmarks), Eval4 use validation (study).
- **Chandra Kruse, Purao & Seidel (2022)** — how designers actually use design principles; informs phrasing our DPs so they're reusable beyond this artifact.
- **vom Brocke (2007)** — reference-model reuse via aggregation, specialization, instantiation, analogy. Elegant theoretical lens for *schema seeding*: Prüfungsschemata are reference models we instantiate and specialize into the graph. Candidate kernel-theory angle.
- **vom Brocke et al. (2020), accumulation & evolution** — frames the growth loop as design-knowledge accumulation (projectability/fitness of the evolving graph). Supports the "system improves with use" claim scientifically rather than as marketing.

## Process & project management

- **Kuechler & Vaishnavi (2008)** — theory development through design cycles; our mid-project reflection on what general knowledge the iterations produced.
- **Sein et al. (2011), ADR** — the considered-and-rejected alternative: ADR presumes intervention in a host organization; we have none (yet). The paper must justify DSRM over ADR explicitly — one paragraph in Method.
- **vom Brocke & Maedche (2019), DSR Grid** — six dimensions (problem, research process, solution, input knowledge, concepts, output knowledge) as a living one-pager. **First PAPER session (P-01) fills this.**
- **vom Brocke et al. (2017)** — tool support for DSR; cite when describing our register/project discipline as part of research rigor.

## Suggested reading order

1. Peffers et al. (2007) → 2. Gregor & Hevner (2013) → 3. Meth et al. (2015) → 4. Venable et al. (2016) → 5. vom Brocke & Maedche (2019) → everything else on demand, per session, via this map.
